''' Ref: https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#id8
Run the celery at the host level by:
ex_e_celery$ celery -A celery1 worker --loglevel=DEBUG --concurrency=1
'''

from celery import Celery
import time
import sys
sys.path.append("..")
from constants import redis_ip, redis_port  # '172.18.122.195


app = Celery('celery_worker', backend=f'redis://{redis_ip}:{redis_port}/1', broker=f'redis://{redis_ip}:{redis_port}/2')
# Backend db 1 is for the results,  broker db 2 is for the tasks queue.

@app.task  # (bind=True)
def add(x, y):
    print(f'Starting task at {time.perf_counter()}')
    #...AsyncResult(self.request.id).state
    time.sleep(9)
    z = x + y
    print(f'Ending task at {time.perf_counter()}')
    return z


def inspect_celery_info():
    # Ref: https://stackoverflow.com/questions/5544629/retrieve-list-of-tasks-in-a-queue-in-celery
    # Inspect all nodes.
    i = app.control.inspect()

    # Show the items that have an ETA or are scheduled for later processing
    scheduled = i.scheduled()

    # Show tasks that are currently active.
    active = i.active()

    # Show tasks that have been claimed by workers
    reserved = i.reserved()

    return scheduled, active, reserved
