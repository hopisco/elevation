import lib.opentopodata.backend as backend
import lib.opentopodata.Dataset as Dataset

import polyline
import h3 

def getElevation(line):
    arr = polyline.decode(line)

    lons = []
    lats = []

    for point in arr:
        lats.append(point[0])
        lons.append(point[1])

    #print(lons)
    #print(lats)

    try:
        elevations = backend._get_elevation_from_path(
            latitudes = lats,
            longitudes= lons,
            path="/home/ubuntu/mooviz-backend/tools/elevationTiles/"
        )

    except Exception as e:
        #print(e)
        return {
            'uphill': 0,
            'downhill': 0,
            'points': []
        }

    points = []

    distance = 0
    uphill = 0
    downhill = 0

    for i in range(len(arr)):
        if i > 0:
            distance += h3.point_dist((arr[i-1][0], arr[i-1][1]), (arr[i][0], arr[i][1]))

            if i < (len(arr)-1) and elevations[i] == elevations[i-1]:
                continue

            if elevations[i] > elevations[i-1]:
                uphill += elevations[i] - elevations[i-1]
            else:
                downhill += elevations[i] - elevations[i-1]

        points.append({
            'lat': arr[i][0],
            'lon': arr[i][1],
            'elevation': elevations[i],
            'distance': distance
        })

    return {
        'uphill': uphill,
        'downhill': downhill,
        'points': points
    }