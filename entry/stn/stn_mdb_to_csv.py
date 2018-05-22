import sys
import os
import arcpy

try:
    from scripts.stn.stn_mdb_to_csv import mdb_to_csv
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
    from scripts.stn.stn_mdb_to_csv import mdb_to_csv


mdb_path = arcpy.GetParameterAsText(0)
yr = int(str(arcpy.GetParameterAsText(1)))
out_dir = arcpy.GetParameterAsText(2)
debug = str(arcpy.GetParameterAsText(3)) == 'true'

csv_dict = mdb_to_csv(mdb_path, yr, out_dir, debug=debug)

arcpy.AddMessage(csv_dict)

arcpy.SetParameterAsText(4, csv_dict['DT_RDWY_RTE'])
arcpy.SetParameterAsText(5, csv_dict['DT_RDWY_LINK'])
arcpy.SetParameterAsText(6, csv_dict['DT_RDWY_CHN'])
arcpy.SetParameterAsText(7, csv_dict['DT_RDWY_RTE_LINK'])
arcpy.SetParameterAsText(8, csv_dict['DT_RDWY_LINK_CHN'])
arcpy.SetParameterAsText(9, csv_dict['DT_RDWY_LINK_HIST'])
arcpy.SetParameterAsText(10, csv_dict['DT_RWRL_CUMT_MILG'])
arcpy.SetParameterAsText(11, csv_dict['DT_RP'])
arcpy.SetParameterAsText(12, csv_dict['DT_REF_SITE'])
