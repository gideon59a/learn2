import socketio
import time

#from my_background_task import my_background_task

sio = socketio.Client()
#sio = socketio.Client(logger=True, engineio_logger=True)  # for logs run this line instead

@sio.event
def connect():
    print('connection established')
    print('my sid is', sio.sid)  # The sid the server returns that identifies the specific client session
    #sio.emit('login', {'userKey': 'Your Streaming API Key'})  # Triggers login event to be processed by the server

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print('disconnected from server_a')

@sio.event
def my_message(data):  # "my_message" is the event name that the server has to refer to
    print('message received with ', data)

'''
@sio.on('handshake')  # Here the event name can be different than the def funcition, I am not fond of this method
def on_message(data):
    print('Got from server_a on handShake:', data)

@sio.event
def calc_square(num):
    print(f'Sending {num} on calc_square')

@sio.event
def my_event(data):
    # handle the message
    print(data)
'''

###################################################
import sys
sys.path.append("..")
from my_http_requests import HttpRequests  # Note that http_requests is a local module rather than the python regular module
from logger import Alogger
URL_PREFIX = "http://127.0.0.1:5903/"

my_logger = Alogger('ex_c.log')
logger = my_logger.get_logger()
http_req = HttpRequests(logger)

def post_task():
    path_post_task = 'start_task'
    data = {"a": "b"}
    url = URL_PREFIX + path_post_task
    http_code, rjson = http_req.post(url, data)
    print(f' json got: {type(rjson)} , {rjson} code: {http_code}')
    return http_code, rjson

def send_some_req():
    http_code, rjson = post_task()
    print(f'http_code: {http_code}, rjson: {rjson}')







#******  STRAT ****************


sio.connect('http://localhost:5903')
print("after connect")
send_some_req()
print("after send_some_req")
sio.emit('message', {"YYY from": "YYY client"})
print('after emit, sleep')
time.sleep(10)
print('Test Finished - exit 0')
sio.disconnect()
exit(0)

#sio.emit('my_message', {"contents2222": "ZZZZZZZZZZZZ"})
print('exit 777')
sio.disconnect()
exit(777)
# The following is an example of a request for which the server answers directly rather than triggering another event
# by the server.
def server_response(status, result):
    print(f'Server responded to my_event: Status: {status} Result: {result}')
get_from_server = sio.emit('calc_square', '9', callback=server_response)
print(f'got from server: {get_from_server}')

time.sleep(3)

# The following line is for client background processing other than the sio. A common example could be user input to the
# client that has to be processed and then trigger some emit towards the server.
#task = sio.start_background_task(my_background_task, sio)

run = False
while run:
    inp = input("Client main. Enter string to emit:\n")
    print(f'String entered by client user:{inp}')
    sio.emit('my_message', {"contents": inp})
    if inp == 'stop':
        run = False
    time.sleep(10)
#exit(0)
sio.wait()
