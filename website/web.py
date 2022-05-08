from flask import Blueprint, request, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_required
from database.models import User, Location
from resources.mail import send_auth_email
import logging
from mongoengine.queryset.visitor import Q
import os

web = Blueprint('web', __name__, template_folder='templates')

@web.route('/categories', methods=['GET'])
@jwt_required(optional=True)
def categories():
    current_identity = get_jwt_identity()
    if current_identity:
        return render_template('categories.html', logged=True)
    else:
        return render_template('categories.html', logged=False)

@web.route('/firecategories', methods=['GET'])
@jwt_required(optional=True)
def firecategories():
    current_identity = get_jwt_identity()
    if current_identity:
        return render_template('firecategories.html', logged=True)
    else:
        return render_template('firecategories.html', logged=False)

@web.route('/policecategories', methods=['GET'])
@jwt_required(optional=True)
def policecategories():
    current_identity = get_jwt_identity()
    if current_identity:
        return render_template('policecategories.html', logged=True)
    else:
        return render_template('policecategories.html', logged=False)

@web.route('/medicalcategories', methods=['GET'])
@jwt_required(optional=True)
def medicalcategories():
    current_identity = get_jwt_identity()
    if current_identity:
        return render_template('medicalcategories.html', logged=True)
    else:
        return render_template('medicalcategories.html', logged=False)

@web.route('/weathercategories', methods=['GET'])
@jwt_required(optional=True)
def weathercategories():
    current_identity = get_jwt_identity()
    if current_identity:
        return render_template('weathercategories.html', logged=True)
    else:
        return render_template('weathercategories.html', logged=False)

@web.route('/userdashboard', methods=['GET', 'POST'])
@jwt_required()
def userdashboard():
    #try:
    user = User.objects.get(id=get_jwt_identity())
    if user.permission == 'dispatcher':
        user_data = []
        for fields in user:
            data = [user.email, user.dispatcherid, user.name, user.permission]
            user_data.append(data)
        final_user_data= user_data[0]
        #print(final_user_data)
        return render_template('dashboard_user.html', final_user_data=final_user_data)
    elif user.permission == 'admin':
        user_list = []
        user_data = []
        users = User.objects.filter(permission='dispatcher')
        for people in users:
            user_data.append(people)
        for fields in user:
            data = [user.email, user.dispatcherid, user.name, user.permission]
            user_data.append(data)
        final_user_data= user_data[0]
        print(user_list)
        #print(final_user_data)
        return render_template('dashboard_admin.html', final_user_data=final_user_data, user_list=user_list)

@web.route('/updateuser', methods=['GET', 'POST'])
@jwt_required()
def updateuser():
    userupdate = User(**request.form)
    user = User.objects.get(id = userupdate.id)
    password1 = userupdate.password
    password2 = userupdate.password2
    password1 = str(password1.strip())
    password2 = str(password2.strip())
    print(userupdate.email)
    if userupdate.email == '':
        print('none')
    else:
        user.modify(email=userupdate.email)

    print(userupdate.name)
    if userupdate.name == '':
        print('none')
    else:
        user.modify(name=userupdate.name)

    print(userupdate.dispatcherid)
    if userupdate.dispatcherid == '':
        print('none')
    else:
        user.modify(dispatcherid=userupdate.dispatcherid)
    if password1 == '':
        print('pass1 empty')
    elif password2 == '':
        print('pass2 empty')
    elif password1 == password2:
        user.modify(password=password1)
        #print(user.password)
        user.update_hash()
        #print('hashed pass saved')
        user.check_password(password2)
        #print('password correct')
        #print(user.password)
        user.modify(password=user.password)
        user.modify(salt=user.salt)
        #print(user.password)
        user.modify(password2=password2)
        #print('pass2 updated')
        user.password2 = ''
    elif password1 != password2:
        print('passwords dont match')
    user.save()
    return redirect(url_for('web.userdashboard'))

@web.route('/about')
@jwt_required(optional=True)
def about():
    current_identity = get_jwt_identity()
    if current_identity:
        return render_template('about.html', logged=True)
    else:
        return render_template('about.html', logged=False)

@web.route('/mail')
@jwt_required()
def send_email():
    user = User.objects.get(id=get_jwt_identity())
    #user.generate_confirmation()
    send_auth_email()
    return redirect(url_for('cad.dispatch'))

@web.route('/addresslookup', methods=['GET', 'POST'])
@jwt_required()
def addresslookup():
    #try:
        address = Location.objects.get(numeric='508')
        address_data = []
        for fields in address:
            data = [address.numeric, address.aptnumeric, address.streetname, address.town, address.state, address.propertyowner, address.propertyresident, address.propertytypelegal, address.propertytypefire, address.historicincidents]
            address_data.append(data)
        final_address_data= address_data[0]
        #print(final_user_data)
        return render_template('addresslookup.html', final_address_data=final_address_data)

@web.route('/ctaddresssearch')
def ctaddresssearch():
    return redirect('https://portal.ct.gov/DEEP/Forestry/Forest-Fire/Forest-Fire-Danger-Report')

@web.route('/finduser', methods=['POST'])
@jwt_required()
def finduser():
    form = User(**request.form)
    searcheduser = form.dispatcherid
    user = User.objects.get(dispatcherid=searcheduser)
    username = user.dispatcherid
    user_data = []
    for fields in user:
        data = [user.email, user.dispatcherid, user.name, user.permission, user.permission, user.id, user.credit, user.phone]
        user_data.append(data)
    final_user_data = user_data[0]
    return render_template('dashboard_admin.html', user=username, final_user_data=final_user_data)

@web.route('/devnotes')
@jwt_required()
def devnotes():
    return render_template('devnotes.html')

@web.route('/abbreviations')
@jwt_required(optional=True)
def abbreviations():
    current_identity = get_jwt_identity()
    if current_identity:
        return render_template('abbreviations.html', logged=True)
    else:
        return render_template('abbreviations.html', logged=False)