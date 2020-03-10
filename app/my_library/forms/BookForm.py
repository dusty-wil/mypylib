from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional, Length


class BookForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=255), Optional(strip_whitespace=True)])
    author = StringField("Author", validators=[DataRequired(), Length(max=64), Optional(strip_whitespace=True)])
    submit = SubmitField("Save")
