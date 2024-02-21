from flask import Blueprint, request, jsonify
from models import *
from auth import *
import constants

from currencymap import CURRENCY_MAP

common = Blueprint("common", __name__)

@common.route('/currencies', methods=['GET'])
def getCurrencies():
    return jsonify(CURRENCY_MAP), 200