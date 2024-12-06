from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from core.forms import ForgotPasswordForm, ResetPasswordForm
from core.models import User, Operator
from core import mail, db, bcrypt
from flask_mail import Message
import secrets

password = Blueprint('password', __name__)

@password.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        operator = Operator.query.filter_by(email=email).first()
        if user:
            token = secrets.token_urlsafe(32)
            user.reset_password_token = token
            db.session.commit()

            reset_url = url_for('password.reset_password', token=token, _external=True)
            message = f"Click the link to reset your password: {reset_url}"
            send_email(user.email, "Password Reset Request", message)

            flash("Instructions to reset your password have been sent to your email.", "success")
            return redirect(url_for('auth.login'))
        elif operator:
            token = secrets.token_urlsafe(32)
            operator.reset_password_token = token
            db.session.commit()

            reset_url = url_for('password.reset_password', token=token, _external=True)
            message = f"Click the link to reset your password: {reset_url}"
            send_email(operator.email, "Password Reset Request", message)

            flash("Instructions to reset your password have been sent to your email.", "success")
            return redirect(url_for('operator.login_operator'))
        else:
            flash("Email address not found.", 'danger')
    return render_template('forgot_password.html', form=form)

@password.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_password_token=token).first()
    if user:
        form = ResetPasswordForm()
        if form.validate_on_submit():
            new_password = form.password.data
            user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            user.reset_password_token = None
            db.session.commit()

            flash("Your password has been successfully reset. You can now log in with your new password.", 'success')
            return redirect(url_for('auth.login'))
        return render_template('reset_password.html', form=form)

    operator = Operator.query.filter_by(reset_password_token=token).first()
    if operator:
        form = ResetPasswordForm()
        if form.validate_on_submit():
            new_password = form.password.data
            operator.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            operator.reset_password_token = None
            db.session.commit()

            flash("Your password has been successfully reset. You can now log in with your new password.", 'success')
            return redirect(url_for('operator.login_operator'))
        return render_template('reset_password.html', form=form)

    flash("Invalid or expired token.", 'danger')
    return redirect(url_for('password.forgot_password'))

def send_email(recipient, subject, html_body):
    msg = Message(subject, recipients=[recipient])
    msg.html = html_body
    mail.send(msg)
