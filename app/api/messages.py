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

@api.route('/messages', methods=['GET', 'POST'])
@login_required
def messages(limit=5, offset=0):
	if request.method == 'GET':
		messages = []
		if offset > 1:
			page_offset=int(offset/limit)
		else:
			page_offset=1
		query = Message.query.paginate(per_page=limit, page=page_offset)
		for message in query.items:
			messages.append({
				'id': message.id,
				'timestamp': message.timestamp,
				'text': message.text,
				'sender': message.sender.username,
				'recipients': [r.username for r in message.recipients],
				})
		return jsonify({"messages": messages}), 200

	if request.method == 'POST':
		try:
			recipients_list = request.json['recipients'].split(',')
			recipients = [User.query.filter_by(username=username.strip()).first()\
				for username in recipients_list]
			sender = User.query.filter_by(username=request.json['sender']).first()
			text = request.json['text']
			sender.send_message(text=text, recipients=recipients)
			return jsonify({'success': True, 'message': 'Message created'}), 201
		except Exception, e:
			return jsonify({'success': False, 'reason': e.message})