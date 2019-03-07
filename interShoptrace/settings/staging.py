from .base import *
import dj_database_url

DEBUG = False

# USED TO DEPLOY IN HEROKU
if 'DATABASE_URL' in os.environ:
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)

if 'SECRET_KEY' in os.environ:
    SECRET_KEY = os.getenv('SECRET_KEY')

ALLOWED_HOSTS = ['internal-shoptrace.herokuapp.com']
