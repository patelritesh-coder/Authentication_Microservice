from flask import Blueprint, request, jsonify
from ..extensions import db, bcrypt
from ..model.user import User 
from ..services.otp_service import set_user_otp, is_otp_valid, clear_otp
from ..config import Config
from twilio.rest import Client
from datetime import timedelta
from flask_jwt_extended import create_access_token

login_bp = Blueprint('login_bp', __name__)

# Twilio setup
twilio_client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)

# Send OTP via SMS
def send_otp_sms(phone_number, otp):
    try:
        message = twilio_client.messages.create(
            body=f"Your OTP is {otp}. It will expire in 5 minutes.",
            from_=Config.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        return message.sid
    except Exception as e:
        print(f"Twilio error: {e}")
        return None

# Login with Email & Password, Send OTP via SMS
@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid email or password'}), 401

    if not user.is_verified:
        return jsonify({'error': 'Please verify your email first.'}), 403

    otp = set_user_otp(user)
    if not send_otp_sms(user.phone_number, otp):
        return jsonify({'error': 'Failed to send OTP'}), 500

    return jsonify({'message': 'OTP sent to your phone number.'}), 200

# Verify OTP and Return JWT Token
@login_bp.route('/verify-login', methods=['POST'])
def verify_login():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')

    if not email or not otp:
        return jsonify({'error': 'Email and OTP are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if not is_otp_valid(user, otp):
        return jsonify({'error': 'Invalid or expired OTP'}), 400

    clear_otp(user)

    access_token = create_access_token(
        identity=user.email,
        additional_claims={"role": user.role},
        expires_delta=timedelta(hours=1)
    )

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'role': user.role
    }), 200
