#!/usr/bin/python3
"""
This is module states
"""
from api.v1.views import (app_views, User, storage)
from flask import (abort, jsonify, make_response, request)


@app_views.route('/users', strict_slashes=False)
def get_all_users():
    """ return all user object """
    get_user = []
    all_users = list(storage.all("User").values())
    for data in all_users:
        get_user.append(data.to_dict())
    return jsonify(get_user)


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    """
    get user in database using amenity id pass through the uri
    """
    if user_id is None:
        abort(404)
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """
    delete user using state id passed in the the uri
    """
    if user_id is None:
        abort(404)
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    create new user
    """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'name' not in data.keys():
        return jsonify({'error': 'Missing name'}), 400

    if 'password' not in data.keys():
        return jsonify({'error': 'Missing password'}), 400

    new_user = User(**data)
    storage.save()
    user_dict = new_user.to_dict()
    return jsonify(user_dict), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """
    get class using user id passed in uri and update it using
    data from http body
    """
    if user_id is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    for key, value in data.items():
        if key == "created_at" or key == 'id' or key == 'updated_at':
            continue
        else:
            setattr(User, key, value)
    user.save()
    storage.save()
    return jsonify(user.to_dict()), 200
