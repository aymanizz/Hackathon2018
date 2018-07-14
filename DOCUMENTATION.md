# Documentation

## Choice of Platform

we chose to build a web platform inorder to reach a bigger audience of
college students, professors, and the working staff. It also enables us to
target mobile phone users through the web browser.

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

### Frontend Languages, Frameworks and Libraries

- HTML
- CSS
- Javascript
- FullCalendar.js
- w3css

### Auxiliary

- git

## Running The Server

1. Install all the requirements.
2. Error Logging server:
  open a terminal and run the following command:
    ```bash
    python3 -m smtpd -n -c DebuggingServer localhost:8025
    ```
3. Run the server:
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
4. Open a browser and enter the url: `localhost:5000`

## Main Idea and Concept

We tackled challenge 3 by creating a feeds/events based system.

For students, each has, by default, a single private feed he can edit
and add events to, students are also able to view professors feeds and
subscribe to them as they wish.
Unlike students, professors can create many public feeds, which students
can subscribe to.

The feeds are delivered in a calendar form, so that students and professors
can see all upcoming events (announcements, news, etc) from all feeds.

## Future Work

- Front-end
- Private messages
- Public and private feeds
- Forums
- Chatting