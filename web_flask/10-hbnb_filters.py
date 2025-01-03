#!/usr/bin/python3

from models import storage

from flask import Flask, render_template

app = Flask(__name__)


def get_objects(cls=None):
    """ Returns the objects of the given class or all objects """
    objects = storage.all(cls)
    return objects

@app.teardown_appcontext
def close_db_session(exception):
    """ Closes a database session """
    storage.close()

@app.route("/hbnb_filters")
def get_all_obj():
    """ """
    all_objects = get_objects()
    all_states = []
    all_amenities = []
    state_cities = {} # dict of states with their cities list
    for key, obj in all_objects.items():
        cls_name = key.split('.')[0]
        if cls_name == "State":
            all_states.append(obj.name)
            state_cities[obj.name] = sorted([city.name for city in obj.cities])
        if cls_name == "Amenity":
            all_amenities.append(obj.name)
    all_states.sort()
    all_amenities.sort()

    return render_template(
        "10-hbnb_filters.html",
        all_amenities=all_amenities,
        all_states=all_states,
        state_cities=state_cities
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)