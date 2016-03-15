# GDAL_Python3
Open Source (geographic) data handling scripts, written in Python 3.4 and 3.5

Last tested (March 2016) with [GDAL 2.0.2](http://www.gisinternals.com/query.html?content=filelist&file=release-1800-x64-gdal-1-11-3-mapserver-6-4-2.zip)

Functions.py is needed by many of these scripts, as it contains basic functions repeatedly required

### MiniScripts.py

A collection of small scripts including:
* conversion of a folder of HDF files to the GeoTiff format
* handling of nested zip files (specific for data from www.vito-eodata.be)
* copy the content of many folders into one (useful when data is packed in folder by month, though all monthly files are required to be in one folder)
* inverse case, copy content of one folder to many (here specifically monthly folders)
* rename files (first to last) to fit the *Year_Month.tif* format used in some of the other scripts
* convert BIL files in ZIP archives to GeoTiffs
* change a number string representing months into month names


### netCDFtoTiff.py

Converts 3D netCDF files (X,Y,Z = lon, lat, value) into multiple single GeoTiff rasters. Requires Functions.py and the [netCDF4](https://netcdf4-python.googlecode.com/svn/trunk/docs/netCDF4-module.html) module

Extent and pixel size must be manually changed, all else is extracted automatically.   
The script returns files that are numbered in continuous order (*1.tif, 2.tif, 3.tif...*)

