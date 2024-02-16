import lib.opentopodata  as opentopodata
import lib.Tiler as Tiler

import polyline
import requests
import os

def getTile(z,x,y):
    url = "https://tiles.mooviz.app/styles/basic-preview/{z}/{x}/{y}.png".format(z=z, x=x, y=y)

    response = requests.get(url, verify=False)
    os.makedirs('/home/ubuntu/tmp/{z}/{x}'.format(z=z, x=x), exist_ok=True)

    with open('/home/ubuntu/tmp/{z}/{x}/{y}.png'.format(z=z, x=x, y=y), 'w') as f:
        f.write(response.content)
        
    print("Got tile")

getTile(z=0, x=0, y=0)

'''
#opentopodata.SELECT_METHOD = 'OLD'
r = opentopodata.getElevation('e{pbFdxahVBJPl@^r@FJKDSBUGeAo@QIUKSAQ@SNSXQ`@Id@Al@HhAEbAANEVM`@Yn@]h@k@x@Yh@m@hAUZWRYNa@LqAXg@Fg@Nm@ZOH_A^e@\WXqAhBg@l@[VWN@V?FG@C@@@B@F?FAF@H?L?DBHRBBBCBKDW@IAK@GDCL?DC?E?I?G@A@@@D@BDJ?D@NDJBLCL?JEFAJCXANEHAHBJLP@L@NANILIPARGHEJGHGPBJ@J@HAFEBKIQSCOGEKCIEIGGGKEI@EBGFCF@LBJBR?N?JADE@GBEBGFIRC@CACEKII?MDC?GCGAI?E?CECMGSKSIME@MFSLKHEJCJAD?NARANE^AP?PBP@J?JAHC?CAGESIQEUAMAK?GDCFIDSHGFCFCL@H?P@LALEPGHKBK@KBGDAJCDE?ECCEG?QDS@WBS@M?M@O@MFQDMDQDpAdAf@`AjAf@f@Td@b@HXJTf@PJHFLRSDEPSTMd@Mb@U`@OTAl@T`@BTCTMPUPUd@We@VQTQTULUBa@Cm@UU@a@Nc@Te@LULQREDSRGMKIg@QKUIYe@c@g@UkAg@g@aAqAeAPELEPELGNALAL?RAVCRAPEF?BDDBD?BE@KFEJCJAJCFIDQ@MAM?QAIBMBGFGRIHEBGFEJ?L@T@PDRHFDB@B?@I?KAKCQ?Q@QD_@@O@S?O@EBKDKJIRMLGDAHLJRFRBLBDD?H?F@FBB?LEH?JHBDB@BAHSFGDCFCDA@E?K?OCSCKAMBGFGDCHAJDFFHFHDJBFDBNPRJHDC@GAIAKCKFQFIDKFI@SHQHM@OAOAMMQCK@IDI@OBY@KDG?KBMCMEKAO?EEKACAEAAA@?F?H?DEBM?EBAF@JAHEVCJCBCCISECM?I?GAG@G?CAAABAFA?GAW{@RaCh@yCt@iAf@[Pc@JaEj@gB\{@Pu@N_@Ee@M_Ae@mBWaAFWL[j@[fAa@dCa@lASj@g@xA_@LSBUCQIMOY_@Qo@Ca@Ba@f@{CB_AM{ACc@YeDEc@CWCMCQCOKWKQKIKEQCUBQF]HQHSDM@QA]A]S_@a@wAyAcB}Aq@c@FMHUHOUOYWa@c@S]MQQMSQSMQMEKAUDYCSEYHw@Cc@Qi@Es@Ka@MSQKMm@Qa@_@CMSAIRILSJMBOVQ?@d@@TD@RCJ?BB?HGJA`@k@V[`@Cd@LPPTLJARIh@IR?ZPh@RlAfAVZFJJFZBj@@TARE\Id@KFO@ICc@BOHML@PJN?HGFKHYJQf@OfA?l@DTIXIVSVORCDMBK@_@AUCUBc@?a@Co@CSAUBIFKBEHCJ?J@PBLAJCHCNEHEHGBGHEJ@JFHJFDBFBF?LAJKRSPMJQFWFEBCD@HDHBJLPVRPTJL@R?PBNJJRHNHLNBR?TANANCHGN?L@HBFHFLFPHRTJJNH|@l@NXDHBJ@@?EAKAU@OCOQ[KIKKOKBGFFLBP?XFPVJRFXLl@Hl@?p@Qb@AFDHHDJBJBNDFDL@JGJENCP@HBHDBJ@TATCZBLHNFFF?FC@@ADGNCHA@AFBFHP@N?REFGAGOCOC@@R@NBPDNHFJ@PITWLSDO@SBWBKDMBOB??JAFAN?LBN@R?T?LI\CVARALCXEVIJMDWH[BOBE@G?IBI?OGEIA?DPBHFFRL^Hf@LNBDFDBDEBG@IBEFCDEFADABABCBABABABABABA@ADCF?@C?A?EAEAEEGCCACCGAEEEAC?E@C@I@C?E@C?ABAB?@@@BBD@BDDB@B@BCBCBEBSFOFGBC@E?CAQCIAE?C@AB?@A?CAEAEAE?A?A?CJAF?D@BP?N?FBBHJ@HALATAL?P@`@Dd@DRBTHFHAHABI?K?OFEDI@CH@B?BCDBP?^RJPDPDLBFFDJBJEJOf@k@BE?CAECA?AA?SMIKEGAG@G@EAKASEUC[?UC[?M@GBKD@CTH\DVBTBL@D@?@GCMAO@K?OAO?IBMFGFGFGRWLMJIHQHKJEDADG?GAEEG?CBAHBF?HKDG@GBAB?FHB?FCJOBEDEJCD@DAJEJ?JBD@FFJ@J?D?DADE@ADB@BB@LCF@DFHDTAP?FBFBBDDJBFDPDHFJFHDL@H@H?H?DDDLDH@FABC@CAIAI@E?KBIJ[?Q?UAS?IAGEECCCCCC?CDCDCDEBGBIAIAE@G@CDAFEB?DB@@FR?JDTHb@J~@Lj@?h@@PD@BQ@IBGPERAPAFGDGHW@G@KBKBIXk@T[LMJKn@Un@EHAHCDG@I?OAQGUISGS?GBGZDJBPBHe@Pa@RYROPAR@TJPHdAn@TFRCJEGK_@s@Qm@CK')
print(r)

print(polyline.decode(r['points']))

Tiler.generateMbTiles(
    minlat=37,
    maxlat=38,
    minlon=-122,
    maxlon=-121,
    srcfile='/home/ubuntu/maptiler/data/planet.mbtiles',
    outfile='/home/ubuntu/tmp.mbtiles'
)

db = sqlite3.connect(
    "file:{0}?mode={1}".format('/home/ubuntu/maptiler/data/planet.mbtiles', 'ro'),
    uri=True,
    isolation_level=None,
)
cursor = db.cursor()
cursor.execute("SELECT name FROM my_db.sqlite_master WHERE type='table'")
row = cursor.fetchone()
print(row)

cursor = db.cursor()
cursor.execute("select name from sqlite_master where type = 'table' ")
print(cursor.fetchall())
row = cursor.fetchone()
print(row)

[('map',), ('images',), ('metadata',), ('',), ('',), ('',), ('',), ('omtm',)]


cursor.execute("select sql from sqlite_master where type = 'table' and name = 'geocoder_data'")
row = cursor.fetchone()
print(row)





import sqlite3
import mapbox_vector_tile as mvt
import gzip
from io import BytesIO
db = sqlite3.connect(
    "file:{0}?mode={1}".format('/home/ubuntu/maptiler/data/planet.mbtiles', 'ro'),
    uri=True,
    isolation_level=None,
)
cursor = db.cursor()
cursor.execute("SELECT tile_data FROM map, images where zoom_level=11 and tile_row=331 and tile_column=793 and images.tile_id = map.tile_id limit 1")
row = cursor.fetchone()
print(row[0])

raw_data = BytesIO(bytes(row[0]))

with gzip.open(raw_data, "rb") as f:
    tile = f.read()

print(tile)
decoded_data = mvt.decode(tile)
print(decoded_data)

import zlib
with open('img.png', 'wb') as output_file:
    output_file.write(zlib.decompress(row[0]))






import osmium
import sys

class NamesHandler(osmium.SimpleHandler):
    def __init__(self):
        osmium.SimpleHandler.__init__(self)
        self.num_nodes = 0
    def node(self, n):
        self.num_nodes += 1
        if 'name' in n.tags:
            print(f'[{self.sum_nodes}] - {n.location}: ' + n.tags['name'])
        
        if self.sum_nodes > 1000:
            exit(-1)

NamesHandler().apply_file('/home/ubuntu/planet-daily.osm.pbf')







import sqlite3
import mapbox_vector_tile as mvt
import gzip
from io import BytesIO

db = sqlite3.connect(
    "file:{0}?mode={1}".format('./planet.mbtiles', 'ro'),
    uri=True,
    isolation_level=None,
)
cursor = db.cursor()
cursor.execute("SELECT tile_data FROM tiles where zoom_level=0 and tile_column=0 and tile_row=0")
row = cursor.fetchone()
print(bytes(row[0]))

raw_data = BytesIO(bytes(row[0]))

with gzip.open(raw_data, "rb") as f:
    tile = f.read()

print(tile)
decoded_data = mvt.decode(tile)
print(decoded_data)

import zlib
with open('img.png', 'wb') as output_file:
    output_file.write(zlib.decompress(row[0]))


import zlib
import json

zoom = 14
col = 2634
row=6361






cursor.execute("SELECT * FROM metadata")
row = cursor.fetchone()
print(row)

cursor.execute("SELECT EXISTS (SELECT 1 FROM images "
             "where zoom_level=? and tile_column=? and tile_row=? LIMIT 1)",(16,10541,25447))

row = cursor.fetchone()
print(row)

from pymbtiles import MBtiles, Tile

with MBtiles('/home/ubuntu/maptiler/data/planet.mbtiles') as src:
    for tile_coords in src.list_tiles():
        print(tile_coords)
        break
'''