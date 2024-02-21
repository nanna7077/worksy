from flask import Blueprint, request, jsonify
from sqlalchemy import or_, func
from models import *
from auth import *
import constants

accounts_views = Blueprint("accounts_views", __name__)

@accounts_views.route('/<int:accountID>', methods=['GET'])
@auth.login_required
def getAccount(accountID):
    try:
        account = Account.query.filter_by(id=accountID).first()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        
        account_ = {
            "id": account.id,
            "fullname": account.fullname,
            "username": account.username,
            "profile_picture": account.profile_picture,
            "created_at": account.created_at,
            "is_available": account.is_available,
            "rating": account.rating,
            "open_to_work": account.open_to_work,
            "price_average": db.session.query(func.avg(AccountJobRelation.amount / AccountJobRelation.duration)).filter_by(id=account.id).scalar() or "Not Available",
            "is_self": account.id == auth.current_user().id,
            "ago": datetime.timedelta(seconds=int((datetime.datetime.utcnow() - account.created_at).total_seconds())).total_seconds(),
            "tags": [
                (lambda tag: {"id": tag.id, "name": tag.name})(Tag.query.filter_by(id=x.tag_id).first()) for x in AccountTagRelation.query.filter_by(account_id = account.id)
            ],

            "receiver_id": account.id,
            "receiver": {"id": account.id, "fullname": account.fullname, "username": account.username, "profile_picture": account.profile_picture}
        }

        if account_["is_self"]:
            try:
                lat, long = float(request.args.get("lat")), float(request.args.get("long"))
                account.last_lat, account.last_long, account.last_updated_at = lat, long, datetime.datetime.utcnow()
                db.session.commit()
            except:
                pass
            account_["email"] = account.email
            account_["phone"] = account.phone

        return jsonify({
            "account": account_
        })

    except Exception as err:
        event = SystemEvent(
            orginated_at = "accounts_views_getAccount",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500


@accounts_views.route('/self', methods=['GET'])
@auth.login_required
def getAccount_self():
    try:
        account = auth.current_user()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        
        try:
            lat, long = float(request.args.get("lat")), float(request.args.get("long"))
            account.last_lat, account.last_long, account.last_updated_at = lat, long, datetime.datetime.utcnow()
            db.session.commit()
        except:
            pass
        
        return jsonify({
            "account": {
                "id": account.id,
                "fullname": account.fullname,
                "username": account.username,
                "email": account.email,
                "phone": account.phone,
                "profile_picture": account.profile_picture,
                "created_at": account.created_at,
                "is_available": account.is_available,
                "rating": account.rating,
                "open_to_work": account.open_to_work,
                "price_average": db.session.query(func.avg(AccountJobRelation.amount / AccountJobRelation.duration)).filter_by(id=account.id).scalar() or "Not Available",
                "tags": [
                    (lambda tag: {"id": tag.id, "name": tag.name})(Tag.query.filter_by(id=x.tag_id).first()) for x in AccountTagRelation.query.filter_by(account_id = account.id)
                ]
            }
        })

    except Exception as err:
        event = SystemEvent(
            orginated_at = "accounts_views_getAccount_self",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@accounts_views.route('/search', methods=['GET'])
@auth.login_required
def searchAccounts():
    try:
        account = auth.current_user()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        
        query = request.args.get("query", "")
        offset = request.args.get("offset", 0)
        limit = request.args.get("limit", 10)

        try:
            offset = int(offset)
            limit = int(limit)
        except:
            return jsonify({"message": "Missing arguments"}), 400

        accounts = Account.query.filter(
            Account.username.like("%{}%".format(query)),
            Account.is_available == True,
            Account.id != account.id
        ).order_by(Account.rating.desc(), Account.last_updated_at.desc()).limit(limit).offset(offset).all()

        return jsonify({
            "accounts": [{
                "id": account.id,
                "fullname": account.fullname,
                "username": account.username,
                "profile_picture": account.profile_picture,
                
                "receiver_id": account.id,
                "receiver": {"id": account.id, "fullname": account.fullname, "username": account.username, "profile_picture": account.profile_picture}
            } for account in accounts]
        })

    except Exception as err:
        event = SystemEvent(
            orginated_at = "accounts_views_searchAccounts",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500