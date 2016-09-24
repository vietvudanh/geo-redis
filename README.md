[![Build Status](https://travis-ci.org/vietvudanh/geo-redis.svg?branch=master)](https://travis-ci.org/vietvudanh/geo-redis)

# geo-redis
Geography REST API for Python using Redis as database. Get use of redis 3.2 [supporting Geo](https://www.compose.com/articles/a-quick-guide-to-redis-3-2s-geo-support/)

# Install

## Requirement

1. FLask
2. Redis-py (current release version do not support geo related query, as mentioned in the [issue](https://github.com/andymccurdy/redis-py/pull/736), I'm using the version on [Github](https://github.com/andymccurdy/redis-py))
    
    Install py `pip install -e lib/redis`

3. Geohash

## Some note

I implement this project as REST API, with Flask, due to current requirement that I need an isolating API. But the core is `geo_radis.py` can be used anywhere.

@VietVU, 2016