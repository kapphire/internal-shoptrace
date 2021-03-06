import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'interShoptrace.settings.development')

app = Celery('interShoptrace')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.redbeat_redis_url = os.getenv('REDIS_URL', 'redis//localhost:6379/0')
app.conf.broker_pool_limit = 1
app.conf.broker_heartbeat = None
app.conf.broker_connection_timeout = 30
app.conf.worker_prefetch_multiplier = 1

app.conf.beat_schedule = {
    'fetch_link_from_firebase': {
        'task': 'links.tasks.task_fetch_link_from_firebase',
        'schedule': crontab(minute=0, hour='5,11,17,23'),
        'options': {'queue': 'inventory', 'expires': 3500.0}
    },
    'get_inventory_from_link': {
        'task': 'links.tasks.task_start_get_inventory',
        'schedule': crontab(minute=0, hour='0,6,12,18'),
        'options': {'queue': 'inventory', 'expires': 7000.0}
    },
    'fetch_link_from_commafeed': {
        'task': 'links.tasks.task_fetch_link_from_commafeed',
        'schedule': crontab(minute=0, hour='2,8,14,20'),
        'options': {'queue': 'inventory', 'expires': 10500.0}
    },
    # 'test_scheduler': {
    #     'task': 'links.tasks.task_test_scheduler',
    #     'schedule': 60.0,
    #     'options': {'queue': 'inventory', 'expires': 59.0}
    # },
}

app.conf.timezone = 'UTC'
