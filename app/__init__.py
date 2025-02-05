from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_login import LoginManager

db = SQLAlchemy()
migrate =Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/financontrol'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(24)
    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import Usuario 
        return Usuario.query.get(int(user_id))

    from app import routes
    routes.init_app(app)

    return app

