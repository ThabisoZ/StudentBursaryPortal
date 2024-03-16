from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
#from .auth import generate_reset_token, send_reset_email, verify_reset_token

auth=Blueprint('auth', __name__)

#Login
@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()  # checking if email exists
        if user:
            if check_password_hash(user.password, password):

                if user.role == 'admin'and email=='admin@gmail.com':
                    login_user(user, remember=True)
                    return redirect(url_for('views.admin_dashboard'))
                
                elif user.role == 'sponsor':
                    login_user(user, remember=True)
                    return redirect(url_for('views.post'))
                
                elif user.role == 'student':
                    login_user(user, remember=True)
                    return redirect(url_for('views.index'))
            else:

                flash('Incorrect password, please try again', category='error')
            
        else:
            flash('Email does not exist', category='error')
            #return ('email do not exist')

    return render_template('login.html', user=current_user)


#logout
@auth.route('/logout')
@login_required
def logout():
    logout_user
    return redirect(url_for('views.home'))


#sign-up
@auth.route('/sign_Up', methods=['GET','POST'])
def signUp():
    if request.method=='POST':
        firstname = request.form.get('firstname')
        lastname=request.form.get('lastname')
        phonenumber=request.form.get('phonenumber')
        role=request.form.get('role')
        email=request.form.get('email')
        password=request.form.get('password')
        confirm_password=request.form.get('confirm_password')

        user=User.query.filter_by(email=email).first()
        if user:

            flash('Email already exist.', category='error')
        
        elif password!=confirm_password:
            flash('Password do not match!!!', category='error')
    
        else:
            #adding user to the database
            new_user=User(email=email, first_name=firstname, last_name=lastname, phone_number=phonenumber, role=role, password=generate_password_hash(password, method='pbkdf2:sha512'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)              
            flash('account created successful', category='success')
            return redirect(url_for('auth.login'))
        
    return render_template('sign_Up.html', user=current_user)

# Import the necessary modules
from website import create_app, db
from website.models import User

# Function to add admin to the database
def seed_admin():
    # Check if admin already exists in the database
    existing_admin = User.query.filter_by(email='admin@gmail.com').first()
    if not existing_admin:
        # If admin doesn't exist, create a new admin record
        admin = User(email='admin@gmail.com', password=generate_password_hash('Admin111', method='pbkdf2:sha512'), role='admin', first_name='admin', last_name='admin', phone_number='1234567890')
        db.session.add(admin)
        db.session.commit()

# Create the Flask application instance
app = create_app()

# Call the seed_admin function to add admin to the database
with app.app_context():
    seed_admin()


#forgot password
import secrets
import string

def generate_reset_token(length=20):
    # Generate a random string of letters and digits for the token
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for _ in range(length))
    return token


#verify reset token function
#from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

'''def verify_reset_token(token, secret_key, expiration=3600):
    s = Serializer(secret_key, expires_in=expiration)
    try:
        # Deserialize the token to check if it's valid
        s.loads(token)
        return True
    except SignatureExpired:
        # Token has expired
        return False
    except BadSignature:
        # Token is invalid
        return False'''
    
'''  #send reset email function
from flask import render_template
from flask_mail import Message
from  .import mail

def send_reset_email(user, token):
    # Render the email template
    message = render_template('reset_email.html', user=user, token=token)
    
    # Create a message object
    msg = Message(subject='Password Reset Request', recipients=[user.email], html=message)
    
    # Send the email
    mail.send(msg)'''


'''
###@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))  # Redirect authenticated users to the home page

    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            # Generate a password reset token and send it via email
            token = generate_reset_token(user)
            send_reset_email(user, token)
            flash('An email with instructions to reset your password has been sent.', category='info')
            return redirect(url_for('login'))
        else:
            flash('Email address not found. Please check your email or register for a new account.', category='error')
    return render_template('forgot_password.html')

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))  # Redirect authenticated users to the home page

    user = verify_reset_token(token)
    if not user:
        flash('Invalid or expired token. Please request a new password reset link.', category='error')
        return redirect(url_for('forgot_password.forgot_password_request'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password == confirm_password:
            # Update the user's password
            user.set_password(password)
            db.session.commit()
            flash('Your password has been reset successfully. You can now log in.', category='success')
            return redirect(url_for('login'))
        else:
            flash('Passwords do not match. Please try again.', 'error')

    return render_template('reset_password.html')

# Utility functions to generate/reset token and send email are assumed to be implemented elsewhere'''
