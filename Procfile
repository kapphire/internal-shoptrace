release: bash release.sh
web: gunicorn interShoptrace.wsgi
celery_beat: celery beat -S redbeat.RedBeatScheduler -A interShoptrace.celeryapp:app --loglevel=debug
celery_inventory: celery worker -Q inventory -A interShoptrace.celeryapp:app -n internal_shoptrace.%%h --loglevel=info  --without-gossip --without-mingle --without-heartbeat --concurrency 2 -Ofair --max-memory-per-child=512000