#!/usr/bin/python3
"""
blueprint
"""
from flask import Blueprint

app_views = Blueprint('api_views', __name__, url_prefix='/api/v1')

from .index import *
from .states import *
from .cities import *
