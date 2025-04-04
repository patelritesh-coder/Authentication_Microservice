# Authentication_Microservice

This is a secure and scalable authentication microservice built using **Flask** and **PostgreSQL**, featuring:

- User Registration & Email OTP Verification
- Login via Password + Phone OTP (Twilio)
- Password Reset via Email Link (JWT-based)
- Role-Based Access Control (Admin, Manager, Employee)
- Admin-only account update with full validation

---

## 🚀 Features

- ✅ User Registration with OTP Email Verification
- ✅ JWT-based Login with OTP via Twilio SMS
- ✅ Secure Password Reset with Tokenized Email Links
- ✅ Role-Based Access Control (RBAC)
- ✅ Admin-only Protected Routes
- ✅ PostgreSQL Integration with SQLAlchemy

---

## 🏗️ Tech Stack

- **Flask** + **Flask-JWT-Extended**
- **Flask-Mail** for emails
- **Twilio API** for OTP via SMS
- **PostgreSQL** with SQLAlchemy ORM
- **Flask-Bcrypt** for secure password hashing
- **JWT** for stateless authentication

---

## API Endpoints
- Method - [POST] http://127.0.0.1:5000/auth/register  -- User Register
- Method - [POST] http://127.0.0.1:5000/auth/verify-email  -- User Email Verify
- Method - [POST] http://127.0.0.1:5000/auth/login  --Log in
- Method - [POST] http://127.0.0.1:5000/auth/verify-login  --Log in Verify OTP
- Method - [POST] http://127.0.0.1:5000/auth/request-password-reset  -- Password Reset Link Sent
- Method - [PUT]  http://127.0.0.1:5000/auth/update-user  -- User Data Update by only Admin
- Method - [GET]  http://127.0.0.1:5000/auth/admin/dashboard  -- Admin Dashboard
- Method - [POST] http://127.0.0.1:5000/auth/reset-password/<token>  -- Reset Password Set
