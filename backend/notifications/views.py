from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from models import *
from auth import *
import constants

notifications_views = Blueprint("notifications_views", __name__)

@notifications_views.route('/count', methods=['GET'])
@auth.login_required
def getNotificationsCount():
    try:
        account = auth.current_user()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        
        notifications = Notification.query.filter_by(account_id=account.id, is_read=False).all()

        return jsonify({
            "count": len(notifications)
        }), 200


    except Exception as err:
        event = SystemEvent(
            orginated_at = "notifications_views_getNotificationsCount",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@notifications_views.route('/read', methods=['GET'])
@auth.login_required
def readNotifications():
    try:
        account = auth.current_user()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        
        notifications = Notification.query.filter_by(account_id=account.id, is_read=False).all()

        return jsonify({
            "notifications": [
                {
                    "id": notification.id,
                    "message": notification.message,
                    "created_at": notification.created_at,
                    "ago": notification.created_at
                } for notification in notifications
            ]
        }), 200


    except Exception as err:
        event = SystemEvent(
            orginated_at = "notifications_views_readNotifications",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@notifications_views.route('/unread', methods=['GET'])
@auth.login_required
def unreadNotifications():
    try:
        account = auth.current_user()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        
        notifications = Notification.query.filter_by(account_id=account.id, is_read=True).all()

        return jsonify({
            "notifications": [
                {
                    "id": notification.id,
                    "message": notification.message,
                    "created_at": notification.created_at,
                    "ago": notification.created_at
                } for notification in notifications
            ]
        }), 200


    except Exception as err:
        event = SystemEvent(
            orginated_at = "notifications_views_unreadNotifications",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500