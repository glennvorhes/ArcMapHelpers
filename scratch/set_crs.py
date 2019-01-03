import arcpy

try:
    import arcpy_geom
    from arcpy_geom import arcpy_descibe
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
    from arcpy_geom import arcpy_descibe

inp = arcpy.GetParameterAsText(0)
desc = arcpy_descibe.ArcpyDescribeFeatureClass(inp)


arcpy.env.outputCoordinateSystem = desc.srs

arcpy.SetParameterAsText(1, inp)


