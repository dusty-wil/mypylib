from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Optional


class ShareLibraryForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Optional(strip_whitespace=True)])
    send = SubmitField("Send")
