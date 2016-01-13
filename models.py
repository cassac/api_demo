from datetime import datetime
from app import db

class Friend(db.Model):
	__tablename__ = 'friends'
	follower_id = db.Column(db.Integer, db.ForeignKey('user.id'),
					primary_key=True)
	followed_id = db.Column(db.Integer, db.ForeignKey('user.id'),
					primary_key=True)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Follower: %s, Followed: %s>'%(self.follower_id,
			self.followed_id)


class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True)
	followed = db.relationship('Friend',
								foreign_keys=[Friend.follower_id],
								backref=db.backref('follower', lazy='joined'),
								lazy='dynamic',
								cascade='all, delete-orphan')
	followers = db.relationship('Friend',
								foreign_keys=[Friend.followed_id],
								backref=db.backref('followed', lazy='joined'),
								lazy='dynamic',
								cascade='all, delete-orphan')

	def follow(self, user):
		if user not in self.followed.all():
			f = Friend(follower=self, followed=user)
			db.session.add(f)
			db.session.commit()

	def unfollow(self, user):
		f = self.followed.filter_by(followed_id=user.id).first()
		if f:
			f = self.followed.filter_by(followed_id=user.id).first()
			db.session.delete(f)
			db.session.commit()

	def is_following(self, user):
		return self.followed.filter_by(
			followed_id=user.id).first() is not None

	def is_followed_by(self, user):
		return self.followers.filter_by(
			follower_id=user.id).first() is not None

	def __init__(self, username):
		self.username = username

	def __repr__(self):
		return '<User %s>' % self.username

