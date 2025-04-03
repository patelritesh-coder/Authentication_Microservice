from flask_mail import Message
from flask import current_app, url_for
from ..extensions import mail
from ..config import Config

def send_otp_email(to_email, otp):
    subject = "Your OTP Code"
    body = f"Your OTP is {otp}. It will expire in 5 minutes."

    msg = Message(subject, sender=Config.MAIL_USERNAME, recipients=[to_email])
    msg.body = body

    mail.send(msg)

def send_reset_email(to_email, token):
    reset_link = url_for('password_bp.reset_password', token=token, _external=True)
    subject = "Reset Your Password"
    html = f"""
    <html>
        <body>
            <p>Click the link below to reset your password:</p>
            <a href="{reset_link}" target="_blank">Reset Password</a>
        </body>
    </html>
    """
    msg = Message(subject, sender=Config.MAIL_USERNAME, recipients=[to_email])
    msg.html = html

    mail.send(msg)
