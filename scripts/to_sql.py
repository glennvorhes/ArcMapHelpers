import arcpy
import sys
import os
from arcpy_geom.from_feature_class import row_to_feature
from arcpy_geom.arcpy_descibe import ArcpyDescribeFeatureClass

try:
    from arcpy_geom import arcpy_descibe
except ImportError:
    sys.path.append(os.path.dirname(__file__))
    from arcpy_geom import arcpy_descibe


def _prepare_col_list(col_list_str):
    col_list_str = col_list_str.strip()

    if len(col_list_str) == 0:
        return []

    pieces = col_list_str.split(',')
    pieces = [p.strip().lower() for p in pieces]
    return pieces


def _prepare_constants(const_str):
    constants_dict = {}

    _constants_parts = const_str.split(',')

    for i in range(len(_constants_parts)):
        _constants_parts[i] = _constants_parts[i].strip()

        key_val = _constants_parts[i].split(':')
        assert len(key_val) == 2

        key_val[0] = key_val[0].strip()
        key_val[1] = key_val[1].strip()

        constants_dict[key_val[0]] = key_val[1]

        try:
            constants_dict[key_val[0]] = float(constants_dict[key_val[0]])

            if constants_dict[key_val[0]] % 1 == 0:
                constants_dict[key_val[0]] = int(constants_dict[key_val[0]])
        except ValueError:
            pass

    return constants_dict


def fc_to_sql(fc, srid, db_table_name, out_file, column_list='', constants_str_input='',
              date_format='%Y-%m-%d', debug=False):
    constants_dict = _prepare_constants(constants_str_input)
    include_cols = _prepare_col_list(column_list)

    desc = ArcpyDescribeFeatureClass(fc)
    search = arcpy.SearchCursor(fc)
    counter = 0

    with open(str(out_file), 'w') as the_file:

        for r in search:
            feat = row_to_feature(r, desc)
            sql_line = feat.as_postgres_sql(db_table_name, srid,
                                            include_columns=include_cols,
                                            fixed_values=constants_dict,
                                            date_format=date_format)

            the_file.write(sql_line + '\n')
            if debug:
                arcpy.AddMessage(sql_line)
                counter += 1
                if counter > 4:
                    break
    del search

    return out_file



# http://prj2epsg.org/epsg/3069
# http://prj2epsg.org/search



