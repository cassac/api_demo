import os
from flask import Flask, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config_name)
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # suppress SQLAlchemy error
	db.init_app(app)

	from .api import api as api_blueprint
	app.register_blueprint(api_blueprint)

	@app.errorhandler(400)
	def bad_request(error):
		return make_response(jsonify({'error': '400: Recheck your syntax'}), 400)

	@app.errorhandler(404)
	def not_found(error):
		return make_response(jsonify({'error': '404: Resource not found'}), 404)

	return app