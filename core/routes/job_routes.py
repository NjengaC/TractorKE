from core.forms import JobForm
from flask import Blueprint, session, render_template, flash, request, redirect, url_for, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from core.models import User, Operator, Job, Farm
from core.sms_service import send_bulk_sms
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from flask_mail import Message
from geopy.distance import geodesic
from core import app, db, bcrypt
from sqlalchemy import or_
from flask import session
import geopy.exc
import retrying
import requests
import secrets
import stripe
import atexit
import json
import os

job = Blueprint('job', __name__)

@job.route('/track_job')
def track_job():
    return render_template('track_job.html')

@job.route('/get_job_status')
def get_job_status():
    job_id = request.args.get('job_id')
    if job_id:
        job = Job.query.filter_by(id=job_id).first()
        if job:
            farm_lat, farm_lng = get_lat_lng(job.farm_location)

            return jsonify({
                'status': job.status,
                'expected_completion': job.expected_completion,
                'farm_location': job.farm_location,
                'farm_coords': {'lat': farm_lat, 'lng': farm_lng},
            }), 200
        else:
            return jsonify({'error': 'Job not found'}), 404
    else:
        return jsonify({'error': 'Job ID not provided'}), 400

@job.route('/request_job', methods=['POST', 'GET'])
@login_required
def request_job():
    form = JobForm()
    step = request.args.get('step', '1')

    if request.method == 'POST':
        if step == '1':
            session['farm_location'] = form.farm_location.data
            return redirect(url_for('job.request_job', step='2'))

        elif step == '2':
            session['job_details'] = form.job_details.data
            return redirect(url_for('job.request_job', step='3'))

        elif step == '3':
            response = requests.post(url_for('job.get_coordinates', _external=True), json={
                'farm_location': session.get('farm_location')
            })

            if response.ok:
                data = response.json()
                session['farm_coords'] = {
                    'lat': data.get('farm_lat'),
                    'lng': data.get('farm_lng')
                }
                return redirect(url_for('job.request_job', session=session, step='4'))
            else:
                flash('Unable to get coordinates. Please try again.', 'error')
                return redirect(url_for('job.request_job', step='2'))

        elif step == '4':
            # Create the job entry in the database
            job = Job(
                user_id=current_user.id,
                farm_location=session['farm_location'],
                job_details=session['job_details'],
                description="Plowing Job"  # Update this based on form input if necessary
            )

            db.session.add(job)
            db.session.commit()

            closest_operator = allocate_job(job)
            if closest_operator:
                flash('Operator Allocated. Check your email for more details', 'success')
            else:
                flash('Allocation in progress. Please wait for an operator to be assigned', 'success')

    return render_template('request_job.html', form=form, step=step)

@job.route('/get_coordinates', methods=['POST'])
def get_coordinates():
    data = request.get_json()
    farm_location = data.get('farm_location')

    farm_lat, farm_lng = get_lat_lng(farm_location)

    if None in (farm_lat, farm_lng):
        return jsonify({"error": "Could not fetch coordinates for the farm location"}), 400
    return jsonify({
        "farm_lat": farm_lat,
        "farm_lng": farm_lng,
    })

def get_lat_lng(location):
    user_agent = 'MyGeocodingApp/1.0'
    geolocator = Nominatim(user_agent=user_agent)
    location = geolocator.geocode(location)
    return location.latitude, location.longitude

def allocate_job(job):
    available_operators = Operator.query.filter_by(status='available').all()

    if not available_operators:
        return None

    farm_location = job.farm_location
    closest_operator = None
    min_distance = float('inf')

    for operator in available_operators:
        distance = calculate_distance(farm_location, operator.current_location)
        if distance < min_distance:
            closest_operator = operator
            min_distance = distance

    if closest_operator:
        job.status = 'allocated'
        job.operator_id = closest_operator.id
        closest_operator.status = 'unavailable'
        db.session.commit()
        notify_operator_new_assignment(closest_operator.email, job, closest_operator)
        send_operator_details_email(job.user.email, closest_operator, job.id)
        user_message = f"Your job has been allocated to an operator. Operator: {closest_operator.name}, Contact: {closest_operator.contact_number}"
        operator_message = f"You have been assigned a new job. Farm location: {job.farm_location}, Job details: {job.job_details}"

        send_bulk_sms(job.user.user_contact, user_message)
        send_bulk_sms(closest_operator.contact_number, operator_message)
        return closest_operator
    else:
        return None

def calculate_distance(location1, location2):
    user_agent = 'MyGeocodingApp/1.0'
    geolocator = Nominatim(user_agent=user_agent)
    location1 = geolocator.geocode(location1)
    location2 = geolocator.geocode(location2)
    current = location1.latitude, location1.longitude
    farm_location = location2.latitude, location2.longitude

    distance = geodesic(farm_location, current).kilometers
    return distance

def notify_operator_new_assignment(operator_email, job, operator):
    msg = Message('New Job Assignment', recipients=[operator_email])
    html_content = render_template('new_assignment_email.html', job=job, operator=operator)
    msg.html = html_content
    mail.send(msg)

def send_operator_details_email(recipient_email, closest_operator, job_id):
    msg = Message('Job Allocation Details', recipients=[recipient_email])
    html_content = render_template('operator_details_email.html', operator=closest_operator, job_id=job_id)
    msg.html = html_content
    mail.send(msg)
