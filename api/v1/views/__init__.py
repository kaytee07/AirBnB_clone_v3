#!/usr/bin/python3
"""
blueprint
"""
from flask import Blueprint
from .index import *
from .states import *


app_views = Blueprint('api_views', __name__, url_prefix='/api/v1')
