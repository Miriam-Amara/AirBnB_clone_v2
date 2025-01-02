#!/usr/bin/python3

"""

"""

from flask import Flask, render_template

from models import storage
from models.state import State
# from models.base_model import BaseModel

app = Flask(__name__)


def get_db(cls=None):
    result = storage.all(cls)
    return result

@app.teardown_appcontext
def close_db(exception):
    storage.close()

@app.route("/states_list", strict_slashes=False)
def get_state():
    # state_obj = []
    all_states = get_db(State)

    # for key, value in all_states.items():
    #     value = value.to_dict()
    #     state_obj.append(value)
    return render_template("7-states_list.html", all_states=all_states)


if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

