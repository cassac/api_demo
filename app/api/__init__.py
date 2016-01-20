from functools import wraps
from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api/v1')

from . import users, messages
