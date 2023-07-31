#!/usr/bin/python3
"""
This is module states
"""
from api.v1.views import (app_views, Amenity, storage)
from flask import (abort, jsonify, make_response, request)


@app_views.route('/amenities', strict_slashes=False)
def get_allamenities():
    """ return all amenity object """
    get_amenity = []
    all_amenities = list(storage.all("Amenity").values())
    for data in all_amenities:
        get_amenity.append(data.to_dict())
    return jsonify(get_amenity)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id):
    """
    get amenity in database using amenity id pass through the uri
    """
    if amenity_id is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """
    delete state using state id passed in the the uri
    """
    if amenity_id is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    create new amenity
    """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'name' not in data.keys():
        return jsonify({'error': 'Missing name'}), 400

    new_amenity = Amenity(**data)
    storage.save()
    amenity_dict = new_amenity.to_dict()
    return jsonify(amenity_dict), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    get class sing samenity id passed in uri and update it using
    data from http body
    """
    if amenity_id is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    for key, value in data.items():
        if key == "created_at" or key == 'id' or key == 'updated_at':
            continue
        else:
            setattr(amenity, key, value)
    amenity.save()
    storage.save()
    return jsonify(amenity.to_dict()), 200
