import os

from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, get_key

from accounts import create as accounts_create
from accounts import views as accounts_views
from accounts import modify as accounts_modify

from jobs import create as jobs_create
from jobs import views as jobs_views
from jobs import modify as jobs_modify

from search import views as search_views

from notifications import create as notifications_create
from notifications import views as notifications_views
from notifications import modify as notifications_modify

from message import create as messages_create
from message import views as messages_views
from message import modify as messages_modify

import common

load_dotenv()

from models import *
import constants

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(40)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 => MB
uri = os.getenv(
    "DATABASE_URL", "sqlite:///database"
)  # Use sqlite3 database in testing and get the database URI from the env for production.
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app=app)

db.init_app(app)


@app.route("/")
def index():
    """
    Hello World Index Page
    """
    return {"message": "Hello World!"}, 200


@app.errorhandler(Exception)
def handle_exception(error):
    if isinstance(error, HTTPException):
        return {"error": error.description}, error.code
    return {"error": str(error)}, 500

app.register_blueprint(accounts_create.accounts_create, url_prefix="/accounts/create")
app.register_blueprint(accounts_views.accounts_views, url_prefix="/accounts/view")
app.register_blueprint(accounts_modify.accounts_modify, url_prefix="/accounts/update")

app.register_blueprint(jobs_create.jobs_create, url_prefix="/jobs/create")
app.register_blueprint(jobs_views.jobs_views, url_prefix="/jobs/view")
app.register_blueprint(jobs_modify.jobs_modify, url_prefix="/jobs/update")

app.register_blueprint(search_views.search_views, url_prefix="/search")

app.register_blueprint(notifications_create.notifications_create, url_prefix="/notifications/create")
app.register_blueprint(notifications_views.notifications_views, url_prefix="/notifications/view")
app.register_blueprint(notifications_modify.notifications_modify, url_prefix="/notifications/update")

app.register_blueprint(messages_create.message_create, url_prefix="/messages/create")
app.register_blueprint(messages_views.message_views, url_prefix="/messages/view")
app.register_blueprint(messages_modify.message_modify, url_prefix="/messages/update")

app.register_blueprint(common.common, url_prefix="/common")

if __name__ == "__main__":
    # Run app for testing
    app.run(debug=True, host="0.0.0.0")
