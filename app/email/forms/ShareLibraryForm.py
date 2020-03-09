from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class ShareLibraryForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    send = SubmitField("Send")
