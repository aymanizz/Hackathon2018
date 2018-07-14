from flask_wtf import FlaskForm
from wtforms import (
	StringField, PasswordField, BooleanField, TextAreaField, SubmitField,
	DateField, SelectField)
from wtforms.validators import (
	DataRequired, Email, EqualTo, ValidationError, Length)

from . import app
from .models import User, Feed


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField(
		'Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
	submit = SubmitField('Save')

	def __init__(self, original_username, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.original_username = original_username

	def validate_username(self, username):
		if username.data != self.original_username:
			user = User.query.filter_by(username=self.username.data).first()
			if user is not None:
				raise ValidationError('Please use a different username.')


class CreateFeedForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	submit = SubmitField('Create Feed')

	def validate_name(self, name):
		feed = Feed.query.filter_by(name=self.name.data).first()
		if feed is not None:
			raise ValidationError('A feed with this name already exists.')


class CreateEventForm(FlaskForm):
	title = StringField('Title',
		validators=[DataRequired(), Length(max=120)])
	start_date = DateField('Start Date', validate=[DataRequired()])
	end_date = DateField('End Date', validators=[DataRequired()])
	description = StringField('Description',
		validators=[Length(min=0, max=256)])
	feed = StringField('Add to Feed', validators=[''])
	submit = SubmitField('Create Event')

	def validate_name(self, name):
		feed = Feed.query.filter_by(id=self.name.data).first()
		if feed is not None:
			raise ValidationError('A feed with this name already exists.')