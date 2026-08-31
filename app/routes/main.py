from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime, date, time
import requests

from app import db
from app.models import Client, Service, Appointment

main_bp = Blueprint("main", __name__)


def _minutes_to_label(total_minutes: int) -> str:
    total_minutes = int(total_minutes or 0)
    h = total_minutes // 60
    m = total_minutes % 60
    if h > 0 and m > 0:
        return f"{h} h {m} min"
    if h > 0:
        return f"{h} h"
    return f"{m} min"


def _get_weather_zagreb():
    """
    Open-Meteo (bez API ključa). Ako pukne, vrati None i stranica i dalje radi.
    """
    try:
        lat, lon = 45.8150, 15.9819  # Zagreb
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&current_weather=true"
            "&timezone=Europe%2FZagreb"
        )
        r = requests.get(url, timeout=6)
        r.raise_for_status()
        data = r.json()

        cw = data.get("current_weather") or {}
        return {
            "city": "Zagreb",
            "time": cw.get("time"),
            "temperature": cw.get("temperature"),
            "windspeed": cw.get("windspeed"),
        }
    except Exception:
        return None


@main_bp.get("/")
@login_required
def home():
    now = datetime.now()

    # counts
    clients_count = Client.query.filter_by(user_id=current_user.id).count()
    services_count = Service.query.filter_by(user_id=current_user.id).count()
    appts_count = Appointment.query.filter_by(user_id=current_user.id).count()

    # danas
    start_today = datetime.combine(date.today(), time.min)
    end_today = datetime.combine(date.today(), time.max)
    today_count = (
        Appointment.query
        .filter(Appointment.user_id == current_user.id)
        .filter(Appointment.date_time >= start_today, Appointment.date_time <= end_today)
        .count()
    )

    # najbliži termini
    upcoming = (
        Appointment.query
        .filter(Appointment.user_id == current_user.id)
        .filter(Appointment.date_time >= now)
        .order_by(Appointment.date_time.asc())
        .limit(5)
        .all()
    )

    # ===== FINANCIJE + SATI RADA (JOIN na Service) =====
    # ukupno (svi termini koji imaju service_id)
    total_rows = (
        db.session.query(Appointment, Service)
        .join(Service, Appointment.service_id == Service.id)
        .filter(Appointment.user_id == current_user.id)
        .all()
    )
    total_revenue = 0.0
    for appt, service in total_rows:
        total_revenue += float(service.price or 0)

    # ovaj mjesec
    month_start = datetime(now.year, now.month, 1)
    if now.month == 12:
        month_end = datetime(now.year + 1, 1, 1)
    else:
        month_end = datetime(now.year, now.month + 1, 1)

    month_rows = (
        db.session.query(Appointment, Service)
        .join(Service, Appointment.service_id == Service.id)
        .filter(Appointment.user_id == current_user.id)
        .filter(Appointment.date_time >= month_start, Appointment.date_time < month_end)
        .all()
    )

    month_revenue = 0.0
    month_minutes = 0
    for appt, service in month_rows:
        month_revenue += float(service.price or 0)
        month_minutes += int(service.duration_min or 0)

    month_hours_label = _minutes_to_label(month_minutes)

    # weather
    weather = _get_weather_zagreb()

    return render_template(
        "home.html",
        clients_count=clients_count,
        services_count=services_count,
        appts_count=appts_count,
        today_count=today_count,
        upcoming=upcoming,
        total_revenue=total_revenue,
        month_revenue=month_revenue,
        month_hours_label=month_hours_label,
        weather=weather,
    )
