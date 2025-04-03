import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Basic App Config
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:ritesh123@localhost/users')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email Config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('EMAIL_USER')
    MAIL_PASSWORD = os.getenv('EMAIL_PASS')

    # Twilio Config (Optional, if needed)
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
