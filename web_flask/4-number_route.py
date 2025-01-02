#!/usr/bin/python3

"""

"""

from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    return "Hello HBNB!"

@app.route("/hbnb", strict_slashes=False)
def hbnb():
    return "HBNB"

@app.route("/c/<text>", strict_slashes=False)
def c_text(text):
    if "_" in text:
        text = text.replace("_", " ")
    return f"C {text}"

@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_text(text="is cool"):
    if "_" in text:
        text = text.replace("_", " ")
    return f"Python {text}"

@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    return f"{n} is a number"


if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
