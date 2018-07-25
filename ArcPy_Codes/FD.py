__author__ = 'Mehran'
# you should define the local variables
# The inputs are in the MainData folder; DEM
# the results are saved in a folder named CommonResults; fillDEM, FD, slopeGrid


# Import modules
import arcpy
from arcpy import env
import os
import matplotlib.pyplot as plt

# Load required toolboxes
arcpy.AddToolbox("C:/Program Files/TauDEM/TauDEM5Arc/TauDEM Tools.tbx")
arcpy.ImportToolbox("C:/Program Files/TauDEM/TauDEM5Arc/TauDEM Tools.tbx")
arcpy.gp.toolbox = "C:/Program Files/TauDEM/TauDEM5Arc/TauDEM Tools.tbx";

# Set environment properties
arcpy.env.overwriteOutput = "True"

# Local variables:
DEM = arcpy.GetParameterAsText(0)
fillDEM = arcpy.GetParameterAsText(1)
FD = arcpy.GetParameterAsText(2)
slopeGrid = arcpy.GetParameterAsText(3)


# Process: Pit Remove
arcpy.AddMessage("Running DEM Filling...")
arcpy.gp.PitRemove(DEM, "8", fillDEM + ".tif")

# Process: D8 Flow Directions
arcpy.AddMessage("Running FD...")
arcpy.gp.D8FlowDir(fillDEM + ".tif", "8", FD + ".tif", slopeGrid + ".tif")


