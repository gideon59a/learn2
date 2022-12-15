from flask import Flask, request
import time
import threading
from dataclasses import dataclass, field

# TEST BY:
# curl -X POST -H 'Content-Type: application/json' http://localhost:5902/start_task -d '{"a":"b"}'
# curl -X GET http://localhost:5902/get_op_status/10


aa = ["" for i in range(10)]
print(aa)
@dataclass
class MyDatabase:
    t_status: list
    t_list: list[int] = range(10)

    def __post_init__(self):
        self.t_status = ["" for _ in range(10)]

t_db = MyDatabase([])

print(f't_db: {t_db}')
print(type(t_db.t_list))
print(t_db.t_list[6])
print(t_db.t_status[6])


def validate_request(data):
    print(f'Validating {data}')
    return 0


def get_new_transaction_id(op_info):
    """get a new transaction ID and put it with along with the operation in the database"""
    print(f'getting transaction id for {op_info}')
    tid = -1
    for i in range(10):
        if not t_db.t_status[i]:
            tid = t_db.t_list[i]
            t_db.t_status[i] = 'inprogress'
            print(f'got tid: {tid}')
            print(f'updated t_db: {t_db}')
            break
    #t_db.t_status[9] = "inprogress"
    return tid


def long_running_task(**kwargs):
    tid = kwargs.get('tid', {})
    print(f'Starting long task with transaction id: {tid}')
    t_db.t_status[tid] = 'inprogress'
    for _ in range(5):
        time.sleep(1)
        print(".")
    print("TASK FINISHED")
    t_db.t_status[tid] = 'done'


def read_op_status(tid):
    """Read op status from db"""
    return {"status":  t_db.t_status[tid], "transaction_id": tid}


app = Flask(__name__)
@app.route('/start_task', methods=['POST'])
def start_task():
    data = request.get_json()
    op_info = {"op": "start_task", "data": data}
    if validate_request(op_info):
        print('should return 400 and some error message')
        return {"status": "Bad request"}, 400
    transaction_id = get_new_transaction_id(op_info)
    print(f'Got new transaction_id: {transaction_id}')
    thread = threading.Thread(target=long_running_task, kwargs={
                    'tid': transaction_id})
    thread.start()
    return {"status": "Accepted", "transaction_id": transaction_id}, 202


@app.route('/get_op_status/<tid>', methods=['GET'])
def get_op_status(tid):
    op_status = read_op_status(int(tid))
    print(f'Asked for status: got {op_status}')
    if op_status["status"] == "done":
        rcode = 200
    else:
        rcode = 202
    return {"status": op_status["status"]}, rcode
    #return op_status, rcode


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5902, debug=True)