from flask_mail import Message
from app import mail
import logging
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger("mail")

def send_auth_email(user):
    msg = Message()
    msg.subject = "Please confirm your email"
    msg.recipients = [user.email]
    msg.sender = 'support@quietcorneralerts.net'
    msg.body = 'Thank you for creating a Quiet Corner Alerts account! Please go to 192.168.1.2:5000/verify and enter your verification code {{user.confirmation}}'
    mail.send(msg)
    logging.info('Authentication email sent to ', user.dispatcherid,' ',user.email)

def send_reset_email(user, resetToken):
    msg = Message()
    msg.subject = "Quiet Corner Alerts Password Reset"
    msg.recipients = [user.email]
    msg.sender = 'support@quietcorneralerts.net'
    msg.body = 'Password Reset https://dev-quiet-corner-alerts-etmmu.ondigitalocean.app/reset/'+ resetToken
    mail.send(msg)
    logging.info('Reset email sent to ' + user.dispatcherid + user.email)
