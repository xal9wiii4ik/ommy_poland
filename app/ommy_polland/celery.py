import os

from celery import Celery
from glob import glob

from celery.schedules import crontab

from ommy_polland import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ommy_polland.settings')
TASKS_FILES = map(lambda x: x.replace('/tasks.py', '').replace('/', '.'), glob('**/tasks.py', recursive=True))

celery_app = Celery('ommy_polland', broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks(TASKS_FILES, force=True)
celery_app.conf.beat_schedule = {
    'remove-old-codes': {
        'task': 'authenticate.remove_old_codes',
        'schedule': crontab(hour='0', minute='0')
    },
}
