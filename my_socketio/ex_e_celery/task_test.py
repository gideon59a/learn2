import time
import sys
from celery1 import add, inspect_celery_info  # The tasks celery worker supports


class TaskTestM:
    def __init__(self, queue_name):
        self.queue_name = queue_name

    def run1(self):
        # *** RUN THE TASK ****
        print(f'Triggering task1 at time {time.perf_counter()}')
        result = add.apply_async((50, 49), queue=self.queue_name)  # call task. Does not block, not waiting for the task to finish.
        # the result is a <class 'celery.result.AsyncResult'>. When directly read it provides the task id.
        print(f'result type is: {type(result)}.\nWhen we print this instance it returns the task id: {result}')
        print(f'But the task id can be also got from result.id: {result.id} ')

        task_id = result.id  # the result is a <class 'celery.result.AsyncResult'> than when read provides the task id.
        print(f'Got task id {task_id} at time {time.perf_counter()}')

        result1 = result.status
        if result1 == 'PENDING':
            print(f'task_id.status (PENDING is expected as the task is being processed): {result1}')
        else:
            print(f'Failure. PENDING was expected')

        print(f'\nPrinting celery inspect info BEFORE waiting: '
              '(Note that Reserved tasks are tasks that have been received, but are still waiting to be executed)')
        print(f'Printing celery inspect info just after task was triggered:')
        self.get_inspect_celery_info()
        print(f'Task status1: {result.status}')
        print(f'Task result1: {result.result}')

        self.wait_for_finish(result)

        print(f'\nPrinting celery inspect info at the END:')
        self.get_inspect_celery_info()
        print('End.')

    @staticmethod
    def wait_for_finish(result):
        print('Waiting for task to finish, 10 sec timeout')
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
    if len(sys.argv) > 1:
        queue_name = sys.argv[1]
    else:  # for pycharm
        queue_name = input("enter celery queue name: ")

    tt = TaskTestM(queue_name)
    tt.run1()
