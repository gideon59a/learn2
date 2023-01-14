# General
### purpose
Learn some celery functionality / how to:
- getting task status and result
- using multiple queues

### Test environment
Python3.9.6
Celery worker & redis: wsl2. 
Task triggered from win10 or the wsl2.

# Running
### Running the celery worker(s)
**file:** celery1.py - The worker that can be run by
$ celery -A celery1 worker --loglevel=DEBUG --concurrency=1
$ celery -A celery1 worker --loglevel=DEBUG --concurrency=1 -Q queue_a -n worker_a@%%h   
$ celery -A celery1 worker --loglevel=DEBUG --concurrency=1 -Q queue_b,celery -n worker_b@%%h 

The 1st will use the default queue that its default name is "celery"
The 2nd is for specific queue.
The 3rd is for two queue, where one of them is the default.

### Running the tasks clients
**file:** call_tasks.py. 
Will use .delay method when no queue name is defined in the command below,   
or .apply_async when a queue name is specified.
Command xamples:
$ python3 call_tasks.py ## A single task is sent to the default queue
$ python3 call_tasks.py celery 1  ## A single task on the "celery" queue
$ python3 call_tasks.py "" 2  ## two tasks on the default queue
$ python3 call_tasks.py queue_a 3  ## three tasks on a queue_a

# Examples
### Using queue per worker
Running celery workers each with its own queue thus imitating dedicated workers for specific tasks.
In this example the celery is run twice, each for its own queue, while redis is common to both.
It doesn't properly imitate the case of two celery servers sharing the same redis queue, but it looks close... 

**Notes:**
* When calling a task **.apply_async** was used rather than .delay!
* in the celery.py adding "app.conf.task_routes" had no effect ?! (todo check)

In my wsl2 Ubuntu I run (after $ cd ex_e_celery) in separated windows:  
$ celery -A celery1 worker --loglevel=DEBUG --concurrency=1 -Q queue_a -n worker_a@%%h   
$ celery -A celery1 worker --loglevel=DEBUG --concurrency=1 -Q queue_b -n worker_b@%%h  

As a result "ps -aux|grep celery" showed two processes per each (I guess 1 for celery management and the 2nd for the single worker)  
When the 2nd (worker_b) was triggered, the 1st one (worker_a) notified:   
sync with worker_b@%N-20N3PF231BWQ, worker_b@%N-20N3PF231BWQ joined the party   
Inspecting 
* $ celery -A celery1 inspect active_queues   


# Monitoring celery
$ celery -A <celery module name> inspect active_queues
