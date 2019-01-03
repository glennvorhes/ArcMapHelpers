import arcpy
import os

arcpy.env.overwriteOutput = True

input_file = arcpy.GetParameterAsText(0)
output_file = arcpy.GetParameterAsText(1)


arcpy.ImportToolbox(r'C:\Users\glenn\PycharmProjects\ArcMapHelpers\ArcMapHelpers.tbx')

input_directory = r'C:\Users\glenn\OneDrive\Desktop'
output_directory = r"C:\temp"


for filename in os.listdir(input_directory):

    if filename.endswith('.csv'):
        print(filename, os.path.join(input_directory, filename))

        arcpy.ExampleCopy_arcmaphelpers(
            os.path.join(input_directory, filename),
            os.path.join(output_directory, filename)
        )




