# django_celery/celery.py

import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project02.settings")
app = Celery("project02")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    'update-fpt': {
        'task': 'store.tasks.fpt',
        'schedule': 180,
    },
    'update-cellphones': {
        'task': 'store.tasks.cellphones',
        'schedule': 180,
    },
    'update-phongvu': {
        'task': 'store.tasks.phongvu',
        'schedule': 180,
    },
    'update-tgdd': {
        'task': 'store.tasks.tgdd',
        'schedule': 180,
    }
}

app.conf.timezone = 'UTC'

app.autodiscover_tasks()