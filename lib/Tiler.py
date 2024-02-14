import math
from pymbtiles import MBtiles, Tile

def generateMbTiles(minlat, maxlat, minlon, maxlon, srcfile='./data/planet.mbtiles', outfile='./data/tmp.mbtiles'):

    tiles = ()

    #Compute region for each zoom
    minlatRad = minlat * math.pi/180.0
    maxlatRad = maxlat * math.pi/180.0

    with MBtiles(srcfile) as src:
        for zoom in range(12,19):
            n = math.pow(2.0, zoom)
            minY = int((1.0 - math.asinh(math.tan(maxlatRad))/math.pi) / 2.0 * n)
            maxY = int((1.0 - math.asinh(math.tan(minlatRad))/math.pi) / 2.0 * n)
            minX = int(n * ((minlon+180)/360))
            maxX = int(n * ((maxlon+180)/360))

            for x in range(minX-1, maxX+1):
                for y in range(minY-1, maxY+1):
                    tiles.append({
                        'data': src.read_tile(z=zoom, x=x, y=y),
                        'zoom': zoom,
                        'x': x,
                        'y': y
                    })

    with MBtiles(outfile, mode='w') as out:
        for tile in tiles:
            out.write_tile(z=tile['zoom'], x=tile['x'], y=tile['y'], data=tile['data'])

        out.write_tiles(tiles)