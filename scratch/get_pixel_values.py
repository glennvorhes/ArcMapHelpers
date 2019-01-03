import arcpy
from uuid  import uuid4

try:
    import arcpy_geom
    from arcpy_geom import arcpy_descibe
except ImportError:
    import sys, os

    sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
    from arcpy_geom import arcpy_descibe


def get_zonal(tabl):

    srch = arcpy.SearchCursor(tabl)
    r = next(srch)
    pix_std = r.getValue("STD")
    pix_mean = r.getValue("MEAN")
    del r, srch

    return pix_std, pix_mean 

inp = arcpy.GetParameterAsText(0)
img = arcpy.GetParameterAsText(1)

all_cnt = int(arcpy.GetCount_management(inp ).getOutput(0))


field_names = [f.name for f in arcpy.ListFields(inp)]



mask = r"C:\temp\truck\{0}_mask.tif".format(uuid4())
one_feature = 'one_feature'
one_feature_copy = r'in_memory\one_f'

upd = arcpy.UpdateCursor(inp)

counter = 0

for r in upd:
    counter += 1
    g = str(r.getValue('guid'))

    color_tif = r"C:\temp\truck\{0}_{1}_color.tif".format(g, str(uuid4()))
    arcpy.AddMessage("{0} of {1}: {2}".format(counter, all_cnt, g))

    arcpy.MakeFeatureLayer_management(inp, 'one_feature', '"guid" = \'{0}\''.format(g))
    arcpy.CopyFeatures_management('one_feature', one_feature_copy)

#    arcpy.PolygonToRaster_conversion(one_feature_copy, 'FID', mask)
    arcpy.gp.ExtractByMask_sa(img, one_feature_copy, color_tif)

    arcpy.MakeRasterLayer_management(color_tif, 'red_pix', band_index=1)
    arcpy.MakeRasterLayer_management(color_tif, 'green_pix', band_index=2)
    arcpy.MakeRasterLayer_management(color_tif, 'blue_pix', band_index=3)

    arcpy.gp.ZonalStatisticsAsTable_sa(one_feature_copy, "guid", 'red_pix', r"in_memory\zone_red", "DATA", "ALL")
    arcpy.gp.ZonalStatisticsAsTable_sa(one_feature_copy, "guid", 'green_pix', r"in_memory\zone_green", "DATA", "ALL")
    arcpy.gp.ZonalStatisticsAsTable_sa(one_feature_copy, "guid", 'blue_pix', r"in_memory\zone_blue", "DATA", "ALL")

    r_std, r_avg = get_zonal(r"in_memory\zone_red")
    g_std, g_avg = get_zonal(r"in_memory\zone_green")
    b_std, b_avg = get_zonal(r"in_memory\zone_blue")

    avg_std = (r_std + g_std + b_std) / 3
    r.setValue('red_std', r_std)
    r.setValue('red_avg', r_avg)
    r.setValue('grn_std', g_std)
    r.setValue('grn_avg', g_avg)
    r.setValue('blu_std', b_std)
    r.setValue('blu_avg', b_avg)
    r.setValue('avg_std', avg_std)

    upd.updateRow(r)

del upd

arcpy.SetParameterAsText(2, inp)
