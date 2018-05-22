import os
import arcpy
from subprocess import Popen

pg_host = os.environ.get('PGHOST')
pg_user = os.environ.get('PGUSER')
pg_password = os.environ.get('PGPASSWORD')

print(pg_host)
print(pg_user)
print(pg_password)

if not pg_host:
    arcpy.AddError("Environment variable '{0}' not set.\n It should be '{1}'".format(
        'PGHOST', 'transport-gis2sql.cee.wisc.edu'
    ))

if not pg_user:
    arcpy.AddError("Environment variable '{0}' not set.\n It should be '{1}'".format(
        'PGUSER', 'transport-gis2sql.cee.wisc.edu'
    ))

if not pg_password:
    arcpy.AddError("Environment variable '{0}' not set.\n Contact TOPS Staff for access (gavorhes@wisc.edu)".format(
        'PGPASSWORD'
    ))

try:
    p = Popen(['psql', '--help'])
    p.wait()
except WindowsError as ex:
    arcpy.AddError("The command line executable 'psql' must be installed with the directory in the 'PATH' environment varialble")

arcpy.SetParameterAsText(0, "true")
