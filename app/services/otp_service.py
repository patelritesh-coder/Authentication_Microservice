import random
from datetime import datetime, timedelta

from ..extensions import db
from ..model.user import User

def generate_otp():
    return str(random.randint(100000, 999999))

def set_user_otp(user):
    otp = generate_otp()
    user.otp = otp
    user.otp_created_at = datetime.utcnow()
    db.session.commit()
    return otp

def is_otp_valid(user, otp, expiry_minutes=10):
    if user.otp != otp:
        return False
    if not user.otp_created_at:
        return False
    if datetime.utcnow() > user.otp_created_at + timedelta(minutes=expiry_minutes):
        return False
    return True

def clear_otp(user):
    user.otp = None
    user.otp_created_at = None
    db.session.commit()
