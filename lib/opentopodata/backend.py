import math
import pyproj

import numpy as np

from rasterio.enums import Resampling
import rasterio
import h3

SELECT_METHOD = 'NEW'

INTERPOLATION_METHODS = {
    "nearest": Resampling.nearest,
    "bilinear": Resampling.bilinear,
    "cubic": Resampling.cubic,
    # 'cubic_spline': Resampling.cubic_spline,
    # 'lanczos': Resampling.lanczos,
}

_TRANSFORMER_CACHE = {}

def _noop(x):
    return x

def safe_is_nan(x):
    try:
        return math.isnan(x)
    except TypeError:
        return False

def reproject_latlons(lats, lons, epsg=None, wkt=None):
    """Convert WGS84 latlons to another projection.

    Args:
        lats, lons: Lists/arrays of latitude/longitude numbers.
        epsg: Integer EPSG code.

    """
    if epsg is None and wkt is None:
        raise ValueError("Must provide either epsg or wkt.")

    if epsg and wkt:
        raise ValueError("Must provide only one of epsg or wkt.")

    if epsg == 4326:
        return lons, lats

    # Validate EPSG.
    if epsg is not None and (not 1024 <= epsg <= 32767):
        raise ValueError("Dataset has invalid epsg projection.")

    # Load transformer.
    to_crs = wkt or f"EPSG:{epsg}"
    if to_crs in _TRANSFORMER_CACHE:
        transformer = _TRANSFORMER_CACHE[to_crs]
    else:
        from_crs = f"EPSG:{4326}"
        transformer = pyproj.transformer.Transformer.from_crs(
            from_crs, to_crs, always_xy=True
        )
        _TRANSFORMER_CACHE[to_crs] = transformer

    # Do the transform.
    x, y = transformer.transform(lons, lats)

    return x, y

def _validate_points_lie_within_raster(xs, ys, lats, lons, bounds, res):
    """Check that querying the dataset won't throw an error.

    Args:
        xs, ys: Lists/arrays of x/y coordinates, in projection of file.
        lats, lons: Lists/arrays of lat/lon coordinates. Only used for error message.
        bounds: rastio BoundingBox object.
        res: Tuple of (x_res, y_res) resolutions.

    Raises:
        InputError: if one of the points lies outside bounds.
    """
    oob_indices = set()

    # Get actual extent. When storing point data in a pixel-based raster
    # format, the true extent is the centre of the outer pixels, but GDAL
    # reports the extent as the outer edge of the outer pixels. So need to
    # adjust by half the pixel width.
    #
    # Also add an epsilon to account for
    # floating point precision issues: better to validate an invalid point
    # which will error out on the reading anyway, than to invalidate a valid
    # point.
    atol = 1e-8
    x_min = min(bounds.left, bounds.right) + abs(res[0]) / 2 - atol
    x_max = max(bounds.left, bounds.right) - abs(res[0]) / 2 + atol
    y_min = min(bounds.top, bounds.bottom) + abs(res[1]) / 2 - atol
    y_max = max(bounds.top, bounds.bottom) - abs(res[1]) / 2 + atol

    # Check bounds.
    x_in_bounds = (xs[0] >= x_min) & (xs[0] <= x_max)
    y_in_bounds = (ys[0] >= y_min) & (ys[0] <= y_max)

    #print(x_in_bounds)
    #print(y_in_bounds)
    #print(xs,x_min,x_max)
    #print(ys,y_min, y_max)

    # Found out of bounds.
    oob_indices.update(np.nonzero(~x_in_bounds)[0])
    oob_indices.update(np.nonzero(~y_in_bounds)[0])
    return sorted([])#oob_indices)

def _get_elevation_from_path(latitudes, longitudes, path, interpolation=Resampling.cubic):
    """Read values at locations in a raster.

    Args:
        lats, lons: Arrays of latitudes/longitudes.
        path: GDAL supported raster location.
        interpolation: method name string.

    Returns:
        z_all: List of elevations, same length as lats/lons.
    """
    z_all = []

    #print(interpolation)
    #print('{} / {}'.format(latitudes, longitudes))
    if SELECT_METHOD == 'NEW':
        areas = []

        print(longitudes)
        print(latitudes)

        dist = 0

        for i in range(len(latitudes)):
            #for i, (lon, lat) in enumerate(zip(longitudes, latitudes)):
            lon = longitudes[i]
            lat = latitudes[i]

            if i > 0:
                dist += h3.point_dist((latitudes[i-1],longitudes[i-1]), (lat, lon))

            areaFound = False

            for area in areas:
                if lon > area['minlon'] and lon < area['maxlon'] and lat > area['minlat'] and lat < area['maxlat']:
                    area['lons'].append(lon)
                    area['lats'].append(lat)
                    area['dist'].append(dist)

                    areaFound = True
                    break

            if areaFound:
                continue

            areas.append({
                'maxlon': math.trunc(lon)+1 if lon > 0 else math.trunc(lon) ,
                'minlon': math.trunc(lon) if lon > 0 else math.trunc(lon)-1,
                'maxlat': math.trunc(lat)+1 if lat > 0 else math.trunc(lat),
                'minlat': math.trunc(lat) if lat > 0 else math.trunc(lat)-1,
                'lats': [lat],
                'lons': [lon],
                'dist': [dist],
                'elevation': []
            })
    
        print(areas)

        for area in areas:
            print("SELECT AREA")
            lons = area['lons']
            lats = area['lats']

            latFilename = 'N{:02}'.format(area['minlat']) if lats[0] > 0 else 'S{:02}'.format(abs(area['minlat']))
            lonFilename = 'E{:02}'.format(area['minlon']) if lons[0] > 0 else 'W{:02}'.format(abs(area['minlon']))
            filename = "ASTGTMV003_{}{}_dem.tif".format(latFilename, lonFilename)

            print(filename)

            try:
                with rasterio.open('{}{}'.format(path, filename)) as f:
                    if f.crs is None:
                        msg = "Dataset has no coordinate reference system."
                        msg += f" Check the file '{path}' is a geo raster."
                        msg += " Otherwise you'll have to add the crs manually with a tool like gdaltranslate."
                        print(msg)
                        raise ValueError(msg)

                    try:
                        if f.crs.is_epsg_code:
                            xs, ys = reproject_latlons(lats, lons, epsg=f.crs.to_epsg())
                        else:
                            xs, ys = reproject_latlons(lats, lons, wkt=f.crs.to_wkt())
                    except ValueError:
                        print("Unable to transform latlons to dataset projection.")
                        raise ValueError("Unable to transform latlons to dataset projection.")

                    # Check bounds.
                    oob_indices = _validate_points_lie_within_raster(
                        xs, ys, lats, lons, f.bounds, f.res
                    )
                    rows, cols = tuple(f.index(xs, ys, op=_noop))

                    # Different versions of rasterio may or may not collapse single
                    # f.index() lookups into scalars. We want to always have an
                    # array.
                    rows = np.atleast_1d(rows)
                    cols = np.atleast_1d(cols)

                    # Offset by 0.5 to convert from center coords (provided by
                    # f.index) to ul coords (expected by f.read).
                    rows = rows - 0.5
                    cols = cols - 0.5

                    # Because of floating point precision, indices may slightly exceed
                    # array bounds. Because we've checked the locations are within the
                    # file bounds,  it's safe to clip to the array shape.
                    rows = rows.clip(0, f.height - 1)
                    cols = cols.clip(0, f.width - 1)

                    # Read the locations, using a 1x1 window. The `masked` kwarg makes
                    # rasterio replace NODATA values with np.nan. The `boundless` kwarg
                    # forces the windowed elevation to be a 1x1 array, even when it all
                    # values are NODATA.
                    for i, (row, col) in enumerate(zip(rows, cols)):
                        if i in oob_indices:
                            print("Out Of bounds")
                            area['elevation'].append(0.0)
                            continue

                        window = rasterio.windows.Window(col, row, 1, 1)

                        z_array = f.read(
                            indexes=1,
                            window=window,
                            resampling=interpolation,
                            out_dtype=float,
                            boundless=True,
                            masked=True,
                        )
                        z = np.ma.filled(z_array, np.nan)[0][0]
                        area['elevation'].append(z)

            # Depending on the file format, when rasterio finds an invalid projection
            # of file, it might load it with a None crs, or it might throw an error.
            except rasterio.RasterioIOError as e:
                #print(e)
                #if "not recognized as a supported file format" in str(e):
                #    msg = f"Dataset file '{path}' not recognised as a geo raster."
                #    msg += " Check that the file has projection information with gdalsrsinfo,"
                #    msg += " and that the file is not corrupt."
                #    raise ValueError(msg)
                #raise e
                print(e)

                area['elevation'].append(0.0)

            except Exception as e:
                print(e)

        points = []
        for area in areas:
            for i in range(len(area['dist'])):
                points.append({
                    'dist': area['dist'][i], 
                    'elevation': area['elevation'][i]
                })

        return sorted(points, key=lambda d: d['dist']) 


    else:
        for i, (lon, lat) in enumerate(zip(longitudes, latitudes)):

            lons = [lon]
            lats = [lat]

            #print('{} / {}'.format(lats, lons))
            
            latFilename = 'N{:02}'.format(int(round(lats[0], 0))) if lats[0] > 0 else 'N{:02}'.format(abs(int(round(lats[0], 0))))
            lonFilename = 'E{:03}'.format(int(round(lons[0]-1, 0))) if lons[0] > 0 else 'W{:03}'.format(abs(int(round(lons[0]-1, 0))))
            filename = "ASTGTMV003_{}{}_dem.tif".format(latFilename, lonFilename)

            #print("Open file ASTGTMV003_{}{}_dem.tif".format(latFilename, lonFilename))

            #interpolation = INTERPOLATION_METHODS.get(interpolation)
            #print("INTERPOLATION")
            #print(interpolation)

            try:
                with rasterio.open('{}{}'.format(path, filename)) as f:
                    if f.crs is None:
                        msg = "Dataset has no coordinate reference system."
                        msg += f" Check the file '{path}' is a geo raster."
                        msg += " Otherwise you'll have to add the crs manually with a tool like gdaltranslate."
                        raise ValueError(msg)

                    try:
                        if f.crs.is_epsg_code:
                            xs, ys = reproject_latlons(lats, lons, epsg=f.crs.to_epsg())
                        else:
                            xs, ys = reproject_latlons(lats, lons, wkt=f.crs.to_wkt())
                    except ValueError:
                        raise ValueError("Unable to transform latlons to dataset projection.")

                    # Check bounds.
                    oob_indices = _validate_points_lie_within_raster(
                        xs, ys, lats, lons, f.bounds, f.res
                    )
                    rows, cols = tuple(f.index(xs, ys, op=_noop))

                    # Different versions of rasterio may or may not collapse single
                    # f.index() lookups into scalars. We want to always have an
                    # array.
                    rows = np.atleast_1d(rows)
                    cols = np.atleast_1d(cols)

                    # Offset by 0.5 to convert from center coords (provided by
                    # f.index) to ul coords (expected by f.read).
                    rows = rows - 0.5
                    cols = cols - 0.5

                    # Because of floating point precision, indices may slightly exceed
                    # array bounds. Because we've checked the locations are within the
                    # file bounds,  it's safe to clip to the array shape.
                    rows = rows.clip(0, f.height - 1)
                    cols = cols.clip(0, f.width - 1)

                    # Read the locations, using a 1x1 window. The `masked` kwarg makes
                    # rasterio replace NODATA values with np.nan. The `boundless` kwarg
                    # forces the windowed elevation to be a 1x1 array, even when it all
                    # values are NODATA.
                    for i, (row, col) in enumerate(zip(rows, cols)):
                        if i in oob_indices:
                            z_all.append(0.0)
                            continue

                        #print("HERE WE ARE")
                        #print(i, row, col)

                        window = rasterio.windows.Window(col, row, 1, 1)
                        #print(window)
                        #print(interpolation)

                        z_array = f.read(
                            indexes=1,
                            window=window,
                            resampling=interpolation,
                            out_dtype=float,
                            boundless=True,
                            masked=True,
                        )
                        z = np.ma.filled(z_array, np.nan)[0][0]
                        z_all.append(z)

            # Depending on the file format, when rasterio finds an invalid projection
            # of file, it might load it with a None crs, or it might throw an error.
            except rasterio.RasterioIOError as e:
                #print(e)
                #if "not recognized as a supported file format" in str(e):
                #    msg = f"Dataset file '{path}' not recognised as a geo raster."
                #    msg += " Check that the file has projection information with gdalsrsinfo,"
                #    msg += " and that the file is not corrupt."
                #    raise ValueError(msg)
                #raise e
                z_all.append(0.0)

        return z_all