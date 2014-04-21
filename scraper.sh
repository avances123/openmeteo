#!/bin/bash
cd $1
fecha=$2
hora=$3
for var in temp2m wind10m_u wind10m_v
do
	for horiz in {1..72}
	do
		tempfile="/tmp/pp-${var}.${fecha}${hora}_${horiz}.tif"
		wget http://data.openmeteoforecast.org/eu12/pp-${var}.${fecha}${hora}_${horiz}.tif -O $tempfile
		gdalwarp -dstnodata 255 -s_srs "+proj=lcc +lon_0=4 +lat_0=47.5 +lat_1=47.5 +lat_2=47.5 +a=6370000. +b=6370000. +no_defs" -t_srs EPSG:4326 /tmp/pp-${var}.${fecha}${hora}_${horiz}.tif pp-${var}.${fecha}${hora}_${horiz}.tif
		rm -f /tmp/pp-${var}.${fecha}${hora}_${horiz}.tif
	done
done
