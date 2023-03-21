from random import randint
from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:*"}})
# This isn't great for security, but it shouldn't be a problem in the context of this app:
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def api():
    return "Home page"


@app.route("/sample")
def sample():
    # Return a random number
    return str(randint(0, 100))


@app.route("/test")
def test_page():
    return render_template("test.html")


@app.route("/rooms")
def rooms():
    # Return a list of valid rooms and their friendly names
    d = {
        "rooms": [
            {"name": "davis339a", "friendly_name": "Davis 339A"},
            {"name": "davis339c", "friendly_name": "Davis 339C"},
            {"name": "davis339e", "friendly_name": "Davis 339E"},
        ]
    }
    return d


@socketio.on("connect")
def on_connect():
    print("Client connected")
    socketio.emit("data", get_data_to_send_client())


def get_fake_room_data():
    d = {}
    for room in rooms()["rooms"]:
        d[room["name"]] = {'alertTime': 'Never', 'minTime': '03-19-2023  05:24:46 AM',
                           'maxTime': '03-21-2023  12:08:56 PM', 'alertValue': 'N/A', 'minValue': '60.5',
                           'maxValue': '67.7', 'minThresh': '50.0', 'maxThresh': '85.0', 'minWThresh': '55.0',
                           'maxWThresh': '74.0', 'minVal': '-4.0', 'maxVal': '185.0', 'units': '&deg;F',
                           'current': str(randint(50, 70)), 'status': 'Normal', 'logscale': '0', 'aclmfreq': '0.0 Hz',
                           'aclmspkth': '50 V', 'aclmswell': '0', 'aclmsags': '0', 'aclmspks': '0', 'aclmcur': '0.0 A',
                           'aclmvolt': '0.0 V', 'aclmrly': 'Closed'}

    return d

def get_data_to_send_client():
    return {"data": get_fake_room_data()}

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
