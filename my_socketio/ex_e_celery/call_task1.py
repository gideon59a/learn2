import redis  # for reading the results
import json
import time

from celery1 import add, inspect_celery_info  # The tasks celery worker supports
from constants import redis_ip


def direct_redis_read_result(task_id):
    """Reading the result directly from redis. For learning only.
    Note that the key with the task_id is written by celery into redis only after the celery task finishes.
    """

    # Read result
    redis_celery_task_key = f'celery-task-meta-{task_id}'
    task_result_0 = rdb1.get(redis_celery_task_key)
    print(f'Reading from redis the result before it is ready in redis: '
          f'Task result: {type(task_result_0)} {task_result_0}')

    # Read the message queue
    tasks_message_queue = rdb2.hgetall("unacked")
    print(f'Reading from redis the tasks waiting in the queue: \n  {tasks_message_queue}')

    print('Waiting 9 sec for the 1st task to finish')
    time.sleep(9)
    task_result = rdb1.get(redis_celery_task_key)
    print(f'Reading from redis the task result key: {type(task_result)}  {task_result} read at {time.perf_counter()}')
    task_result_dict = json.loads(task_result.decode("utf-8"))
    print(f'so it has status: {task_result_dict["status"]}  with result: {task_result_dict["result"]}')

    # Redis keys will be automatically deleted after a day. If one wants to directly delete then use:
    # rdb1.delete(redis_celery_task_key)  # clean the result from redis after it is read


def get_inspect_celery_info():
    scheduled, active, reserved = inspect_celery_info()
    print(f'scheduled tasks: {scheduled}')
    print(f'active tasks: {active}')
    print(f'reserved tasks: {reserved}')
    print('\n')


rdb1 = redis.Redis(host=redis_ip, port=6379, db=1)  # connect to redis for directly reading the results
rdb2 = redis.Redis(host=redis_ip, port=6379, db=2)  # connect to redis for directly reading the message
print(f'Connected to redis')

# *** RUN THE TASK ****
print(f'Triggering task1 at time {time.perf_counter()}')
result = add.delay(5, 13)  # call task. Does not block, not waiting for the task to finish.
print(f'Triggering task2 at time {time.perf_counter()}')
result2 = add.delay(22, 14)  #
print(f'Tasks were triggered')


# the result is a <class 'celery.result.AsyncResult'>. When directly read it provides the task id.
print(f'result type is: {type(result)}.\nWhen we print this instance it returns the task id: {result}')
print(f'But the task id can be also got from result.id: {result.id} ')

task_id = result.id  # the result is a <class 'celery.result.AsyncResult'> than when read provides the task id.
print(f'Got task id {task_id} at time {time.perf_counter()}')

result1 = result.status
if result1 == 'PENDING':
    print(f'task_id.status (PENDING is expected as the task is being processed): {result1}')
else:
    print(f'???!!! For some reason the 2nd tasks was enqueues only after 1st task was ended - SO THE TEST HAS FAILED')

print(f'\nPrinting celery inspect info BEFORE waiting: '
      '(Note that Reserved tasks are tasks that have been received, but are still waiting to be executed)')
get_inspect_celery_info()

direct_redis_read_result(task_id)  # for learning only

print(f'Printing celery inspect info after waiting:')
get_inspect_celery_info()


print(f'\nAfter the long redis waiting, time is {time.perf_counter()}.\nReading using celery AsyncResult instance:')
print(f'Task status1: {result.status}')
print(f'Task result1: {result.result}')

print(f'Task status2: {result2.status}')
print(f'Task result2: {result2.result}')

print('Waiting for result2 to finish, 10 sec timeout')
for i in range(10):
    status2 = result2.status
    print(f'Task status2: {result2.status}')
    if status2 != 'PENDING':
        print(f'Task result2: {result2.result}')
        break
    else:
        i += 1
    time.sleep(1)

print(f'\nPrinting celery inspect info at the END:')
get_inspect_celery_info()
print('End.')
