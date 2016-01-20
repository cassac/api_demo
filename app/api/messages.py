from functools import wraps
from flask import request, jsonify, abort
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

@api.route('/messages', methods=['GET'])
@login_required
def messages():
	if request.method == 'GET':
		messages = []
		for message in Message.query.all():
			messages.append({
				'id': message.id,
				'text': message.text,
				'sender': message.sender.username,
				'recipients': [r.username for r in message.recipients],
				})
		return jsonify({"messages": messages}), 200