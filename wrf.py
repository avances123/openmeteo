from osgeo import gdal,gdalconst,ogr,osr
import sys
import numpy as np
from scipy import interpolate
import re
import psycopg2
from psycopg2.extras import DictCursor


try:
    conn = psycopg2.connect("dbname='openmeteo'")
except:
    print "I am unable to connect to the database"



def get_stations(minLon=-45.6607629, minLat=26.4099379, maxLon=53.7130834, maxLat=63.8717332):
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute("""SELECT * from estaciones where geom && ST_MakeEnvelope(%f,%f,%f,%f)""" % (minLon, minLat, maxLon, maxLat))
    l = list(cur.fetchall())
    cur.close()  
    return l

def insert_pred(icao,var,pasada,horiz,data):
    cur = conn.cursor()
    cur.execute("""INSERT INTO wrf (icao,pasada,horiz,%s) VALUES ('%s',to_timestamp('%s','YYYYMMDDHH24'),'%s',%f)""" % (var,icao,pasada,horiz,data))
    conn.commit()
    cur.close()


def main(filepath):
    """
    http://gis.stackexchange.com/a/42846/4100
    """
    m = re.search('pp-(.+)\.(\d{10})_(\d)',filepath)
    var = m.group(1)
    pasada = m.group(2)
    horiz = m.group(3)
    print var,pasada,horiz
    raster = gdal.Open(filepath,gdalconst.GA_ReadOnly)
    valores = raster.ReadAsArray() #(262, 695)
    upper_left_x, x_size, x_rotation, upper_left_y, y_rotation, y_size = raster.GetGeoTransform()
    y_index, x_index = np.nonzero(valores < 255)
    x_coords = x_index * x_size + upper_left_x + (x_size / 2) #add half the cell size
    y_coords = y_index * y_size + upper_left_y + (y_size / 2) #to centre the point
    
    indexes = np.column_stack((x_index,y_index))
    coords = np.column_stack((x_coords,y_coords))
    validos = valores[y_index,x_index]


    estaciones = get_stations()
    print "Num estaciones: %d" % len(estaciones)
    puntos = []
    for i in estaciones:
        puntos.append([i['lon'],i['lat']])
    interp = interpolate.griddata(coords, validos, puntos, method='linear', fill_value=255)

    for i,estacion in enumerate(estaciones):
        insert_pred(estacion['icao'],var,pasada,horiz,interp[i])
    
        

main(sys.argv[1])
conn.close()
















    # driver = ogr.GetDriverByName('ESRI Shapefile')
    # shapeData = driver.CreateDataSource('ogr_pts')
    # srs = osr.SpatialReference()
    # srs.ImportFromWkt(raster.GetProjection())
    # layer = shapeData.CreateLayer('ogr_pts', srs, ogr.wkbPoint)
    # layerDefinition = layer.GetLayerDefn()

    # # Creo un shp para ver si estoy haciendo bien los puntos
    # i = 0
    # for x,y in coords:
    #     print i,x,y
    #     point = ogr.Geometry(ogr.wkbPoint)
    #     point.SetPoint(0, x, y)

    #     feature = ogr.Feature(layerDefinition)
    #     feature.SetGeometry(point)
    #     feature.SetFID(i)
    #     feature.SetField("temp", validos[i])

    #     layer.CreateFeature(feature)

    #     i += 1



