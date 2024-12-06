from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json
from datetime import datetime
from core import db, login_manager
import random
from datetime import timedelta
import uuid


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    user_contact = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    reset_password_token = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Operator(db.Model, UserMixin):
    __tablename__ = 'operators'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=False)
    vehicle_registration = db.Column(db.String(50), unique=True, nullable=False)
    current_location = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='operator')
    status = db.Column(db.String(20), default='available')
    assigned_jobs = db.relationship('Job', back_populates='assigned_operator')
    
    def __repr__(self):
        return f"Operator('{self.name}', '{self.contact_number}', '{self.vehicle_type}')"


class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    operator_id = db.Column(db.String(36), db.ForeignKey('operators.id'), nullable=True)
    farm_location = db.Column(db.String(255), nullable=False)
    job_type = db.Column(db.String(50), nullable=False)  # plowing, tilling, etc.
    job_details = db.Column(db.String(400), nullable=True)  # Additional job info
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='pending')
    price = db.Column(db.Float, nullable=False, default=0.0)  # Job price
    is_paid = db.Column(db.Boolean, default=False)  # Track payment status
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assigned_operator = db.relationship('Operator', back_populates='assigned_jobs')

    def __repr__(self):
        return f"Job('{self.id}', '{self.job_type}', '{self.status}', 'Paid: {self.is_paid}')"


class BookingAgent(db.Model, UserMixin):
    __tablename__ = 'booking_agents'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='booking_agent')
    
    def __repr__(self):
        return f"BookingAgent('{self.name}', '{self.contact_number}')"


class Admin(db.Model, UserMixin):
    __tablename__ = 'admins'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='admin')

    def __repr__(self):
        return f"Admin('{self.username}', '{self.email}')"


class Farm(db.Model):
    __tablename__ = 'farms'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    polygon_boundary = db.Column(db.Text, nullable=True)  # Store polygon as text or GeoJSON

    def __repr__(self):
        return f"Farm('{self.name}', '{self.location}')"
