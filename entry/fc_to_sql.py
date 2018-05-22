import sys
import os
import arcpy

try:
    from scripts.to_sql import fc_to_sql
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
    from scripts.to_sql import fc_to_sql

fc = arcpy.GetParameterAsText(0)
srid = int(str(arcpy.GetParameterAsText(1)))
db_table_name = arcpy.GetParameterAsText(2)
column_list = arcpy.GetParameterAsText(3)
constants = str(arcpy.GetParameterAsText(4))
date_format = str(arcpy.GetParameterAsText(5))
out_file = arcpy.GetParameterAsText(6)
debug = str(arcpy.GetParameterAsText(7)) == 'true'

# fc = r'C:\Users\glenn\Desktop\stn_api\stn_2014.gdb\rdwy_chn_arc'
# srid = 3069
# db_table_name = 'dt_rdwy_chn_geom'
# column_list = 'RDWY_CHN_ID'
# constants = "year:2014"
# date_format = '%Y-%m-%d'
# out_file = r'C:\tmp2\chain_2014.sql'
# debug = True

fc_to_sql(fc, srid, db_table_name, out_file, column_list=column_list,
          constants_str_input=constants, date_format=date_format, debug=debug)
