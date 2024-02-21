from flask import Blueprint, request, jsonify
from models import *
from auth import *
import constants

message_create = Blueprint("message_create", __name__)

@message_create.route('/conversation/new', methods=['POST'])
@auth.login_required
def createConversation():
    try:
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400

        receiver_id = request.json.get("receiver_id")
        receiver_username = request.json.get("receiver_username")
        if receiver_id:
            receiver = Account.query.filter_by(id=receiver_id).first()
        elif receiver_username:
            receiver = Account.query.filter_by(username=receiver_username).first()
        else:
            return jsonify({"message": "Missing arguments"}), 400

        if not receiver:
            return jsonify({"error": "Receiver not found"}), 404
        
        conversation = Conversation.query.filter_by(
            sender_id=auth.current_user().id,
            receiver_id=receiver.id
        ).first() or Conversation.query.filter_by(
            sender_id=receiver.id,
            receiver_id=auth.current_user().id
        ).first()

        if conversation:
            return jsonify({"message": "Conversation already exists", "conversation": {
                "id": conversation.id,
                "sender_id": conversation.sender_id,
                "sender": (lambda x: {"id": x.id, "fullname": x.fullname, "username": x.username})((lambda x: x if x else None)(Account.query.filter_by(id=conversation.sender_id).first())),
                "receiver_id": conversation.receiver_id,
                "receiver": (lambda x: {"id": x.id, "fullname": x.fullname, "username": x.username})((lambda x: x if x else None)(Account.query.filter_by(id=conversation.receiver_id).first())),
                "created_at": conversation.created_at
            }}), 400
                
        conversation = Conversation(
            sender_id=auth.current_user().id,
            receiver_id=receiver.id
        )

        db.session.add(conversation)
        db.session.commit()

        return jsonify({
            "conversation": {
                "id": conversation.id,
                "sender_id": conversation.sender_id,
                "sender": (lambda x: {"id": x.id, "fullname": x.fullname, "username": x.username})((lambda x: x if x else None)(Account.query.filter_by(id=conversation.sender_id).first())),
                "receiver_id": conversation.receiver_id,
                "receiver": (lambda x: {"id": x.id, "fullname": x.fullname, "username": x.username})((lambda x: x if x else auth.current_user())(Account.query.filter_by(id=conversation.receiver_id).first())),
                "created_at": conversation.created_at
            }}), 200

    except Exception as err:
        event = SystemEvent(
            orginated_at = "message_create_createConversation",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@message_create.route('/conversation/<int:conversationID>/new', methods=['POST'])
@auth.login_required
def createMessage(conversationID):
    try:
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        
        content = request.json.get("content", "")
        conversation = Conversation.query.filter_by(id=conversationID).first()
        
        if not content:
            return jsonify({"message": "Missing arguments"}), 400
        if not conversation:
            return jsonify({"error": "Conversation not found"}), 404
        if len(content) > 19999:
            return jsonify({"message": "Message too long"}), 400
        
        message = Message(
            conversation_id=conversationID,
            sender_id=auth.current_user().id,
            message=content,
        )

        db.session.add(message)
        db.session.commit()

        return jsonify({
            "message": {
                "id": message.id,
                "sender_id": message.sender_id,
                "content": message.message,
                "created_at": message.created_at,
                "is_read": message.is_read
            }}), 200

    except Exception as err:
        event = SystemEvent(
            orginated_at = "message_create_createMessage",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500