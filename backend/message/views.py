from flask import Blueprint, request, jsonify
from sqlalchemy import or_, func
from models import *
from auth import *
import constants

message_views = Blueprint("message_views", __name__)


@message_views.route('/conversations', methods=['GET'])
@auth.login_required
def getConversations():
    try:
        account = auth.current_user()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        
        offset = request.args.get("offset", 0)
        limit = request.args.get("limit", 10)

        try:
            offset = int(offset)
            limit = int(limit)
        except:
            return jsonify({"message": "Missing arguments"}), 400

        converations = Conversation.query.filter(
            or_(
                Conversation.sender_id == account.id,
                Conversation.receiver_id == account.id
            )
        ).order_by(Conversation.created_at.desc()).limit(limit).offset(offset).all()

        return jsonify({
            "conversations": [{
                "id": conversation.id,
                "sender_id": conversation.sender_id,
                "sender": (lambda x: {"id": x.id, "fullname": x.fullname, "username": x.username, "profile_picture": x.profile_picture})(Account.query.filter_by(id=conversation.sender_id).first()),
                "receiver_id": conversation.receiver_id,
                "receiver": (lambda x: {"id": x.id, "fullname": x.fullname, "username": x.username, "profile_picture": x.profile_picture})(Account.query.filter_by(id=conversation.receiver_id).first()),
                "created_at": conversation.created_at,
                "ago": datetime.timedelta(seconds=int((datetime.datetime.utcnow() - conversation.created_at).total_seconds())).total_seconds()
            } for conversation in converations]
        })
    
    except Exception as err:
        event = SystemEvent(
            orginated_at = "messages_views_getConversations",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@message_views.route('/conversations/search/<query>', methods=['POST'])
@auth.login_required
def searchConversations(query):
    try:
        account = auth.current_user()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        
        offset = request.args.get("offset", 0)
        limit = request.args.get("limit", 10)

        try:
            offset = int(offset)
            limit = int(limit)
        except:
            return jsonify({"message": "Missing arguments"}), 400
        
        accounts = Account.query.filter(
            Account.username.like("%{}%".format(query))
        ).limit(limit).offset(offset).all()

        conversations = Conversation.query.filter(
            or_(
                Conversation.sender_id.in_([account.id for account in accounts]),
                Conversation.receiver_id.in_([account.id for account in accounts])
            )
        ).offset(offset).limit(limit).all()

        return {"conversations": [{
                "id": conversation.id,
                "sender_id": conversation.sender_id,
                "sender": (lambda x: {"id": x.id, "fullname": x.fullname, "username": x.username, "profile_picture": x.profile_picture})(Account.query.filter_by(id=conversation.sender_id).first()),
                "receiver_id": conversation.receiver_id,
                "receiver": (lambda x: {"id": x.id, "fullname": x.fullname, "username": x.username, "profile_picture": x.profile_picture})(Account.query.filter_by(id=conversation.receiver_id).first()),
                "created_at": conversation.created_at,
                "ago": datetime.timedelta(seconds=int((datetime.datetime.utcnow() - conversation.created_at).total_seconds())).total_seconds()
            } for conversation in conversations]}, 200
        
    except Exception as err:
        event = SystemEvent(
            orginated_at = "messages_views_searchConversations",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@message_views.route('/conversations/<int:conversationID>/messages', methods=['GET'])
@auth.login_required
def getConversation(conversationID):
    try:
        account = auth.current_user()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        
        offset = request.args.get("offset", 0)
        limit = request.args.get("limit", 10)

        try:
            offset = int(offset)
            limit = int(limit)
        except:
            return jsonify({"message": "Missing arguments"}), 400
        
        conversation = Conversation.query.filter_by(id=conversationID).first()
        if not conversation:
            return jsonify({"error": "Conversation not found"}), 404

        messages = Message.query.filter_by(conversation_id=conversationID).order_by(Message.created_at.desc()).limit(limit).offset(offset).all()

        return jsonify({
            "messages": [{
                "id": message.id,
                "sender_id": message.sender_id,
                "sender": (lambda x: {"id": x.id, "fullname": x.fullname, "username": x.username})((lambda x: x if x else account)(Account.query.filter_by(id=message.sender_id).first())),
                "content": message.message,
                "created_at": message.created_at,
                "is_read": message.is_read
            } for message in messages]
        }), 200

    except Exception as err:
        event = SystemEvent(
            orginated_at = "messages_views_getConversation",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500