import redis  # for reading the results
import json
import time

from celery1 import add  # The tasks celery worker supports
from constants import redis_ip

rdb1 = redis.Redis(host=redis_ip, port=6379, db=1)  # connect to redis for reading the results

# *** RUN THE TASK ****
task_id = add.delay(4, 12)  # call task. Will block until the task ends
print(f'res:{task_id}')

# Read result
redis_celery_task_key = f'celery-task-meta-{task_id}'
time.sleep(1)  # Looks like there must be some delay between task end and reading the key from redis
task_result = rdb1.get(redis_celery_task_key)
print(f'Task result: {type(task_result)}  {task_result}')
task_result_dict = json.loads(task_result.decode("utf-8"))
print(f'Final status: {task_result_dict["status"]}  with result: {task_result_dict["result"]}')
rdb1.delete(redis_celery_task_key)  # clean the result from redis after it is read
