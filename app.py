from flask import Flask, jsonify, request, g
import logging
from logging.handlers import TimedRotatingFileHandler
from redis_handler import GeoRedis
from constant import StatusCode
from constant import GeoConstant

# flask
app = Flask(__name__)
app.config.from_object('config.DevConfig')


@app.route('/', methods=['GET'])
def index():
    return 'Dump'


@app.route('/all', methods=['GET'])
def list_all():
    key = app.config['REDIS_KEY']
    data = geo_redis.get_all(key)
    if data is not None:
        response = jsonify({'locations': data})
        response.status_code = StatusCode.SUCCESS
    else:
        response = jsonify({'message': 'cannot retrieve all data'})
        response.status_code = StatusCode.SERVER_ERROR
    return response


@app.route('/add', methods=['POST'])
def add():
    val_check = False
    try:
        lat = float(request.form['lat'])
        lon = float(request.form['lon'])
        if GeoConstant.LAT_MIN <= lat <= GeoConstant.LAT_MAX \
                and GeoConstant.LON_MIN <= lon <= GeoConstant.LON_MAX:
            val_check = True
    except ValueError as e:
        print e
    if not val_check:
        response = jsonify({'message': 'lon, lat value not correct'})
        response.status_code = StatusCode.BAD_REQUEST
        return response

    name = request.form['name']
    key = app.config['REDIS_KEY']

    ret_check = False
    if lon and lat and name:
        ret_check = geo_redis.add(key, lat, lon, name)
    response = jsonify({
        'message': 'add {0} at [{1}, {2}]success'.format(name, lat, lon)})
    response.status_code = StatusCode.SUCCESS if ret_check else StatusCode.SERVER_ERROR

    return response


@app.route('/delete/<name>', methods=['DELETE'])
def delete(name):
    key = app.config['REDIS_KEY']
    ret_check = geo_redis.delete(key, name)

    response = jsonify(
        message='Delete success' if ret_check else 'Cannot delete')
    response.status_code = StatusCode.SUCCESS if ret_check else StatusCode.BAD_REQUEST
    return response


@app.route('/get/<name>', methods=['GET'])
def get_location(name):
    location_data = geo_redis.get_by_name(name)
    if location_data:
        response = jsonify(location_data)
        response.status_code = StatusCode.SUCCESS
    else:
        response = jsonify({'message': 'No location exist'})
        response.status_code = StatusCode.BAD_REQUEST
    return response


@app.route('/update/', methods=['PUT'])
def update(id):
    pass


@app.route('/get_by_radius', methods=['GET'])
def get_by_radius():
    if all(arg in request.args for arg in ['lon', 'lat', 'radius']):
        lat = float(request.args['lat'])
        lon = float(request.args['lon'])
        radius = float(request.args['radius'])

        unit = request.args['unit'] if 'unit' in request.args else 'km'

        key = app.config['REDIS_KEY']
        response = jsonify({
            'locations': geo_redis.get_by_radius(key, lat, lon, radius, unit),
            'unit': unit,
            'origin': {
                'lat': lat,
                'lon': lon
            }
        })
        response.status_code = StatusCode.SUCCESS
        return response
    else:
        response = jsonify(
            {'message': 'Not enough parameters: lon, lat, radius'})
        response.status_code = StatusCode.BAD_REQUEST
        return response


@app.route('/get_by_radius_name', methods=['GET'])
def get_by_radius_name():
    if all(arg in request.args for arg in ['name', 'radius']):
        radius = float(request.args['radius'])
        name = request.args['name']
        unit = request.args['unit'] if 'unit' in request.args else 'km'

        key = app.config['REDIS_KEY']
        response = jsonify({
            'locations': geo_redis.get_by_radius_member(key, name, radius, unit),
            'unit': unit,
            'origin': geo_redis.get_by_name(name)
        })
        response.status_code = StatusCode.SUCCESS
        return response
    else:
        response = jsonify({'message': 'Not enough parameters: name, radius'})
        response.status_code = StatusCode.BAD_REQUEST
        return response

if __name__ == '__main__':
    # log handler
    handler = TimedRotatingFileHandler(
        app.config['LOGGING_FILE'], when='d', interval=1)
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # redis
    geo_redis = GeoRedis(app=app, host=app.config['REDIS_HOST'], port=app.config[
                         'REDIS_PORT'], db=app.config['REDIS_DB'])

    # run
    app.run(host='')
