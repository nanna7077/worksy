from flask import Blueprint, request, jsonify
from models import *
from auth import *
import constants
from .functions import *
import dotenv
import os
import google.generativeai as genai

genai_views = Blueprint("genai_views", __name__)

VERTEX_AI_API_KEY = os.getenv("VERTEX_AI_API_KEY") or dotenv.get_key(key_to_get="VERTEX_AI_API_KEY", dotenv_path=".env")

# llm = VertexAI(temperature=0, model_name="text-bison@001", location="us-central1", key=VERTEX_AI_API_KEY)

genai.configure(api_key=VERTEX_AI_API_KEY)
model = genai.GenerativeModel('gemini-pro', tools=[actions])

chats = {}

@genai_views.route('/conversation', methods=['GET'])
def newConversation():
    global chats

    # try:
    sessionkey = request.headers.get(constants.AUTHENTICATION_HEADER)
    if not sessionkey:
        sessionkey = None
    else:
        sessionkey = sessionkey.lstrip("Bearer ")

    question = request.args.get("question", None)
    contextID = request.args.get("context", hash(datetime.datetime.now().timestamp()))
    if contextID != None:
        contextID = int(contextID)
    if not question:
        return jsonify({"message": "Missing arguments"}), 400
    
    
    if contextID in chats:
        chat = chats[contextID]['chat']
        sessionkey = chats[contextID]['sessionkey']
    else:
        chat = model.start_chat()
        chats[contextID] = {'chat': chat, 'sessionkey': sessionkey}

    if sessionkey:
        response = chat.send_message(f"{question} with sessionkey {sessionkey} for request without logging in again.")
    else:
        response = chat.send_message(question)
    fc = response.candidates[0].content.parts[0].function_call
    try:
        r_ = response.text
    except:
        if fc.name == "login":
            if sessionkey:
                if Session.query.filter(Session.sessionkey == sessionkey).first():
                    if Account.query.filter_by(id=Session.query.filter(Session.sessionkey == sessionkey).first().account_id).first():
                        chats[contextID]['sessionkey'] = sessionkey
                        chats.update({contextID: chats[contextID]})
                        chats=chats
                        return {"response": "Login successful", "context": contextID}
                    else:
                        Session.query.filter(Session.sessionkey == sessionkey).delete()
                        return {"response": "Invalid SessionKey"}, 404
                else:
                    return {"response": "Invalid SessionKey"}, 404
            result = login(fc.args['username'], fc.args['password'])
            sessionkey = None
            if Account.query.filter_by(username=fc.args['username']).first():
                if sha256(fc.args['password'].encode()).hexdigest() == Account.query.filter_by(username=fc.args['username']).first().password_hash:
                    sessionkey = createSession(Account.query.filter_by(username=fc.args['username']).first().id, request.headers.get("User-Agent"), constants.getClientIPAddress(request))
                    chats[contextID]['sessionkey'] = sessionkey
                    chats.update({contextID: chats[contextID]})
                    chats=chats
                    return {"response": "Login successful", "context": contextID}
                else:
                    return {"response": "Wrong password"}, 400
            else:
                return {"response": "No account with that username"}, 400
        elif fc.name == "register":
            result = register(fc.args['fullname'], fc.args['username'], fc.args['password'], fc.args['email'], fc.args['phone'])
        elif fc.name == "view_self_account":
            result = view_self_account(fc.args['sessionkey'])
        elif fc.name == "view_another_account":
            result = view_another_account(fc.args['sessionkey'], fc.args['accountID'])
        elif fc.name == "search_accounts_by_query":
            result = search_accounts_by_query(fc.args['sessionkey'], fc.args['query'])
        elif fc.name == "toggle_open_to_work":
            result = set_open_to_work(fc.args['sessionkey'])
        elif fc.name == "view_all_skills":
            result = view_all_skills(fc.args['sessionkey'])
        elif fc.name == "add_skill":
            result = add_skill(fc.args['sessionkey'], fc.args['tagID'])
        elif fc.name == "remove_skill":
            result = remove_skill(fc.args['sessionkey'], fc.args['tagID'])
        elif fc.name == "list_jobs":
            result = list_jobs(fc.args['sessionkey'])
        else:
            return {"response": "Something went wrong"}, 400
        response = chat.send_message(
            glm.Content(
                parts = [ glm.Part(
                    function_response = glm.FunctionResponse(
                        name=fc.name,
                        response={'result': result}
                    )
                )]
            )
        )
    return {"response": "".join(response.candidates[0].content.parts[0].text), "context": contextID}

    # except Exception as err:
    #     event = SystemEvent(
    #         orginated_at = "genai_views_conversation",
    #         description = str(err),
    #         context = str(request),
    #         level=constants.SystemEventType.ERROR.value
    #     )
    #     db.session.add(event)
    #     db.session.commit()
    #     return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500