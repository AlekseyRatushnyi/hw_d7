import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send_weekly': {
        'task': 'news.tasks.send_spam_email',
        # 'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'schedule': crontab(minute='*/1'),
    }
}
