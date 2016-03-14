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
