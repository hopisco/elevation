
import abc

from rasterio.enums import Resampling
import rasterio

class Dataset(abc.ABC):
    """Base class for Dataset.

    The elevation data could be split over multiple files. This class exists
    to map a location to a particular file.
    """

    # By default, assume raster spans whole globe.
    wgs84_bounds = rasterio.coords.BoundingBox(-180, -90, 180, 90)

    @classmethod
    def load_dataset(cls, tile_path = 'data/etopo1/ETOPO1.tif'):
        try:
            with rasterio.open(tile_path):
                pass
        except rasterio.RasterioIOError as e:
            raise ValueError("Unsupported filetype for '{}'.".format(tile_path))
        
        return SingleFileDataset(
            'ETOPO1', tile_path=tile_path, wgs84_bounds=None
        )

    @abc.abstractmethod
    def location_paths(self, lats, lons):
        """File corresponding to each location.

        Args:
            lats, lons: Lists of locations.

        Returns:
            List of filenames, same length as locations.
        """

class SingleFileDataset(Dataset):
    def __init__(self, name, tile_path, wgs84_bounds=None):
        """A dataset consisting of a single raster file.

        Args:
            name: String used in request url and as datasets dictionary key.
            tile_path: String path to single raster file.
        """
        self.name = name
        self.tile_path = tile_path
        if wgs84_bounds:
            self.wgs84_bounds = wgs84_bounds

    def location_paths(self, lats, lons):
        """File corresponding to each location.

        Args:
            lats, lons: Lists of locations.

        Returns:
            List of filenames, same length as locations.
        """
        assert len(lats) == len(lons)
        return [self.tile_path] * len(lats)