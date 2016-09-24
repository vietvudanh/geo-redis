[![Build Status](https://travis-ci.org/vietvudanh/geo-redis.svg?branch=master)](https://travis-ci.org/vietvudanh/geo-redis)

# geo-redis
Geography API for Python using 

# Install

## Requirement

1. FLask
2. Redis-py (current release version do not support geo related query, as mentioned in the [issue](https://github.com/andymccurdy/redis-py/pull/736), I'm using the version on [Github](https://github.com/andymccurdy/redis-py))
    
    Install py `pip install -e lib/redis`

3. Geohash