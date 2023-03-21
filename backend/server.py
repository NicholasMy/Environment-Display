from random import randint
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:*"}})

@app.route("/")
def api():
    return "Home page"


@app.route("/sample")
def sample():
    # Return a random number
    return str(randint(0, 100))


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


def main():
    app.run("0.0.0.0", 8085)


if __name__ == "__main__":
    main()
