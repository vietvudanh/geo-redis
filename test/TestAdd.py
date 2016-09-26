from TestGeoredis import TestGeoredis

class TestAdd(TestGeoredis):

    test_data_success = [
        (50.0, 120.0, 'Hanoi'),
        (80.0, 120.0, 'Tokyo'),
        (30.0, 120.0, 'Osaka'),
        (30.0, 50.0, 'New York')
    ]

    test_data_wrong_lon_lat = [
        (100.0, 90.0, 'Hanoi'),
        (-91.0, 90.0, 'Shanghai'),
        (91.0, 90.0, 'Hong Kong'),
        (90.0, -181.0, 'Tokyo'),
        (90.0, 181.0, 'LA'),
        ('3A', 181.0, 'Osaka'),
        ('3A', '123v', 'New York')
    ]

    def test_add_success(self):
        for lat, lon, name in self.test_data_success:
            self.assertTrue(self.geo_redis.add(self.KEY, lat, lon, name))

    def test_add_fail(self):
        for lat, lon, name in self.test_data_wrong_lon_lat:
            self.assertFalse(self.geo_redis.add(self.KEY, lat, lon, name))

if __name__ == '__main__':
    unittest.main()
