from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .config import Config
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from .models import db, models_list


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


class DatabaseView(BaseView):
    @expose("/")
    def index(self):
        data = {}
        for model in models_list:
            model_name = model.__tablename__
            entries = db.session.query(model).all()
            data[model_name] = entries
        return self.render("admin/database_view.html", data=data)


admin.add_view(
    CombinedDatabaseView(name="Database Overview", endpoint="database_overview")
)

from . import models, pages_routes, api_routes, perms
from .api_routes import api_blueprint
from .pages_routes import pages_blueprint

app.register_blueprint(api_blueprint)
app.register_blueprint(pages_blueprint)

with app.app_context():
    db.create_all()
