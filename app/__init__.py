import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import app_config

db = SQLAlchemy()
login_manager= LoginManager()

def create_app(config_name):
    # create and configure the app
   # Les configuration de l'application
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    
    # enregistrement des extension 
    db.init_app(app)
    migrate = Migrate(app, db)
    #bcrypt.init_app(app)
    login_manager.init_app(app)
    # enregistrement des blueprint
    from . import authentification
    app.register_blueprint(authentification.bp)
    
    return app

from . import models