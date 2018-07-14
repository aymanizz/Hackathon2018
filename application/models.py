from datetime import datetime, date

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from . import db

subscribers = db.Table('subscribers',
	db.Column('subscriber_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('feed_id', db.Integer, db.ForeignKey('feed.id'))
)

class Feed(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True)
	owner_id = db.Column(
		db.Integer, db.ForeignKey('user.id'), index=True)

	def __repr__(self):
		return '<Feed {}>'.format(self.name)

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	type = db.Column(db.Integer)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), unique=True)
	password_hash = db.Column(db.String(128))
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)
	about_me = db.Column(db.String(140))
	subscriptions = db.relationship(
		'Feed', secondary=subscribers,
		primaryjoin=(subscribers.c.subscriber_id == id),
		secondaryjoin=(subscribers.c.feed_id == Feed.id),
		backref=db.backref('subscribers', lazy='dynamic'), lazy='dynamic')
	
	def set_password(self, new_password):
		self.password_hash = generate_password_hash(new_password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def subscribe(self, feed):
		if not self.is_subscribed(feed):
			self.subscriptions.append(feed)

	def unsubscribe(self, feed):
		if self.is_subscribed(feed):
			self.subscriptions.remove(feed)

	def is_subscribed(self, feed):
		return self.subscriptions.filter(
			subscribers.c.feed_id == feed.id).count() > 0

	def subscribed_events(self):
		return Event.query.join(
			subscribers, (subscribers.c.feed_id == Event.feed_id)).filter(
				subscribers.c.subscriber_id == self.id
				and Event.start_month == date.today().month).order_by(
					Event.start_day.desc())

	def __repr__(self):
		return '<User {}>'.format(self.username)


class Event(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	feed_id = db.Column(
		db.Integer, db.ForeignKey('feed.id'), index=True)
	title = db.Column(db.String(120), unique=True)
	description = db.Column(db.String(256), unique=True)
	# YYYY:MM:DD HH:MM:SS
	start_day = db.Column(db.DateTime, index=True)
	start_month = db.Column(db.DateTime, index=True)
	end_day = db.Column(db.DateTime, index=True)
	end_month = db.Column(db.DateTime, index=True)

	def __repr__(self):
		return "<Event [title: {}, desc: {}]>".format(self.title, self.description)


# class Student(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)

# 	def __repr__(self):
# 		return '<Student {}>'.format(self.id)


# class Professor(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)

# 	def __repr__(self):
# 		return '<Professor {}>'.format(self.id)