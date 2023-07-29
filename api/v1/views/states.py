#!/user/bin/python3
"""
This is a view for state
"""
import os
import sys
from flask import jsonify
from models.state import State
from models import storage
from . import app_views
parent_directory = os.path.abspath(os.path.join(os.path.dirname('app.py'), '..', '..', '..'))
sys.path.append(parent_directory)


@app_views.route('/states')
def get_state():
    """ return all state object """
    get_state = []
    all_states = list(storage.all("State").values())
    for data in all_states:
        get_state.append(data.to_dict())
        print(data.to_dict())
    return jsonify(get_state)
