from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class UserRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    user_contact = StringField('Contact Number', validators=[DataRequired(), Length(min=10, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = SubmitField('Remember Me')
    submit = SubmitField('Login')


class OperatorRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(min=10, max=20)])
    vehicle_type = StringField('Vehicle Type', validators=[DataRequired()])
    vehicle_registration = StringField('Vehicle Registration', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class UpdateOperatorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(min=10, max=20)])
    vehicle_type = StringField('Vehicle Type', validators=[DataRequired()])
    vehicle_registration = StringField('Vehicle Registration', validators=[DataRequired()])
    submit = SubmitField('Update Profile')


class JobForm(FlaskForm):
    farm_location = StringField('Farm Location', validators=[DataRequired()])
    job_type = StringField('Job Type', validators=[DataRequired()])  # Could be a dropdown with options
    job_details = StringField('Job Details', validators=[Length(max=400)])  # Optional
    submit = SubmitField('Request Job')


class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Password Reset Email')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')



