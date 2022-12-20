# ref:
#   https://flask-socketio.readthedocs.io/en/latest/getting_started.html
#   https://stackoverflow.com/questions/48160130/using-flask-socketio-and-the-socketio-client

from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
sio = SocketIO(app)


@sio.on('connect')
def connect():
    print(f'connected.')

@sio.on('disconnect')
def disconnect():
    print('disconnected ')

@sio.on('message')
def message(data):
    print(data)  # {'from': 'client'}
    emit('response', {'from': 'server'})


"""
@sio.on('login')
def login(sid, data):
    print(f'As login got from client: {data}')


@sio.on('my_message')
def my_message(sid, data):
    # When this event arrives at the server_a, the server_a will create another event for answering this request.
    msg = f'Data received on server_a from sid {sid} on my_message event : {data}'
    print(f'Now echo it to client: {msg}')
    sio.emit('handshake', msg)


@sio.on('calc_double')
def calc_double(sid, num):
    print(f'Got {num} on calc_double')
    result = num * num
    return "OK", result


@sio.on('calc_square')
def calc_square(sid, data):
    # handle the message
    mult = int(data) * int(data)
    print(f'GOT on my_event: {data} ')
    return "OK", mult
"""

@app.route('/start_task', methods=['POST'])
def start_task():
    data = request.get_json()
    print(f'Client sent start task requesting: {data} ')
    return {"status": "ok server heard you"}, 200

#def start_task(data):
#    print(f'Client sent start task {data}')



if __name__ == '__main__':
    sio.run(app, port=5903, debug=True)
