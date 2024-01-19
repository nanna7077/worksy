from flask import Blueprint, request, jsonify
from models import *
from auth import *
import constants

accounts_create = Blueprint("accounts_create", __name__)


@accounts_create.route("/register", methods=["POST"])
def register():
    try:
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        
        fullname = request.json.get("fullname", None)
        username = request.json.get("username", None)
        email = request.json.get("email", None)
        phone = request.json.get("phone", None)
        password = request.json.get("password", None)
        if not username or not email or not phone or not password:
            return jsonify({"msg": "Missing arguments"}), 400

        if Account.query.filter_by(email=email).first() is not None:
            return jsonify({"msg": "Email already used :("}), 400
        if Account.query.filter_by(phone=phone).first() is not None:
            return jsonify({"msg": "Phone Number is already used. Try resetting your password."}), 400

        account = Account(
            fullname=fullname,
            username=username,
            email=email,
            phone=phone,
            password_hash=sha256(password.encode()).hexdigest(),
        )
        db.session.add(account)
        db.session.commit()
        return jsonify({"msg": "Account created"}), 200
    
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