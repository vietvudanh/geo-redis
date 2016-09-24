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

def check_lat_lon_value(lat, lon):
    try:
        float(lat)
        float(lon)
    except ValueError:
        return False
    if GeoConstant.LAT_MIN <= lat <= GeoConstant.LAT_MAX \
        and GeoConstant.LON_MIN <= lon <= GeoConstant.LON_MAX:
        return True
    return False