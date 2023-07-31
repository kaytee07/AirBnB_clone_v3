#!/usr/bin/python3
"""
blueprint
"""
from flask import Blueprint
from models.state import State
from models.city import City
from models import storage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
app_views = Blueprint('api_views', __name__, url_prefix='/api/v1')

from .index import *
from .states import *
from .cities import *
from .amenities import *
from .users import *
from .places import *
