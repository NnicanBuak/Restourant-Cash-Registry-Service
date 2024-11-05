from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .config import Config
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask('Restourant Cash Register Service', template_folder="app/pages", static_folder="app/public", static_url_path="")
app.config.from_object(Config)

db = SQLAlchemy(app)
jwt = JWTManager(app)

from app import models, page_routes, perms

with app.app_context():
    db.create_all()