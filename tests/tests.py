import unittest
from app import create_app, db
from app.models import User

class TestStringMethods(unittest.TestCase):

	def setUp(self):
		self.app = create_app('config.TestingConfig')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_user_creation(self):
		user = User(username='User1')
		db.session.add(user)
		db.session.commit()
		user = User.query.first()

        # self.assertEqual(user.username, 'User1')


if __name__ == '__main__':
    unittest.main()