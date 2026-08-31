from flask import Blueprint, render_template, redirect, url_for, flash, request, Response
from flask_login import login_required, current_user

from sqlalchemy import func
from io import StringIO
import csv

from app import db
from app.models import Client, Appointment, Service
from app.forms.client_forms import ClientForm

clients_bp = Blueprint("clients", __name__, url_prefix="/clients")


@clients_bp.get("/")
@login_required
def list_clients():
    q = request.args.get("q", "").strip()
    query = Client.query.filter_by(user_id=current_user.id)

    if q:
        query = query.filter(Client.name.ilike(f"%{q}%"))

    clients = query.order_by(Client.name.asc()).all()
    return render_template("clients/list.html", clients=clients, q=q)


@clients_bp.get("/<int:client_id>")
@login_required
def client_detail(client_id: int):
    client = Client.query.filter_by(id=client_id, user_id=current_user.id).first_or_404()

    # zadnjih 10 termina za tog klijenta (najnoviji prvi)
    last_appts = (
        Appointment.query
        .filter_by(user_id=current_user.id, client_id=client.id)
        .order_by(Appointment.date_time.desc())
        .limit(10)
        .all()
    )

    # agregati: broj termina, potrošeno, minute (bez canceled)
    agg = (
    db.session.query(
        func.coalesce(func.count(Appointment.id), 0),
        func.coalesce(func.sum(Service.price), 0),
        func.coalesce(func.sum(Service.duration_min), 0),
    )
    .select_from(Appointment)  # <-- OVO JE KLJUČNO
    .join(Service, Service.id == Appointment.service_id)
    .filter(Appointment.user_id == current_user.id)
    .filter(Appointment.client_id == client.id)
    .filter(Appointment.status != "canceled")
    .one()
)

    total_appts = int(agg[0] or 0)
    total_spent = float(agg[1] or 0)
    total_minutes = int(agg[2] or 0)

    # mape servisa da u templateu ne radiš dodatne upite
    service_ids = {a.service_id for a in last_appts}
    services = Service.query.filter(Service.id.in_(service_ids)).all() if service_ids else []
    service_map = {s.id: s for s in services}

    return render_template(
        "clients/detail.html",
        client=client,
        last_appts=last_appts,
        service_map=service_map,
        total_appts=total_appts,
        total_spent=total_spent,
        total_minutes=total_minutes,
    )


@clients_bp.route("/new", methods=["GET", "POST"])
@login_required
def create_client():
    form = ClientForm()
    if form.validate_on_submit():
        client = Client(
            name=form.name.data,
            email=form.email.data or None,
            phone=form.phone.data or None,
            user_id=current_user.id,
        )
        db.session.add(client)
        db.session.commit()
        flash("Klijent je dodan ✅", "success")
        return redirect(url_for("clients.list_clients"))

    return render_template("clients/form.html", form=form, title="Novi klijent")


@clients_bp.route("/<int:client_id>/edit", methods=["GET", "POST"])
@login_required
def edit_client(client_id: int):
    client = Client.query.filter_by(id=client_id, user_id=current_user.id).first_or_404()

    form = ClientForm(obj=client)
    if form.validate_on_submit():
        client.name = form.name.data
        client.email = form.email.data or None
        client.phone = form.phone.data or None
        db.session.commit()
        flash("Klijent je ažuriran ✅", "success")
        return redirect(url_for("clients.list_clients"))

    return render_template("clients/form.html", form=form, title="Uredi klijenta")


@clients_bp.post("/<int:client_id>/delete")
@login_required
def delete_client(client_id: int):
    client = Client.query.filter_by(id=client_id, user_id=current_user.id).first_or_404()
    db.session.delete(client)
    db.session.commit()
    flash("Klijent obrisan.", "info")
    return redirect(url_for("clients.list_clients"))


@clients_bp.get("/export")
@login_required
def export_clients_csv():
    clients = Client.query.filter_by(user_id=current_user.id).order_by(Client.name.asc()).all()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "name", "email", "phone"])

    for c in clients:
        writer.writerow([c.id, c.name, c.email or "", c.phone or ""])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=clientra_clients.csv"},
    )
