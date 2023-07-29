#!/usr/bin/app
"""
/status route
"""
from flask import jsonify
from . import app_views


@app_views.route('/status')
def status():
    """ return status code """
    return jsonify({"status": "OK"})
