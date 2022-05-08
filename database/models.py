from mongoengine import Document, EmailField, StringField, DateTimeField, BooleanField, DecimalField
from flask_bcrypt import generate_password_hash, check_password_hash
import string, random
from itsdangerous import URLSafeTimedSerializer
from app import app
import dateutil
from datetime import *

class User(Document):
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, min_length=6)
    password2 = StringField()
    salt = StringField()
    confirmation = StringField()
    permission = StringField()
    name = StringField()
    phone = StringField()
    credit = StringField()
    dispatcherid = StringField()
    lastconnection = DateTimeField()
    lastconnectiondate = DateTimeField()
    lastconnectiontime = DateTimeField()
    alertincidents = StringField()
    alerttowns = StringField()
    def hash_password(self):
        chars = string.ascii_letters + string.punctuation
        size = 12
        self.salt = ''.join(random.choice(chars) for x in range(size))
        self.password = generate_password_hash(self.password + self.salt).decode('utf8')
    def update_hash(self):
        salt = str(User.salt)
        self.password = generate_password_hash(self.password + self.salt).decode('utf8')
    def set_permission(self):
        self.permission = 'baseuser'
    def generate_confirmation(self):
        chars = string.ascii_letters + string.digits
        size = 6
        self.confirmation =''.join(random.choice(chars) for x in range(size))
        print(self.confirmation)
    def check_password(self, password):
        return check_password_hash(self.password, password + self.salt)
    def serialize(self):
        return {
            'id': str(self.id),
            'email': self.email,
            'permission': self.permission,
            'confirmation': self.confirmation,
            'name': self.name,
            'phone': str(self.phone),
            'credit': self.credit,
            'dispatcherid': self.dispatcherid,
            'lastconnection': self.lastconnection,
            'lastconnectiondate': self.lastconnectiondate,
            'lastconnectiontime': self.lastconnectiontime,
            'alertincidents': self.alertincidents,
            'alerttowns': self.alerttowns,

        }

class Calls(Document):
    dispatcher = StringField()
    dispatcher_credit = StringField()
    date = StringField()
    times = StringField()
    town = StringField()
    state = StringField()
    roadname = StringField()
    incident = StringField()
    narrative = StringField()
    active = StringField()
    highway = StringField()
    frequency = StringField()
    datetime = DateTimeField()
    flagged = BooleanField()
    lat = DecimalField(precision=7)
    lon = DecimalField(precision=7)
    updated = BooleanField()
    def serialize(self):
        return {
            'id': str(self.id),
            'dispatcher': self.dispatcher,
            'dispatcher_credit': self.dispatcher_credit,
            'date': self.date,
            'times': self.times,
            'town': self.town,
            'state': self.state,
            'roadname': self.roadname,
            'incident': self.incident,
            'narrative': self.narrative,
            'active': self.active,
            'highway': self.highway,
            'frequency': self.frequency,
            'datetime': self.datetime,
            'flagged': self.flagged,
            'lat': self.lat,
            'lon': self.lon,
            'updated': self.updated,
        }
class Chat(Document):
    dispatcher = StringField()
    message = StringField()
    datetime = DateTimeField()
    date = StringField()
    times = StringField()
    def serialize(self):
        return {
            'dispatcher': self.dispatcher,
            'message': str(self.message),
            'datetime': self.datetime,
            'date': self.date,
            'times': self.times,
        }

class People(Document): #Document for individual people records
    firstname = StringField() #Individuals first name
    lastname = StringField() #Individuals last name
    oln = StringField() #Individuals liscnense number
    description = StringField() #Description of individual as seen on liscense
    #dob
    address = StringField() #Individuals address/associated adresses
    phonenumber = StringField() #Individuals phone number
    vehicle = StringField() #Individuals registered/associated vehicles
    watchlist = StringField() #Watchlist tags, ie. warrant, firearm, violent toward responders, medical notes? etc
    #Picture of person
    # historical incidents
    def serialize(self):
        return {
            'fistname': self.firstname,
            'lastname': self.lastname,
            'oln': self.oln,
            'description': self.description,
            'address': self.address,
            'phonenumber': self.phonenumber,
            'vehicle': self.vehicle,
            'watchlist': self.watchlist,
        }

class Location(Document): #Document for indicidual Addresses
    numeric = StringField() #Address, do town and state need to be seperate?
    aptnumeric = StringField()#subaddresses, ie apartments
    streetname = StringField() #street name
    town = StringField()
    state = StringField()
    propertyowner = StringField()#Person who owns property
    propertyresident = StringField()#Person who resides at property this may need to be proken into multple fields for multiple people
    propertytypelegal = StringField()#Type of property legal
    propertytypefire = StringField()#Type of property fire
    #picture of address
    historicincidents = StringField()#historical incidents
    def serialize(self):
        return {
            'numeric': self.numeric,
            'aptnumeric': self.aptnumeric,
            'streetname': self.streetname,
            'town': self.town,
            'state': self.state,
            'propertyowner': self.propertyowner,
            'propertyresident': self.propertyresident,
            'propertytypelegal': self.propertytypelegal,
            'propertytypefire': self.propertytypefire,
            'historicincidents': self.historicincidents,
        }

class Vehicle(Document): #Document for individual vehicles
    vin = StringField() #Vehicle VIN
    #Liscence plate
    #liscense plate state, this may be fine in address?
    #Color of Vehcicle
    #Make
    #Model
    #Year
    #registered owner
    #Registered Address
    #Notes such as damamage
    #picture of vehicle
    #historical incidents

class Keys(Document):  # Document for Keys
    name = StringField()
    key = StringField()  #
    expiration_date = StringField()
    def serialize(self):
        return {
            'name': self.name,
            'key': self.key,
            'expiration_date': self.expiration_date,
        }

