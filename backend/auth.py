from flask_httpauth import HTTPTokenAuth

from models import *
import constants

auth = HTTPTokenAuth(scheme="Bearer", realm=None, header=constants.AUTHENTICATION_HEADER)

@auth.verify_token
def verify_password(sessionkey):
    try:
        session = Session.query.filter(Session.sessionkey == sessionkey).first()
        if not session or session.expires_at < datetime.datetime.utcnow():
            return None
        return Account.query.filter(Account.id == session.account_id).first()
    except Exception as err:
        return None

@auth.error_handler
def handle401(error):
    return {"error": "UnAuthorized"}, 401

def createSession(accountID, deviceName, IPAddress):
    sessionkey = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(256))
    session = Session(
        account_id=accountID,
        expires_at=datetime.datetime.utcnow() + datetime.timedelta(days=constants.SESSION_EXPIRATION_DAYS),
        deviceName=deviceName,
        IPAddress=IPAddress,
        sessionkey=sessionkey
    )
    db.session.add(session)
    db.session.commit()

    return sessionkey

def getRequestUser(sessionkey):
    requestsession = Session.query.filter_by(sessionkey=sessionkey).first()
    
    if not requestsession:
        return {"error": "Invalid SessionKey"}, 404
    if requestsession.expires_at <= datetime.datetime.now():
        return {"error": "Session Expired"}, 401
    
    requestuser = Account.query.filter_by(id=requestsession.accountID).first()
    if not requestuser:
        return {"error": "Account associated with SessionKey does not exist!"}, 404
    
    return requestuser
