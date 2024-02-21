from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from models import *
from auth import *
import constants

notifications_create = Blueprint("notifications_create", __name__)