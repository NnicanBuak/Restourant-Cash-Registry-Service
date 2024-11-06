from flask_admin import AdminIndexView, expose
from .models import Customer, Purchase


class DashboardView(AdminIndexView):
    @expose("/")
    def dashboard(self):
        customer_count = Customer.query.count()
        purchase_count = Purchase.query.count()
        return self.render(
            "admin/index.html",
            customer_count=customer_count,
            purchase_count=purchase_count,
        )
