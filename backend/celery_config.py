from celery import Celery
from celery.schedules import crontab

celery = Celery(__name__, broker='redis://localhost:6379/0',
backend='redis://localhost:6379/0')

CELERY_BEAT_SCHEDULE = {
'daily_user_reminder': {
    'task': 'tasks.daily_user_reminder',
    'schedule': 120.0,
    #'schedule': crontab(hour=17, minute=0),
    },
    'generate_monthly_report': {
    'task': 'tasks.generate_monthly_report',
    'schedule': 120.0,
    #'schedule': crontab(day_of_month=30, hour=23, minute=59),
    },
}
celery.conf.beat_schedule = CELERY_BEAT_SCHEDULE

#Bash Celery Commands 
'''celery -A tasks.celery beat --loglevel=info
celery -A tasks.celery worker --loglevel=info'''