from flask import Blueprint, request, jsonify
from sqlalchemy import or_, func
from models import *
from auth import *
import constants

jobs_modify = Blueprint("jobs_modify", __name__)

@jobs_modify.route('/<int:jobId>/applications/<int:applicationId>/application_status', methods=['PUT'])
@auth.login_required
def setApplicationStatus(jobId, applicationId):
    try:
        account = auth.current_user()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        
        applicationStatus = request.json.get("status").strip()
        if not applicationStatus:
            return jsonify({"message": "Missing arguments"}), 400

        application = JobApplication.query.filter_by(id=applicationId).first()
        job = Job.query.filter_by(id=jobId).first()
        if not application:
            return jsonify({"error": "Application not found"}), 404
        if not job:
            return jsonify({"error": "Job not found"}), 404
        
        if application.job_id != jobId:
            return jsonify({"error": "Application does not belong to this job"}), 404
        if job.created_by != account.id:
            return jsonify({"error": "Job does not belong to this account"}), 404
        
        application.status = applicationStatus
        db.session.commit()

        notification = Notification(
            account_id = application.account_id,
            message = f"Your application status has been changed to {applicationStatus} for the job {job.address}",
            created_at = application.created_at,
            action = "/job/" + str(jobId)
        )
        db.session.add(notification)
        db.session.commit()

        return jsonify({"message": "Application status updated"}), 200
    except Exception as err:
        event = SystemEvent(
            orginated_at = "jobs_modify_setApplicationStatus",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@jobs_modify.route('/<int:jobId>/applications/<int:workerId>/hired', methods=['PUT'])
@auth.login_required
def setHired(jobId, workerId):
    try:
        account = auth.current_user()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        
        application = JobApplication.query.filter_by(job_id=jobId, account_id=workerId).first()
        job = Job.query.filter_by(id=jobId).first()
        if not application:
            return jsonify({"error": "Application not found"}), 404
        if not job:
            return jsonify({"error": "Job not found"}), 404
        if application.job_id != job.id:
            return jsonify({"error": "Application does not belong to this account"}), 404
        if job.created_by != account.id:
            return jsonify({"error": "Job does not belong to this account"}), 404
        
        application.status = "hired"
        db.session.commit()

        accountJobRelation = AccountJobRelation(
            worker_account_id = workerId,
            poster_account_id = job.created_by,
            job_id = jobId,
            amount = application.quoted_amount,
            currency = job.currency,
            status = "started",
        )
        db.session.add(accountJobRelation)
        db.session.commit()

        notification = Notification(
            account_id = workerId,
            message = f"You have been hired for the job {job.address}",
            created_at = application.created_at,
            action = "/job/" + str(jobId)
        )
        db.session.add(notification)
        db.session.commit()
        
        return jsonify({"message": "Application status updated"}), 200
    
    except Exception as err:
        event = SystemEvent(
            orginated_at = "jobs_modify_setHired",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@jobs_modify.route('/<int:jobId>/markComplete', methods=['PUT'])
@auth.login_required
def markComplete(jobId):
    try:
        account = auth.current_user()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        
        try:
            rating = int(request.json.get("rating"))
            if not rating:
                raise Exception
        except:
            return jsonify({"message": "Missing arguments"}), 400
        
        if not (isinstance(rating, int) or isinstance(rating, float)) or rating < 0 or rating > 5:
            return jsonify({"error": "Invalid rating"}), 400
        job = Job.query.filter_by(id=jobId).first()
        if not job:
            return jsonify({"error": "Job not found"}), 404
        jobRelation = AccountJobRelation.query.filter_by(job_id=jobId, worker_account_id=account.id).first()
        if not jobRelation:
            return jsonify({"error": "Job relation not found"}), 404
        
        jobRelation.worker_rating = rating
        jobRelation.finished_at = datetime.datetime.utcnow()
        jobRelation.duration = (jobRelation.finished_at - jobRelation.created_at).total_seconds()
        jobRelation.status = "completed"

        db.session.commit()

        return jsonify({"message": "Job status updated"}), 200
    except Exception as err:
        event = SystemEvent(
            orginated_at = "jobs_modify_markComplete",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@jobs_modify.route('/<int:jobId>/pay', methods=['PUT'])
@auth.login_required
def pay(jobId):
    try:
        account = auth.current_user()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        
        job = Job.query.filter_by(id=jobId).first()
        if not job:
            return jsonify({"error": "Job not found"}), 404
        jobRelation = AccountJobRelation.query.filter(AccountJobRelation.job_id == jobId, AccountJobRelation.is_paid == False).first()
        if not jobRelation:
            return jsonify({"error": "Job already paid"}), 400
        
        jobRelation.is_paid = True

        db.session.commit()

        return jsonify({"message": "Job status updated"}), 200
    except Exception as err:
        event = SystemEvent(
            orginated_at = "jobs_modify_pay",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@jobs_modify.route('/<int:jobId>/workerRating', methods=['PUT'])
@auth.login_required
def setWorkerRating(jobId):
    try:
        account = auth.current_user()
        if not account:
            return jsonify({"error": "Account not found"}), 404
        
        try:
            rating = int(request.json.get("rating"))
            if not rating:
                raise Exception
        except:
            return jsonify({"message": "Missing arguments"}), 400
        
        if not (isinstance(rating, int) or isinstance(rating, float)) or rating < 0 or rating > 5:
            return jsonify({"error": "Invalid rating"}), 400
        job = Job.query.filter_by(id=jobId).first()
        if not job:
            return jsonify({"error": "Job not found"}), 404
        jobRelation = AccountJobRelation.query.filter_by(job_id=jobId, worker_account_id=account.id).first()
        if not jobRelation:
            return jsonify({"error": "Job relation not found"}), 404
        
        jobRelation.worker_rating = rating

        db.session.commit()

        return jsonify({"message": "Job status updated"}), 200
    except Exception as err:
        event = SystemEvent(
            orginated_at = "jobs_modify_setWorkerRating",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500