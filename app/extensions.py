from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
jwt = JWTManager()
