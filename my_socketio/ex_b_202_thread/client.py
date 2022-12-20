import json
import sys
import time

sys.path.append("..")

from my_http_requests import HttpRequests
from logger import Alogger

URL_PREFIX = "http://127.0.0.1:5902/"

my_logger = Alogger('ex_b.log')
logger = my_logger.get_logger()
http_req = HttpRequests(logger)

def post_task():
    path_post_task = 'start_task'
    data = {"a": "b"}
    url = URL_PREFIX + path_post_task
    http_code, rjson = http_req.post(url, data)
    print(f' json got: {type(rjson)} , {rjson} code: {http_code}')
    return http_code, rjson

def get_op_status(tid):
    path_get_status = f'get_op_status/{tid}'
    url = URL_PREFIX + path_get_status
    http_code, rjson = http_req.get(url)
    print(f'json got: {type(rjson)} , {rjson} code: {http_code}')
    return http_code, rjson

def test_server(logger):
    http_code, rjson = post_task()
    transaction_id = rjson["transaction_id"]
    timeout = 10
    print('\n')
    if http_code == 202:
        for i in range(timeout):
            print('waiting')
            time.sleep(1)
            http_code, rjson = get_op_status(transaction_id)
            if http_code != 202:
                print(f'Got status: {rjson["status"]}')
                break


def main():

    test_server(logger)

if __name__ == '__main__':
    main()
