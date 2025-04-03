from flask import Blueprint, request, jsonify
from ..extensions import db, bcrypt
from ..model.user import User  # Fixed path if it was 'model' instead of 'models'
from ..services.otp_service import set_user_otp, is_otp_valid, clear_otp
from ..services.email_service import send_otp_email
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.role_required import role_required


auth_bp = Blueprint('auth_bp', __name__)

# ✅ User Registration
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if User.query.filter((User.email == data['email']) | (User.phone_number == data['phone_number'])).first():
        return jsonify({'error': 'Email or phone number already registered'}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone_number=data['phone_number'],
        password=hashed_password,
        role=data.get('role', 'employee')
    )

    db.session.add(new_user)
    db.session.commit()

    otp = set_user_otp(new_user)
    send_otp_email(new_user.email, otp)

    return jsonify({'message': 'User registered successfully. Check email for OTP.'}), 201

# ✅ Verify Email with OTP
@auth_bp.route('/verify-email', methods=['POST'])
def verify_email():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if not is_otp_valid(user, otp):
        return jsonify({'error': 'Invalid or expired OTP'}), 400

    user.is_verified = True
    clear_otp(user)

    return jsonify({'message': 'Email verified successfully'}), 200

# ✅ Admin-only route
@auth_bp.route('/admin/dashboard', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def admin_dashboard():
    return jsonify({'message': 'Welcome Admin! You have full access.'})

# ✅ Manager + Admin route
@auth_bp.route('/manager/summary', methods=['GET'])
@jwt_required()
@role_required(['admin', 'manager'])
def manager_summary():
    return jsonify({'message': 'Welcome Manager/Admin! You can manage resources.'})


@auth_bp.route('/update-user', methods=['PUT'])
@jwt_required()
@role_required(['admin'])
def update_user_by_admin():
    data = request.get_json()
    target_email = data.get('email')

    if not target_email:
        return jsonify({'error': 'Email is required'}), 400

    # Get the admin's email from JWT
    current_admin_email = get_jwt_identity()

    # Find target user
    target_user = User.query.filter_by(email=target_email).first()
    if not target_user:
        return jsonify({'error': 'User not found'}), 404

    # Prevent admin from editing themselves via this route
    if target_user.role == 'admin' and target_email == current_admin_email:
        return jsonify({'error': 'You cannot update your own account from this route.'}), 403

    # Prevent admin from editing another admin
    if target_user.role == 'admin':
        return jsonify({'error': 'You are not allowed to update another admin’s information.'}), 403

    # ✅ Update allowed fields
    if 'first_name' in data:
        target_user.first_name = data['first_name']
    if 'last_name' in data:
        target_user.last_name = data['last_name']
    if 'phone_number' in data:
        target_user.phone_number = data['phone_number']
    if 'password' in data:
        target_user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    db.session.commit()
    return jsonify({'message': f"User '{target_email}' updated successfully."}), 200