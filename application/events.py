from json import dumps, loads
from flask_login import login_required, current_user
from flask import (
	request,
	session,
	render_template,
	redirect,
	url_for,
	flash,
	abort
)

from . import app, db
from .models import Feed, User, Event
from .forms import CreateFeedForm

@app.route('/feeds', methods=['POST'])
@login_required
def feeds():
	# [ ] does current user has privalage to create a new feed
	# [ ] if not
	if current_user.type != 'Professor':
		abort(403)
	form = CreateFeedForm()
	if form.validate_on_submit():
		feed = Feed(name=form.name.data, owner_id=current_user.id)
		db.session.add(feed)
		db.session.commit()
		flash('Created a new feed')
		return redirect(url_for('feeds'))
	return render_template('feeds.html', form=form)

@app.route('/api/events')
@login_required
def all_user_events():
	# Get all user events
	# [ ] get user id
	# [ ] get all user feeds
	# [ ] get all events with feeds ids
	feed_id = request.args.get('feed_id', None)
	if feed_id is not None:
		feed = Feed.query.filter_by(id=feed_id).first_or_404()
		user = User.query.filter_by(id=feed.owner_id).first()
		if user.id == current_user.id:
			return redirect(url_for('user', user=user))
		current_user.unsubscribe(feed)
		db.session.commit()
		flash('You have unsubscribed from {} feed.'.format(feed.name))
		return 