# Documentation

## Requirements

- Python 3
- Flask
  - WTForms
  - WTF-Forms
  - Flask-Login
- FullCalendar
- Linux OS: **not mandatory** but you will have to edit the commands in section *Running The Server* to use your OS commands.

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