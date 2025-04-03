from flask import Flask
from .extensions import db, bcrypt, mail, jwt
from .config import Config
from .routes.auth import auth_bp
from .routes.login import login_bp
from .routes.password import password_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(login_bp, url_prefix='/auth')
    app.register_blueprint(password_bp, url_prefix='/auth')

    with app.app_context():
        db.create_all()

    return app
