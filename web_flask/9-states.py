#!/usr/bin/python3

"""

"""

from models import storage
from models.state import State

from flask import Flask, render_template, request


app = Flask(__name__)

def get_objects(cls=None):
    """ Returns all instances of the State class """
    result = storage.all(cls)
    return result

def id_exists(id, cls=None):
    """ Checks whether a given ID exits in the database"""
    all_objects = get_objects(cls)
    objects = list(all_objects.values())
    for obj in objects:
        if id == obj.id:
            return obj
    return None



@app.teardown_appcontext
def close_db(exception):
    storage.close()


@app.route("/states", strict_slashes=False)
def get_states():
    """ Returns a list of states by their names and IDs"""
    all_states = list(get_objects(State).values())
    states = [(state.name, state.id) for state in all_states]
    states.sort()

    return render_template("9-states.html", states=states)

@app.route("/states/<id>", strict_slashes=False)
def get_obj_by_id(id):
    """ """
    obj = id_exists(id, cls=State)

    if not obj:
        return render_template("9-states.html", result="Not found!")
    else:
        cities = [(city_obj.name, city_obj.id) for city_obj in obj.cities]
        cities.sort()
        return render_template("9-states.html", obj=obj, cities=cities)




if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
