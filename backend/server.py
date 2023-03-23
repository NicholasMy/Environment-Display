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
    # return {"data": get_fake_room_data()}
    data = {}

    for monitor in monitors:
        data[monitor.name] = monitor.fetch_data()

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
