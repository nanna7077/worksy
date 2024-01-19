from flask_httpauth import HTTPTokenAuth

from models import *
import constants

auth = HTTPTokenAuth(scheme="Bearer", realm=None, header=constants.AUTHENTICATION_HEADER)

@auth.verify_token
def verify_password(sessionkey):
    session = Session.query.filter_by(sessionkey=sessionkey).first()
    if not session or session.expires_at < datetime.datetime.utcnow():
        return False
    account = Account.query.filter_by(id=session.accountID).first()
    if not account or account.isDisabled:
        return False
    return True

@auth.error_handler
def handle401(error):
    return {"error": "UnAuthorized"}, 401

def createSession(accountID, deviceName, IPAddress):
    session = Session(
        accountID=accountID,
        expires_at=datetime.datetime.utcnow() + datetime.timedelta(days=constants.SESSION_EXPIRATION_DAYS),
    )
    db.session.add(session)
    db.session.commit()

    return session.sessionkey

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
