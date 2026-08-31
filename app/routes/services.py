from flask import Blueprint, render_template, redirect, url_for, flash, request, Response
from flask_login import login_required, current_user
from sqlalchemy import exists

from app import db
from app.models import Service, Appointment
from app.forms.service_forms import ServiceForm

import csv
from io import StringIO


services_bp = Blueprint("services", __name__, url_prefix="/services")


@services_bp.get("/")
@login_required
def list_services():
    q = request.args.get("q", "").strip()
    query = Service.query.filter_by(user_id=current_user.id)

    if q:
        query = query.filter(Service.name.ilike(f"%{q}%"))

    services = query.order_by(Service.name.asc()).all()
    return render_template("services/list.html", services=services, q=q)


@services_bp.route("/new", methods=["GET", "POST"])
@login_required
def create_service():
    form = ServiceForm()
    if form.validate_on_submit():
        service = Service(
            name=form.name.data,
            price=form.price.data,
            duration_min=form.duration_min.data,
            user_id=current_user.id,
        )
        db.session.add(service)
        db.session.commit()
        flash("Usluga je dodana ✅", "success")
        return redirect(url_for("services.list_services"))

    return render_template("services/form.html", form=form, title="Nova usluga")


@services_bp.route("/<int:service_id>/edit", methods=["GET", "POST"])
@login_required
def edit_service(service_id: int):
    service = Service.query.filter_by(id=service_id, user_id=current_user.id).first_or_404()

    form = ServiceForm(obj=service)
    if form.validate_on_submit():
        service.name = form.name.data
        service.price = form.price.data
        service.duration_min = form.duration_min.data
        db.session.commit()
        flash("Usluga je ažurirana ✅", "success")
        return redirect(url_for("services.list_services"))

    return render_template("services/form.html", form=form, title="Uredi uslugu")


@services_bp.post("/<int:service_id>/delete")
@login_required
def delete_service(service_id: int):
    service = Service.query.filter_by(id=service_id, user_id=current_user.id).first_or_404()

    in_use = db.session.query(
        exists().where(
            (Appointment.user_id == current_user.id) &
            (Appointment.service_id == service.id)
        )
    ).scalar()

    if in_use:
        flash("Ne mogu obrisati uslugu jer postoji termin koji ju koristi. Prvo obriši termine.", "danger")
        return redirect(url_for("services.list_services"))

    db.session.delete(service)
    db.session.commit()
    flash("Usluga obrisana.", "info")
    return redirect(url_for("services.list_services"))


@services_bp.get("/export")
@login_required
def export_services_csv():
    services = Service.query.filter_by(user_id=current_user.id).order_by(Service.name.asc()).all()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "name", "price", "duration_min"])

    for s in services:
        writer.writerow([s.id, s.name, f"{float(s.price):.2f}", s.duration_min])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=clientra_services.csv"},
    )
