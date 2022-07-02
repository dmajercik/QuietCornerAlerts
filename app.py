from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
import configparser
from flask_ckeditor import CKEditor

config = configparser.RawConfigParser()
configFilePath = r'secret.config'
config.read(configFilePath)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = config.get('key','jwt_secret_key')
app.config['MONGODB_SETTINGS'] = config.get('key','mongodb')
app.secret_key = config.get('key','app_secret_key')
app.config['MAIL_SERVER'] = "mail.privateemail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = config.get('key','mail_username')
app.config['MAIL_PASSWORD'] = config.get('key','mail_password')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['JWT_TOKEN_LOCATION'] = 'cookies'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False # Probably shouldn't be False but I can't figure out a better way
app.config['CKEDITOR_PKG_TYPE'] = 'standard'

ckeditor = CKEditor(app)
mail = Mail(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


from new.database.db import initialize_db
from new.resources.routes import initialize_routes

initialize_db(app) # Run the function after app and config init. End of the file works well.

initialize_routes(app)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()

