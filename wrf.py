from osgeo import gdal,gdalconst,ogr,osr
import sys
import numpy as np





def get_coords(filepath):
    """
    http://gis.stackexchange.com/a/42846/4100
    """
    raster = gdal.Open(filepath,gdalconst.GA_ReadOnly)
    matriz = raster.ReadAsArray() #(262, 695)
    upper_left_x, x_size, x_rotation, upper_left_y, y_rotation, y_size = raster.GetGeoTransform()
    y_index, x_index = np.nonzero(matriz < 255)
    x_coords = x_index * x_size + upper_left_x + (x_size / 2) #add half the cell size
    y_coords = y_index * y_size + upper_left_y + (y_size / 2) #to centre the point
    
    
    driver = ogr.GetDriverByName('ESRI Shapefile')
    shapeData = driver.CreateDataSource('ogr_pts')
    srs = osr.SpatialReference()
    srs.ImportFromWkt(raster.GetProjection())
    layer = shapeData.CreateLayer('ogr_pts', srs, ogr.wkbPoint)
    layerDefinition = layer.GetLayerDefn()


    indexes = np.column_stack((x_index,y_index))
    coords = np.column_stack((x_coords,y_coords))
    i = 0
    for x,y in coords:
        print x,y
        point = ogr.Geometry(ogr.wkbPoint)
        point.SetPoint(0, x, y)

        feature = ogr.Feature(layerDefinition)
        feature.SetGeometry(point)
        feature.SetFID(i)

        layer.CreateFeature(feature)

        i += 1


get_coords(sys.argv[1])
