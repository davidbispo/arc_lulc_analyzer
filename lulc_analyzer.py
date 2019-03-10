# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 13:37:24 2018

@author: David Bispo
"""

import archook
import numpy as np
import os
archook.get_arcpy()
import arcpy
from arcpy import env
import pandas as pd 

subbasins = r'C:\Users\David\Desktop\Barigui\SwatBarigui7\SwatBarigui7.mdb\ArcHydro\Watershed'
#arcpy.MakeFeatureLayer_management(subbasins, "subbasins_lyr")
temp_workspace = r'C:\Users\David\Documents\ArcGIS\Default.gdb'
landuse = r'D:\OneDrive\Dissertacao\2.GIS Data\2.General Data\Barigui_database.gdb\barigui\brg_usosolo'
#arcpy.MakeFeatureLayer_management(landuse, "landuse_lyr")

def batch_clip(mask,lulc,temp_gdb):
    for i in range(1,159):
        query = "GRIDCODE = %s"%(i)
        arcpy.SelectLayerByAttribute_management ("subbasins_lyr", "NEW_SELECTION", query)
        output = os.path.join(temp_workspace,"temp%s"%i)
        arcpy.Clip_analysis(lulc, "subbasins_lyr", output)
        print ("Creating lulc %s"%i)
    print ("Done!")
#batch_clip(mask = subbasins, lulc = landuse, temp_gdb = temp_workspace )

def leusosolo(temp_gdb):
    env.workspace = temp_gdb
    features = arcpy.ListFeatureClasses() 
    n = 0
    for item in features:
        dataDictionary = {}
        with arcpy.da.SearchCursor(item, ["SOLOUSO_DE","Shape_Area"]) as cursor:
            n+=1
            print ("Reading subbasin %s" % n)
            for row in cursor:
                solouso = row[0]
                Shape_Area = row[1]/(1000**2)
                dataDictionary["subbasin_number"] = n
                if solouso not in dataDictionary.keys():
                    dataDictionary[solouso] = Shape_Area
                else:
                    current_area = dataDictionary[solouso]
                    new_area = current_area + Shape_Area
                    dataDictionary[solouso] = new_area
            if item == features[0]:
                df = pd.DataFrame(dataDictionary, index=[0])   
            else:
                new_df = pd.DataFrame(dataDictionary,index=[0])   
                df = df.append(new_df)
    df.to_excel("lulc_analysys.xlsx")            
    print "Data Analysis Complete"

leusosolo(temp_workspace)