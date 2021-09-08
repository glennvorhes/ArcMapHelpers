import arcpy
import sys
import os

try:
    from scripts.flip_geom import flip_geom
except ImportError:

    add_path = os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir)

    arcpy.AddMessage(add_path)

    sys.path.append(add_path)

    from scripts.flip_geom import flip_geom

lyr = arcpy.GetParameterAsText(0)

flip_geom(lyr)

arcpy.AddMessage("Flipped Lines: {0}".format(arcpy.GetCount_management(lyr).getOutput(0)))


