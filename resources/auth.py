from flask import Blueprint, request, make_response, render_template, redirect, url_for, flash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, set_access_cookies, jwt_required, decode_token
from database.models import User
import datetime
from app import jwt
import logging
from itsdangerous import URLSafeTimedSerializer
from resources.mail import send_auth_email, send_reset_email
import os
import configparser

config = configparser.RawConfigParser()
configFilePath = r'secret.config'
config.read(configFilePath)

auth = Blueprint('auth', __name__, template_folder='templates')
auth.secret_key = config.get('key','auth_secret_key')
ts = URLSafeTimedSerializer(auth.secret_key) # I don't think this is needed

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger("auth")

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = User(**request.form)
        email = str.lower(user.email)
        #email_check = User.get(email=email)
        #if email_check == None:
            #user.email = email
        if user.password == user.password2:
            user.hash_password()
            user.password2 = ''
            user.set_permission()
            user.save()
            try:
                send_auth_email(user)
            except ConnectionRefusedError:
                logging.info('Authentication email failed')
                pass  # Mail server isn't working right now
            accessToken = create_access_token(identity=str(user.id), expires_delta=datetime.timedelta(days=1))
            resp = make_response(redirect(url_for('cad.dispatch')))  # Redirect to wherever after login
            set_access_cookies(resp, accessToken, max_age=60 * 60 * 24)  # Expires in 1 day
            return resp
        else:
            flash('Passwords do not match')
            return render_template('signup.html')
    else:
        if request.cookies.get('access_token_cookie'):
            return redirect(url_for('auth.login'))
        return render_template('signup.html') # Our signup page


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        body = request.form
        try:
            user = User.objects.get(email=str.lower(body['email']))
        except:
            flash('User not found')
            return render_template('login.html', failed=True)  # Our login page
        authorized = user.check_password(body['password'])
        if not authorized:
            flash('Wrong Password')
            return render_template('login.html', failed=True) # Our login page
        accessToken = create_access_token(identity=str(user.id), expires_delta=datetime.timedelta(days=1))
        resp = make_response(redirect(url_for('cad.dispatch'))) # Redirect to wherever after login
        set_access_cookies(resp, accessToken, max_age=60*60*24) # Expires in 1 day
        return resp
    else:
        if request.cookies.get('access_token_cookie'):
            return redirect(url_for('cad.dispatch'))
        return render_template('login.html') # Our login page


@auth.after_app_request
@jwt_required(optional=True)
def refresh(response):
    identity = get_jwt_identity()
    if identity:
        expTimestamp = get_jwt()['exp']
        now = datetime.datetime.now()
        targetTimestamp = datetime.datetime.timestamp(now + datetime.timedelta(minutes=30))
        if targetTimestamp > expTimestamp:
            accessToken = create_access_token(identity=identity, expires_delta=datetime.timedelta(days=1))
            set_access_cookies(response, accessToken, max_age=60*60*24)
    return response

@jwt.unauthorized_loader
def unauthorized_loader_handler(callback):
    return redirect('/login')

@auth.route('/forgot', methods=['GET', 'POST'])
def forgotPassword():
    if request.method == 'POST':
        email = request.form['email']
        user = User.objects.get(email=email)
        if not user:
            # ERROR
            return render_template('forgot.html')
        expires = datetime.timedelta(hours=24)
        resetToken = create_access_token(str(user.id), expires_delta=expires)
        print(resetToken)
        send_reset_email(user, resetToken)
        return render_template('forgot.html', finished=True)
    else:
        if request.cookies.get('access_token_cookie'):
            return redirect(url_for('cad.dispatch'))
        return render_template('forgot.html')

@auth.route('/reset/<resetToken>', methods=['GET', 'POST'])
def resetPassword(resetToken):
    if request.method == 'POST':
        pass1 = request.form.get('pass1')
        pass2 = request.form.get('pass2')
        token = request.form.get('resetToken')
        print(token, token)
        if not token:
            # ERROR
            print('1')
            return redirect(url_for('auth.forgotPassword'))
        if not pass1 or not pass2:
            # ERROR
            print('2')
            return render_template('reset.html', token=token)
        if pass1 == pass2:
            userId = decode_token(token)['sub']
            user = User.objects.get(id=userId)
            user.modify(password=pass1)
            user.hash_password()
            user.save()
            return redirect(url_for('auth.login'))
        return render_template('reset.html', token=token)
    else:
        if request.cookies.get('access_token_cookie'):
            return redirect(url_for('cad.dispatch'))
        token = request.args.get(resetToken)
        resetsToken=resetToken
        print(resetsToken)
        print(resetToken)
        print(token)
        if not token:
            print('3')
            return redirect(url_for('auth.forgotPassword'))
        return render_template('reset.html', token=token)
