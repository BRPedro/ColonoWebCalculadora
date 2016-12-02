from osgeo import gdal,osr
file = gdal.Open('C:\\Users\\aariasr\\Documents\\exom- seccion 2 completa_transparent_mosaic_group1.tif')
band1 = file.GetRasterBand(1)
band2 = file.GetRasterBand(2)
a = [band1.ReadAsArray()[0][0],band2.ReadAsArray()[0][0]]
print a



ds=gdal.Open(r'C:\\Users\\aariasr\\Documents\\exom- seccion 2 completa_transparent_mosaic_group1.tif')
prj=ds.GetProjection()
print prj

srs=osr.SpatialReference(wkt=prj)
if srs.IsProjected:
    print srs.GetAttrValue('projcs')
print srs.GetAttrValue('geogcs')



ds = gdal.Open('C:\\Users\\aariasr\\Documents\\exom- seccion 2 completa_transparent_mosaic_group1.tif')
width = ds.RasterXSize
height = ds.RasterYSize
gt = ds.GetGeoTransform()
minx = gt[0]
miny = gt[3] + width*gt[4] + height*gt[5]
maxx = gt[0] + width*gt[1] + height*gt[2]
maxy = gt[3]
print minx,miny,maxx,maxy