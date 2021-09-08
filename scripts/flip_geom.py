import arcpy
from arcpy_geom import ArcpyDescribeFeatureClass
from arcpy_geom.from_feature_class import row_to_feature
from arcpy_geom.features import LineString


def flip_geom(pth):

    desc = ArcpyDescribeFeatureClass(pth)

    upd = arcpy.UpdateCursor(pth)

    for r in upd:
        feat = row_to_feature(r, desc)
        assert isinstance(feat, LineString)

        feat.flip_vertices()
        r.shape = feat.shape
        upd.updateRow(r)

    del upd


if __name__ == '__main__':

    flip_geom(r'T:\Staff\Vorhes\scratch\test_out.shp')
    print('here')

