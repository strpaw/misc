import unittest
from .arinc424_shorthand_conversion import *


class DistToLonLatTests(unittest.TestCase):
    def test_is_longitude_dmh(self):
        valid_lon_dmh = ['00000E', '00100W', '02900E', '10000E', '17900E']

        for lon in valid_lon_dmh:
            self.assertTrue(Arinc424CoordinatesConversion.is_longitude_dmh(lon))

        invalid_lon_dmh = ['00000', '00125W', '02900S', '10022E', '179E', '18100E']
        for lon in invalid_lon_dmh:
            self.assertFalse(Arinc424CoordinatesConversion.is_longitude_dmh(lon))

    def test_is_is_latitude_dmh(self):
        valid_lat_dmh = ['0000N', '0100N', '2900S', '9000N']

        for lat in valid_lat_dmh:
            self.assertTrue(Arinc424CoordinatesConversion.is_latitude_dmh(lat))

        invalid_lat_dmh = ['0000', '1000E', '2330S', '23S', '9100N']
        for lat in invalid_lat_dmh:
            self.assertFalse(Arinc424CoordinatesConversion.is_longitude_dmh(lat))

    def test_get_arinc424_format_tmpl(self):
        self.assertEqual(Arinc424CoordinatesConversion.LON_LESS_HUNDRED_TMPL,
                         Arinc424CoordinatesConversion.get_arinc424_format_tmpl('099E'))
        self.assertEqual(Arinc424CoordinatesConversion.LON_EQUAL_GRATER_HUNDRED_TMPL,
                         Arinc424CoordinatesConversion.get_arinc424_format_tmpl('100W'))
        self.assertEqual(Arinc424CoordinatesConversion.LON_EQUAL_GRATER_HUNDRED_TMPL,
                         Arinc424CoordinatesConversion.get_arinc424_format_tmpl('101W'))

    def test_coord_to_arinc424(self):
        self.assertEqual('50N60', Arinc424CoordinatesConversion.coord_to_arinc424(lat='5000N', lon='16000W'))
        self.assertEqual('5060N', Arinc424CoordinatesConversion.coord_to_arinc424(lat='5000N', lon='06000W'))
        self.assertEqual('50E60', Arinc424CoordinatesConversion.coord_to_arinc424(lat='5000N', lon='16000E'))
        self.assertEqual('5060E', Arinc424CoordinatesConversion.coord_to_arinc424(lat='5000N', lon='06000E'))
        self.assertEqual('50W60', Arinc424CoordinatesConversion.coord_to_arinc424(lat='5000S', lon='16000W'))
        self.assertEqual('5060W', Arinc424CoordinatesConversion.coord_to_arinc424(lat='5000S', lon='06000W'))
        self.assertEqual('5060S', Arinc424CoordinatesConversion.coord_to_arinc424(lat='5000S', lon='06000E'))
        self.assertEqual('50S60', Arinc424CoordinatesConversion.coord_to_arinc424(lat='5000S', lon='16000E'))