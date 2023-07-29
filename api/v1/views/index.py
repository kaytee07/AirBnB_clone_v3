#!/usr/bin/app
"""
/status route
"""
import os
import sys
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models.user import User
from flask import jsonify
from . import app_views
parent_directory = os.path.abspath(os.path.join(os.path.dirname('app.py'), '..', '..', '..'))
sys.path.append(parent_directory)

@app_views.route('/status')
def status():
    """ return status code """
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def stats():
    """retrieve number of each object by type"""
    all_stat = {}
    all_classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }
    for key, value in all_classes.items():
        all_stat[key] = storage.count(value)

    return jsonify(all_stat)
