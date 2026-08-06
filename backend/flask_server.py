from flask import render_template, Flask, jsonify
import redis
import json
import threading
from flask_socketio import SocketIO

app = Flask(__name__, static_folder="../frontend/style",
            template_folder="../frontend/templates")
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
socketio=SocketIO(app)

def run_flask():
    app.run(debug=False, port=4000)


redis_data_arr = []


def redis_waiter():
    last_id = "0"
    print("yes im working guys", last_id)
    while True:

        response = r.xread({"data": last_id}, block=6500, count=15)
        if response:
            stream_key, value = response[0]
            for entry_id, fields in value:
                last_id = entry_id

                print(fields)
                redis_data_arr.append(fields)
                print("yessss")
                if len(redis_data_arr)>=10:
                    socketio.emit("Data", {"value": redis_data_arr})




@app.route("/")
def Homepage():
    return render_template("homepage.html", file="main.js")


# @app.route("/get_data")
# def get_data():
#     global redis_data_arr
#     sent_data = redis_data_arr

#     redis_data_arr = []

#     return jsonify({"arr": sent_data})


# print(redis_data_arr)


def start_socket():
    socketio.run(app, debug=False,port=4000)


if __name__ == "__main__":

    t = threading.Thread(target=redis_waiter)
    t2 = threading.Thread(target=start_socket)
    t.start()
    t2.start()
    t.join()
    t2.join()
