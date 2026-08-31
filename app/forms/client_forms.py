from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp


class ClientForm(FlaskForm):
    name = StringField(
        "Ime i prezime",
        validators=[
            DataRequired(message="Ime je obavezno."),
            Length(min=2, max=120, message="Ime mora imati 2–120 znakova."),
        ],
    )

    email = StringField(
        "Email",
        validators=[
            Optional(),
            Email(message="Unesi ispravan email."),
            Length(max=120, message="Email može imati najviše 120 znakova."),
        ],
    )

    phone = StringField(
        "Telefon",
        validators=[
            Optional(),
            Length(max=15, message="Telefon može imati najviše 15 znamenki."),
            Regexp(r"^[0-9]*$", message="Telefon smije sadržavati samo brojeve."),
        ],
    )

    submit = SubmitField("Spremi")
        
