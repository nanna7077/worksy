from flask import Blueprint, request, jsonify
from models import *
from auth import *
from hashlib import md5
import constants

accounts_create = Blueprint("accounts_create", __name__)


@accounts_create.route("/register", methods=["POST"])
def register():
    try:
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        
        fullname = request.json.get("fullName", None)
        username = request.json.get("username", None)
        email = request.json.get("email", None)
        phone = request.json.get("phone", None)
        password = request.json.get("password", None)
        if not username or not email or not phone or not password or not fullname:
            return jsonify({"message": "Missing arguments"}), 400

        if Account.query.filter_by(email=email).first() is not None:
            return jsonify({"message": "Email already used :("}), 400
        if Account.query.filter_by(phone=phone).first() is not None:
            return jsonify({"message": "Phone Number is already used. Try resetting your password."}), 400
        if Account.query.filter_by(username=username).first() is not None:
            return jsonify({"message": "Username already used :("}), 400

        account = Account(
            fullname=fullname,
            username=username,
            email=email,
            phone=phone,
            profile_picture=f"https://www.gravatar.com/avatar/{md5(email.lower().encode()).hexdigest()}?",
            password_hash=sha256(password.encode()).hexdigest(),
        )
        db.session.add(account)

        db.session.commit()
        return jsonify({"message": "Account created"}), 200
    
    except Exception as err:
        event = SystemEvent(
            orginated_at = "accounts_create_register",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500


@accounts_create.route("/login", methods=["POST"])
def login():
    try:
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        if not username or not password:
            return jsonify({"message": "Missing arguments"}), 400

        account = Account.query.filter_by(username=username).first()
        if account is None:
            return jsonify({"message": "No account with that username"}), 400
        if sha256(password.encode()).hexdigest() != account.password_hash:
            return jsonify({"message": "Wrong password"}), 400

        sessionkey = createSession(account.id, request.headers.get("User-Agent"), constants.getClientIPAddress(request))
        return jsonify({"sessionkey": sessionkey}), 200

    except Exception as err:
        event = SystemEvent(
            orginated_at = "accounts_create_login",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500