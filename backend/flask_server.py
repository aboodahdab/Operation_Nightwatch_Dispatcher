from flask import render_template, Flask, jsonify
import redis
import json
import threading
from flask_socketio import SocketIO

app = Flask(__name__,static_folder="../frontend/style",
            template_folder="../frontend/templates")
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
socketio = SocketIO(app)


def run_flask():
    app.run(debug=False, port=4000)

redis_data_arr = []


def redis_waiter():
    last_id = "0"
    print("REDIS IS WORKING.")
    while True:

        response = r.xread({"data": last_id}, block=6500, count=15)
        if response:
            stream_key, value = response[0]
            for entry_id, fields in value:
                last_id = entry_id

                print(fields)

                print("--"*14)
                socketio.emit("Data", fields)



@app.route("/")
def Homepage():
    return render_template("homepage.html", file="main.js")





def start_socket():
    socketio.run(app, debug=False, port=4000)


if __name__ == "__main__":

    t = threading.Thread(target=redis_waiter)
    t2 = threading.Thread(target=start_socket)
    t.start()
    t2.start()
    t.join()
    t2.join()
