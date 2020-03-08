from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length
from datetime import date


class BookLibForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    isbn = StringField("ISBN", validators=[DataRequired()])
    purch_date = DateField("Purchase Date", default=date.today, format="%m/%d/%Y")
    notes = TextAreaField("Notes", validators=[Length(max=1024)])
    submit = SubmitField("Save")