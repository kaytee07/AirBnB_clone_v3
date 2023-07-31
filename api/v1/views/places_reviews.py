#!/usr/bin/python3
"""
View for Places that handles all RESTful API actions
"""

from api.v1.views import (app_views, Place, User, Review, storage)
from flask import (abort, jsonify, request)


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def places_all(place_id):
    """ returns list of all Place objects linked to a given City """
    reviews = list(storage.all("Review").values())
    review_in_place = []
    for review in reviews:
        if review.place_id == place_id:
            review_in_place.append(review.to_dict())
    if len(review_in_place) == 0:
        abort(404)
    return jsonify(review_in_place), 200


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """ handles GET method """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review_dict = review.to_dict()
    return jsonify(review_dict)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_review(review_id):
    """ handles DELETE method """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ handles POST method """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'name' not in data or not data['name']:
        return jsonify({'error': 'Missing name'}), 400

    if 'user_id' not in data or not data['user_id']::
        return jsonify({'error': 'Missing user_id'}), 400

    if 'text' not in data or not data['text']:
        return jsonify({'error': 'Missing text'}), 400

    if not storage.get(User, data.user_id):
        abort(404)

    if not storage.get(Place, place_id):
        abort(404)

    review = Review(**data)
    review['place_id'] = place_id
    review.save()
    review_dict = review.to_dict()
    return jsonify(review_dict), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """ handles PUT method """
    if review_id is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return jsonify({'Not a JSON'}), 400

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    for key, value in data.items():
        if key == "created_at" or key == 'id' or key == 'updated_at':
            continue
        else:
            setattr(review, key, value)
    review_dict = review.to_dict()
    review.save()
    review.save()
    return jsonify(review_dict), 201
