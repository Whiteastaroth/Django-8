import os                             # импортируем библиотеку для взаимодействия с операционной системой
from celery import Celery             # импортируем библиотеку Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send_notification_every_monday_8am': {
        'task': 'news.tasks.weekly_newsletter',
        'schedule': crontab(hour="8", minute="0", day_of_week='monday'),
    },
}