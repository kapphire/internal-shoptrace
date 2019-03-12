For Windows :
<!-- - celery beat -S redbeat.RedBeatScheduler -A interShoptrace.celeryapp:app --loglevel=debug
 -->
- celery beat -S redbeat.RedBeatScheduler -A interShoptrace.celeryapp:app --pidfile= --loglevel=debug
 
- celery worker -Q inventory -A interShoptrace.celeryapp:app -l info -P gevent

- SECRET_KEY : fl!3*dy@g%99b*#t5i+@zoc$yogoqk#col8i2fyeb&818144l&
- DJANGO_SETTINGS_MODULE : interShoptrace.settings.staging
