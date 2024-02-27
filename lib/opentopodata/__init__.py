import lib.opentopodata.backend as backend

import polyline
import h3 

def getElevation(line):
    arr = polyline.decode(line)

    lons = []
    lats = []

    for point in arr:
        #if len(lats) > 0:
        #    d = h3.point_dist((lats[-1],lons[-1]), (point[0], point[1]))
        #    if d < 0.06:
        #        continue

        lats.append(point[0])
        lons.append(point[1])

    #print(lons)
    #print(lats)

    try:
        elevations = backend._get_elevation_from_path(
            latitudes = lats,
            longitudes= lons,
            path="./data/"
        )

    except Exception as e:
        #print(e)
        return {
            'uphill': 0,
            'downhill': 0,
            'points': ''
        }

    points = []

    distance = 0
    uphill = 0
    downhill = 0
    details = []

    if backend.SELECT_METHOD == 'NEW':
        for i in range(len(elevations)):
            if i > 0:
                if elevations[i]['elevation'] > elevations[i-1]['elevation']:
                    uphill += elevations[i]['elevation'] - elevations[i-1]['elevation']
                else:
                    downhill += elevations[i]['elevation'] - elevations[i-1]['elevation']

            points.append((elevations[i]['dist'], elevations[i]['elevation']))
            details.append({
                'lon': elevations[i]['point']['lon'],
                'lat': elevations[i]['point']['lat'],
                'ele': elevations[i]['elevation']
            })

    else:
        for i in range(len(elevations)):
            if i > 0:
                distance += h3.point_dist((lats[i-1], lons[i-1]), (lats[i], lons[i]))

                if i < (len(arr)-1) and elevations[i] == elevations[i-1]:
                    continue

                if elevations[i] > elevations[i-1]:
                    uphill += elevations[i] - elevations[i-1]
                else:
                    downhill += elevations[i] - elevations[i-1]

            points.append((distance, elevations[i]))

            #points.append({
            #    'lat': arr[i][0],
            #    'lon': arr[i][1],
            #    'elevation': elevations[i],
            #    'distance': distance
            #})

    return {
        'uphill': uphill,
        'downhill': downhill,
        'points': polyline.encode(points),
        'details': details
    }