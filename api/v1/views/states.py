#!/user/bin/python3
"""
This is a view for state
"""
#import os
#import sys
#from flask import jsonify, abort, request
#from models.state import State
#from models import storage
#from . import app_views
#parent_directory = os.path.abspath(os.path.join(os.path.dirname
                                                ('app.py'), '..', '..', '..'))
#sys.path.append(parent_directory)


@app_views.route('/states')
#def get_allstate():
    """ return all state object """
#    get_state = []
#    all_states = list(storage.all("State").values())
#    for data in all_states:
#        get_state.append(data.to_dict())
#    return jsonify(get_state)


#@app_views.route('/states/<state_id>')
#def get_state(state_id):
    """
    get state in database using state id pass through the uri
    """
#    if state_id is None:
#        abort(404)
#    state = storage.get(State, state_id)
#    if state is None:
#        abort(404)
#   return jsonify(state.to_dict())


#@app_views.route('/states/<state_id>', methods=['DELETE'])
#def del_state(state_id):
    """
    delete state using state id passed in the the uri
    """
#    if state_id is None:
#        abort(404)
#    state = storage.get(State, state_id)
#    if state is None:
#        abort(404)
#    storage.delete(state)
#    return jsonify({}), 200


#@app_views.route('/states', methods=['POST'])
#def create_state():
    """
    create new state
    """
#    data = request.get_json()
#    if data is None:
#        return jsonify({'error': 'Not a JSON'}), 400

#    if 'name' not in data:
#        return jsonify({'error': 'Missing name'}), 400

#    new_state = State(**data)
#    storage.save()
#    state_dict = new_state.to_dict()
#   return jsonify(state_dict), 201


#@app_views.route('/states/<state_id>', methods=['PUT'])
#def update_state(state_id):
    """
    get class using state id passed in uri and update it using
    data from http body
    """
#    if state_id is None:
#        abort(404)
#    data = request.get_json()
#    print(data)
#    if data is None:
#        return jsonify({'error': 'Not a JSON'}), 400

#    state = storage.get(State, state_id)
#    print(state)
#    if state is None:
#        abort(404)

#    for key, value in data.items():
#        if key == "created_at" or key == 'id' or key == 'updated_at':
#            continue
#        else:
#            setattr(state, key, value)
#    state.save()
#    storage.save()
#    return jsonify(state.to_dict()), 200
