from osgeo import gdal
""""
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

"""
""""
imagen = gdal.Open('C:\\Users\\aariasr\\Documents\\exom- seccion 2 completa_transparent_mosaic_group1.tif')  # se carga la imagen que se encuentra en la direccion dir.
band1 = imagen.GetRasterBand(1)
print len(band1.ReadAsArray()),len(band1.ReadAsArray()[0])
"""



file = gdal.Open('C:\\Users\\aariasr\\Documents\\exom- seccion 2 completa_transparent_mosaic_group1.tif')
band1 = file.GetRasterBand(1)
band2 = file.GetRasterBand(2)
largo = len(band1.ReadAsArray())//4
a = band1.ReadAsArray()[:largo-]
print a