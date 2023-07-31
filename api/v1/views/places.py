#!/usr/bin/python3
"""
This is module states
"""
from api.v1.views import (app_views, Place, storage)
from flask import (abort, jsonify, make_response, request)


@app_views.route('/places', strict_slashes=False)
def get_all_places():
    """ return all place object """
    get_place = []
    all_places = list(storage.all("Place").values())
    for data in all_places:
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


@app_views.route('/places', methods=['POST'], strict_slashes=False)
def create_place():
    """
    create new place
    """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'name' not in data.keys():
        return jsonify({'error': 'Missing name'}), 400

    new_place = Place(**data)
    storage.save()
    place_dict = new_place.to_dict()
    return jsonify(place_dict), 201


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
