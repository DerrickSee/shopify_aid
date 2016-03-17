from celery import Celery
import os
from django.conf import settings


app = Celery('example')

app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
