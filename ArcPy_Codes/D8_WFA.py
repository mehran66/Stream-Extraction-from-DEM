__author__ = 'Mehran'
# you should define the local variables
# the results are saved in a folder named WFAResults; FA, streamGrid, streamOrderGrid_tif, networkTree_txt, networkCoord_txt, stream_shp, watershed_tif, watershed_shp

# Import modules
import arcpy
from arcpy import env
import os
import matplotlib.pyplot as plt
arcpy.CheckOutExtension("Spatial")
arcpy.CheckOutExtension("3D")

# Load required toolboxes
arcpy.AddToolbox("C:/Program Files/TauDEM/TauDEM5Arc/TauDEM Tools.tbx")
arcpy.ImportToolbox("C:/Program Files/TauDEM/TauDEM5Arc/TauDEM Tools.tbx")
arcpy.gp.toolbox = "C:/Program Files/TauDEM/TauDEM5Arc/TauDEM Tools.tbx";

# Set environment properties
arcpy.env.overwriteOutput = "True"

# Local variables:
fillDEM = arcpy.GetParameterAsText(0)
FD = arcpy.GetParameterAsText(1)
surfaceRatio = arcpy.GetParameterAsText(2)
Results = arcpy.GetParameterAsText(3)
thresholdStart = arcpy.GetParameterAsText(4)
thresholdSteps = arcpy.GetParameterAsText(5)
thresholdEnd = arcpy.GetParameterAsText(6)


FA = Results + r"\FA.tif"
streamGrid = Results + r"\streamGrid"

streamOrderGrid_tif = Results + r"\streamOrderGrid_tif"
networkTree_txt = Results + r"\networkTree_txt"
networkCoord_txt = Results + r"\networkCoord_txt"
stream_shp = Results + r"\stream_shp"
watershed_tif = Results + r"\watershed_tif"
watershed_shp = Results + r"\watershed_shp"


# Process: D8 Contributing Area
arcpy.gp.D8ContributingArea(FD, "", surfaceRatio, "false", "8", FA )

for threshold in range(int(thresholdStart),int(thresholdEnd),int(thresholdSteps)):

    # Process: Stream Definition By Threshold
    arcpy.gp.StreamDefByThreshold(FA, "", threshold, "8", streamGrid + str(threshold) + ".tif")

    # Process: Stream Reach And Watershed
    arcpy.gp.StreamReachAndWatershed(fillDEM, FD, FA, streamGrid + str(threshold) + ".tif", "", "false", "8", streamOrderGrid_tif + str(threshold) + ".tif", networkTree_txt + str(threshold) + ".txt", networkCoord_txt + str(threshold) + ".txt", stream_shp + str(threshold) + ".shp", watershed_tif + str(threshold) + ".tif")

    # converting watershed grids to vector
    arcpy.RasterToPolygon_conversion(watershed_tif + str(threshold) + ".tif", watershed_shp + str(threshold), simplify="SIMPLIFY", raster_field="Value")

    # Run Add surface information tool
    arcpy.AddSurfaceInformation_3d(stream_shp + str(threshold) + ".shp", fillDEM, out_property="Z_MIN;Z_MAX;SURFACE_LENGTH;AVG_SLOPE", method="BILINEAR", sample_distance="", z_factor="1", pyramid_level_resolution="0", noise_filtering="NO_FILTER")
