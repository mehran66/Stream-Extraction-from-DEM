__author__ = 'Mehran'
# This code finds the up stream path based on the FD matrix after the interactive selection of an arbitrary point


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

# Load required toolboxes
arcpy.AddToolbox("C:/Program Files/TauDEM/TauDEM5Arc/TauDEM Tools.tbx")
arcpy.ImportToolbox("C:/Program Files/TauDEM/TauDEM5Arc/TauDEM Tools.tbx")
arcpy.gp.toolbox = "C:/Program Files/TauDEM/TauDEM5Arc/TauDEM Tools.tbx";

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")
env.overwriteOutput = True

# ******************************************************************************
def move_to_next_pixel(fdr, fa, row, col):
    # get the fdr pixel value (x,y)
    temp = fa[row, col]
    downPixel = fdr[row, col]


    value = [fa[row, col+1], fa[row-1, col+1], fa[row-1, col], fa[row-1, col-1], fa[row, col-1], fa[row+1, col-1], fa[row+1, col], fa[row+1, col+1]]
    value[downPixel-1] = 0
    while True:
        valueMax = max(value)
        idx = max(range(len(value)), key = lambda i: value[i])
        if valueMax < temp:
            if valueMax == 1.0 or valueMax == 0:
                idx = 9
                break
            else:
                idx +=1
                break
        elif valueMax == 1.0 or valueMax == 0:
            idx = 9
            break
        else:
            value[idx] = 0
    #
    # /4/3/2/
    #/5/X/1/
    #/6/7/8/
    #

    # move the pixel
    if idx == 1:
        col +=1
    elif idx ==2:
        col +=1
        row -=1
    elif idx ==3:
        row -=1
    elif idx ==4:
        col -=1
        row -=1
    elif idx ==5:
        col -=1
    elif idx ==6:
        col -=1
        row +=1
    elif idx ==7:
        row +=1
    elif idx ==8:
        col +=1
        row +=1
    elif idx ==9:
        col = -1
        row = -1

    return (row, col)

# ******************************************************************************
# Local variables:
# Create a point object
fs = arcpy.GetParameter(0)
if fs == '#' or not fs:
	fs = "in_memory"

f = arcpy.FeatureSet(fs) # create a 
geom = json.loads(f.JSON)['features'][0]['geometry']
my_x = geom['x']
my_y = geom['y']
pnt = arcpy.Point(my_x, my_y)
arcpy.AddMessage ('Selected Point = (%5.3f,%5.3f)'% (geom['x'], geom['y']))

# Local variables:

fillDEM = arcpy.GetParameterAsText(1)
FD = arcpy.GetParameterAsText(2)
FA = arcpy.GetParameterAsText(3)
trace_points = arcpy.GetParameterAsText(4)
trace_outpath = arcpy.GetParameterAsText(5)

# Convert rasters to array

fillDEM_Array = arcpy.RasterToNumPyArray(fillDEM, nodata_to_value=0)
FD_Array = arcpy.RasterToNumPyArray(FD, nodata_to_value=0)
FA_Array = arcpy.RasterToNumPyArray(FA, nodata_to_value=0)



# Create raster object to get metadata
ux = arcpy.GetRasterProperties_management(fillDEM,"LEFT")
uy = arcpy.GetRasterProperties_management(fillDEM,"TOP")
cell_width = arcpy.GetRasterProperties_management(fillDEM,"CELLSIZEX")
cell_height = arcpy.GetRasterProperties_management(fillDEM, "CELLSIZEY")

# Convert point coordinates into raster indices
c = abs (int(((float(ux.getOutput(0)))-pnt.X) / (float(cell_width.getOutput(0)))))
r = abs (int(((float(uy.getOutput(0)))-pnt.Y) / (float(cell_height.getOutput(0)))))


z = fillDEM_Array[r,c]
coords=[]
while (int(z)!=0):
    # move downstream
    last_r = r
    last_c = c
    r,c = move_to_next_pixel(FD_Array,FA_Array,r,c)

    if r == -1:
        break

    # adjust x and y
    my_x += (c-last_c)*(float(cell_width.getOutput(0)))
    my_y += (last_r-r)*(float(cell_width.getOutput(0)))
    z = fillDEM_Array[r,c]
    print z

    # save this coordinate
    coords.append((my_x,my_y,z))


# write the output to the text file
#with open ("coords1.txt", "w") as f:
#    for temp in coords:
#        f.write("%5.5f, %5.5f, %5.5f\n" % (temp[0],temp[1],temp[2]))


# create the output feature class (point)
direcoryPath = os.path.dirname (trace_points)
filePath = os.path.basename (trace_points)
arcpy.CreateFeatureclass_management(direcoryPath, filePath,'POINT')

# create the output feature class (polyline)
direcoryPath = os.path.dirname (trace_outpath)
filePath = os.path.basename (trace_outpath)
arcpy.CreateFeatureclass_management(direcoryPath, filePath,'POLYLINE')

# create the point and line segment objects
point = arcpy.Point()
line_seg = arcpy.Array()

cursor1 = arcpy.InsertCursor(trace_points)
feat1 = cursor1.newRow()

featurelist = []
cursor2 = arcpy.InsertCursor(trace_outpath)
feat2 = cursor2.newRow()
for i in range(1, len(coords)-1):
    # Set X and Y for start and end points
    point.X = coords[i-1][0]
    point.Y = coords[i-1][1]
    feat1.shape = point
    cursor1.insertRow(feat1)
    line_seg.add(point)
    point.X = coords[i][0]
    point.Y = coords[i][1]
    line_seg.add(point)

    #Create a polyline object based on the array of points
    polyline = arcpy.Polyline(line_seg)

    # Clear the array for future use
    line_seg.removeAll()

    #Append to the list of polyline objects
    featurelist.append(polyline)

    #Insert the feature
    feat2.shape = polyline
    cursor2.insertRow(feat2)

del feat1
del cursor1
del feat2
del cursor2


