from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .config import Config
from flask_admin import Admin


app = Flask(
    "Restourant Cash Register Service",
    template_folder="app/pages",
    static_folder="app/public",
    static_url_path="",
)
app.config.from_object(Config)


db = SQLAlchemy(app)
jwt = JWTManager(app)
admin = Admin(app, name='MyApp Admin', template_mode='bootstrap3')

from app import models, pages_routes, api_routes, perms
from app.api_routes import api_blueprint
from app.pages_routes import pages_blueprint

app.register_blueprint(api_blueprint)
app.register_blueprint(pages_blueprint)

with app.app_context():
    db.create_all()
