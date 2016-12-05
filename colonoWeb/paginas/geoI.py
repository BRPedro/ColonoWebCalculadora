from osgeo import gdal
from osgeo import osr

import sys

# =============================================================================
def Usage():
    print('Usage: val_at_coord.py [-display_xy] [longitude latitude | -coordtype=georef X Y] filename')
    print('')
    print('By default, the 2 first arguments are supposed to be the location')
    print('in longitude, latitude order. If -coordtype=georef is specified before')
    print('the next 2 values will be interpreted as the X and Y coordinates')
    print('in the dataset spatial reference system.')
    sys.exit( 1 )

# =============================================================================

display_xy = True
coordtype_georef = False
longitude,latitude  = 1198167.424524,748491.105690

filename = 'C:\\Users\\aariasr\\Documents\\exom- seccion 2 completa_transparent_mosaic_group1.tif'

# =============================================================================
# Parse command line arguments.
# =============================================================================
i = 1
while i < len(sys.argv):
    arg = sys.argv[i]

    if arg == '-coordtype=georef':
        coordtype_georef = True

    elif arg == '-display_xy':
        display_xy = True

    elif longitude is None:
        longitude = float(arg)

    elif latitude is None:
        latitude = float(arg)

    elif filename is None:
        filename = arg

    else:
        Usage()

    i = i + 1

if longitude is None:
    Usage()
if latitude is None:
    Usage()
if filename is None:
    filename()

# Open input dataset
ds = gdal.Open( filename, gdal.GA_ReadOnly )
if ds is None:
    print('Cannot open %s' % filename)
    sys.exit(1)

# Build Spatial Reference object based on coordinate system, fetched from the
# opened dataset
if coordtype_georef:
    X = longitude
    Y = latitude
else:
    srs = osr.SpatialReference()
    srs.ImportFromWkt(ds.GetProjection())

    srsLatLong = srs.CloneGeogCS()
    # Convert from (longitude,latitude) to projected coordinates
    ct = osr.CoordinateTransformation(srsLatLong, srs)
    (X, Y, height) = 0,0,0

# Read geotransform matrix and calculate corresponding pixel coordinates
geomatrix = ds.GetGeoTransform()
x = 3524
y = 100

if display_xy:
    print('x=%d, y=%d' % (x, y))

if x < 0 or x >= ds.RasterXSize or y < 0 or y >= ds.RasterYSize:
    print('Passed coordinates are not in dataset extent')
    sys.exit(1)

res = ds.ReadAsArray(x,y,1,1)
if len(res.shape) == 2:
    print(res[0][0])
else:
    for val in res:
        print(val[0][0]),"1010101"