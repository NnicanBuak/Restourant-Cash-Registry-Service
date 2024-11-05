from flask import Flask
from flask_jwt_extended import JWTManager
from .config import Config
from flask_admin import Admin
from .models import db
from .views import *


app = Flask(
    "Restourant Cash Register Service",
    template_folder="app/pages",
    static_folder="app/public",
    static_url_path="",
)
app.config.from_object(Config)


db.init_app(app)
jwt = JWTManager(app)
admin = Admin(app, name="Ca$hReg Admin", template_mode="bootstrap3")


admin.add_view(DatabaseView(name="Database View", endpoint="database_view"))

from .api_routes import api_blueprint
from .pages_routes import pages_blueprint

app.register_blueprint(api_blueprint)
app.register_blueprint(pages_blueprint)

with app.app_context():
    db.create_all()
