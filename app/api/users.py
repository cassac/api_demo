from functools import wraps
from flask import request, jsonify, abort, make_response
from utils import check_auth, authenticate
from . import api
from ..models import *

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

@api.route('/users', methods=['GET', 'POST'])
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

@api.route('/users/<username>', methods=['GET', 'POST', 'DELETE'])
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