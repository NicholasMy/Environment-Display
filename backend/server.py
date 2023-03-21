from random import randint

from flask import Flask

app = Flask(__name__)


@app.route("/")
def api():
    return "Home page"


@app.route("/sample")
def sample():
    # Return a random number
    return str(randint(0, 100))


def main():
    app.run("0.0.0.0", 8085)


if __name__ == "__main__":
    main()
