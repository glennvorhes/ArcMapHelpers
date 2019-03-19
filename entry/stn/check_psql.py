import os
import arcpy
import subprocess

pg_host = os.environ.get('PGHOST')
pg_user = os.environ.get('PGUSER')
pg_password = os.environ.get('PGPASSWORD')

# print(pg_host)
# print(pg_user)
# print(pg_password)

success = True


if not pg_host:
    arcpy.AddError("Environment variable '{0}' not set.\n It should be '{1}'".format(
        'PGHOST', 'transport-gis2sql.cee.wisc.edu'
    ))
    success = False

if not pg_user:
    arcpy.AddError("Environment variable '{0}' not set.\n It should be '{1}'".format(
        'PGUSER', 'editor'
    ))
    success = False

if not pg_password:
    arcpy.AddError("Environment variable '{0}' not set.\n Contact TOPS Staff for access (gavorhes@wisc.edu)".format(
        'PGPASSWORD'
    ))
    success = False

try:
    p = subprocess.Popen(['psql', '--help'], stdout=subprocess.PIPE, shell=True)
    p.wait()
except WindowsError as ex:
    success = False
    arcpy.AddError("""
The command line executable 'psql'
must be installed with the directory containing psql.exe
in the 'PATH' environment variable.
Download from https://www.enterprisedb.com/download-postgresql-binaries
Choose any 9.x version
extract only the 'bin' directory to a location and add it to the 'PATH'""")

if success:
    try:
        p = subprocess.Popen(['psql', '-c', 'select version();', 'db'], stdout=subprocess.PIPE, shell=True)
        p.wait()
        if p.returncode != 0:
            arcpy.AddMessage(p.returncode)
            success = False
            arcpy.AddError("""
Test connection to database failed. 
It may not be available on your network.
Try using using VPN and ping {0}""".format(pg_host))
    except WindowsError as ex:
        pass


arcpy.SetParameterAsText(0, 'true' if success else 'false')
