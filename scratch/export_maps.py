# import modules and site-packages
import os
import arcpy

# set input and output arguments
input_mxd = arcpy.GetParameterAsText(0)
output_folder = arcpy.GetParameterAsText(1)
field_name = r"guid"

# export each data driven page out as a jpeg
mxd = arcpy.mapping.MapDocument(input_mxd)
for i in range(1, mxd.dataDrivenPages.pageCount + 1):
    mxd.dataDrivenPages.currentPageID = i
    row = mxd.dataDrivenPages.pageRow
    # I've created a variable page_name to store the current page name
    page_name = row.getValue(field_name)
    arcpy.AddMessage("Processing {}".format(page_name))
    # I've used os.path.join to join the path and file name for the output jpegs
    arcpy.mapping.ExportToJPEG(mxd, os.path.join(output_folder, page_name + ".jpg"), resolution=200)