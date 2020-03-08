from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, TextAreaField
from wtforms.validators import Length
from datetime import date


class LibEntryForm(FlaskForm):
    purch_date = DateField("Purchase Date", default=date.today, format="%m/%d/%Y")
    notes = TextAreaField("Notes", validators=[Length(max=1024)])
    submit = SubmitField("Save")
