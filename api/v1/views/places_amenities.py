#!/usr/bin/python3
"""
new view for the link between Place and Amenity
"""
from api.v1.views import (app_views, Place, Amenity, storage)
from flask import (abort, jsonify, make_response, request)


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def all_amenity_of_place(place_id):
    """ returns list of all Place objects linked to a given City """
    place = storage.get(Place, place_id)
    amenity_in_place = []
    for amenity in place.amenities:
        amenity_in_place.append(amenity.to_dict())
    if len(amenity_in_place) == 0:
        abort(404)
    return jsonify(amenity_in_place), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """ handles DELETE method """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    for amenity in place.amenities:
        if amenity.id == amenity_id:
            storage.delete(amenity)
        else:
            abort(404)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def amenity_to_place(place_id, amenity_id):
    """ handles POST method """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    for amenity in place.amenities:
        if amenity.id == amenity_id:
            return jsonify(amenity.to_dict())
        else:
            abort(404)
