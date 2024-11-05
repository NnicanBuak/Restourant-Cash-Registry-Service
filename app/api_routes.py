from .models import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from .models import User, Purchase, PurchaseItem
from .perms import admin_required
from .make_response import make_response, make_error
from datetime import datetime
import json

api = Blueprint('api', __name__)


@api.route("/api/register", methods=["POST"])
def register():
    data = request.args.to_dict()
    new_user = User(
        name=data["name"], passhash=generate_password_hash(data["password"])
    )
    db.session.add(new_user)
    db.session.commit()
    return make_response({"msg": "User created successfully"})


@api.route("/api/login", methods=["GET"])
def login():
    data = request.args.to_dict()
    user = User.query.filter_by(name=data["name"]).first()
    if user and check_password_hash(user.passhash, data["password"]):
        access_token = create_access_token(
            identity={"name": user.name, "is_admin": user.is_admin}
        )
        return jsonify(access_token=access_token), 200
    return make_error({"msg": "Bad username or password"}, 401)


@api.route("/api/confirm_user/<int:user_id>", methods=["POST"])
@jwt_required()
@admin_required()
def confirm_user(user_id):
    user = User.query.get(user_id)

    if user is None:
        return make_error({"msg": "User not found"}, 404)

    user.is_confirmed = True
    db.session.commit()

    return make_response({"msg": f"Пользователь {user.name} был подтверждён.\n "})


@api.route("/api/add_purchase", methods=["POST", "GET"])
def add_purchase():
    data = request.args.to_dict(flat=True)

    try:
        if data['status'] not in Purchase.status_enum:
            return make_error("Error field", 401)
        if data['type'] not in Purchase.type_enum:
            return make_error("Error field", 401)

        purchase = {}

        purchase['customer_id'] = int(data['customer_id'])
        purchase['user_id'] = int(data['user_id'])
        purchase['location_id'] = int(data['location_id'])
        purchase['total_before_tax'] = float(data['total_before_tax'])
        purchase['tax_amount'] = float(data['tax_amount'])
        purchase['total'] = float(data['total'])
        purchase['datetime'] = datetime.strptime(data['datetime'], '%d.%m.%Y')
        purchase['table_number'] = int(data['table_number'])
        purchase['promotion_id'] = int(data['promotion_id'])
        purchase['status'] = data['status']
        purchase['type'] = data['type']
        purchase['delivery_address'] = data['delivery_address']

        new_purchase = Purchase(**purchase)
        prods = json.loads(data['products'])

        db.session.add(new_purchase)
        db.session.commit()

        for product in prods:
            product_id = product['product_id']
            purchase_id = new_purchase.id
            quantity = product['quantity']
            sale_price = product['sale_price']

            item = PurchaseItem(product_id=product_id, purchase_id=purchase_id,
                                quantity=quantity, sale_price=sale_price)
            db.session.add(item)

        db.session.commit()

    except Exception as ex:
        return make_error("Uncaught error", 400)

    return make_response({'id': new_purchase.id})


@api.route("/api/purchases/<int:purchase_id>", methods=["GET"])
def get_purchase(purchase_id):
    purchase = Purchase.query.get(purchase_id)
    if not purchase:
        return make_error({"error": "Purchase not found"}, 404)
    try:
        return make_response({
            "id": purchase.id,
            "customer_id": purchase.customer_id,
            "user_id": purchase.user_id,
            "location_id": purchase.location_id,
            "total_before_tax": purchase.total_before_tax,
            "tax_amount": purchase.tax_amount,
            "total": purchase.total,
            "datetime": purchase.datetime,
            "table_number": purchase.table_number,
            "delivery_address": purchase.delivery_address,
            "promotion_id": purchase.promotion_id,
            "status": purchase.status,
            "type": purchase.type
        })
    except Exception as ex:
        return make_error(ex, 402)


@api.route("/api/purchases/<int:purchase_id>", methods=["DELETE"])
def delete_purchase(purchase_id):
    purchase = Purchase.query.get(purchase_id)
    if not purchase:
        return make_error({"error": "Purchase not found"}, 404)
    db.session.delete(purchase)
    db.session.commit()
    return make_response({"message": "Purchase deleted"})


@api.route("/api/purchase_items/<int:purchase_id>", methods=["GET"])
def get_purchase_item(purchase_id):
    purchase = Purchase.query.get(purchase_id)
    if not purchase:
        return make_error({"error": "Purchase item not found"}, 404)
    mini_items = []
    for item in purchase.purchase_items:
        mini_items.append(
            {
                'id': item.id,
                'purchase_id': item.purchase_id,
                'product_id': item.product_id,
                'quantity': item.quantity,
                'sale_price': item.sale_price
            }
        )
    return make_response(mini_items)