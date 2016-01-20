import unittest
from app import db
from app.models import User

class TestStringMethods(unittest.TestCase):

    def test_user_creation(self):
        user = User(username='User1')
        db.session.add(user)
        db.session.commit()
        user = User.query.first()
        self.assertEqual(user.username, 'User1')


if __name__ == '__main__':
    unittest.main()