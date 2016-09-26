from TestGeoredis import TestGeoredis

class TestDelete(TestGeoredis):

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

    def setUp(self):
        # data for test
        for lat, lon, name in self.test_data_added:
            self.geo_redis.add(self.KEY, lat, lon, name)

        self.added_data = self.geo_redis.get_all(self.KEY)

    def test_delete_success(self):
        for location in self.added_data:
            self.assertTrue(self.geo_redis.delete(self.KEY, location['key_name']))

    def test_delete_fail(self):
        for name in self.test_data_fail:
            self.assertFalse(self.geo_redis.delete(self.KEY, name))

if __name__ == '__main__':
    unittest.main()
