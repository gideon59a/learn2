''' Ref: https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#id8
Run the celery at the host level by:
ex_e_celery$ celery -A celery1 worker --loglevel=DEBUG
'''

from celery import Celery
import sys
sys.path.append("..")
from constants import redis_ip, redis_port  # '172.18.122.195


#app = Celery('celery1', broker=f'redis://{redis_ip}:{redis_port}/1')
app = Celery('celery1', backend=f'redis://{redis_ip}:{redis_port}/1', broker=f'redis://{redis_ip}:{redis_port}/1')

@app.task
def add(x, y):
    return x + y
