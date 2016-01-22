from flask import jsonify

from ..models import *

def check_auth(username, password):
	user = User.query.filter_by(username=username).first()
	return user.verify_password(password)

def authenticate():
	return jsonify({'message': 'Invalid username and/or password.'}), 401