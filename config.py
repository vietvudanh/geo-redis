import logging

class Config():
  DEBUG = False
  TESTING = False

  # log
  LOGGING_FILE =  'log/log'
  LOGGING_LEVEL = logging.DEBUG
  LOGGING_FORMAT = '%(asctime)s [%(levelname)s] %(pathname)s::%(lineno)d %(funcName)s(): %(message)s'

  # redis
  REDIS_PORT = 6379
  REDIS_HOST = 'localhost'
  REDIS_DB = 0
  REDIS_KEY = 'LOCATION'


class DevConfig(Config):
  DEBUG = True