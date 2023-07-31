#!/usr/bin/python3
"""
This is module states
"""
from api.v1.views import (app_views, Place, storage)
from flask import (abort, jsonify, make_response, request)


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places_in_city(city_id):
    """ return all place object """
    get_place = []
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    for data in city.places:
        get_place.append(data.to_dict())
    return jsonify(get_place)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_places(place_id):
    """
    get place in database using place id pass through the uri
    """
    if place_id is None:
        abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """
    delete place using place id passed in the the uri
    """
    if place_id is None:
        abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    create new place
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    if 'user_id' not in r.keys():
        return "Missing user_id", 400
    user = storage.get("User", r.get("user_id"))
    if user is None:
        abort(404)
    if 'name' not in r.keys():
        return "Missing name", 400
    r["city_id"] = city_id
    s = Place(**r)
    s.save()
    return jsonify(s.to_json()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """
    get class using place id passed in uri and update it using
    data from http body
    """
    if place_id is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    for key, value in data.items():
        if key == "created_at" or key == 'id' or key == 'updated_at':
            continue
        else:
            setattr(Place, key, value)
    place.save()
    storage.save()
    return jsonify(place.to_dict()), 200
