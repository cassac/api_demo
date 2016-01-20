from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Friend(db.Model):
	__tablename__ = 'friend'
	follower_id = db.Column(db.Integer, db.ForeignKey('user.id'),
					primary_key=True)
	followed_id = db.Column(db.Integer, db.ForeignKey('user.id'),
					primary_key=True)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Follower: %s, Followed: %s>'%(self.follower_id,
			self.followed_id)

class Message(db.Model):
	__tablename__ = 'message'
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(200), nullable=False)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)
	sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	sender = db.relationship('User', backref=db.backref('sent_messages'))
	# recipients =

	def __init__(self, text, sender_id):
		self.text = text
		self.sender_id = sender_id

	def __repr__(self):
		return 'Message(%d): "%s"' %(self.id, self.text[:20])


class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True)
	password_hash = db.Column(db.String(128))
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

	def __init__(self, username):
		self.username = username

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User %s>' % self.username

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