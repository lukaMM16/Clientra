from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ServiceForm(FlaskForm):
    name = StringField("Naziv usluge", validators=[DataRequired(), Length(min=2, max=120)])
    price = DecimalField("Cijena (€)", places=2, validators=[DataRequired(), NumberRange(min=0)])
    duration_min = IntegerField("Trajanje (min)", validators=[DataRequired(), NumberRange(min=5, max=600)])
    submit = SubmitField("Spremi")
