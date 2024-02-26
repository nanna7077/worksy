## Worksy Backend

### Running the application

1. Install the dependencies with `python -m pip install -r requirements.txt` inside a virtual environment.
2. Create the following environment variables:
   1. DATABASE_URL (SQLAlchemy compatible connection string. Recommended to be a postgres database, if not then please install the correct driver for your database)
   2. VERTEX_AI_API_KEY (from https://ai.google.dev/)
3. Initialize the database with 
   ```
   python
   >>> import app
   >>> with app.app.app_context:
   >>>     app.db.create_all()
   >>> exit()
4. Start the application with `python app.py` for development or `python pywsgi.py` for production.
5. [Optional] Link the systemd service file `worksy.service` to /etc/systemd/system/ for automatic startup.


### Debugging the application

The error's from the application will be logged in the `systemevents` table of your database and it's respective event ID will be returned on the error. Please refer to the `SystemEvent` model for more details. On database connection fail, the logging will resort to printing the error on the stderr.