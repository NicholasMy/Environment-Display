from datetime import datetime
from random import randint
from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
from NTIEnvironmentMonitor import NTIEnvironmentMonitor
from backend import login_secrets as secrets

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:*"}})
# This isn't great for security, but it shouldn't be a problem in the context of this app:
socketio = SocketIO(app, cors_allowed_origins="*")
CACHED_DATA = None

monitors = [
    NTIEnvironmentMonitor("davis339a", "Davis 339A", "https://temp-davis-339a.cse.buffalo.edu/",
                          secrets.NTI_USERNAME, secrets.NTI_PASSWORD),
    NTIEnvironmentMonitor("davis339c", "Davis 339C", "https://temp-davis-339c.cse.buffalo.edu/",
                          secrets.NTI_USERNAME, secrets.NTI_PASSWORD),
    NTIEnvironmentMonitor("davis339e", "Davis 339E", "https://temp-davis-339e.cse.buffalo.edu/",
                          secrets.NTI_USERNAME, secrets.NTI_PASSWORD)
]


@app.route("/")
def api():
    return "Whoops, you probably meant to load the frontend or make a specific API call."


# @app.route("/test")
# def test_page():
#     return render_template("test.html")


@app.route("/rooms")
def rooms():
    # Return a list of valid rooms and their friendly names

    rooms_list = []
    for monitor in monitors:
        rooms_list.append({
            "name": monitor.name,
            "friendly_name": monitor.friendly_name
        })

    d = {
        "rooms": rooms_list
    }
    return d


@app.route("/data")
def data():
    return get_data_to_send_client(True)


@socketio.on("connect")
def on_connect():
    print("Client connected")
    socketio.emit("data", get_data_to_send_client())


def get_data_to_send_client(use_cache=False):
    global CACHED_DATA
    # This is blocking, so it will delay websocket connections while running
    if use_cache and CACHED_DATA:
        return {"data": CACHED_DATA}

    data = {}

    for monitor in monitors:
        data[monitor.name] = monitor.fetch_data()

    data["time"] = datetime.now().isoformat()

    CACHED_DATA = data

    return {"data": data}


def background_sender():
    while True:
        socketio.sleep(2)
        socketio.emit("data", get_data_to_send_client())


def main():
    # app.run("0.0.0.0", 8085)
    # threading.Thread(target=background_sender).start()
    socketio.start_background_task(target=background_sender)
    socketio.run(app, "0.0.0.0", 8085)
    # socketio.run(app)


if __name__ == "__main__":
    main()
