from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime

from app import db
from app.models import Appointment, Client, Service
from app.forms.appointment_forms import AppointmentForm  
from app.utils.emailer import send_email
import csv
from io import StringIO
from flask import Response


appointments_bp = Blueprint("appointments", __name__, url_prefix="/appointments")


def _fill_choices(form: AppointmentForm):
    clients = Client.query.filter_by(user_id=current_user.id).order_by(Client.name.asc()).all()
    services = Service.query.filter_by(user_id=current_user.id).order_by(Service.name.asc()).all()

    form.client_id.choices = [(c.id, c.name) for c in clients]
    form.service_id.choices = [
        (s.id, f"{s.name} ({float(s.price):.2f} € / {s.duration_min} min)") for s in services
    ]
    return clients, services


@appointments_bp.get("/")
@login_required
def list_appointments():
    q = request.args.get("q", "").strip()
    query = Appointment.query.filter_by(user_id=current_user.id)

    if q:
        try:
            dt = datetime.fromisoformat(q)
            query = query.filter(Appointment.date_time >= dt)
        except Exception:
            query = query.filter(Appointment.status.ilike(f"%{q}%"))

    appts = query.order_by(Appointment.date_time.desc()).all()

    clients = Client.query.filter_by(user_id=current_user.id).all()
    services = Service.query.filter_by(user_id=current_user.id).all()
    client_map = {c.id: c for c in clients}
    service_map = {s.id: s for s in services}

    return render_template(
        "appointments/list.html",
        appts=appts,
        q=q,
        client_map=client_map,
        service_map=service_map,
    )


@appointments_bp.route("/new", methods=["GET", "POST"])
@login_required
def create_appointment():
    form = AppointmentForm()
    clients, services = _fill_choices(form)

    if not clients or not services:
        flash("Prvo dodaj barem jednog klijenta i jednu uslugu.", "info")
        return redirect(url_for("main.home"))

    if form.validate_on_submit():
        appt = Appointment(
            user_id=current_user.id,
            client_id=form.client_id.data,
            service_id=form.service_id.data,
            date_time=form.date_time.data,
            status=form.status.data,
            note=form.note.data or None,
        )
        db.session.add(appt)
        db.session.commit()

        # ---- OBICNI MAIL (ako je konfiguriran + klijent ima email) ----
        client = Client.query.filter_by(id=appt.client_id, user_id=current_user.id).first()
        service = Service.query.filter_by(id=appt.service_id, user_id=current_user.id).first()

        if client and client.email:
            subject = "Clientra - Potvrda termina"
            body = (
                f"Pozdrav {client.name},\n\n"
                f"Termin je uspješno zakazan:\n"
                f"- Usluga: {service.name if service else '-'}\n"
                f"- Datum/Vrijeme: {appt.date_time.strftime('%d.%m.%Y %H:%M')}\n"
                f"- Status: {appt.status}\n\n"
                f"Hvala!\nClientra"
            )
            send_email(client.email, subject, body)
        # -------------------------------------------------------------

        flash("Termin je dodan ✅", "success")
        return redirect(url_for("appointments.list_appointments"))

    return render_template("appointments/form.html", form=form, title="Novi termin")


@appointments_bp.route("/<int:appt_id>/edit", methods=["GET", "POST"])
@login_required
def edit_appointment(appt_id: int):
    appt = Appointment.query.filter_by(id=appt_id, user_id=current_user.id).first_or_404()

    form = AppointmentForm(obj=appt)
    clients, services = _fill_choices(form)

    if not clients or not services:
        flash("Nedostaju klijenti ili usluge. Dodaj ih prvo.", "danger")
        return redirect(url_for("appointments.list_appointments"))

    if form.validate_on_submit():
        appt.client_id = form.client_id.data
        appt.service_id = form.service_id.data
        appt.date_time = form.date_time.data
        appt.status = form.status.data
        appt.note = form.note.data or None
        db.session.commit()

        flash("Termin je ažuriran ✅", "success")
        return redirect(url_for("appointments.list_appointments"))

    return render_template("appointments/form.html", form=form, title="Uredi termin")


@appointments_bp.post("/<int:appt_id>/delete")
@login_required
def delete_appointment(appt_id: int):
    appt = Appointment.query.filter_by(id=appt_id, user_id=current_user.id).first_or_404()
    db.session.delete(appt)
    db.session.commit()

    flash("Termin obrisan.", "info")
    return redirect(url_for("appointments.list_appointments"))

@appointments_bp.get("/export")
@login_required
def export_appointments_csv():
    appts = Appointment.query.filter_by(user_id=current_user.id).order_by(Appointment.date_time.desc()).all()

    # mape za naziv klijenta/usluge
    clients = Client.query.filter_by(user_id=current_user.id).all()
    services = Service.query.filter_by(user_id=current_user.id).all()
    client_map = {c.id: c for c in clients}
    service_map = {s.id: s for s in services}

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "date_time", "client", "service", "status", "note"])

    for a in appts:
        client_name = client_map[a.client_id].name if a.client_id in client_map else ""
        service_name = service_map[a.service_id].name if a.service_id in service_map else ""
        writer.writerow([
            a.id,
            a.date_time.strftime("%Y-%m-%d %H:%M"),
            client_name,
            service_name,
            a.status,
            a.note or "",
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=clientra_appointments.csv"},
    )

