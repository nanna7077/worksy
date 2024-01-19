from hashlib import sha256
import string
import random
import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_picture = db.Column(db.String(256), nullable=True, default="https://placehold.jp/150x150.png")
    fullname = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(260), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    sessionkey = db.Column(db.String(256), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(20000), nullable=False)
    occurred_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

class SystemEvent(db.Model):
    __tablename__ = 'systemevents'

    id = db.Column(db.Integer, primary_key=True)
    orginated_at = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    context = db.Column(db.String(20000), nullable=False)
    occured_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    level = db.Column(db.Integer, nullable=False)