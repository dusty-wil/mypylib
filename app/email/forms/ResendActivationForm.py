from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email


class ResendActivationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    send = SubmitField("Send")





