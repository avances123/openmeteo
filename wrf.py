from osgeo import gdal,gdalconst
import sys
import numpy as np



def get_coords(filepath):
    """
    http://gis.stackexchange.com/a/42846/4100
    """
    raster = gdal.Open(filepath,gdalconst.GA_ReadOnly)
    matriz = raster.ReadAsArray() #(262, 695)
    upper_left_x, x_size, x_rotation, upper_left_y, y_rotation, y_size = raster.GetGeoTransform()
    y_index, x_index = np.nonzero(matriz > 254)
    x_coords = x_index * x_size + upper_left_x + (x_size / 2) #add half the cell size
    y_coords = y_index * y_size + upper_left_y + (y_size / 2) #to centre the point
    print x_coords,y_coords

get_coords(sys.argv[1])
