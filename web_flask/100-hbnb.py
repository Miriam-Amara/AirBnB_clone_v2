#!/usr/bin/python3

"""

"""

from models import storage
from models.place import Place
from models.state import State
from models.amenity import Amenity

from flask import Flask, render_template, request


app = Flask(__name__)

def get_states(cls=State):
    """ Returns sorted state objects """
    all_states = storage.all(cls=cls)
    states = []
    for obj in all_states.values():
        cities = [city.name for city in obj.cities]
        states.append((obj.name, sorted(cities)))
    return states


def get_amenities(cls=Amenity):
    """ Returns sorted amenities objects """
    all_amenities = storage.all(cls=cls)
    amenities = [obj.name for obj in all_amenities.values()]
    amenities.sort()
    return amenities


def get_places(cls=Place, current_page=None, page_size=None):
    """
    Returns paginated Place objects and
    the total number of rows in place table
    """
    all_places, total_rows = storage.all(cls=cls,
                        current_page=current_page,
                        page_size=page_size
                    )
    place_obj = list(all_places.values())
    places = {}

    for place in place_obj:
        guest = "Guests" if place.max_guest > 1 else "Guest"
        room = "Rooms" if place.number_rooms > 1 else "Room"
        bathroom = "Bathrooms" if place.number_bathrooms > 1 else "Bathroom"
        amenities = [amenity.name for amenity in place.amenities]
        reviews = [
            (f"{review.user.first_name} {review.user.last_name}",
             review.updated_at.strftime("%d %B %Y"), review.text)
             for review in place.reviews
        ]
        place_attributes = {
                            "price": place.price_by_night,
                            "max_guest": f"{place.max_guest} {guest}",
                            "room": f"{place.number_rooms} {room}",
                            "bathroom": f"{place.number_bathrooms} {bathroom}",
                            "description": place.description,
                            "owner": f"{place.user.first_name} {place.user.last_name}",
                            "amenities": amenities,
                            "reviews": reviews,
                        }
        places[place.name] = place_attributes
        


    # get two place objects at a time with list of tuples
    # places = [(obj[i], obj[i+1]) for i in range(0, 6, 2)]
    return places, total_rows


@app.teardown_appcontext
def close_db_session(exception):
    """ closes database session """
    storage.close()


@app.route("/hbnb", strict_slashes=False)
def get_hbnb_homepage():
    """ """
    states = get_states()
    amenities = get_amenities()
    current_page = request.args.get('page', 1)

    try:
        current_page = int(current_page)
    except ValueError:
        return "Invalid page number!", 400
    places, total_rows = get_places(current_page=current_page, page_size=10)
    
    return render_template(
        "100-hbnb.html",
        states=states,
        amenities=amenities,
        places=places,
        total_rows=total_rows
    )



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

