import re
import sys


class Arinc424CoordinatesConversion:

    ARINC424_LETTER = {'NW': 'N',
                       'NE': 'E',
                       'SW': 'W',
                       'SE': 'S'}

    HEMISPHERES = {'N': ('W', 'N'),
                   'E': ('E', 'N'),
                   'W': ('W', 'S'),
                   'S': ('E', 'S')}

    # Templates for ARINC424 shorthand coordinates
    LON_LESS_HUNDRED_TMPL = '{lat}{lon}{letter}'
    LON_EQUAL_GRATER_HUNDRED_TMPL = '{lat}{letter}{lon}'

    LON_DMH_FULL_DEGREES_REGEX = re.compile(r'''(180|1[0-7]\d|0\d{2}|0{2}\d)
                               (00[EW])
                               ''', re.VERBOSE)

    LAT_DMH_FULL_DEGREES_REGEX = re.compile(r'''(90|[0-8]\d|)
                                   (00[NS])
                                   ''', re.VERBOSE)

    ARINC424_REGEXS = {'LON_LESS_HUNDRED_REGEX': re.compile(r'''(?P<lat>\d{2})  # First two of latitude
                                                                (?P<lon>\d{2})  # Second and third of longitude
                                                                (?P<letter>[NSEW])  # Letter designator 
                                                            ''', re.VERBOSE),
                       'LON_EQUAL_GRATER_HUNDRED_REGEX': re.compile(r'''(?P<lat>\d{2})  # First two of latitude
                                                                        (?P<letter>[NSEW])  # Letter designator 
                                                                        (?P<lon>\d{2})  # Second and third of longitude
                                                                     ''', re.VERBOSE)}

    @staticmethod
    def is_longitude_dmh(lon):
        """ Checks if longitude is in DMH format (Degrees, minutes, hemisphere) and is full degrees.
        :param lon: str, longitude in DMH format, e.g. 13500E
        :return: bool:
        """
        return bool(Arinc424CoordinatesConversion.LON_DMH_FULL_DEGREES_REGEX.match(lon))

    @staticmethod
    def is_latitude_dmh(lat):
        """ Checks if latitude is in DMH format (Degrees, minutes, hemisphere) and is full degrees.
        :param lat: str, longitude in DMH format, e.g. 3500N
        :return: bool:
        """
        return bool(Arinc424CoordinatesConversion.LAT_DMH_FULL_DEGREES_REGEX.match(lat))

    @staticmethod
    def get_hemispheres_from_coord_pair(lon, lat):
        """ Gets hemisphere characters from longitude and latitude
        :param lon: str, longitude in DMH format
        :param lat: str, latitude in DMH format
        :return: str: hemisphere characters from lon and lat
        """
        lon_hem = lon[-1]
        lat_hem = lat[-1]
        return lat_hem + lon_hem

    @staticmethod
    def get_arinc424_format_tmpl(lon):
        lon_int = int(lon[:3])
        if lon_int < 100:
            return Arinc424CoordinatesConversion.LON_LESS_HUNDRED_TMPL
        else:
            return Arinc424CoordinatesConversion.LON_EQUAL_GRATER_HUNDRED_TMPL

    @staticmethod
    def coord_to_arinc424(lon, lat):
        """ Converts full degrees coordinates to ARINC424 format.
        :param lon: str, longitude in DMH format
        :param lat: str, latitude in DMH format
        :return: str: full degrees coordinates in ARINC424 format
        """
        hems = Arinc424CoordinatesConversion.get_hemispheres_from_coord_pair(lon, lat)
        arinc424_letter = Arinc424CoordinatesConversion.ARINC424_LETTER[hems]
        arinc424_format = Arinc424CoordinatesConversion.get_arinc424_format_tmpl(lon)
        lon = lon[1:3]
        lat = lat[:2]
        return arinc424_format.format(lat=lat, lon=lon, letter=arinc424_letter)

    @staticmethod
    def is_lon_lat_arinc424_code_within_range(lon, lat):
        """ Checks if longitude and latitude parts of ARINC424 code are witihn range.
        :param lon: str, longitude part from ARINC424 code
        :param lat: str, latitude part from ARINC424 code
        :return: bool:
        """
        msg = ''
        is_within_range = True

        if int(lon) > 80:
            is_within_range = False
            msg = 'Longitude part can\'t be grater the 80. '

        if int(lat) > 90:
            is_within_range = False
            msg += 'Latitude part can\'t be grater the 90.'

        if not is_within_range:
            print(msg)

        return is_within_range

    @staticmethod
    def arinc424_to_coordinates(arinc424):
        """ Converts from ARINC424 shorthand format to DM format
        :param arinc424: str, coordinates in ARINC424 shorthand code
        :return: str, coordinates in DMH format, e.g.: 16000W 5000N
        """
        for regex in Arinc424CoordinatesConversion.ARINC424_REGEXS:
            if Arinc424CoordinatesConversion.ARINC424_REGEXS.get(regex).match(arinc424):
                groups = Arinc424CoordinatesConversion.ARINC424_REGEXS.get(regex).search(arinc424)
                letter = groups.group('letter')
                lat = groups.group('lat')
                lon = groups.group('lon')

                if Arinc424CoordinatesConversion.is_lon_lat_arinc424_code_within_range(lon, lat):
                    lon_hem, lat_hem = Arinc424CoordinatesConversion.HEMISPHERES[letter]
                    if regex == 'LON_LESS_HUNDRED_REGEX':
                        return '0{}00{} {}00{}'.format(lon, lon_hem, lat, lat_hem)
                    elif regex == 'LON_EQUAL_GRATER_HUNDRED_REGEX':
                        return '1{}00{} {}00{}'.format(lon, lon_hem, lat, lat_hem)


def main(args):
    if len(args) == 1:  # ARINC424 -> Lon, Lat
        coordinates = Arinc424CoordinatesConversion.arinc424_to_coordinates(args[0])
        if coordinates is not None:
            print(coordinates)
        else:
            print('Input is not ARINC424 code for full degrees.')
    elif len(args) == 2:  # Lon, lat -> ARINC424
        lon, lat = args
        if Arinc424CoordinatesConversion.is_longitude_dmh(lon) and Arinc424CoordinatesConversion.is_latitude_dmh(lat):
            arinc424_code = Arinc424CoordinatesConversion.coord_to_arinc424(lon, lat)
            print(arinc424_code)
        else:
            print('Input coordinates must be full degrees in DMH format, example: 12200E')

    else:
        print('Usage if you want to convert from ARINC424 code to Longitude and latitude:\n'
              'arinc424_shorthand_conversion.py <arinc424_code>\n'
              'Usage if you want to convert from Longitude and latitude ARINC424 code:\n'
              'arinc424_shorthand_conversion.py <longitude_dmh> <latitude_dmh>)')


if __name__ == '__main__':
    main(sys.argv[1:])
