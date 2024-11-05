from . import admin, db
from flask_admin.contrib.sqla import ModelView
from .models import models

for model in models:
  admin.add_view(ModelView(model, db.session))