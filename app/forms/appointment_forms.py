from flask_wtf import FlaskForm
from wtforms import SelectField, DateTimeLocalField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional, Length

class AppointmentForm(FlaskForm):
    client_id = SelectField("Klijent", coerce=int, validators=[DataRequired()])
    service_id = SelectField("Usluga", coerce=int, validators=[DataRequired()])

    date_time = DateTimeLocalField(
        "Datum i vrijeme",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()]
    )

    status = SelectField(
        "Status",
        choices=[
            ("scheduled", "Scheduled"),
            ("done", "Done"),
            ("canceled", "Canceled"),
        ],
        validators=[DataRequired()]
    )

    note = TextAreaField("Napomena", validators=[Optional(), Length(max=1000)])
    submit = SubmitField("Spremi")
