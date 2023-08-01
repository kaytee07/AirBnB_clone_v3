#!/usr/bin/python3
"""
View for Places that handles all RESTful API actions
"""

from api.v1.views import (app_views, User, City, Place, storage)
from flask import (abort, jsonify, request, make_response)
from flasgger.utils import swag_from


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
        return jsonify({'error': 'Not a JSON'}), 400

    if 'name' not in data or not data['name']:
        return jsonify({'error': 'Missing name'}), 400

    if 'user_id' not in data or not data['user_id']:
        return jsonify({'error': 'Missing user_id'})

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
    if place_id is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return jsonify({'Not a JSON'}), 400

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    for key, value in data.items():
        if key == "created_at" or key == 'id' or key == 'updated_at':
            continue
        else:
            setattr(place, key, value)
    place_dict = place.to_dict()
    place.save()
    storage.save()
    return jsonify(place_dict), 200


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/places/search.yml', methods=['POST'])
def search_places_by_id():
    """ search places by id """
    if request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)
