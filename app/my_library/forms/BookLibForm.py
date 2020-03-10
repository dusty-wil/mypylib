from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from datetime import date


class BookLibForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=255), Optional(strip_whitespace=True)])
    author = StringField("Author", validators=[DataRequired(), Length(max=64), Optional(strip_whitespace=True)])
    isbn = StringField("ISBN", validators=[DataRequired(), Length(max=16), Optional(strip_whitespace=True)])
    purch_date = DateField("Purchase Date", default=date.today, format="%m/%d/%Y")
    notes = TextAreaField("Notes", validators=[Length(max=1024), Optional(strip_whitespace=True)])
    submit = SubmitField("Save")

    def validate_isbn(self, isbn):
        if not isbn.data.isnumeric():
            raise ValidationError("The ISBN is invalid or is not numeric")
