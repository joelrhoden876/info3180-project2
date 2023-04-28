from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])
    firstname = StringField("First Name", validators=[InputRequired()])
    lastname = StringField("Last Name", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    location = StringField("Location", validators=[InputRequired()])
    biography = TextAreaField("Biography", validators=[InputRequired()])
    profile = FileField("Profile", validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])

class PostForm(FlaskForm):
    photo = FileField("Photo", validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    caption = TextAreaField("Caption", validators=[InputRequired()])