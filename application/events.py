from json import dumps, loads
from flask import (
	request,
	session,
	render_template,
	redirect,
	url_for,
	flash,
)

from . import app, get_db

@app.route('/api/events')
def events():
	# Get all user events
	# [ ] get user id
	# [ ] get all user feeds
	# [ ] get all events with feeds ids
	user_id = 1 # TODO: put id here
	db = get_db()
	cursor = db.cursor()
	# get the user feeds
	feeds_ids = cursor.execute('''
		SELECT FEED_ID FROM SUBSCRIPTIONS WHERE SUBSCRIBER_ID=?
	''', (user_id,))
	# get the events from the selected feeds
	events = []
	for feed_id in feeds_ids:
		events.append(
			cursor.execute('''
				SELECT * FROM EVENTS WHERE FEED_ID=?
			''', feed_id))
	return events