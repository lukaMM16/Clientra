from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from datetime import datetime

from sqlalchemy import func

from app import db
from app.models import Appointment, Client, Service

api_bp = Blueprint("api", __name__, url_prefix="/api")


# ---------------------------
# APPOINTMENTS API
# ---------------------------
@api_bp.get("/appointments")
@login_required
def api_appointments():
    status = request.args.get("status")
    date_from = request.args.get("from")
    date_to = request.args.get("to")

    query = Appointment.query.filter_by(user_id=current_user.id)

    if status:
        query = query.filter(Appointment.status == status)

    if date_from:
        try:
            dt_from = datetime.fromisoformat(date_from)
            query = query.filter(Appointment.date_time >= dt_from)
        except ValueError:
            pass

    if date_to:
        try:
            dt_to = datetime.fromisoformat(date_to)
            query = query.filter(Appointment.date_time <= dt_to)
        except ValueError:
            pass

    appointments = query.order_by(Appointment.date_time.asc()).all()

    data = []
    for a in appointments:
        client = Client.query.get(a.client_id)
        service = Service.query.get(a.service_id)

        data.append({
            "id": a.id,
            "date_time": a.date_time.isoformat(),
            "status": a.status,
            "note": a.note,
            "client": {
                "id": client.id,
                "name": client.name,
                "email": client.email,
                "phone": client.phone,
            } if client else None,
            "service": {
                "id": service.id,
                "name": service.name,
                "price": float(service.price),
                "duration_min": service.duration_min,
            } if service else None,
        })

    return jsonify({
        "count": len(data),
        "results": data,
    })


# ---------------------------
# SUMMARY / DASHBOARD API
# ---------------------------
@api_bp.get("/summary")
@login_required
def api_summary():
    clients_count = Client.query.filter_by(user_id=current_user.id).count()
    services_count = Service.query.filter_by(user_id=current_user.id).count()
    appointments_count = Appointment.query.filter_by(user_id=current_user.id).count()

    # financije (bez canceled)
    q = (
        db.session.query(
            func.coalesce(func.sum(Service.price), 0),
            func.coalesce(func.sum(Service.duration_min), 0),
        )
        .select_from(Appointment)
        .join(Service, Service.id == Appointment.service_id)
        .filter(Appointment.user_id == current_user.id)
        .filter(Appointment.status != "canceled")
    )

    total_revenue, total_minutes = q.one()

    hours = int(total_minutes or 0) // 60
    mins = int(total_minutes or 0) % 60

    return jsonify({
        "clients": clients_count,
        "services": services_count,
        "appointments": appointments_count,
        "revenue_total": float(total_revenue or 0),
        "work_time": {
            "hours": hours,
            "minutes": mins,
            "label": f"{hours} h {mins} min",
        }
    })
