from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
from models import *


@app.route('/api/v1/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def users():
	if request.method == 'GET':
		users = []
		for user in User.query.all():
			users.append({
				"id": user.id,
				"username": user.username
				})
		return jsonify({"users": users}), 200

	if request.method == 'POST':
		try:
			user = User(username=request.json['username'])
			db.session.add(user)
			db.session.commit()
			return jsonify({"success": True, "message": "User created"}), 201
		except Exception, e:
			return jsonify({"success": False, "reason": e.message})

@app.route('/api/v1/users/<username>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user(username):
	if request.method == 'GET':
		user = User.query.filter_by(username=username).first()
		if user is None:
			return jsonify({"success": False, "reason": "User not found"}), 400
		user = [{"id": user.id, "username": user.username}]
		return jsonify({"users": user}), 200

	if request.method == 'POST':
		user = User.query.filter_by(username=username).first()
		if user is None:
			return jsonify({"success": False, "reason": "User not found"}), 400
		if "new_username" in request.json:
			user.username = request.json['new_username']		
		try:		
			db.session.commit()
			return jsonify({"success": True, "message": "User updated"}), 200
		except Exception, e:
			return jsonify({"success": False, "reason": e.message})

	if request.method == 'DELETE':
		user = User.query.filter_by(username=username).first()
		if user is None:
			return jsonify({"success": False, "reason": "User not found"}), 400
		db.session.delete(user)
		db.session.commit()
		return jsonify({"success": True, "message": "User deleted"}), 200

if __name__ == '__main__':
	app.run(debug=True)