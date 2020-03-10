from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Optional


class RequestPasswordResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Optional(strip_whitespace=True)])
    submit = SubmitField("Request Reset")
