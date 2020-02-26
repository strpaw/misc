import unittest
from .azm_dist_to_lonlat import *


class DistToLonLatTests(unittest.TestCase):

    def test_check_distance(self):
        self.assertEqual(False, check_distance(-1))
        self.assertEqual(False, check_distance(0))
        self.assertEqual(True, check_distance(1))
        self.assertEqual(True, check_distance(100.1))
        self.assertEqual(True, check_distance('255.3'))
        self.assertEqual(False, check_distance('test'))

    def test_check_azimuth(self):
        self.assertEqual(False, check_azimuth(-1))
        self.assertEqual(True, check_azimuth(0))
        self.assertEqual(True, check_azimuth(0.1))
        self.assertEqual(True, check_azimuth(360))
        self.assertEqual(False, check_azimuth(360.1))
        self.assertEqual(True, check_azimuth('122.44'))
        self.assertEqual(False, check_azimuth('qwerty'))

    def test_lon_dms_to_dd(self):
        self.assertEqual(None, lon_dms_to_dd('test'))
        self.assertEqual(None, lon_dms_to_dd('045 30 00.00'))
        self.assertEqual(None, lon_dms_to_dd('045 30 00.00 A'))
        self.assertEqual(None, lon_dms_to_dd('01 05 32.00'))
        self.assertEqual(None, lon_dms_to_dd('045 5 3 E'))

        self.assertEqual(None, lon_dms_to_dd('181 00 00.00 E'))
        self.assertEqual(None, lon_dms_to_dd('180 01 00.00 E'))
        self.assertEqual(None, lon_dms_to_dd('180 00 01 E'))
        self.assertEqual(None, lon_dms_to_dd('180 00 00.1 E'))

        self.assertEqual(180.0, lon_dms_to_dd('180 00 00 E'))
        self.assertEqual(180.0, lon_dms_to_dd('180 00 00.0 E'))
        self.assertEqual(-180.0, lon_dms_to_dd('180 00 00.000 W'))
        self.assertEqual(-45.5, lon_dms_to_dd('045 30 00.00 W'))

        self.assertEqual(1.4297222222222223, lon_dms_to_dd('001 25 47.00 E'))
        self.assertEqual(-179.99999722222222, lon_dms_to_dd('179 59 59.99 W'))
        self.assertEqual(-2.777777777777778e-05, lon_dms_to_dd('000 00 00.1 W'))
        self.assertEqual(-114.78535833333333, lon_dms_to_dd('114 47 07.29 W'))

    def test_lat_dms_to_dd(self):
        self.assertEqual(None, lat_dms_to_dd('test'))
        self.assertEqual(None, lat_dms_to_dd('45 30 00.00'))
        self.assertEqual(None, lat_dms_to_dd('45 30 00.00 A'))
        self.assertEqual(None, lat_dms_to_dd('1 05 32.00'))
        self.assertEqual(None, lat_dms_to_dd('45 5 3 E'))

        self.assertEqual(None, lat_dms_to_dd('91 00 00.00 N'))
        self.assertEqual(None, lat_dms_to_dd('90 01 00.00 S'))
        self.assertEqual(None, lat_dms_to_dd('90 00 01 N'))
        self.assertEqual(None, lat_dms_to_dd('90 00 00.1 N'))

        self.assertEqual(90.0, lat_dms_to_dd('90 00 00 N'))
        self.assertEqual(90.0, lat_dms_to_dd('90 00 00.0 N'))
        self.assertEqual(-90.0, lat_dms_to_dd('90 00 00.000 S'))
        self.assertEqual(-45.5, lat_dms_to_dd('45 30 00.00 S'))

        self.assertEqual(1.4297222222222223, lat_dms_to_dd('01 25 47.00 N'))
        self.assertEqual(79.99999722222222, lat_dms_to_dd('79 59 59.99 N'))
        self.assertEqual(-2.777777777777778e-05, lat_dms_to_dd('00 00 00.1 S'))
        self.assertEqual(14.785358333333333, lat_dms_to_dd('14 47 07.29 N'))

    def test_dd_to_dmsh(self):
        self.assertEqual('000 00 00.0000 E', dd2_to_dmsh(0, A_LON))
        self.assertEqual('032 30 00.0000 W', dd2_to_dmsh(-32.5, A_LON))
        self.assertEqual('103 45 20.0388 W', dd2_to_dmsh(-103.75556633255578, A_LON))
        self.assertEqual('001 00 00.0200 E', dd2_to_dmsh(1.00000555, A_LON))

        self.assertEqual('00 00 00.0000 N', dd2_to_dmsh(0, A_LAT))
        self.assertEqual('32 30 00.0000 S', dd2_to_dmsh(-32.5, A_LAT))
        self.assertEqual('73 45 20.0388 S', dd2_to_dmsh(-73.75556633255578, A_LAT))
        self.assertEqual('01 00 00.0200 N', dd2_to_dmsh(1.00000555, A_LAT))

    def test_vincenty_direct_solution(self):
        self.assertEqual((29.999999999999964, 30.009020994857025),
                         vincenty_direct_solution(30, 30, 0, 1000.0, WGS84_A, WGS84_B, WGS84_F))
        self.assertEqual((-100.07770065280457, -63.64343250842656),
                         vincenty_direct_solution(-100.5, -63.5, 127.5, 26377.435, WGS84_A, WGS84_B, WGS84_F))
