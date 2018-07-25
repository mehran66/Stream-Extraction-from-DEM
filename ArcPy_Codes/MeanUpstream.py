__author__ = 'Mehran'

# Import arcpy module
print "importing arcpy (this takes a while)..."
import arcpy
from arcpy import env
from arcpy.sa import *
import numpy
import math
import os
import matplotlib.pyplot as plt
import scipy
import json


# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")
env.overwriteOutput = True

# Load required toolboxes
arcpy.AddToolbox("C:/Program Files/TauDEM/TauDEM5Arc/TauDEM Tools.tbx")
arcpy.ImportToolbox("C:/Program Files/TauDEM/TauDEM5Arc/TauDEM Tools.tbx")
arcpy.gp.toolbox = "C:/Program Files/TauDEM/TauDEM5Arc/TauDEM Tools.tbx";


# Local variables:
FD = arcpy.GetParameterAsText(0)
FA = arcpy.GetParameterAsText(1)

inputLayers = arcpy.GetParameterAsText(2)
inputLayers_list = inputLayers.split(";")

# Process each road type
for lyrs in inputLayers_list:
  arcpy.AddMessage("Processing: {}".format(lyrs))

outputLayers_folder = arcpy.GetParameterAsText(3)

for lyrs in inputLayers_list:
  temp = outputLayers_folder + "\S" + os.path.basename (lyrs)
  arcpy.gp.D8ContributingArea(FD, "", lyrs, "false", "8", temp)
  outRas = Divide(temp, FA)
  outRas.save(outputLayers_folder + "\M" + os.path.basename (lyrs))

  #temp = outputLayers_folder + os.path.basename (lyrs)
  #arcpy.gp.RasterCalculator_sa(%temp% / %FA%, outputLayers_folder + "\M" +  os.path.basename (lyrs))

  #arcpy.gp.D8ContributingArea(FD, "", lyrs, "false", "8", outputLayers_folder + "\temp" + os.path.basename (lyrs) )
  #outRas = Divide(temp, FA)
  #outRas.save(outputLayers_folder + "\MUp" + os.path.basename (lyrs))

