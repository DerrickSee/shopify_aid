import os
from .base import *
import psycopg2

try:
    from urllib.parse import urlparse, uses_netloc
except ImportError:
    from urlparse import urlparse, uses_netloc


# Parse database configuration from $DATABASE_URL
DATABASES['default'] =  dj_database_url.config()

# Enable Persistent Connections
DATABASES['default']['CONN_MAX_AGE'] = 500

redis_url = urlparse.urlparse(os.environ.get('REDIS_URL'))
CACHES = {
    "default": {
         "BACKEND": "redis_cache.RedisCache",
         "LOCATION": "{0}:{1}".format(redis_url.hostname, redis_url.port),
         "OPTIONS": {
             "PASSWORD": redis_url.password,
             "DB": 0,
         }
    }
}
