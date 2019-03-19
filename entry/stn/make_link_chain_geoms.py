

import subprocess
import arcpy

yr = int(arcpy.GetParameterAsText(0))
ready = str(arcpy.GetParameterAsText(1)) == 'true'

db_name = 'db'


def check_link_chain_geom_count(_yr):
    c = '"select stn.build_chain_geoms({0});"'.format(_yr)
    _args = ['psql', '-c', c, db_name]

    _p = subprocess.Popen(' '.join(_args), stdout=subprocess.PIPE, shell=True)
    _proc_stdout = _p.communicate()[0].strip()
    _p.wait()

    arcpy.AddMessage(_proc_stdout)
    count_row = int(_proc_stdout.split('\n')[2])
    arcpy.AddMessage("{0} link chain geoms built for year {1}".format(count_row, _yr))


if ready:
    check_link_chain_geom_count(yr)
    arcpy.SetParameterAsText(2, 'true')
else:
    arcpy.AddWarning("All tables were not loaded correctly in previous steps")
    arcpy.SetParameterAsText(2, 'false')
