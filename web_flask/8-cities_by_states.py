#!/usr/bin/python3

"""

"""

from flask import Flask, render_template

from models import storage
from models.state import State


app = Flask(__name__)


def get_states(cls=None):
    result = storage.all(cls)
    return result

@app.teardown_appcontext
def close_db(exception):
    storage.close()

@app.route("/cities_by_states", strict_slashes=False)
def get_state():
    """ """
    all_states = list(get_states(State).values())

    states = [(state.name, state) for state in all_states]
    states.sort()
    
    state_cities = {}
    for data in states:
        state = data[1]
        cities = [(city_obj.name, city_obj.id) for city_obj in state.cities]
        cities.sort()
        state_cities[state] = cities

    return render_template("8-cities_by_states.html", state_cities=state_cities)


if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

