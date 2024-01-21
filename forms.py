from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,HiddenField, TextField
from wtforms.validators import InputRequired,Length


class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(),Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired(),Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(),Length(max=30)])
    email = StringField("Email",validators=[InputRequired(),Length(max=50)])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(),Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm (FlaskForm):
   
    tittle = StringField("Tittle", validators=[InputRequired(),Length(max=100)])
    content =TextField("Content", validators=[InputRequired(),Length(max=100)])

    




