from ..extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    
    password = db.Column(db.String(255), nullable=False)
    otp = db.Column(db.String(6), nullable=True)
    otp_created_at = db.Column(db.DateTime, nullable=True)
    
    is_verified = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(20), default='user')  # e.g., admin, manager, user

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
