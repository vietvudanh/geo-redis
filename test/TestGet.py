from TestGeoredis import TestGeoredis

class TestGet(TestGeoredis):
    
    test_data_added = [
        (50.0, 120.0, 'Hanoi'),
        (80.0, 120.0, 'Tokyo'),
        (30.0, 120.0, 'Osaka'),
        (30.0, 50.0, 'New York')
    ]

    test_data_fail = [
        1,
        1.0,
        -200,
        9999,
        'abc123',
        'efg',
        'LOCATION::urn5x1g8c13'
    ]

    all_data = None

    def setUp(self):
        for lat, lon, name in self.test_data_added:
            self.geo_redis.add(self.KEY, lat, lon, name)

    def test_get_all(self):
        all_data = self.geo_redis.get_all(self.KEY)
        self.assertEqual(len(all_data), len(self.test_data_added))
        self.assertIsInstance(all_data, list)

    def test_get_one_success(self):
        all_data = self.geo_redis.get_all(self.KEY)
        for location in all_data:
            self.assertIsInstance(self.geo_redis.get_by_name(location['key_name']), dict)

    def test_get_one_fail(self):
        for name in self.test_data_fail:
            self.assertNotIsInstance(self.geo_redis.get_by_name(str(name)), dict)

if __name__ == '__main__':
    unittest.main()
