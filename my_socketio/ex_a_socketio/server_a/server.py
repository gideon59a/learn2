import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

@sio.event
def connect(sid, environ):
    """On connection the server creates a sid for the socket connection, as printed below"""
    print('connect ', sid)
    print(f'environ: {environ}')

@sio.event
def login(sid, data):
    print(f'As login got from client: {data}')

@sio.event
def my_message(sid, data):
    '''When this event arrives at the server_a, the server_a will create another event for answering this request.'''
    msg = f'Data received on server_a from sid {sid} on my_message event : {data}'
    print(f'Now echo it to client: {msg}')
    sio.emit('handshake', msg)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.event
def calc_double(sid, num):
    print(f'Got {num} on calc_double')
    result = num * num
    return "OK", result

@sio.event
def calc_square(sid, data):
    # handle the message
    mult = int(data) * int(data)
    print(f'GOT on my_event: {data} ')
    return "OK", mult




if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5901)), app)
