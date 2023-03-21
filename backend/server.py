from random import randint
from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:*"}})
socketio = SocketIO(app)


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


def background_sender():
    while True:
        socketio.sleep(2)
        socketio.emit("data", {"data": randint(0, 100)})


def main():
    # app.run("0.0.0.0", 8085)
    # threading.Thread(target=background_sender).start()
    socketio.start_background_task(target=background_sender)
    socketio.run(app, "0.0.0.0", 8085)
    # socketio.run(app)


if __name__ == "__main__":
    main()
