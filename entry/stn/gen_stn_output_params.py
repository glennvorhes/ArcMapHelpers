import arcpy
import os

wk = str(arcpy.GetParameterAsText(0))
yr = int(str(arcpy.GetParameterAsText(1)))


assert os.path.isdir(wk)

arcpy.SetParameterAsText(2, "year:{0}".format(yr))

chn_sql = os.path.join(wk, 'chain_geom_{0}.sql'.format(yr))
link_sql = os.path.join(wk, 'link_geom_{0}.sql'.format(yr))
rp_sql = os.path.join(wk, 'rp_geom_{0}.sql'.format(yr))
ref_sql = os.path.join(wk, 'ref_site_geom_{0}.sql'.format(yr))

for f in [chn_sql, link_sql, rp_sql, ref_sql]:
    with open(f, 'w') as the_f:
        the_f.write('\t')

arcpy.SetParameterAsText(3, chn_sql)
arcpy.SetParameterAsText(4, link_sql)
arcpy.SetParameterAsText(5, rp_sql)
arcpy.SetParameterAsText(6, ref_sql)


