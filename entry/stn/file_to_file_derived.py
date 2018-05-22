import arcpy

f = arcpy.GetParameterAsText(0)
arcpy.SetParameterAsText(1, f)
