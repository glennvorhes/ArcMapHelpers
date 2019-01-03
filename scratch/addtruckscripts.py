import arcpy


try:
    import arcpy_geom
    from arcpy_geom import arcpy_descibe
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
    from arcpy_geom import arcpy_descibe

inp = arcpy.GetParameterAsText(0)

field_names = [f.name for f in arcpy.ListFields(inp)]

for f in ['near_cor', 'near_ramp']:
    if f not in field_names:
        arcpy.AddField_management(inp, f, "SHORT")

for f in ['combo', 'guid']:
    if f not in field_names:
        arcpy.AddField_management(inp, f, "TEXT", "", "", 50)

for f in ['zone_min', 'zone_max', 'zone_avg']:
    if f not in field_names:
        arcpy.AddField_management(inp, f, "DOUBLE")

for f in ['flag']:
    if f not in field_names:
        arcpy.AddField_management(inp, f, "SHORT")

for f in ['red_std', 'red_avg', 'grn_std', 'grn_avg', 'blu_std', 'blu_avg', 'avg_std']:
    if f not in field_names:
        arcpy.AddField_management(inp, f, "DOUBLE")


desc = arcpy_descibe.ArcpyDescribeFeatureClass(inp)
arcpy.env.outputCoordinateSystem = desc.srs

arcpy.SetParameterAsText(1, inp)

