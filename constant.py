class StatusCode(object):
    # Success
    SUCCESS = 200

    # Client Error
    BAD_REQUEST = 400

    # Server Error
    SERVER_ERROR = 500

    # prevent set 
    def __setattr__(self, *_):
        pass

class GeoConstant(object):
    # Lon & Lat boundary
    LON_MAX = 180
    LON_MIN = -180
    LAT_MAX = 85
    LAT_MIN = -85

    # prevent set 
    def __setattr__(self, *_):
        pass