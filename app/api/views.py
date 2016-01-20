from functools import wraps
from flask import request, jsonify, abort, make_response
from . import api
from ..models import *

def check_auth(username, password):
	user = User.query.filter_by(username=username).first()
	return user.verify_password(password)

def authenticate():
	return jsonify({'message': 'Invalid username and/or password.'}), 401

def login_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth:
			return authenticate()
		elif not check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)
	return decorated

@api.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Recheck your syntax'}), 400)

@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource not found'}), 404)

@api.route('/api/v1/users', methods=['GET', 'POST'])
def users():
	if request.method == 'GET':
		users = []
		for user in User.query.all():
			users.append({
				'id': user.id,
				'username': user.username
				})
		return jsonify({"users": users}), 200

	if request.method == 'POST':
		user = User.query.filter_by(username=request.json['username']).first()
		if user is not None:
			return jsonify({'success': False, 'error': 'Username already taken'}), 400
		try:
			user = User(username=request.json['username'])
			db.session.add(user)
			db.session.commit()
			return jsonify({'success': True, 'message': 'User created'}), 201
		except Exception, e:
			return jsonify({'success': False, 'reason': e.message})

@api.route('/api/v1/users/<username>', methods=['GET', 'POST', 'DELETE'])
@login_required
def user(username):
	if request.method == 'GET':
		user = User.query.filter_by(username=username).first()
		if user is None:
			abort(400)
		user = [{'id': user.id, 'username': user.username}]
		return jsonify({'users': user}), 200

	if request.method == 'POST':
		user = User.query.filter_by(username=username).first()
		new_username = User.query.filter_by(username=request.json['new_username']).first()
		if user is None:
			abort(400)
		if new_username is None and user is not None:
			user.username = request.json['new_username']
		else:
			return jsonify({'error': 'Username already taken'}), 400		
		try:		
			db.session.commit()
			return jsonify({'success': True, 'message': 'User updated'}), 200
		except Exception, e:
			abort(400)

	if request.method == 'DELETE':
		user = User.query.filter_by(username=username).first()
		if user is None:
			abort(400)
		db.session.delete(user)
		db.session.commit()
		return jsonify({'success': True, 'message': 'User deleted'}), 200