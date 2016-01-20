from functools import wraps
from flask import request, jsonify, abort, make_response
from utils import check_auth, authenticate
from . import api
from ..models import *

@api.route('/api/v1/messages', methods=['GET'])
def messages():
	if request.method == 'GET':
		messages = []
		for message in Message.query.all():
			messages.append({
				'id': message.id,
				'text': message.text,
				})
		return jsonify({"messages": messages}), 200