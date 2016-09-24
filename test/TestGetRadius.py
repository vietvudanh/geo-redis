from TestGeoredis import TestGeoredis


class TestGetRadius(TestGeoredis):

    test_data_added = [
        (50.0, 120.0, 'Hanoi'),
        (80.0, 120.0, 'Tokyo'),
        (30.0, 120.0, 'Osaka'),
        (30.0, 50.0, 'New York')
    ]

    test_data_origin_success = [
        (0.0, 0.0, 100, 'km'),
        (50.0, 50.0, 1000, 'm'),
        (25.0, 50.0, 8000, 'mi'),
        (80.0, 20.0, 1000, 'ft')
    ]

    test_data_origin_fail = [
        (0.0, 0.0, 100, 'kmm'),
        ('b', 0.0, 100, 'km'),
        ('b', 'a', 100, 'km'),
        (85, 'a', 8000, 'm'),
        (91.0, 0.0, 100, 'km'),
        (-91.0, 0.0, 100, 'km'),
        (25.0, -181.0, 8000, 'm'),
        (100.0, -181.0, 1000, 'ft'),
        (95.0, -181.0, 1000, 'ftt')
    ]

    test_data_name_fail = [
        ('abc', 10000, 'km'),
        ('LOCATION::123123ad', 'abc', 'km'),
        ('abc', 'abc', 'km'),
        (123, 10000, 'f'),
        (123, 10000, 'm'),
    ]

    def setUp(self):
        for lat, lon, name in self.test_data_added:
            self._geo_redis.add(self.KEY, lat, lon, name)

    def test_get_by_radius_success(self):
        for lat, lon, r, unit in self.test_data_origin_success:
            self.assertIsInstance(self._geo_redis.get_by_radius(
                self.KEY, lat, lon, r, unit), list)

    def test_get_by_radius_fail(self):
        for lat, lon, r, unit in self.test_data_origin_fail:
            self.assertEqual(self._geo_redis.get_by_radius(
                self.KEY, lat, lon, r, unit), None)

    def test_get_by_radius_member_success(self):
        all_data = self._geo_redis.get_all(self.KEY)
        for location in all_data:
            self.assertIsInstance(self._geo_redis.get_by_radius_member(
                self.KEY, location['key_name'], 10000, 'km'), list)

    def test_get_by_radius_member_fail(self):
        for name, r, unit in self.test_data_name_fail:
            if unit:
                self.assertEqual(self._geo_redis.get_by_radius_member(
                    self.KEY, name, r, unit), None)
            else:
                self.assertEqual(self._geo_redis.get_by_radius_member(
                    self.KEY, name, r), None)

if __name__ == '__main__':
    unittest.main()
