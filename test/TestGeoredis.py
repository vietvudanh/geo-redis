import unittest
from mock import Mock
from utils.geo_redis import GeoRedis
import redis

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

        pool = redis.ConnectionPool(host=self.HOST, port=self.PORT, db=self.TEST_DB)
        self.geo_redis = GeoRedis(app, pool)

    def tearDown(self):
        self.geo_redis.redis_conn.flushdb()

