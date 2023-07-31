#!/usr/bin/python3
"""
return the status of my api
"""
from flask import Flask, jsonify
import sys
import os
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

parent_directory = os.path.abspath(os.path.
                                   join(os.path.dirname('app.py'), '..', '..'))
sys.path.append(parent_directory)

app = Flask(__name__)

app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_storage(exception):
    """ close storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Custom handler for 404 errors."""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    app.run(host=host, port=port, threaded=True)
