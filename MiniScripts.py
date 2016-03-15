# -*- coding: utf-8 -*-

#Collection of small scripts

import os, shutil, zipfile
import gdal
from gdalconst import *

import Functions as funcs


###############################################################################
#HDF to TIFF
###############################################################################

#convert NDVI HDF rasters to GeoTiffs using hdfTOtif

#define input and output folder
inFol = ".../in/"
outFol = "/OutTiffs/"

for filex in os.listdir(inFol):
    extent = [800,2300,300,2500]
    nameHDF = inFol + filex
    outFile = outFol + filex[:-3] + "tif"
    funcs.hdfTOtif(nameHDF,outFile,extent) # Functions.py needed



###############################################################################
#EXTRACT ZIP FILES FROM MANY FOLDERS
###############################################################################

#extract (nested) zip files in many folders into one
#very specific for data from www.vito-eodata.be

inFol = ".../In/"
outFol = ".../Out/"

for folds in os.listdir(inFol):
    for files in os.listdir(inFol+folds):
        if files[-3:].lower() == "zip":
            zipName = inFol+folds+"/"+files
            zipped = zipfile.ZipFile(zipName, mode='r')
            print("File " + files + " opened")
            
            for j in zipped.namelist():
                if j[-7:].lower() == "ndv.hdf":
                    zipped.extract(j, outFol, pwd=None)
                    print(j + " extracted")
            
            #extracts folder with the file, now copy extracted file from
            #its folder to main output and rename
            for i in os.listdir(outFol):
                if os.path.isdir(outFol+i):
                    for k in os.listdir(outFol+i):
                        if k[:4] == "0001":
                            os.rename(outFol+i+"/"+k,outFol+i+"/"+folds[18:26]+".hdf")
        

###############################################################################
#COPY MANY TO ONE
###############################################################################

#in this folder are many folders, all files will be copied into the outer Folder

inFol = '/in/'

for fols in os.listdir(inFol):
    if os.path.isdir(inFol+fols):
        for files in os.listdir(inFol+fols):
            shutil.copyfile(inFol+fols+"/"+files,inFol+"/"+files)


###############################################################################
#COPY ONE TO MANY
###############################################################################

#copy monthly files that are in one folder (e.g. OutMonth) into monthly folders
#(01_Jan 02_Feb etc.) within this first folder. Input files should be in the form
#1999_01.tif
            
inFol =  '/in/'

monthNum = ['01', '02', '03', '04', '05', '06', 
            '07', '08', '09', '10', '11', '12']
            
monthName = ["Jan", "Feb","Mar","Apr","May","Jun",
             "Jul","Aug", "Sep", "Oct", "Nov", "Dec"]

# start and endpoint of the data must be specificied
startYear = 1999
endYear = 2013

#loop over all months, create a folder for each and copy files from main folder            
for moNum,moName in zip(monthNum,monthName):

    #define current sub-directory
    curDir = inFol+moNum + "_" + moName 
    
    #if curDir already exists, delete it
    if os.path.isdir(curDir):
        os.remove(curDir)
    os.mkdir(curDir)

    #copying process
    for yeari in range(startYear,endYear+1):
        year = str(yeari)
        shutil.copyfile(inFol + year + "_" + moNum + ".tif", 
                        curDir + "/" + year + "_" + moNum + ".tif")




###############################################################################
#RENAME FILES BY MONTH AND YEAR
############################################################################### 

#Rename data from first to last in folder to Year_Month.tif notation     
#Input FIles must be numbered from 1.tif to x.tif...
                   
inFol = ".../in/"
startYear = 1999    #First year of data input
endYear = 2013      #Last year of data input

fileList = []
for x in range(1,len(os.listdir(inFol))+1):
    fileList.append(str(x) + ".tif")

x = 0
for yeari in range(startYear,endYear+1):
    year = str(yeari)
    for monthi in range(1,13):        

        if monthi > 9:
            month = str(monthi)
        else:
            month = "0" + str(monthi)

        os.rename(inFol + fileList[x], inFol + year + "_" + month + ".tif")
        x = x+1


###############################################################################
#CONVERT BIL files in ZIP archives to GeoTIFFS
############################################################################### 

# When you accidentally downloaded a couple hundred SRTM scenes from earthexplorer.usgs.gov/
# just to realize you did not change the format to GeoTiff

inFol = ".../BIL_SRTM_Original/"
outFol = ".../Single_TIFF_SRTM/"
scratchFol = ".../Scratch/Convert/" #extract files here first before converting


for zipFile in os.listdir(inFol):               #iterate through zip Files in folder
    if zipFile[-3:].lower() == "zip":
        zipName = inFol+zipFile
        zipped = zipfile.ZipFile(zipName, mode='r')
        zipped.extractall(scratchFol, pwd=None) #Extract all contents in zip to scratch
        
        for j in os.listdir(scratchFol):           #convert BIL files in scratch 
            if j[-3:].lower() == "bil":
                BIL = scratchFol + j
                out = outFol+zipFile[:8]+".tif"
                funcs.BILtoTIF(BIL, out)           # Functions.py needed
        
        #remove all file contents in scratch 
        for old_file in os.listdir(scratchFol):
            file_path = os.path.join(scratchFol, old_file)
            os.remove(file_path)
        
        print(zipFile, " done")
                  


###############################################################################
# Write a file where number strings of months are converted to string names
############################################################################### 

"""
In.txt contains a number of months combinations in the form of

1    101112131415161718192021
2    1011121314151617181920
3    10111213141516171819
4    101112131415161718
5    1011121314151617
6    10111213141516
7    101112131415
8    1011121314
9    10111213
...

This script analyzes the number strings and appends the month names, saves it to Out.txt
1 = Jan, 13 = Jan of the following year
2 = Feb, 14 = Feb of the following year
10 = Oct

1 101112131415161718192021 Oct,Nov,Dec,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,
2 1011121314151617181920 Oct,Nov,Dec,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,
3 10111213141516171819 Oct,Nov,Dec,Jan,Feb,Mar,Apr,May,Jun,Jul,
4 101112131415161718 Oct,Nov,Dec,Jan,Feb,Mar,Apr,May,Jun,
5 1011121314151617 Oct,Nov,Dec,Jan,Feb,Mar,Apr,May,
6 10111213141516 Oct,Nov,Dec,Jan,Feb,Mar,Apr,
7 101112131415 Oct,Nov,Dec,Jan,Feb,Mar,
8 1011121314 Oct,Nov,Dec,Jan,Feb,
9 10111213 Oct,Nov,Dec,Jan,

"""

inFile = "/In.txt"
outFile = "/Out.txt"

inTxt = open(inFile, "r")
outTxt = open(outFile, "a")

monthName = ["Jan", "Feb","Mar","Apr","May","Jun",
             "Jul","Aug", "Sep", "Oct", "Nov", "Dec"]
             

for lines in inTxt.readlines():
    lineList= []
    x = lines.split()
    xStart = x[1][0] 
    
    if (x[1][:2] == "10" or x[1][:2] == "11" or 
        (len(x[1]) > 2 and x[1][:2] == "12" and x[1][2] == "1")):
        
        for mon in range(0,len(x[1]),2):
            mon2 = x[1][mon:mon+2]            
            if int(mon2) > 12:
                monNum = int(mon2) - 13   #number that extracts monthName from list
            else:
                monNum = int(mon2) - 1
            
            monName = monthName[monNum]
            lineList.append(monName)
        
        outTxt.write(x[0] + " " + x[1] + " ")
        for e in lineList:
            outTxt.write(e + ",")
        outTxt.write("\n")
    
    else: 
        monList = []
        intStart = int(xStart)
        xNew = xStart
        for num in range(int(xStart)+1,24):            
            xNew = xNew + str(num)
            if num > 12:
                monList.append(monthName[num-13])
            else:
                monList.append(monthName[num-1])
            
            if xNew == x[1]:
                outTxt.write(x[0] + " " + x[1] + " " + monthName[int(xStart)-1] + ",")
                for e in monList:
                    outTxt.write(e + ",")
                outTxt.write("\n")
            

inTxt.close()
outTxt.close()
