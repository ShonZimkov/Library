from sqlalchemy import Column, Integer, String
from base import Base
from flask_login import UserMixin
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

# create User table
class User(UserMixin, Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True)
    username = Column(String(15), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(80))

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = password

#create a form for login
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

#create a form for register
class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])