from flask import Blueprint, request, jsonify
from sqlalchemy import or_, func
from models import *
from auth import *
import constants

jobs_views = Blueprint("jobs_views", __name__)

@jobs_views.route('/tags/list/all', methods=['GET'])
def getTags():
    try:
        tags = Tag.query.all()
        
        return jsonify({
            "tags": [{"name": tag.name, "id": tag.id} for tag in tags]
        })
    except Exception as err:
        event = SystemEvent(
            orginated_at = "jobs_views_getTags",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@jobs_views.route('/selfposted/list/all', methods=['GET'])
@auth.login_required
def get_self_posted_jobs():
    try:
        account = auth.current_user()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        jobs = Job.query.filter_by(created_by=account.id).all()
        
        return jsonify({
            "jobs": [{
                "id": job.id,
                "description": job.description,
                "lat": job.lat,
                "long": job.long,
                "address": job.address,
                "currency": job.currency,
                "price_range_start": job.price_range_start,
                "price_range_end": job.price_range_end,
                "duration_range_start": job.duration_range_start,
                "duration_range_end": job.duration_range_end,
                "duration_range_unit": job.duration_range_unit,
                "is_available": job.is_available,
                "created_at": job.created_at,
                "applications": JobApplication.query.filter_by(job_id = job.id).count(),
                "is_hired": JobApplication.query.filter_by(job_id = job.id, status="hired").first() != None,
                "is_paid": (lambda x: x.is_paid if x else True)(AccountJobRelation.query.filter_by(job_id = job.id, is_paid=False).first()),
                "tags": [
                    (lambda tag: {"id": tag.id, "name": tag.name})(Tag.query.filter_by(id=x.tag_id).first()) for x in JobTagRelation.query.filter_by(job_id = job.id)
                ]
            } for job in jobs][::-1]
        })

    except Exception as err:
        event = SystemEvent(
            orginated_at = "jobs_views_get_self_posted_jobs",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@jobs_views.route('/list/by/boundary', methods=['POST'])
@auth.login_required
def getJobsByBoundary():
    try:
        account = auth.current_user()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        
        mapsCurrentBounds = request.get_json().get("mapsCurrentBounds")
        if not mapsCurrentBounds:
            return jsonify({"message": "Missing arguments"}), 400
        
        # Filter jobs by professional tags for associated account
        jobs = Job.query.filter(
                Job.lat.between(mapsCurrentBounds["sw"]["lat"], mapsCurrentBounds["ne"]["lat"]),
                Job.long.between(mapsCurrentBounds["sw"]["lng"], mapsCurrentBounds["ne"]["lng"]),
                Job.is_available == True
        ).order_by(Job.created_at.desc()).limit(10).all()
        
        return jsonify({
            "jobs": [{
                "id": job.id,
                "lat": job.lat,
                "long": job.long,
                "currency": job.currency,
                "price_range_start": job.price_range_start,
                "price_range_end": job.price_range_end,
                "duration_range_start": job.duration_range_start,
                "duration_range_end": job.duration_range_end,
                "duration_range_unit": job.duration_range_unit,
                "ago": datetime.timedelta(seconds=int((datetime.datetime.utcnow() - job.created_at).total_seconds())).total_seconds(),
            } for job in jobs][::-1]
        })
    except Exception as err:
        event = SystemEvent(
            orginated_at = "jobs_views_getJobsByBoundary",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@jobs_views.route('/list/by/radius', methods=['GET'])
@auth.login_required
def getJobsByRadius():
    try:
        account = auth.current_user()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        
        radius = request.args.get("radius", constants.DEFAULT_LIST_RADIUS)
        lat = request.args.get("lat")
        long = request.args.get("long")

        try:
            if not lat or not long:
                raise Exception
            radius = float(radius)
            lat = float(lat if lat else account.last_lat)
            long = float(long if long else account.last_long)
        except Exception as err:
            print(err)
            return jsonify({"message": "Missing arguments"}), 400
        
        modlat, modlong = constants.haversine_add_distance_to_coordinates(lat, long, radius)
        jobs = Job.query.filter(
            or_(
                Job.lat.between(lat, modlat),
                Job.long.between(long, modlong),
                Job.lat.between(-modlat, lat),
                Job.long.between(-modlong, long)
            ),
            Job.is_available == True
        ).order_by(Job.created_at.desc()).limit(10).all()

        return jsonify({
            "jobs": [{
                "id": job.id,
                "currency": job.currency,
                "address": job.address,
                "price_range_start": job.price_range_start,
                "price_range_end": job.price_range_end,
                "duration_range_start": job.duration_range_start,
                "duration_range_end": job.duration_range_end,
                "duration_range_unit": job.duration_range_unit,
                "ago": datetime.timedelta(seconds=int((datetime.datetime.utcnow() - job.created_at).total_seconds())).total_seconds(),
            } for job in jobs][::-1]
        })


    except Exception as err:
        event = SystemEvent(
            orginated_at = "jobs_views_getJobsByRadius",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@jobs_views.route('/<int:jobId>', methods=['GET'])
@auth.login_required
def getJobById(jobId):
    try:
        account = auth.current_user()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        job = Job.query.filter_by(id=jobId).first()
        if not job:
            return jsonify({"error": "Job not found"}), 404
        
        job_ = {
            "id": job.id,
            "description": job.description,
            "address": job.address,
            "is_available": job.is_available,
            "created_at": job.created_at,
            "created_by": Account.query.filter_by(id=job.created_by).first().username,
            "lat": job.lat,
            "long": job.long,
            "currency": job.currency,
            "price_range_start": job.price_range_start,
            "price_range_end": job.price_range_end,
            "duration_range_start": job.duration_range_start,
            "duration_range_end": job.duration_range_end,
            "duration_range_unit": job.duration_range_unit,
            "ago": datetime.timedelta(seconds=int((datetime.datetime.utcnow() - job.created_at).total_seconds())).total_seconds(),
            "tags": [(lambda tag: {"name": tag.name, "id": tag.id})(Tag.query.filter_by(id=tag_.tag_id).first()) for tag_ in JobTagRelation.query.filter_by(job_id=job.id).all()],
            "rating": db.session.query(func.avg(AccountJobRelation.poster_rating)).filter_by(worker_account_id=job.created_by).scalar() or 5.0,
        }

        if account.open_to_work:
            job_["applied"] = JobApplication.query.filter_by(job_id=job.id, account_id=account.id).first()

        return jsonify({
            "job": job_
        })

    except Exception as err:
        event = SystemEvent(
            orginated_at = "jobs_views_getJobById",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@jobs_views.route('/history/previous_jobs')
@auth.login_required
def getPreviousJobs():
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

        prevjobs = AccountJobRelation.query.filter_by(worker_account_id=account.id).order_by(AccountJobRelation.created_at.desc(), AccountJobRelation.status).limit(limit).offset(offset).all()

        return jsonify({
            "prevJobs": [{
                "id": job.id,
                "worker": (lambda x: {"id": x.id, "username": x.username, "fullname": x.fullname, "profile_picture": x.profile_picture, "rating": x.rating} if x else None)(Account.query.filter_by(id=job.worker_account_id).first()),
                "poster": (lambda x: {"id": x.id, "username": x.username, "fullname": x.fullname, "profile_picture": x.profile_picture, "rating": x.rating} if x else None)(Account.query.filter_by(id=job.poster_account_id).first()),
                "job":( lambda job_: {
                    "id": job_.id,
                    "description": job_.description,
                    "address": job_.address,
                    "is_available": job_.is_available,
                    "created_at": job_.created_at,
                    "created_by": Account.query.filter_by(id=job_.created_by).first().username,
                    "lat": job_.lat,
                    "long": job_.long,
                    "currency": job_.currency,
                    "price_range_start": job_.price_range_start,
                    "price_range_end": job_.price_range_end,
                    "duration_range_start": job_.duration_range_start,
                    "duration_range_end": job_.duration_range_end,
                    "duration_range_unit": job_.duration_range_unit,
                    "ago": datetime.timedelta(seconds=int((datetime.datetime.utcnow() - job_.created_at).total_seconds())).total_seconds(),
                })(Job.query.filter_by(id=job.job_id).first()),
                "amount": job.amount,
                "currency": job.currency,
                "status": job.status,
                "worker_rating": job.worker_rating,
                "poster_rating": job.poster_rating,
                "created_at": job.created_at,
                "finished_at": job.finished_at,
                "duration": job.duration,
                "is_paid": job.is_paid,
                "ago": datetime.timedelta(seconds=int((datetime.datetime.utcnow() - job.created_at).total_seconds())).total_seconds(),
            } for job in prevjobs]
        })
        
    except Exception as err:
        event = SystemEvent(
            orginated_at = "jobs_views_getPreviousJobs",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@jobs_views.route('/history/applications')
@auth.login_required
def getApplications():
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

        applications = JobApplication.query.filter_by(account_id=account.id).order_by(JobApplication.created_at.desc(), JobApplication.status).limit(limit).offset(offset).all()

        return jsonify({
            "applications": [{
                "id": application.id,
                "created_at": application.created_at,
                "status": application.status.replace("_", " ").title(),
                "quoted_amount": application.quoted_amount,
                "job":( lambda job_: {
                    "id": job_.id,
                    "description": job_.description,
                    "address": job_.address,
                    "is_available": job_.is_available,
                    "created_at": job_.created_at,
                    "created_by": Account.query.filter_by(id=job_.created_by).first().username,
                    "lat": job_.lat,
                    "long": job_.long,
                    "currency": job_.currency,
                    "price_range_start": job_.price_range_start,
                    "price_range_end": job_.price_range_end,
                    "duration_range_start": job_.duration_range_start,
                    "duration_range_end": job_.duration_range_end,
                    "duration_range_unit": job_.duration_range_unit,
                    "ago": datetime.timedelta(seconds=int((datetime.datetime.utcnow() - job_.created_at).total_seconds())).total_seconds(),
                })(Job.query.filter_by(id=application.job_id).first()),
            } for application in applications]
        })

    except Exception as err:
        event = SystemEvent(
            orginated_at = "jobs_views_getApplications",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@jobs_views.route('/<int:jobID>/applications')
@auth.login_required
def getJobApplications(jobID):
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

        applications = JobApplication.query.filter_by(job_id=jobID).order_by(JobApplication.quoted_amount.desc(), JobApplication.status, JobApplication.created_at.desc()).limit(limit).offset(offset).all()

        return jsonify({
            "applications": [{
                "id": application.id,
                "quoted_amount": application.quoted_amount,
                "created_at": application.created_at,
                "status": application.status.replace("_", " ").title(),
                "ago": datetime.timedelta(seconds=int((datetime.datetime.utcnow() - application.created_at).total_seconds())).total_seconds(),
                "applicant":( lambda account_: {
                    "id": account_.id,
                    "fullname": account_.fullname,
                    "username": account_.username,
                    "profile_picture": account_.profile_picture
                })(Account.query.filter_by(id=application.account_id).first()),
            } for application in applications]
        })


    except Exception as err:
        event = SystemEvent(
            orginated_at = "jobs_views_getJobApplications",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500