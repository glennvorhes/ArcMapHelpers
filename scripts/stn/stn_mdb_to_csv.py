import os
import csv
import arcpy
from collections import defaultdict

arcpy.env.overwriteOutput = True


def _parse_table(table_path, yr_, out_dir_, primary_key_cols, debug):
    tmp_table = r'in_memory\tmp_table'

    arcpy.CopyRows_management(table_path, tmp_table)

    # arcpy.AddField_management(tmp_table, 'year', 'LONG')
    # arcpy.CalculateField_management(tmp_table, 'year', yr_)

    out_csv = os.path.join(out_dir_, os.path.basename(table_path)) + '.csv'

    arcpy.CopyRows_management(tmp_table, out_csv)

    out_rows = []
    unique = []

    with open(out_csv, 'r') as f:
        reader = csv.reader(f)

        header_row = next(reader)
        header_row = [header_row[j].lower() for j in range(len(header_row))]
        header_dict = {header_row[j]: j for j in range(len(header_row))}
        header_row[0] = 'year'
        out_rows.append(header_row)

        counter = 0

        for rr in reader:
            # pk = ' '.join([rr[header_dict[k]] for k in primary_key_cols])

            if 'lcm_desc' in header_dict:
                rr[header_dict['lcm_desc']] = rr[header_dict['lcm_desc']].replace(',', ' ').replace("'", '').replace(
                    '"', '')

            # if pk in unique:
            #     # print('dup')
            #     continue
            #
            # unique.append(pk)
            rr[0] = yr_
            out_rows.append(rr)

            if debug:
                counter += 1
                if counter > 10:
                    break

    with open(out_csv, 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL, delimiter=',', lineterminator='\n')
        writer.writerows(out_rows)

    return out_csv


def mdb_to_csv(mdb_path, yr, out_dir, debug=False):

    if os.path.isdir(os.path.join(out_dir, os.pardir)):
        if os.path.isdir(out_dir):
            pass
        else:
            os.mkdir(out_dir)
    else:
        arcpy.AddError('Parent directory of\n{0}\ndoes not exist'.format(out_dir))

    table_dict = {
        'DT_RDWY_RTE': ['rdwy_rte_id'],
        'DT_RDWY_LINK': ['rdwy_link_id'],
        'DT_RDWY_CHN': ['rdwy_chn_id'],
        'DT_RDWY_RTE_LINK': ['rdwy_rte_id', 'rdwy_link_id'],
        'DT_RDWY_LINK_CHN': ['rdwy_link_id', 'rdwy_chn_id'],
        'DT_RDWY_LINK_HIST': ['link_hist_id'],
        'DT_RWRL_CUMT_MILG': ['rwrl_id'],
        'DT_RP': ['rp_id'],
        'DT_REF_SITE': ['ref_site_id']
    }

    output_dict = defaultdict(str)

    for k, v in table_dict.items():
        output_dict[k] = _parse_table(os.path.join(mdb_path, k), yr, out_dir, v, debug)
        arcpy.AddMessage("Parsed Table: {0}".format(k))

    return output_dict


if __name__ == '__main__':
    arcpy.AddError('cannot be here')
    _mdb_path = r'C:\Users\glenn\Desktop\stn_api\tables_2016\LCS_Tables.mdb'
    _out_dir = r'C:\tmp2\stn2016_2'
    _yr = 2016

    csv_dict = mdb_to_csv(_mdb_path, _yr, _out_dir, debug=True)

    print(csv_dict)










