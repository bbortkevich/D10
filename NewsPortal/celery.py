import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal') # имя папки где лежит этот файл
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
       'monday_8am_send_newsletters': {
        'task': 'news.tasks.sending_week_newsletters_celery',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        # 'schedule': crontab(minute='*/1'),
        'args':()
    },

}