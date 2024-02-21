from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from models import *
from auth import *
import constants

notifications_modify = Blueprint("notifications_modify", __name__)


@notifications_modify.route('/markRead', methods=['POST'])
@auth.login_required
def markRead():
    try:
        account = auth.current_user()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        notificationId = request.args.get("notificationId", None)

        if not notificationId:
            return jsonify({"message": "Missing arguments"}), 400

        notification = Notification.query.filter_by(id=notificationId).first()
        if not notification:
            return jsonify({"message": "Notification not found"}), 404
        notification.is_read = True
        db.session.commit()

        return jsonify({"message": "Notification marked as read"}), 200

    except Exception as err:
        event = SystemEvent(
            orginated_at = "notifications_modify_markRead",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500