from flask import Flask
from flask_jwt_extended import JWTManager
from .config import Config
from flask_admin import Admin
from .api_routes import api
from .pages_routes import pages
from .models import db
from .views import *


app = Flask(
    "Restourant Cash Register Service",
    template_folder="app/pages",
    static_folder="app/public",
    static_url_path="",
)
app.config.from_object(Config)
app.register_blueprint(pages)
app.register_blueprint(api)


db.init_app(app)
jwt = JWTManager(app)
admin = Admin(app, name="Ca$hReg Admin", template_mode="bootstrap3")


admin.add_view(DatabaseView(name="Database View", endpoint="database_view"))


with app.app_context():
    db.create_all()
