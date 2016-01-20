import os

ROOT_DIR = os.path.dirname(__file__)

class BaseConfig(object):
	'Base configuration class'
	SECRET_KEY = 'very secret secret key'

	@staticmethod
	def init_app(app):
		pass

class ProductionConfig(BaseConfig):
	'Production specific configuration'
	DEBUG = False
	TESTING = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(ROOT_DIR, 'production.sqlite')

class DevelopmentConfig(BaseConfig):
	'Development environment specific configuration'
	DEBUG = True
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(ROOT_DIR, 'development.sqlite')

class TestingConfig(BaseConfig):
	'Testing environment specific configuration'
	DEBUG = False
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(ROOT_DIR, 'test.sqlite')			
	WTF_CSRF_ENABLED = False

