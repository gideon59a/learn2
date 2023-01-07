# Example 1: multiple tasks
Files:
* celery1.py - the celery instance and tasks
* call_task1.py - calling tasks
Run:
$ celery -A celery1 worker --loglevel=DEBUG --concurrency=1
$ python3 call_task_b.py

# Example #2: multiple queues, separated workers
Running celery separately each with its own queue.
In this example the celery is run twice, each for its own queue, while redis is common to both.
It doesn't properly imitate the case of two celery servers sharing the same redis queue, but it looks close... 

**Notes:**
* When calling a task **.apply_async** was used rather than .delay!
* in the celery.py adding "app.conf.task_routes" had no effect ?! (todo check)

In my wsl2 Ubuntu I run (after $ cd ex_e_celery) in separated windows:
$ celery -A celery_a worker --loglevel=DEBUG --concurrency=1 -Q queue_a -n worker_a@%%h 
$ celery -A celery_b worker --loglevel=DEBUG --concurrency=1 -Q queue_a -n worker_b@%%h

As a result "ps -aux|grep celery" showed two processes per each (I guess 1 for celery management and the 2nd for the single worker)
When the 2nd (worker_b) was triggered, the 1st one (worker_a) notified: 
sync with worker_b@%N-20N3PF231BWQ, worker_b@%N-20N3PF231BWQ joined the party 
Inspecting 
$ celery -A celery_a inspect active_queues 
$ celery -A celery_b inspect active_queues
both provided the two queues (in different order)

# Monitoring celery
$ celery -A <celery module name> inspect active_queues
