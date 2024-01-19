import os

from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, get_key

from accounts import create as accounts_create

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

db.init_app(app)


@app.route("/")
def index():
    """
    Hello World Index Page
    """
    return {"message": "Hello World!"}, 200


app.register_blueprint(accounts_create.accounts_create)


if __name__ == "__main__":
    # Run app for testing
    app.run(debug=True, host="0.0.0.0")
