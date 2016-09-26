import redis
import traceback
import Geohash
import json
import re
from constant import check_lat_lon_value

class GeoRedis(object):
    """
    Wrapper class for working with Redis GEO set commands introduced in version 3.2
    (https://www.compose.com/articles/a-quick-guide-to-redis-3-2s-geo-support/)
    """

    HASH_PRECISION = 11  # precison for python geohash lib, match redis GEOHASH

    UNITS = ['km', 'm', 'mi', 'ft']

    def __init__(self, app, pool):
        try:
            self.app = app
            self.redis_conn = redis.StrictRedis(connection_pool=pool)
        except Exception as e:
            print e
            self.app.logger.error('Cannot init GeoRedis')

    # PRIVATE
    def _key_name(self, key, hash_name):
        """
        Create key in format: [KEY]::[NAME]. This format will be used in:
            (1) direct store by set()
            (2) name in geoadd([KEY], [NAME])
        """
        return "{0}::{1}".format(key, hash_name)

    def is_key_name_format(self, key_name):
        """
        Check if key_name is in format: [KEY]::[NAME]
        """
        pattern = re.compile('[A-Z]+::[a-z0-9]+')
        if pattern.match(key_name): return True
        return False

    def _break_key_name(self, key_name):
        """
        Break key in format [KEY]::[NAME] in to [KEY] and [NAME]
        """
        return key_name.split('::')

    def _geo_hash(self, lat, lon):
        """
        Return the geohash from Geohas lib from: https://github.com/vinsci/geohash/
        with precision is 11 bit, equal to GEOHASH from Redis's core
        """
        return Geohash.encode(lat, lon, precision=GeoRedis.HASH_PRECISION)

    def _get_data_as_json(self, key):
        """
        Fetch data form Redis's get() and convert to object
        """
        value = self.redis_conn.get(key)
        if value: return json.loads(value)
        return None

    def _set_data_as_json(self, key, data):
        """
        Store data using Redis's set() as json dumps
        """
        return self.redis_conn.set(key, json.dumps(data))

    def _check_unit(self, unit):
        return unit in self.UNITS

    # PUBLIC
    def add(self, key, lat, lon, name, data={}):
        """
        Add a new location to:
            (1) direct store using set(), to store addition data: name, 
            description, etc...
            (2) store to sorted set using geoadd, to store lat, lon, name
        """
        try:
            hash_name = self._geo_hash(lat, lon)
            self.redis_conn.geoadd(
                key, lon, lat, self._key_name(key, hash_name))
            data['name'] = name
            self._set_data_as_json(self._key_name(
                key, hash_name), data)
        except Exception as e:
            self.app.logger.error('Cannot add location {}'.format(
                {'key': key, 'lon': lon, 'lat': lat, 'name': name}))
            self.app.logger.error(traceback.format_exc())
            return False
        return True

    def delete(self, key, name):
        """
        Remove location from redis
        (1) remove data from delete(name)
        (2) remove to sorted set using zrem(key, name)
        """
        try:
            if not (self.redis_conn.zscore(key, name) and self.redis_conn.get(name)):
                self.app.logger.error(
                    "member {0} not exist in key {1}".format(name, key))
                return False
            self.redis_conn.zrem(key, name)
            self.redis_conn.delete(name)
        except Exception as e:
            self.app.logger.error('Cannot delete {}'.format(
                {'key': key, 'name': name}))
            self.app.logger.error(traceback.format_exc())
            return False
        return True

    def get_by_name(self, key_name):
        """
        Return data for a location: name, lat, lon, addition data...
        """
        if not self.is_key_name_format(key_name): return None

        key, name = self._break_key_name(key_name)
        data = self._get_data_as_json(key_name)
        if data:
            data['lat'], data['lon'] = self.redis_conn.geopos(key, key_name)[
                0]
            return data
        else:
            return None

    def get_by_radius(self, key, lat, lon, radius, unit='km'):
        """
        Return list of locations in redis in a radius from original lat, lon.
        Data return: lat, lon, distance to orignal, additional data
        """
        if not self._check_unit(unit)\
            or not check_lat_lon_value(lat, lon):
            return None
        try:
            distance_data = self.redis_conn.georadius(
                key, lat, lon, radius, unit, True)
            data = []
            for location, dist in distance_data:
                data_location =  self._get_data_as_json(location)
                data_location['distance'] = dist
                data_location['lat'], data_location['lon'] = \
                    self.redis_conn.geopos(key, location)[0]
                data.append(data_location)
            return data
        except Exception as e:
            print e
            self.app.logger.error('Cannot get radius {}'.format(
                {'key': key, 'lon': lon, 'lat': lat, 'radius': radius, 'unit': unit}))
            self.app.logger.error(traceback.format_exc())
            return None

    def get_by_radius_member(self, key, name, radius, unit='km'):
        """
        Return list of locations in redis from a given location from redis.
        Data return: lat, lon, distance to orignal, additional data
        """
        if not self._check_unit(unit):
            return None
        try:
            distance_data = self.redis_conn.georadiusbymember(
                key, name, radius, unit, True)
            data = []
            for location, dist in distance_data:
                if location == name: continue # skip original member
                data_location =  self._get_data_as_json(location)
                data_location['distance'] = dist
                data_location['lat'], data_location['lon'] = \
                    self.redis_conn.geopos(key, location)[0]
                data.append(data_location)
            return data
        except Exception as e:
            self.app.logger.error('Cannot get data by radius {}'.format(
                {'key': key, 'name': name, 'radius': radius, 'unit': unit}))
            self.app.logger.error(traceback.format_exc())
            return None

    def get_all(self, key):
        """
        Return all locations in redis, with lat, lon, additional data
        TODO: Probaly just debug function, remove this after done
        """
        try:
            names_data = self.redis_conn.zrange(key, 0, -1)
            data = []
            for name in names_data:
                data_location = self._get_data_as_json(name)
                data_location['key_name'] = name
                data_location['lat'], data_location['lon'] = \
                    self.redis_conn.geopos(key, name)[0]
                data.append(data_location)
            return data
        except:
            self.app.logger.error(traceback.format_exc())
            return None
