from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app import db
from app.models import User
from app.forms.auth_forms import RegisterForm, LoginForm

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.get("/register")
@auth_bp.post("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RegisterForm()
    if form.validate_on_submit():
        existing_email = User.query.filter_by(email=form.email.data.lower()).first()
        if existing_email:
            flash("Email je već registriran.", "danger")
            return render_template("auth/register.html", form=form)

        existing_username = User.query.filter_by(username=form.username.data).first()
        if existing_username:
            flash("Korisničko ime je zauzeto.", "danger")
            return render_template("auth/register.html", form=form)

        user = User(
            username=form.username.data,
            email=form.email.data.lower(),
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Račun je kreiran! Sad se možeš prijaviti.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)

@auth_bp.get("/login")
@auth_bp.post("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if not user or not user.check_password(form.password.data):
            flash("Neispravan email ili lozinka.", "danger")
            return render_template("auth/login.html", form=form)

        login_user(user)
        flash("Uspješna prijava ✅", "success")

        next_page = request.args.get("next")
        return redirect(next_page or url_for("main.home"))

    return render_template("auth/login.html", form=form)

@auth_bp.get("/logout")
@login_required
def logout():
    logout_user()
    flash("Odjavljen si.", "info")
    return redirect(url_for("main.home"))
