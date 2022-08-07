from flask import Blueprint, request, make_response, render_template, redirect, url_for, flash
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt, set_access_cookies, jwt_required, decode_token
from new.database.models import User
import datetime
from app import jwt
import logging
from itsdangerous import URLSafeTimedSerializer
from new.resources.mail import send_auth_email, send_reset_email
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




