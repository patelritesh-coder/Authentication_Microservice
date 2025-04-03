from flask import Blueprint, request, jsonify
from flask import current_app as app
from ..extensions import db, bcrypt
from ..model.user import User
from ..services.email_service import send_reset_email
import jwt
import datetime

password_bp = Blueprint('password_bp', __name__)

# Request Password Reset
@password_bp.route('/request-password-reset', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    email = data.get('email')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Create JWT token valid for 30 minutes
    payload = {
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    send_reset_email(email, token)
    return jsonify({'message': 'Password reset link sent to your email.'}), 200

# Reset Password Using Token
@password_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        email = data.get('email')
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 400
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    new_password = request.get_json().get('new_password')
    if not new_password:
        return jsonify({'error': 'New password is required'}), 400

    user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    db.session.commit()

    return jsonify({'message': 'Password updated successfully.'}), 200
