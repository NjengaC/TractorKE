from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import (
    DataRequired, Length, Email, EqualTo, Regexp, ValidationError
)
from flask_login import current_user
from core.models import User, Operator, Job, BookingAgent, Admin, Farm


# -----------------------------
# User Registration Form
# -----------------------------
class UserRegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=2, max=100, message='Username must be between 2 and 100 characters.')
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Please enter a valid email address.')
        ]
    )
    user_contact = StringField(
        'Contact Number',
        validators=[
            DataRequired(),
            Regexp(
                r'^[0-9]{10,20}$',
                message='Please enter a valid contact number (10-20 digits).'
            )
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Password should be at least 6 characters long.')
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken. Please choose another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('A user with this email already exists. Please choose another one.')


# -----------------------------
# Login Form
# -----------------------------
class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Please enter a valid email address.')
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# -----------------------------
# Operator Registration Form
# -----------------------------
class OperatorRegistrationForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=2, max=100, message='Name must be between 2 and 100 characters.')
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Please enter a valid email address.')
        ]
    )
    contact_number = StringField(
        'Contact Number',
        validators=[
            DataRequired(),
            Regexp(
                r'^[0-9]{10,20}$',
                message='Please enter a valid contact number (10-20 digits).'
            )
        ]
    )
    vehicle_type = StringField(
        'Vehicle Type',
        validators=[
            DataRequired(),
            Length(min=2, max=50, message='Vehicle type must be between 2 and 50 characters.')
        ]
    )
    vehicle_registration = StringField(
        'Vehicle Registration',
        validators=[
            DataRequired(),
            Length(min=2, max=50, message='Vehicle registration must be between 2 and 50 characters.')
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Password should be at least 6 characters long.')
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Register')

    def validate_name(self, name):
        operator = Operator.query.filter_by(name=name.data).first()
        if operator:
            raise ValidationError('Name is already taken. Please choose another one.')

    def validate_email(self, email):
        operator = Operator.query.filter_by(email=email.data).first()
        if operator:
            raise ValidationError('An operator with this email already exists. Please choose another one.')

    def validate_contact_number(self, contact_number):
        operator = Operator.query.filter_by(contact_number=contact_number.data).first()
        if operator:
            raise ValidationError('An operator with this contact number already exists.')


# -----------------------------
# Update Account Form (User)
# -----------------------------
class UpdateAccountForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=2, max=100, message='Username must be between 2 and 100 characters.')
        ]
    )
    user_contact = StringField(
        'Contact Number',
        validators=[
            DataRequired(),
            Regexp(
                r'^[0-9]{10,20}$',
                message='Please enter a valid contact number (10-20 digits).'
            )
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Please enter a valid email address.')
        ]
    )
    password = PasswordField(
        'New Password',
        validators=[
            Length(min=6, message='Password should be at least 6 characters long.')
        ]
    )
    confirm_password = PasswordField(
        'Confirm New Password',
        validators=[
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is already taken. Please choose another one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('A user with this email already exists. Please choose another one.')


# -----------------------------
# Update Operator Form
# -----------------------------
class UpdateOperatorForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=2, max=100, message='Name must be between 2 and 100 characters.')
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Please enter a valid email address.')
        ]
    )
    contact_number = StringField(
        'Contact Number',
        validators=[
            DataRequired(),
            Regexp(
                r'^[0-9]{10,20}$',
                message='Please enter a valid contact number (10-20 digits).'
            )
        ]
    )
    vehicle_type = StringField(
        'Vehicle Type',
        validators=[
            DataRequired(),
            Length(min=2, max=50, message='Vehicle type must be between 2 and 50 characters.')
        ]
    )
    vehicle_registration = StringField(
        'Vehicle Registration',
        validators=[
            DataRequired(),
            Length(min=2, max=50, message='Vehicle registration must be between 2 and 50 characters.')
        ]
    )
    area_of_operation = StringField(
        'Area of Operation',
        validators=[
            DataRequired(),
            Length(min=2, max=100, message='Area of operation must be between 2 and 100 characters.')
        ]
    )
    current_location = StringField(
        'Current Location',
        validators=[
            DataRequired(),
            Length(min=5, max=100, message='Current location must be between 5 and 100 characters.')
        ]
    )
    submit = SubmitField('Update Profile')

    def validate_name(self, name):
        if name.data != current_user.name:
            operator = Operator.query.filter_by(name=name.data).first()
            if operator:
                raise ValidationError('Name is already taken. Please choose another one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            operator = Operator.query.filter_by(email=email.data).first()
            if operator:
                raise ValidationError('An operator with this email already exists. Please choose another one.')

    def validate_contact_number(self, contact_number):
        if contact_number.data != current_user.contact_number:
            operator = Operator.query.filter_by(contact_number=contact_number.data).first()
            if operator:
                raise ValidationError('An operator with this contact number already exists.')


# -----------------------------
# Job Request Form
# -----------------------------
class JobForm(FlaskForm):
    farm_location = StringField(
        'Farm Location',
        validators=[
            DataRequired(),
            Length(min=5, max=255, message='Farm location must be between 5 and 255 characters.')
        ]
    )
    job_type = SelectField(
        'Job Type',
        choices=[
            ('plowing', 'Plowing'),
            ('tilling', 'Tilling'),
            ('harvesting', 'Harvesting'),
            ('sowing', 'Sowing'),
            ('other', 'Other')
        ],
        validators=[DataRequired()]
    )
    job_details = TextAreaField(
        'Job Details',
        validators=[
            Length(max=400, message='Job details cannot exceed 400 characters.')
        ]
    )
    price = StringField(
        'Price ($)',
        validators=[
            DataRequired(),
            Regexp(
                r'^\d+(\.\d{1,2})?$',
                message='Please enter a valid price (up to 2 decimal places).'
            )
        ]
    )
    submit = SubmitField('Request Job')

    def validate_farm_location(self, farm_location):
        # You can add validation to ensure the farm exists
        farm = Farm.query.filter_by(location=farm_location.data).first()
        if not farm:
            raise ValidationError('Farm location does not exist. Please enter a valid location.')

    def validate_price(self, price):
        try:
            value = float(price.data)
            if value <= 0:
                raise ValidationError('Price must be greater than zero.')
        except ValueError:
            raise ValidationError('Invalid price format.')


# -----------------------------
# Forgot Password Form
# -----------------------------
class ForgotPasswordForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Please enter a valid email address.')
        ]
    )
    submit = SubmitField('Send Password Reset Email')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('There is no account with that email. You must register first.')

        operator = Operator.query.filter_by(email=email.data).first()
        admin = Admin.query.filter_by(email=email.data).first()
        if not user and not operator and not admin:
            raise ValidationError('There is no account associated with this email.')


# -----------------------------
# Reset Password Form
# -----------------------------
class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'New Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Password should be at least 6 characters long.')
        ]
    )
    confirm_password = PasswordField(
        'Confirm New Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Reset Password')

