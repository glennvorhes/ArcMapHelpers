import sys
import os
import arcpy

arcpy.env.OverwriteOutput = True

try:
    from scripts.util import make_guid
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
    from scripts.util import make_guid

arcpy.SetParameterAsText(0, make_guid())

