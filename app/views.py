# views.py
from flask_admin import BaseView, expose
from .models import db, models_list

class DatabaseView(BaseView):
    @expose("/")
    def index(self):
        data = {}
        for model in models_list:
            model_name = model.__tablename__
            entries = db.session.query(model).all()
            if not entries:
                return self.render("admin/database_view.html", data={}, message="Нет данных для отображения")
            data[model_name] = entries
        return self.render("admin/database_view.html", data=data)
