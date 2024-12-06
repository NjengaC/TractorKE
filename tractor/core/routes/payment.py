from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from core import mail
from core.models import Job, User
from core import app, db
from flask_mail import Message
import stripe
import os

secret_key = os.getenv('STRIPE_SECRET_KEY')
publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY')

stripe_keys = {
    "secret_key": secret_key,
    "publishable_key": publishable_key,
}

stripe.api_key = stripe_keys['secret_key']

payment = Blueprint('payment', __name__)

# Payment success route
@payment.route('/payment_success', methods=['POST'])
@login_required
def payment_success():
    # Implement the logic after successful payment
    flash('Payment successful!', 'success')
    return redirect(url_for('main.home'))

# Checkout route (render checkout page)
@payment.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    job_id = request.args.get('job_id')
    job = Job.query.get(job_id)
    
    if not job:
        flash('Job not found.', 'danger')
        return redirect(url_for('main.home'))

    return render_template('checkout.html', key=stripe_keys['publishable_key'], job=job)


@payment.route('/charge', methods=['POST'])
@login_required
def charge():
    job_id = request.form.get('job_id')
    job = Job.query.get(job_id)

    if not job:
        return jsonify({'error': 'Job not found'}), 404

    # Amount in cents (Stripe works in the smallest currency unit)
    amount = int(job.price * 100)  # Convert to cents

    try:
        # Create a Stripe customer and charge them
        customer = stripe.Customer.create(
            email=current_user.email,
            source=request.form['stripeToken']
        )

        # Charge the customer
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description=f'Job Payment for Job ID: {job.id}'
        )

        # Mark the job as paid and commit to the database
        job.is_paid = True
        db.session.commit()

        # Notify user via email
        send_payment_notification_email(current_user.email, job)

        flash('Payment successful! Job is now in progress.', 'success')
        return jsonify({'success': True})

    except stripe.error.StripeError as e:
        flash(f"Payment error: {e.user_message}", 'danger')
        return jsonify({'error': e.user_message}), 400

# Helper function to send payment notification email
def send_payment_notification_email(recipient_email, job):
    msg = Message('Payment Received for Your Job', recipients=[recipient_email])
    msg.body = f"Your payment for the job with ID {job.id} has been received. The job is now in progress."
    mail.send(msg)

