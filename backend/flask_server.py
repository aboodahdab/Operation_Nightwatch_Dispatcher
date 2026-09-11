from flask import render_template, Flask, jsonify, send_from_directory, request
import redis
import json
import threading
from flask_socketio import SocketIO
from functions import add_to_data, read_file

app = Flask(__name__, static_folder="../frontend/style",
            template_folder="../frontend/templates")
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
socketio = SocketIO(app)
HISTORY_FILE_PATH = "coords_History.json"


def run_flask():
    app.run(debug=False, port=4000)


redis_data_arr = []
history_arr = []


def redis_waiter():
    last_id = "0"
    print("REDIS IS WORKING.")
    while True:

        response = r.xread({"data": last_id}, block=6500, count=15)
        if response:
            stream_key, value = response[0]
            for entry_id, fields in value:
                last_id = entry_id

                print("Received:", fields)

                print("--"*14)
                socketio.emit("Data", fields)


def redis_history_waiter():
    last_id = "0"
    print("REDIS HISTORY IS WORKING.")
    while True:

        response = r.xread({"history": last_id}, block=6500, count=15)
        if response:
            stream_key, value = response[0]
            for entry_id, fields in value:
                last_id = entry_id

                socketio.emit("History_Data", fields)


@app.route("/")
def Homepage():
    return render_template("homepage.html", file="main.js")


@app.route("/history")
def send_history():

    return jsonify({"history": history_arr})


def start_socket():
    print("Starting Flask:")
    socketio.run(app, debug=False, port=4000)


@app.route("/read_history_file", methods=["GET"])
def reading_file():
    try:
        data = read_file(HISTORY_FILE_PATH)

        return send_from_directory('.', HISTORY_FILE_PATH),200
    except Exception as err:
        print("error reading history", err)
        return jsonify({"status":"fail","message":"Server internal error"}),500


@app.route("/write_to_history_file", methods=["POST"])
# we shall be those who write the history! lol
def writing_to_history():
    if request.is_json:
        data = request.get_json()

        query=data["query"]
        data = add_to_data(HISTORY_FILE_PATH,query)

        return jsonify({"status": "success", "message": "added data to the history file."}), 200
    return jsonify({"status": "fail", "message": "request must be JSON"}), 415


if __name__ == "__main__":

    t = threading.Thread(target=redis_waiter)
    t2 = threading.Thread(target=start_socket)
    t3 = threading.Thread(target=redis_history_waiter)

    t.start()
    t2.start()
    t3.start()

    t.join()
    t2.join()
    t3.join()
