from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Optional(strip_whitespace=True)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=16)])

    remember = BooleanField("Remember Me")
    login = SubmitField("Log In")
