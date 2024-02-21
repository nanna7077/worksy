from flask import Blueprint, request, jsonify
from sqlalchemy import or_, func
from models import *
from auth import *
import constants

search_views = Blueprint("search_views", __name__)

@search_views.route('/jobs', methods=['GET'])
@auth.login_required
def searchJobs():
    try:
        account = auth.current_user()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        
        query = request.args.get("query", "")
        lat = request.args.get("lat")
        long = request.args.get("long")
        offset = request.args.get("offset", 0)
        
        try:
            lat, long = float(lat), float(long)
        except:
            return jsonify({"error": "Missing arguments"}), 400

        jobs = Job.query.filter(
            or_(
                Job.address.like("%{}%".format(query)),
                Job.description.like("%{}%".format(query)),
                Job.id.in_(
                    JobTagRelation.query
                    .filter_by(tag_id = (lambda x: x.id if x else -1)(Tag.query.filter(Tag.name.like("%{}%".format(query))).first()))
                    .with_entities(JobTagRelation.job_id)
                )
            ),
            Job.is_available == True
        ).order_by(Job.created_at.desc(), Job.lat - lat, Job.long - long).limit(constants.DEFAULT_SEARCH_LIMIT).offset(offset).all()

        jobs = sorted(jobs, key=lambda job: Account.query.filter_by(id=job.created_by).first().rating, reverse=True)

        return jsonify({
            "jobs": [{
                "id": job.id,
                "address": job.address,
                "currency": job.currency,
                "price_range_start": job.price_range_start,
                "price_range_end": job.price_range_end,
                "duration_range_start": job.duration_range_start,
                "duration_range_end": job.duration_range_end,
                "duration_range_unit": job.duration_range_unit,
                "is_available": job.is_available,
                "created_at": job.created_at,
                "rating": db.session.query(func.avg(AccountJobRelation.poster_rating)).filter_by(worker_account_id=job.created_by).scalar() or 5.0,
                "tags": [
                    (lambda tag: {"id": tag.id, "name": tag.name})(Tag.query.filter_by(id=x.tag_id).first()) for x in JobTagRelation.query.filter_by(job_id = job.id)
                ],
                "ago": datetime.timedelta(seconds=int((datetime.datetime.utcnow() - job.created_at).total_seconds())).total_seconds(),
            } for job in jobs][::-1]
        })
    except Exception as err:
        event = SystemEvent(
            orginated_at = "search_views_searchJobs",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@search_views.route('/workers', methods=['GET'])
@auth.login_required
def searchWorkers():
    try:
        account = auth.current_user()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        
        query = request.args.get("query", "")
        lat = request.args.get("lat")
        long = request.args.get("long")
        offset = request.args.get("offset", 0)
        
        try:
            lat, long = float(lat), float(long)
        except:
            return jsonify({"error": "Missing arguments"}), 400

        workers = Account.query.filter(
            Account.username.like("%{}%".format(query)),
            Account.is_available == True,
            Account.open_to_work == True
        ).order_by(Account.rating.desc(), Account.last_lat - lat, Account.last_long - long).limit(constants.DEFAULT_SEARCH_LIMIT).offset(offset).all()

        return jsonify({
            "workers": [{
                "id": worker.id,
                "fullname": worker.fullname,
                "username": worker.username,
                "profile_picture": worker.profile_picture,
                "created_at": worker.created_at,
                "is_available": worker.is_available,
                "rating": worker.rating,
                "price_average": db.session.query(func.avg(AccountJobRelation.amount / AccountJobRelation.duration)).filter_by(worker_account_id=worker.id).scalar() or "Not Available",
                "tags": [
                    (lambda tag: {"id": tag.id, "name": tag.name})(Tag.query.filter_by(id=x.tag_id).first()) for x in AccountTagRelation.query.filter_by(account_id = worker.id)
                ],
                "ago": datetime.timedelta(seconds=int((datetime.datetime.utcnow() - worker.created_at).total_seconds())).total_seconds(),
            } for worker in workers][::-1]
        })

    except Exception as err:
        event = SystemEvent(
            orginated_at = "search_views_searchWorkers",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500