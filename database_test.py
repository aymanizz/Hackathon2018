from datetime import datetime, timedelta
import unittest
from application import app, db
from application.models import User, Event, Feed

class UserModelCase(unittest.TestCase):
	def setUp(self):
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_password_hashing(self):
		u = User(username='susan')
		u.set_password('cat')
		self.assertFalse(u.check_password('dog'))
		self.assertTrue(u.check_password('cat'))

	def test_subscribe(self):
		u1 = User(username='john', email='john@example.com')
		u2 = User(username='susan', email='susan@example.com')
		f = Feed(name='susan_feed', owner_id=u2.id)
		db.session.add(u1)
		db.session.add(u2)
		db.session.add(f)
		db.session.commit()
		self.assertEqual(u1.subscriptions.all(), [])
		self.assertEqual(u2.subscriptions.all(), [])

		u1.subscribe(f)
		db.session.commit()
		self.assertTrue(u1.is_subscribed(f))
		self.assertEqual(u1.subscriptions.count(), 1)
		self.assertEqual(u1.subscriptions.first().name, 'susan_feed')
		self.assertEqual(f.subscribers.count(), 1)
		self.assertEqual(f.subscribers.first().username, 'john')

		u1.unsubscribe(f)
		db.session.commit()
		self.assertFalse(u1.is_subscribed(f))
		self.assertEqual(u1.subscriptions.count(), 0)
		self.assertEqual(f.subscribers.count(), 0)

if __name__ == '__main__':
	unittest.main(verbosity=2)