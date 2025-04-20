from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from core import mail, db
from core.models import User, Operator, Job, FAQ
from sqlalchemy.exc import IntegrityError
from flask_mail import Message
from sqlalchemy import or_

# Blueprint for main routes
main = Blueprint('main', __name__)

# Home route - Redirect users based on role
@main.route('/')
@main.route('/home')
def home():
    """ Home route to either dashboards or Getting started section """
    if current_user.is_authenticated and current_user.role == 'operator':
        return redirect(url_for('operator.operator_dashboard'))
    elif current_user.is_authenticated and current_user.role == 'admin':
        return redirect(url_for('admin.admin_dashboard'))
    elif current_user.is_authenticated and current_user.role == 'booking_agent':
        return redirect(url_for('agent.agent_dashboard'))
    return render_template('home.html', title='Home')


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/contacts')
def contacts():
    return render_template('contact.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@main.route('/support', methods=['GET', 'POST'])
def support():
    """
    Support route with FAQ search functionality and email notification to support
    """
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        comment = request.form.get('comment')

        if not name or not email or not comment:
            flash('Please fill out all fields.', 'error')
        else:
            msg = Message(subject='User Comment', recipients=['tractorappsupport@gmail.com'])
            msg.body = f"Name: {name}\nEmail: {email}\nComment: {comment}"

            try:
                mail.send(msg)
                flash('Email sent successfully! Our support team will get back to you shortly', 'success')
            except Exception as e:
                flash('Something unexpected happened! Please try again', 'error')

        # Redirect to the support page after processing the form data
        return redirect(url_for('main.support'))

    if request.method == 'GET':
        search_query = request.args.get('search_query', '').strip()

        if search_query:
            search_words = search_query.split()

            filter_conditions = []

            for word in search_words:
                question_condition = FAQ.question.ilike(f'%{word}%')
                answer_condition = FAQ.answer.ilike(f'%{word}%')

                filter_conditions.append(question_condition)
                filter_conditions.append(answer_condition)

            combined_condition = or_(*filter_conditions)

            existing_faqs = FAQ.query.filter(combined_condition).all()

            faqs_dict = [{'question': faq.question, 'answer': faq.answer} for faq in existing_faqs]
            existing_faqs = jsonify(faqs_dict)
            return existing_faqs

    return render_template('support.html')
