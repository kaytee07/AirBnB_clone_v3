#!/usr/bin/python3
"""
This is module states
"""
from api.v1.views import (app_views, State, City, storage)
from flask import (abort, jsonify, request)


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_city_by_state(state_id):
    """ get all cities in the same state """
    state = list(storage.all("City").values())
    city_in_state = []
    if state is None:
        abort(404)
    for data in state:
        if data.state_id == state_id:
            city_in_state.append(data.to_dict())
    return jsonify(city_in_state), 200


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    """
    get city in database using state id pass through the uri
    """
    if city_id is None:
        abort(404)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """
    delete state using state id passed in the the uri
    """
    if city_id is None:
        abort(404)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    create new state
    """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'name' not in data.keys():
        return jsonify({'error': 'Missing name'}), 400

    city = City(**data)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """
    get class using state id passed in uri and update it using
    data from http body
    """
    if city_id is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    city = storage.get(City, city_id)
    dict = city.to_dict()
    if city is None:
        abort(404)

    for key, value in data.items():
        if key == "created_at" or key == 'id' or key == 'updated_at':
            continue
        else:
            setattr(city, key, value)
    city.save()
    storage.save()
    return jsonify(dict), 200
