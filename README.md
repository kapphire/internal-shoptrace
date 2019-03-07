For Windows :
- celery beat -S redbeat.RedBeatScheduler -A interShoptrace.celeryapp:app --loglevel=debug
- celery worker -Q inventory -A interShoptrace.celeryapp:app -l info -P gevent