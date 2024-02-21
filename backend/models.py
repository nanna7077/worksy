from hashlib import sha256
import string
import random
import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_picture = db.Column(db.String(256), nullable=True)
    fullname = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(260), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=5)
    open_to_work = db.Column(db.Boolean, default=False, nullable=False)
    last_lat = db.Column(db.Float, nullable=False, default=0)
    last_long = db.Column(db.Float, nullable=False, default=0)
    last_updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class AccountJobRelation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    worker_account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    poster_account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"), nullable=False)
    amount = db.Column(db.Float, nullable=True)
    currency = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(120), nullable=False)
    worker_rating = db.Column(db.Float, nullable=True) # Rating the worker
    poster_rating = db.Column(db.Float, nullable=True, default=5) # Rating the poster
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    finished_at = db.Column(db.DateTime, nullable=True)
    duration = db.Column(db.Float, nullable=True) # In hours


class AccountTagRelation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), nullable=False)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20000), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    long = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(1020), nullable=False)
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    duration_range_start = db.Column(db.Integer, nullable=False)
    duration_range_end = db.Column(db.Integer, nullable=False)
    duration_range_unit = db.Column(db.String(20), nullable=False, default="hours")
    price_range_start = db.Column(db.Integer, nullable=False)
    price_range_end = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(20), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)


class JobTagRelation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), nullable=False)


class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    quoted_amount = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(120), nullable=False)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    sessionkey = db.Column(db.String(256), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    deviceName = db.Column(db.String(256), nullable=True)
    IPAddress = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    message = db.Column(db.String(20000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    action = db.Column(db.String(120), nullable=False)
    is_read = db.Column(db.Boolean, default=False)


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversation.id"), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    message = db.Column(db.String(20000), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
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