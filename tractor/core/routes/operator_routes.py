from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, login_required, logout_user
from core import db, bcrypt, mail
from core.forms import OperatorRegistrationForm, LoginForm, UpdateOperatorForm
from core.models import Operator, Job
from sqlalchemy.exc import IntegrityError
from flask_mail import Message
import logging

operator = Blueprint('operator', __name__)
logger = logging.getLogger(__name__)

# Operator Registration Route
@operator.route('/register', methods=['GET', 'POST'])
def register_operator():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = OperatorUserRegistrationForm()
    if form.validate_on_submit():
        existing_operator = Operator.query.filter(
            (Operator.email == form.email.data) | (Operator.contact_number == form.contact_number.data)
        ).first()

        if existing_operator:
            flash('Email or contact already exists. Please choose different details.', 'danger')
            return redirect(url_for('operator.register_operator'))

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        operator = Operator(
            name=form.name.data,
            email=form.email.data,
            contact_number=form.contact_number.data,
            vehicle_type=form.vehicle_type.data,
            vehicle_registration=form.vehicle_registration.data,
            password=hashed_password,
            role='operator'
        )
        db.session.add(operator)

        try:
            db.session.commit()
            welcome_msg = render_template('welcome_operator_mail.html', operator=operator)
            msg = Message(f'Welcome to the Tractor Operator App, {operator.name}!', recipients=[operator.email])
            msg.html = welcome_msg
            mail.send(msg)
            flash('Operator account created successfully!', 'success')
            return redirect(url_for('operator.login_operator'))
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f'IntegrityError: {e}')
            flash('An error occurred while creating the operator account. Please try again.', 'danger')

    return render_template('register_operator.html', title='Register as Operator', form=form)

# Operator Login Route
@operator.route('/login', methods=['GET', 'POST'])
def login_operator():
    if current_user.is_authenticated and current_user.role == 'operator':
        return redirect(url_for('operator.operator_dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        operator = Operator.query.filter_by(email=form.email.data).first()

        if operator and bcrypt.check_password_hash(operator.password, form.password.data):
            login_user(operator)
            flash(f'Welcome back, {operator.name}!', 'success')
            return redirect(url_for('operator.operator_dashboard'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')

    return render_template('login_operator.html', title='Operator Login', form=form)

# Operator Dashboard Route
@operator.route('/dashboard')
@login_required
def operator_dashboard():
    jobs = Job.query.filter_by(operator_id=current_user.id).all()
    return render_template('operator_dashboard.html', jobs=jobs, operator=current_user)

# Operator Edit Profile Route
@operator.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_operator_profile():
    form = UpdateOperatorForm()
    if request.method == 'GET':
        form.email.data = current_user.email
        form.name.data = current_user.name
        form.contact_number.data = current_user.contact_number
        form.vehicle_type.data = current_user.vehicle_type
        form.vehicle_registration.data = current_user.vehicle_registration
    elif request.method == 'POST':
        if form.validate_on_submit():
            current_user.email = form.email.data
            current_user.name = form.name.data
            current_user.contact_number = form.contact_number.data
            current_user.vehicle_type = form.vehicle_type.data
            current_user.vehicle_registration = form.vehicle_registration.data
            db.session.commit()
            flash('Your operator profile has been updated!', 'success')
            return redirect(url_for('operator.operator_dashboard'))
    return render_template('edit_operator_profile.html', title='Edit Operator Profile', form=form, operator=current_user)

