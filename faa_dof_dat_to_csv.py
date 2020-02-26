""" Function to convert DOF (Digital Obstacle File) from dat format to csv format according to
    Digital Obstacle File Jun 19, 2018 specification.

    For more information please refer to:
    https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/dof/media/DOF_README_06-19-2018.pdf
    https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/dof/

    Data in csv format can be easily imported Geographic Information Systems (GIS) software or database.
"""
import csv


def dms2dd(dmsh):
    """ Converts DMS format of latitude, longitude in DOF file to DD format
    param: dms: string, latitude or longitude in degrees, minutes, seconds format
    return: dd: float, latitude or longitude in decimal degrees format
    """
    h = dmsh[-1]  # Get hemisphere
    dms = dmsh[:-1]  # Trim last character with hemisphere
    dms_parts = dms.split(' ')  # Split into 3-element list: degrees, minutes, seconds
    d = float(dms_parts[0])
    m = float(dms_parts[1])
    s = float(dms_parts[2])

    dd = d + m / 60 + s / 3600
    if h in ['W', 'S']:
        dd = - dd
    return dd


def faa_dof2csv(in_file, output_file):
    """ Converts Digital Obstacle File dat format into csv format and calculates latitude and longitude in DD format.
    :param in_file: str, Digital Obstacle File path
    :param output_file: str, output CSV file path
    """
    cvs_field_names = ['oas_code',
                       'obs_number',
                       'verif_stat',
                       'country_id',
                       'state_id',
                       'city_name',
                       'lat_dms',
                       'lon_dms',
                       'obs_type',
                       'quantity',
                       'agl_height',
                       'ams_height',
                       'lighting',
                       'hor_acc',
                       'vert_acc',
                       'mar_indicator',
                       'faa_study_number',
                       'action',
                       'jdate',
                       'lat_dd',
                       'lon_dd']

    with open(in_file, 'r') as dof_file:
        with open(output_file, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=cvs_field_names, delimiter=',')
            writer.writeheader()
            line_nr = 0
            for line in dof_file:
                line_nr += 1
                if line_nr < 5:  # Skip first 4 lines - header of DOF
                    pass
                else:
                    # Write parsed data to output file
                    lat_dms = line[35:47]
                    lon_dms = line[48:61]
                    writer.writerow({'oas_code': line[0:2],
                                     'obs_number': line[3:9],
                                     'verif_stat': line[10],
                                     'country_id': line[12:14],
                                     'state_id': line[15:17],
                                     'city_name': line[18:34].rstrip(),
                                     'lat_dms': lat_dms,
                                     'lon_dms': lon_dms,
                                     'obs_type': line[62:80].rstrip(),
                                     'quantity': line[81],
                                     'agl_height': line[83:88],
                                     'ams_height': line[89:94],
                                     'lighting': line[95],
                                     'hor_acc': line[97],
                                     'vert_acc': line[99],
                                     'mar_indicator': line[101],
                                     'faa_study_number': line[103:117].strip(),
                                     'action': line[118],
                                     'jdate': line[120:127],
                                     'lat_dd': str(lat_dms),
                                     'lon_dd': str(lon_dms)})
