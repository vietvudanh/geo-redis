import unittest
from mock import Mock
from utils.geo_redis import GeoRedis

class TestGeoredis(unittest.TestCase):
    HOST = 'localhost'
    PORT = 6379
    TEST_DB = 1

    KEY = 'LOCATION'

    def __init__(self, *args, **kwargs):
        super(TestGeoredis, self).__init__(*args, **kwargs)
        app = Mock()
        app.logger = Mock()
        app.logger.error = lambda s : None
        app.logger.info = lambda s : None

        self._geo_redis = GeoRedis(app, host=self.HOST, port=self.PORT, db=self.TEST_DB)

    def tearDown(self):
        self._geo_redis._redis_conn.flushdb()

