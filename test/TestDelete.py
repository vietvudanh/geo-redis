import unittest
from redis_handler import *
from mock import Mock

class TestAdd(unittest.TestCase):

    HOST = 'localhost'
    PORT = 6379
    TEST_DB = 9

    KEY = 'LOCATION'

    test_data_success = [
        (50.0, 120.0, 'Hanoi'),
        (80.0, 120.0, 'Tokyo')
    ]

    test_data_wrong_lon_lat = [
        (100.0, 90.0, 'Hanoi'),
        (90.0, -200.0, 'Tokyo'),
        ('3A', -200.0, 'Osaka'),
        ('3A', '123v', 'New York')
    ]

    def setUp(self):
        # fake Flask app logger
        app = Mock()
        app.logger = Mock()
        app.logger.error = lambda s : None
        app.logger.info = lambda s : None

        self._geo_redis = GeoRedis(app, host=self.HOST, port=self.PORT, db=self.TEST_DB)
        pass

    def tearDown(self):
        self._geo_redis._redis_conn.flushdb()
        pass

    def test_add_success(self):
        for lat, lon, name in self.test_data_success:
            self.assertTrue(self._geo_redis.add(self.KEY, lat, lon, name))

    def test_add_fail(self):
        for lat, lon, name in self.test_data_wrong_lon_lat:
            self.assertFalse(self._geo_redis.add(self.KEY, lat, lon, name))

if __name__ == '__main__':
    unittest.main()
