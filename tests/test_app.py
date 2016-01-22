import unittest
from flask import current_app, url_for
from app import create_app, db
from app.models import User

# Run all tests in individual module
#python manage.py test -t test_app.TestApp

# Run specific test in individual module
#python manage.py test -t test_app.TestApp.test_direct_user_creation

class TestApp(unittest.TestCase):

	def setUp(self):
		self.app = create_app('config.TestingConfig')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_app_exists(self):
		self.assertFalse(current_app is None)

	def test_app_is_testing(self):
		self.assertTrue(current_app.config['TESTING'])

	def test_direct_user_creation(self):
		user = User(username='User1')
		db.session.add(user)
		db.session.commit()
		user = User.query.first()
		self.assertTrue(user.username, 'User1')


if __name__ == '__main__':
    unittest.main()