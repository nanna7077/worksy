from flask import Blueprint, request, jsonify
from models import *
from auth import *
import constants

jobs_create = Blueprint("jobs_create", __name__)

@jobs_create.route('/new', methods=['POST'])
@auth.login_required
def createJob():
    try:
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        
        selectedTags = request.json.get("tags", [])
        description = request.json.get("description", "")
        address = request.json.get("address", "")
        position = request.json.get("position", {"latitude": None, "longitude": None})
        duration_range_start = request.json.get("duration_range_start", 0)
        duration_range_end = request.json.get("duration_range_end", 0)
        duration_range_unit = request.json.get("duration_range_unit", 'hours')
        price_currency = request.json.get("price_currency", 'INR')
        price_range_start = request.json.get("price_range_start", 0)
        price_range_end = request.json.get("price_range_end", 0)

        account = auth.current_user()

        if len(selectedTags) == 0 or not description or not address or not position or not duration_range_start or not duration_range_end or not duration_range_unit or not price_currency or not price_range_start or not price_range_end:
            return jsonify({"message": "Missing arguments"}), 400
        if not account:
            return jsonify({"error": "Account not found"}), 404

        job = Job(
            description=description,
            lat=int(position["latitude"]),
            long=int(position["longitude"]),
            address=address,
            is_available=True,
            duration_range_start=int(duration_range_start),
            duration_range_end=int(duration_range_end),
            duration_range_unit=duration_range_unit,
            price_range_start=int(price_range_start),
            price_range_end=int(price_range_end),
            currency=price_currency,
            created_by=account.id
        )
        db.session.add(job)
        db.session.commit()

        for tag in selectedTags:
            jobTag = JobTagRelation(
                job_id=job.id,
                tag_id=tag['id']
            )
            db.session.add(jobTag)
        db.session.commit()

        for account in Account.query.filter(
            Account.is_available == True,
            Account.open_to_work == True,
            Account.last_lat.between(job.lat - 0.5, job.lat + 0.5),
            Account.last_long.between(job.long - 0.5, job.long + 0.5)
        ).all():
            notification = Notification(
                account_id=account.id,
                message=f"New job available: {job.description}",
                created_at=datetime.datetime.utcnow(),
                action="/job/{job_id}".format(job_id=job.id)
            )
            db.session.add(notification)
            db.session.commit()

        return jsonify({"message": "Job created"}), 200

    except Exception as err:
        event = SystemEvent(
            orginated_at = "jobs_create_createJob",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500

@jobs_create.route('/apply', methods=['POST'])
@auth.login_required
def applyJob():
    try:
        job_id = request.args.get("jobId", None)
        quoted_amount = request.args.get("quoted_amount", None)
        if not job_id:
            return jsonify({"message": "Missing arguments"}), 400
        if not Job.query.filter_by(id=job_id).first():
            return jsonify({"message": "Job not found"}), 404
        if not quoted_amount and quoted_amount >= 0:
            return jsonify({"message": "Missing arguments"}), 400
        
        account = auth.current_user()
        if not account:
            return jsonify({"error": "Account not found"}), 404

        job = Job.query.filter_by(id=job_id).first()
        
        if not job.is_available:
            return jsonify({"message": "Job not available"}), 400
        
        jobapplication = JobApplication(
            job_id=job_id,
            account_id=account.id,
            status="pending_view",
            quoted_amount=quoted_amount
        )
        db.session.add(jobapplication)
        db.session.commit()

        return jsonify({"message": "Job applied"}), 200

    except Exception as err:
        event = SystemEvent(
            orginated_at = "jobs_create_applyJob",
            description = str(err),
            context = str(request),
            level=constants.SystemEventType.ERROR.value
        )
        db.session.add(event)
        db.session.commit()
        return {"error": f"Unhandled exception encountered. Please report to Admin with error ID {event.id}"}, 500