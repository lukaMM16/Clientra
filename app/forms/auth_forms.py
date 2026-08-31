from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegisterForm(FlaskForm):
    username = StringField("Korisničko ime", validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Lozinka", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Potvrdi lozinku", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Kreiraj račun")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Lozinka", validators=[DataRequired()])
    submit = SubmitField("Prijavi se")
