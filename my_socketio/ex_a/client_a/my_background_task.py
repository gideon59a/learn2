import time

def server_response(status, result):
    print(f'Server responded to my_event: Status: {status} Result: {result}')

def my_background_task(sio):
    """ The background process that receives inputs from the user, send the request to the server and gets a response
    In this example the server has to square the number it gets from the client"""
    loop = True
    while loop:
        print(f'client background task00')
        binp = int(input('background task input - Enter integer:\n'))
        print(f'Entered: {binp}')
        get_from_server = sio.emit('calc_square', binp, callback=server_response)
        print(f'my_background_task got from server: {get_from_server}')
        loop = False

