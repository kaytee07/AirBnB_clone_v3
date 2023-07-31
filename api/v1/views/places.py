#!/usr/bin/python3
"""
View for Places that handles all RESTful API actions
"""

from api.v1.views import (app_views, User, City, Place, storage)
from flask import (abort, jsonify, request)


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_all(city_id):
    """ returns list of all Place objects linked to a given City """
    places = list(storage.all("Place").values())
    place_in_city = []
    for place in places:
        if place.city_id == city_id:
            place_in_city.append(place.to_dict())
    if len(place_in_city) == 0:
        abort(404)
    return jsonify(place_in_city), 200


@app_views.route('/places/<place_id>', methods=['GET'])
def place_get(place_id):
    """ handles GET method """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place_dict = place.to_dict()
    return jsonify(place_dict)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def place_delete(place_id):
    """ handles DELETE method """
    empty_dict = {}
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify(empty_dict), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_post(city_id):
    """ handles POST method """
    data = request.get_json()
    if data is None:
        return jsonify({'Not a JSON'}), 400

    if 'name' not in data.keys():
        return jsonify({'Missing name'}), 400

    if 'user_id' not in data.keys():
        return jsonify({'Missing user_id'})

    if not storage.get(User, data.user_id):
        abort(404)

    place = Place(**data)
    place.city_id = city_id
    place.save()
    place_dict = place.to_dict()
    return jsonify(place_dict), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def place_put(place_id):
    """ handles PUT method """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
        if key not in ignore_keys:
            place.bm_update(key, value)
    place.save()
    place = place.to_json()
    return jsonify(place), 200
