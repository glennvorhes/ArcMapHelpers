import os
import arcpy
from collections import OrderedDict
import subprocess
from datetime import datetime

db_name = 'db'


def _check_row_count(table, _yr):
    c = '"SELECT COUNT(*) FROM {0} WHERE year = {1};"'.format(table, _yr)
    _args = ['psql', '-c', c, db_name]
    # arcpy.AddMessage(sql)
    # arcpy.AddMessage(k)

    _p = subprocess.Popen(' '.join(_args), stdout=subprocess.PIPE, shell=True)
    _proc_stdout = _p.communicate()[0].strip()
    _p.wait()

    count_row = int(_proc_stdout.split('\n')[2])

    if count_row > 0:
        arcpy.AddMessage("{0} rows in {1} for year {2}".format(count_row, table, _yr))
        return True
    else:
        arcpy.AddWarning("0 rows in {0} for year {1}".format(table, _yr))
        return False


if __name__ == "__main__":

    link_geom_sql = arcpy.GetParameterAsText(0)
    chain_geom_sql = arcpy.GetParameterAsText(1)
    rp_geom_sql = arcpy.GetParameterAsText(2)
    ref_site_geom_sql = arcpy.GetParameterAsText(3)

    route_csv = arcpy.GetParameterAsText(4)
    route_link_csv = arcpy.GetParameterAsText(5)
    link_chain_csv = arcpy.GetParameterAsText(6)
    link_hist_csv = arcpy.GetParameterAsText(7)
    cumt_milg_csv = arcpy.GetParameterAsText(8)
    link_csv = arcpy.GetParameterAsText(9)
    chain_csv = arcpy.GetParameterAsText(10)
    rp_csv = arcpy.GetParameterAsText(11)
    ref_site_csv = arcpy.GetParameterAsText(12)

    yr = int(arcpy.GetParameterAsText(13))

    sql = 'INSERT INTO stn.stn_version (year, loaded) VALUES ({0}, \'{1}\');'.format(
        yr, datetime.now().strftime('%Y-%m-%d'))

    p = subprocess.Popen(['psql', '-c', sql, db_name])
    p.wait()

    if p.returncode == 0:
        arcpy.AddMessage('Added new version record for year {0}'.format(yr))
    else:
        arcpy.AddMessage('Version record for year {0} exists'.format(yr))

    table_file_dict = OrderedDict()

    table_file_dict['stn.dt_rdwy_rte'] = route_csv
    table_file_dict['stn.dt_rdwy_link'] = link_csv
    table_file_dict['stn.dt_rdwy_chn'] = chain_csv
    table_file_dict['stn.dt_rdwy_rte_link'] = route_link_csv
    table_file_dict['stn.dt_rdwy_link_chn'] = link_chain_csv
    table_file_dict['stn.dt_rdwy_link_hist'] = link_hist_csv
    table_file_dict['stn.dt_rp'] = rp_csv
    table_file_dict['stn.dt_ref_site'] = ref_site_csv
    table_file_dict['stn.dt_rwrl_cumt_milg'] = cumt_milg_csv

    for k, v in table_file_dict.items():

        args = ['psql', '-c', 'delete from {0} where year = {1};'.format(k, yr), db_name]
        arcpy.AddMessage('\nRunning: ' + ' '.join(args))
        p = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
        p.wait()

        args = ['psql', '-c', "\"\\copy {0} FROM {1} DELIMITER ',' CSV HEADER;\"".format(k, v), db_name]
        arcpy.AddMessage('\nRunning: ' + ' '.join(args))
        p = subprocess.Popen(' '.join(args), stdout=subprocess.PIPE, shell=True)
        proc_stdout = p.communicate()[0].strip()
        p.wait()

        arcpy.AddMessage(proc_stdout)

        if p.returncode == 0:
            arcpy.AddMessage('Loaded {0} into {1}'.format(v, k))
        else:
            arcpy.AddWarning('### Error loading {0} into {1} ####'.format(v, k))

    geom_file_dict = {
        'stn.dt_rdwy_link_geom': link_geom_sql,
        'stn.dt_rdwy_chn_geom': chain_geom_sql,
        'stn.dt_rp_geom': rp_geom_sql,
        'stn.dt_ref_site_geom': ref_site_geom_sql
    }

    for k, v in geom_file_dict.items():
        args = ['psql', '-c', 'delete from {0} where year = {1};'.format(k, yr), db_name]
        arcpy.AddMessage('\nRunning: ' + ' '.join(args))
        p = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
        p.wait()

        args = ['psql', '-f', v, db_name]
        arcpy.AddMessage('\nRunning: ' + ' '.join(args))
        p = subprocess.Popen(' '.join(args), stdout=subprocess.PIPE, shell=True)
        proc_stdout = p.communicate()[0].strip()
        p.wait()

        if p.returncode == 0:
            arcpy.AddMessage('Loaded {0} into {1}'.format(v, k))
        else:
            arcpy.AddWarning('### Error loading {0} into {1} ####'.format(v, k))

    success = True

    for k in table_file_dict.keys():
        s = _check_row_count(k, yr)
        success = success and s

    for k in geom_file_dict.keys():
        s = _check_row_count(k, yr)
        success = success and s

    if success:
        arcpy.AddMessage('All tables loaded successfully')
        arcpy.SetParameterAsText(14, 'true')
    else:
        arcpy.AddWarning('Some tables did not load')
        arcpy.SetParameterAsText(14, 'false')


