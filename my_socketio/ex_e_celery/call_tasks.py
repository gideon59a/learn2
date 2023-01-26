import redis  # for reading the results
import json
import time
import sys

from celery_worker import add, inspect_celery_info  # The tasks celery worker supports
from constants import redis_ip


class CallTaskTest:
    def __init__(self, queue_name="", tasks_num=1):
        self.queue_name = queue_name
        self.tasks_num = tasks_num
        self.rdb1 = redis.Redis(host=redis_ip, port=6379, db=1)  # connect to redis for directly reading the results
        self.rdb2 = redis.Redis(host=redis_ip, port=6379, db=2)  # connect to redis for directly reading the message
        print(f'Connected to redis')
        print(f'Running {tasks_num} task(s) on queue {queue_name}')

    def send_task(self, *args):
        """For sending a task to the default message queue the .delay celery method was used.
        For sending to a specified queue the .apply_async celery method was used"""
        print(f'Task args: {args}')
        if self.queue_name:
            result = add.apply_async(args, queue=self.queue_name)
        else:
            result = add.delay(*args)
        return result

    def runt(self):
        # *** RUN THE TASK ****
        print(f'Triggering task1 at time {time.perf_counter()}')
        result = self.send_task(1, 10)
        print(f'Task1 was triggered at time {time.perf_counter()}')
        result2 = None
        if self.tasks_num > 1:
            print(f'Triggering task2 at time {time.perf_counter()}')
            result2 = self.send_task(2, 20)
            print(f'Task2 was triggered at time {time.perf_counter()}')
        if self.tasks_num > 2:
            print(f'Triggering task3 at time {time.perf_counter()}')
            result3 = self.send_task(3, 30)
        print(f'Task(s) were triggered. Time is {time.perf_counter()}')

        print("\nNote: The below result is a <class 'celery.result.AsyncResult'>. When directly read it provides the task id.")
        print(f'result type is: {type(result)}.\n'
              f'When we print this instance it returns the task id: {result}\n'
              f'as its __repr__ is the task id:  {repr(result)}\n'
              f'  while the task id can be also got from result.id: {result.id}')

        task_id = result.id
        print(f'Time is {time.perf_counter()}')

        status1 = result.status
        if status1 == 'PENDING':
            print(f'\ntask_id.status (PENDING is expected as the task is being processed): {status1}')
        else:
            print(
                f'???!!! For some reason the 2nd tasks was enqueues only after 1st task was ended - SO THE TEST HAS FAILED')

        self.direct_redis_read_task_queue()

        print(f'\nCelery info - Printing celery inspect info BEFORE waiting for the result: '
              '(Note that Reserved tasks are tasks that have been received but are still waiting to be executed)')
        self.get_inspect_celery_info()

        print('\nRedis info - Reading from redis task1 result before it appears in redis: ')
        self.direct_redis_read_result(task_id)  # for learning only
        print(f'Celery: Waiting for the 1st task to finish. Time is {time.perf_counter()}')
        self.wait_for_finish(result)
        print('\nRedis info - Reading from redis the result after task 1 is done. '
              'See task2 is now in the active tasks queue:')
        self.direct_redis_read_result(task_id)
        print(f'Celery info - Printing celery inspect info after task 1 is done:')
        self.get_inspect_celery_info()

        if self.tasks_num > 1:
            print(f'Task status2: {result2.status}')
            print(f'Task result2: {result2.result}')
            self.wait_for_finish(result2)

            print('\nRedis info: Reading from redis the result after task 2 is done. ')
            self.direct_redis_read_result(result2.task_id)
            print(f'\nPrinting celery inspect info at the END (see no tasks are now in the active tasks queue):')

        self.get_inspect_celery_info()

        if self.tasks_num > 2:
            print(f'Task status3: {result3.status}')
            print(f'Task result3: {result3.result}')
            self.wait_for_finish(result3)

        print('End.')

    def direct_redis_read_task_queue(self):
        """Read the tasl message queue from redis"""

        # Note it is not clear for me when tasks are put in "unacked" redis key and when in the main queue.
        # some ref is http://www.ines-panker.com/2020/10/28/celery-explained.html, which is not too clear as well.
        # But, in my tests:
        # when the worker is not available tasks were put into the key=queue name, and once the worker started
        # the tasks moved under "unacked" key.

        def read_queue(redis_message_queue_name):
            try:
                if redis_message_queue_name == "unacked":
                    tasks_message_queue = self.rdb2.hgetall(redis_message_queue_name)
                    print(f'Reading from redis message queue "{redis_message_queue_name}" '
                          f'the tasks that are still waiting in the queue:) # \n {tasks_message_queue}')
                    print_bytes_dict(tasks_message_queue)
                else:
                    tasks_message_queue = self.rdb2.lrange(redis_message_queue_name, 1, 99)
                    print(f'Reading from redis message queue "{redis_message_queue_name}":')
                    i = 1
                    for task_in_queue in tasks_message_queue:
                        task_in_queue_dict = json.loads(task_in_queue.decode("utf-8"))
                        print(f'Task #{i}:{task_in_queue_dict}')
                        i += 1
                        #for key, val in task_in_queue_dict.items():
                        #    print(key, val)

            except Exception as e:
                print(f'Error when reading redis task queue. Error: {str(e)}')

        def print_bytes_dict(dict_in_bytes):
            for key, val in dict_in_bytes.items():
                print(key.decode("utf-8"), val.decode("utf-8"))

        print('\nRedis info - Reading task queue:')
        found = False
        if self.rdb2.exists("unacked"):
            read_queue("unacked")
            found = True

        if not self.queue_name:
            queue_name = "celery"
        else:
            queue_name = self.queue_name
        if self.rdb2.exists(queue_name):
            read_queue(queue_name)
            found = True
        if not found:
            print("Redis task queue not found, probably because all tasks were already taken by workers.\n"
                  "or maybe the unacked key was used for a non default queue, a case which I have not checked.\n"
                  "Note that by default a worker takes some 4 tasks fot itself. "
                  "To see tasks in queue just for testing one may stop the worker...")


    def direct_redis_read_result(self, task_id):
        """Reading the result directly from redis. For learning only.
        Note that the key with the task_id is written by celery into redis only after the celery task finishes.
        """
        # Note: Redis keys will be automatically deleted after a day. If one wants to directly delete then use:
        # or use e.g. rdb1.delete(redis_celery_task_key) to clean the result from redis after it is read.

        # Read result:
        redis_celery_task_key = f'celery-task-meta-{task_id}'
        task_result = self.rdb1.get(redis_celery_task_key)
        print(f'Redis Task result: {type(task_result)} {task_result}')
        if task_result:  # result exists
            print(f'Reading from redis the task result key: {type(task_result)}  {task_result} read at {time.perf_counter()}')
            task_result_dict = json.loads(task_result.decode("utf-8"))
            print(f'so it has status: {task_result_dict["status"]}  with result: {task_result_dict["result"]}')


    @staticmethod
    def wait_for_finish(result):
        print('Polling celery result waiting for task to finish, 10 sec timeout')
        for i in range(10):
            status = result.status
            print(f'Task status: {result.status}')
            if status != 'PENDING':
                print(f'Task result: {result.result}')
                break
            else:
                i += 1
            time.sleep(1)

    @staticmethod
    def get_inspect_celery_info():
        scheduled, active, reserved = inspect_celery_info()
        print(f'scheduled tasks: {scheduled}')
        print(f'active tasks: {active}')
        print(f'reserved tasks: {reserved}')
        print('\n')


if __name__ == "__main__":
    print('For sending a task to the a specific task queue enter the queue name. Otherwise press enter')
    tasks_num = 1
    queue_name = 'celery'
    if len(sys.argv) > 1:
        queue_name = sys.argv[1]
        if len(sys.argv) > 2:
            tasks_num = int(sys.argv[2])
    else:  # for pycharm
        queue_name = input("Enter celery task queue name: ")
        tasks_num = input("Enter 1 for single task test, or 2 for two tasks test (default=1):")
        if tasks_num:
            tasks_num = int(tasks_num)
        else:
            tasks_num = 1
    print(f'Running {type(tasks_num)} {tasks_num} tasks using queue {queue_name} ')
    tt = CallTaskTest(queue_name, tasks_num)
    tt.runt()
