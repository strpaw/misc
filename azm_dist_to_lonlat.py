import re
import math

# Parameters of WGS84 ellipsoid
WGS84_A = 6378137.0  # semi-major axis of the WGS84 ellipsoid in m
WGS84_B = 6356752.3141  # semi-minor axis of the WGS84 ellipsoid in m
WGS84_F = 1 / 298.25722210088  # flattening of the WGS84 ellipsoid

# Units of measure
UOM_M = 'M'
UOM_KM = 'KM'
UOM_FEET = 'FEET'
UOM_SM = 'SM'
UOM_NM = 'NM'

# Types of angle
A_LON = 'LON'
A_LAT = 'LAT'

# Longitude and latitude regular expression,  format DMSH space separated
LON_DMSH_PATTERN = re.compile(r'''(?P<deg>\d{3})  # Degrees
                                  (\s)  # Delimiter
                                  (?P<min>[0-5]\d)  # Minutes
                                  (\s)  # Delimiter
                                  (?P<sec>[0-5]\d\.\d+|[0-5]\d)  # Second and decimal seconds
                                  (\s)
                                  (?P<hem>[EW])  # Hemisphere indicator
                               ''', re.VERBOSE)

LAT_DMSH_PATTERN = re.compile(r'''(?P<deg>\d{2}) # Degrees
                                  (\s)  # Delimiter
                                  (?P<min>[0-5]\d) # Minutes
                                  (\s)  # Delimiter
                                  (?P<sec>[0-5]\d\.\d+|[0-5]\d) # Seconds and decimal seconds
                                  (\s)
                                  (?P<hem>[NS])  # Hemisphere indicator
                                ''', re.VERBOSE)


def check_distance(dist):
    """ Checks if distance is valid.
    Assumption: valid distance is a positive float or integer number.
    :param dist: float, distance to check
    :return bool: True if dist is a valid distance, False otherwise
    """
    try:
        d = float(dist)
    except ValueError:
        return False
    else:
        return bool(d > 0)


def check_azimuth(azm):
    """ Checks if azimuth is valid.
    Assumption: valid azimuth is a float or integer number within interval <0, 360>
    :param azm: float, azimuth to check
    :return: bool: True if azm is a valid azimuth, False otherwise
    """
    try:
        a = float(azm)
    except ValueError:
        return False
    else:
        return bool(0 <= a <= 360)


def lon_dms_to_dd(dmsh):
    """ Converts longitude in degrees, minutes, seconds, hemisphere suffix (DMSH) format space separated to
     decimal degrees (DD) format .
    :param dmsh: str, longitude in DMSH format
    :return: dd: float, longitude in DD format, None if dmsh argument is invalid longitude in DMSH format
    """
    if LON_DMSH_PATTERN.match(dmsh):
        dms_parts = LON_DMSH_PATTERN.search(dmsh)
        h = dms_parts.group('hem')
        if h in 'EW':
            d = int(dms_parts.group('deg'))
            m = int(dms_parts.group('min'))
            s = float(dms_parts.group('sec'))
            if d > 180 or (d == 180 and (m > 0 or s > 0)):
                return None
            else:
                dd = d + m / 60 + s / 3600
                if h == 'W':
                    return -dd
                else:
                    return dd


def lat_dms_to_dd(dmsh):
    """ Converts latitude in degrees, minutes, seconds, hemisphere suffix (DMSH) format space separated to
     decimal degrees (DD) format .
    :param dmsh: str, latitude in DMSH format
    :return: dd: float, longitude in DD format, None if dmsh argument is invalid longitude in DMSH format
    """
    if LAT_DMSH_PATTERN.match(dmsh):
        dms_parts = LAT_DMSH_PATTERN.search(dmsh)
        h = dms_parts.group('hem')
        if h in 'NS':
            d = int(dms_parts.group('deg'))
            m = int(dms_parts.group('min'))
            s = float(dms_parts.group('sec'))
            if d > 90 or (d == 90 and (m > 0 or s > 0)):
                return None
            else:
                dd = d + m / 60 + s / 3600
                if h == 'S':
                    return -dd
                else:
                    return dd


def dd2_to_dmsh(dd, ang_type):
    """ Converts coordinate in DD (decimal degrees format) to DMSH (Degress, Minutes, Seconds, Hemisphere)
    space delimited format.
    :param: dd: float, latitude or longitude in decimal degrees format
    :param: ang_type: string, coordinate type
    :return: dmsh: string, latitude or longitude in DMSH format
    """
    dmsh, h = '', ''

    if dd < 0:
        if ang_type == A_LON:
            h = 'W'
        elif ang_type == A_LAT:
            h = 'S'
    else:
        if ang_type == A_LON:
            h = 'E'
        elif ang_type == A_LAT:
            h = 'N'

    abs_dd = math.fabs(dd)

    d = int(math.floor(abs_dd))
    m = int(math.floor((abs_dd - d) * 60))
    s = round((((abs_dd - d) * 60) - m) * 60, 4)

    if ang_type == A_LON:
        dmsh = '{d:03d} {m:02d} {s:07.4f} {h}'.format(d=d, m=m, s=s, h=h)
    elif ang_type == A_LAT:
        dmsh = '{d:02d} {m:02d} {s:07.4f} {h}'.format(d=d, m=m, s=s, h=h)

    return dmsh


def vincenty_direct_solution(lon_initial, lat_initial_, azimuth_initial, distance, a, b, f):
    """ Computes the latitude and longitude of the second point based on latitude, longitude,
    of the first point and distance and azimuth from first point to second point.
    Uses the algorithm by Thaddeus Vincenty for direct geodetic problem.
    For more information refer to: http://www.ngs.noaa.gov/PUBS_LIB/inverse.pdf
    :param lon_initial: float, longitude of the initial  point in decimal degrees format
    :param lat_initial_: float, latitude of the initial point in decimal degrees format
    :param azimuth_initial, azimuth from the initial point to the end point in decimal degrees format
    :param distance: float, distance from first point to second point; meters
    :param a: float, semi-major axis of ellipsoid in meters
    :param b: float, semi-minor axis of ellipsoid in meters
    :param f: float, flattening of ellipsoid
    :return lon_end, lat_end: float, float longitude and longitude of the end point in decimal degrees format
    """
    # Convert latitude, longitude, azimuth of the initial point to radians
    lon1 = math.radians(lon_initial)
    lat1 = math.radians(lat_initial_)
    alfa1 = math.radians(azimuth_initial)

    sin_alfa1 = math.sin(alfa1)
    cos_alfa1 = math.cos(alfa1)

    # U1 - reduced latitude
    tan_u1 = (1 - f) * math.tan(lat1)
    cos_u1 = 1 / math.sqrt(1 + tan_u1 * tan_u1)
    sin_u1 = tan_u1 * cos_u1

    # sigma1 - angular distance on the sphere from the equator to initial point
    sigma1 = math.atan2(tan_u1, math.cos(alfa1))

    # sin_alfa - azimuth of the geodesic at the equator
    sin_alfa = cos_u1 * sin_alfa1
    cos_sq_alfa = 1 - sin_alfa * sin_alfa
    u_sq = cos_sq_alfa * (a * a - b * b) / (b * b)
    A = 1 + u_sq / 16384 * (4096 + u_sq * (-768 + u_sq * (320 - 175 * u_sq)))
    B = u_sq / 1024 * (256 + u_sq * (-128 + u_sq * (74 - 47 * u_sq)))

    sigma = distance / (b * A)
    sigmap = 1
    sin_sigma, cos_sigma, cos2sigma_m = None, None, None

    while math.fabs(sigma - sigmap) > 1e-12:
        cos2sigma_m = math.cos(2 * sigma1 + sigma)
        sin_sigma = math.sin(sigma)
        cos_sigma = math.cos(sigma)
        d_sigma = B * sin_sigma * (cos2sigma_m + B / 4 * (
                    cos_sigma * (-1 + 2 * cos2sigma_m * cos2sigma_m) - B / 6 * cos2sigma_m * (
                        -3 + 4 * sin_sigma * sin_sigma) * (-3 + 4 * cos2sigma_m * cos2sigma_m)))
        sigmap = sigma
        sigma = distance / (b * A) + d_sigma

    var_aux = sin_u1 * sin_sigma - cos_u1 * cos_sigma * cos_alfa1  # Auxiliary variable

    # Latitude of the end point in radians
    lat2 = math.atan2(sin_u1 * cos_sigma + cos_u1 * sin_sigma * cos_alfa1,
                      (1 - f) * math.sqrt(sin_alfa * sin_alfa + var_aux * var_aux))

    lamb = math.atan2(sin_sigma * sin_alfa1, cos_u1 * cos_sigma - sin_u1 * sin_sigma * cos_alfa1)
    C = f / 16 * cos_sq_alfa * (4 + f * (4 - 3 * cos_sq_alfa))
    L = lamb - (1 - C) * f * sin_alfa * (
                sigma + C * sin_sigma * (cos2sigma_m + C * cos_sigma * (-1 + 2 * cos2sigma_m * cos2sigma_m)))
    # Longitude of the end point in radians
    lon2 = (lon1 + L + 3 * math.pi) % (2 * math.pi) - math.pi

    # Convert to decimal degrees
    lon_end = math.degrees(lon2)
    lat_end = math.degrees(lat2)

    return lon_end, lat_end


def compute_position(lon_dmsh, lat_dmsh, azimuth, distance):
    """ Computes position of end point based on position of initial point and initial azimuth.
    :param lon_dmsh: str, initial longitude in DMSH format
    :param lat_dmsh: str, initial longitude in DMSH format
    :param azimuth: str, initial azimuth
    :param distance: str, distance from initial point to end point in meters
    """
    err_msg = ''
    is_input_valid = True

    lon_initial_dd = lon_dms_to_dd(lon_dmsh)
    lat_initial_dd = lat_dms_to_dd(lat_dmsh)

    if lon_initial_dd is None:
        is_input_valid = False
        err_msg = 'Longitude should be in format DMSH.\n'

    if lat_initial_dd is None:
        is_input_valid = False
        err_msg += 'Latitude should be in format DMSH.\n'

    if check_azimuth(azimuth) is False:
        is_input_valid = False
        err_msg += 'Azimuth should be a number within interval <0, 360>.\n'

    if check_distance(distance) is False:
        is_input_valid = False
        err_msg += 'Distance should be a positive number.\n'

    if is_input_valid:

        lon2_dd, lat2_dd = vincenty_direct_solution(lon_initial_dd, lat_initial_dd,
                                                    float(azimuth), float(distance), WGS84_A, WGS84_B, WGS84_F)

        end_lon_dmsh = dd2_to_dmsh(lon2_dd, A_LON)
        end_lat_dmsh = dd2_to_dmsh(lat2_dd, A_LAT)
        print('End longitude: {}'.format(end_lon_dmsh))
        print('End latitude: {}'.format(end_lat_dmsh))
    else:
        print(err_msg)


def main():
    lon1_dms = input('Initial Longitude: ')
    lat1_dms = input('Initial Latitude: ')
    azm = input('Initial Azimuth: ')
    dist = input('Distance in meters: ')

    compute_position(lon1_dms, lat1_dms, azm, dist)


if __name__ == '__main__':
    main()
