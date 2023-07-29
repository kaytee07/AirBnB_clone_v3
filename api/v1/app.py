#!/usr/bin/python3
"""
return the status of my api
"""
from flask import Flask
import sys
import os
from models import storage
from api.v1.views import app_views
parent_directory = os.path.abspath(os.path.join(os.path.dirname('app.py'), '..', '..'))
sys.path.append(parent_directory)

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage(exception):
    """ close storage """
    storage.close()

if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    app.run(host=host, port=port, threaded=True)
