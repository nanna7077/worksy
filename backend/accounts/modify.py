from flask import Blueprint, request, jsonify
from models import *
from auth import *
import constants

accounts_modify = Blueprint("accounts_modify", __name__)

@accounts_modify.route('/visibility/<int:visibilityType>', methods=['PUT'])
@auth.login_required
def setVisibility(visibilityType):
    try:
        account = auth.current_user()
        account.is_available = (visibilityType == 1)
        db.session.commit()

        return jsonify({"message": "Visibility updated"}), 200
    except Exception as err:
        event = SystemEvent(
            orginated_at = "accounts_modify_setVisibility",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@accounts_modify.route('/fullname', methods=['PUT'])
@auth.login_required
def setFullname():
    try:
        account = auth.current_user()
        fullname = request.json.get("fullname", None)
        if not fullname:
            return jsonify({"message": "Missing arguments"}), 400
        account.fullname = fullname
        db.session.commit()

        return jsonify({"message": "Fullname updated"}), 200
    except Exception as err:
        event = SystemEvent(
            orginated_at = "accounts_modify_setFullname",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@accounts_modify.route('/email', methods=['PUT'])
@auth.login_required
def setEmail():
    try:
        account = auth.current_user()
        email = request.json.get("email", None)
        if not email:
            return jsonify({"message": "Missing arguments"}), 400
        account.email = email
        db.session.commit()

        return jsonify({"message": "Email updated"}), 200
    except Exception as err:
        event = SystemEvent(
            orginated_at = "accounts_modify_setEmail",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@accounts_modify.route('/phone', methods=['PUT'])
@auth.login_required
def setPhone():
    try:
        account = auth.current_user()
        phone = request.json.get("phone", None)
        if not phone:
            return jsonify({"message": "Missing arguments"}), 400
        account.phone = phone
        db.session.commit()

        return jsonify({"message": "Phone updated"}), 200
    except Exception as err:
        event = SystemEvent(
            orginated_at = "accounts_modify_setPhone",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@accounts_modify.route('/password', methods=['PUT'])
@auth.login_required
def setPassword():
    try:
        account = auth.current_user()
        password = request.json.get("password", None)
        if not password:
            return jsonify({"message": "Missing arguments"}), 400
        account.password_hash = sha256(password.encode()).hexdigest()
        db.session.commit()

        return jsonify({"message": "Password updated"}), 200
    except Exception as err:
        event = SystemEvent(
            orginated_at = "accounts_modify_setPassword",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@accounts_modify.route('/open_to_work', methods=['PUT'])
@auth.login_required
def setOpenToWork():
    try:
        account = auth.current_user()
        account.open_to_work = not account.open_to_work
        db.session.commit()

        return jsonify({"message": "Open to work updated"}), 200
    except Exception as err:
        event = SystemEvent(
            orginated_at = "accounts_modify_setOpenToWork",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@accounts_modify.route('/tags/add', methods=['POST'])
@auth.login_required
def addTag():
    try:
        account = auth.current_user()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        tagId = request.json.get("tagId", None)

        if not tagId:
            return jsonify({"message": "Missing arguments"}), 400

        accountTagRelation = AccountTagRelation(account_id=account.id, tag_id=tagId)
        db.session.add(accountTagRelation)
        db.session.commit()

        return jsonify({"message": "Tag added"}), 200

    except Exception as err:
        event = SystemEvent(
            orginated_at = "accounts_modify_addTag",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500


@accounts_modify.route('/tags/remove', methods=['POST'])
@auth.login_required
def removeTag():
    try:
        account = auth.current_user()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        tagId = request.json.get("tagId", None)

        if not tagId:
            return jsonify({"message": "Missing arguments"}), 400

        accountTagRelation = AccountTagRelation.query.filter_by(account_id=account.id, tag_id=tagId).first()
        if not accountTagRelation:
            return jsonify({"message": "Tag not found"}), 404
        db.session.delete(accountTagRelation)
        db.session.commit()

        return jsonify({"message": "Tag removed"}), 200

    except Exception as err:
        event = SystemEvent(
            orginated_at = "accounts_modify_removeTag",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500