# Documentation

## Requirements

### Backend Languages, Frameworks and Plugins

- Python 3
- Flask
  - WTForms
  - WTF-Forms
  - Flask-Login
  - Flask-Migrate
  - Flask-SQLAlchemy
  - Jinja2
- Linux OS: **not mandatory** but you will have to edit the commands in
  section *Running The Server* to use your OS commands.

### Frontend Languages, Frameworks and Libraries

- HTML
- CSS
- Javascript
- FullCalendar.js
- w3css

## Running The Server

1. Error Logging server:
  open a terminal and run the following command:
    ```bash
    python3 -m smtpd -n -c DebuggingServer localhost:8025
    ```
2. Run the server:
  open another terminal and from the project root folder
  (WHEREVER_THE_PROJECT_IS_LOCATED/ABC/) run the following commands:
    ```bash
    export MAIL_SERVER=localhost
    export MAIL_PORT=8025
    export FLASK_APP=run.py
    export FLASK_DEBUG=0
    export SQLALCHEMY_DATABASE_URI='/model/database.db'
    flask run
    ```
3. Open a browser and enter the url: `localhost:5000`

## Main Idea and Concept

We tackled challenge 3 by creating a feeds/events based system.

For students, each has, by default, a single private feed he can edit
and add events to, students are also able to view professors feeds and
subscribe to them as they wish.
Unlike students, professors can create many public feeds, which students
can subscribe to.

The feeds are delivered in a calendar form, so that students and professors
can see all upcoming events (announcements, news, etc) from all feeds
seemlessly.

## Future Work

- private messages
- public and private feeds
- forums
- chatting