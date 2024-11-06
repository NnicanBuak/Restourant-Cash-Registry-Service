from .models import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from .models import User, Purchase, PurchaseItem
from .perms import admin_required
from .make_response import make_response

api = Blueprint('api', __name__)


@api.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    new_user = User(
        name=data["name"], passhash=generate_password_hash(data["password"])
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User created successfully"}), 201


@api.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(name=data["name"]).first()
    if user and check_password_hash(user.passhash, data["password"]):
        access_token = create_access_token(
            identity={"name": user.name, "is_admin": user.is_admin}
        )
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401


@api.route("/api/admin/confirm_user/<int:user_id>", methods=["GET", "POST"])
@jwt_required()
@admin_required()
def confirm_user(user_id):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"msg": "User not found"}), 404

    user.is_confirmed = True
    db.session.commit()

    return jsonify({"msg": f"Пользователь {user.name} был подтверждён.\n "}), 200


@api.route("/api/add_purchase", methods=["POST", "GET"])
def add_purchase():
    data = request.args.to_dict(flat=True)
    new_purchase = Purchase(**data)
    db.session.add(new_purchase)
    db.session.commit()
    return make_response({'id': new_purchase.id})


@api.route("/api/purchases/<int:purchase_id>", methods=["GET"])
def get_purchase(purchase_id):
    purchase = Purchase.query.get(purchase_id)
    if not purchase:
        return jsonify({"error": "Purchase not found"}), 404
    return jsonify({
        "id": purchase.id,
        "customer_id": purchase.customer_id,
        "employee_id": purchase.employee_id,
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


@api.route("/api/purchases/<int:purchase_id>", methods=["PUT"])
def update_purchase(purchase_id):
    data = request.json
    purchase = Purchase.query.get(purchase_id)
    if not purchase:
        return jsonify({"error": "Purchase not found"}), 404
    for key, value in data.items():
        setattr(purchase, key, value)
    db.session.commit()
    return jsonify({"message": "Purchase updated"})


@api.route("/api/purchases/<int:purchase_id>", methods=["DELETE"])
def delete_purchase(purchase_id):
    purchase = Purchase.query.get(purchase_id)
    if not purchase:
        return jsonify({"error": "Purchase not found"}), 404
    db.session.delete(purchase)
    db.session.commit()
    return jsonify({"message": "Purchase deleted"})


@api.route("/api/purchase_items", methods=["POST"])
def create_purchase_item():
    data = request.json
    new_purchase_item = PurchaseItem(**data)
    db.session.add(new_purchase_item)
    db.session.commit()
    return jsonify({"id": new_purchase_item.id}), 201


@api.route("/api/purchase_items/<int:purchase_item_id>", methods=["GET"])
def get_purchase_item(purchase_item_id):
    purchase_item = PurchaseItem.query.get(purchase_item_id)
    if not purchase_item:
        return jsonify({"error": "Purchase item not found"}), 404
    return jsonify({
        "id": purchase_item.id,
        "purchase_id": purchase_item.purchase_id,
        "product_id": purchase_item.product_id,
        "quantity": purchase_item.quantity,
        "sale_price": purchase_item.sale_price
    })


@api.route("/api/purchase_items/<int:purchase_item_id>", methods=["PUT"])
def update_purchase_item(purchase_item_id):
    data = request.json
    purchase_item = PurchaseItem.query.get(purchase_item_id)
    if not purchase_item:
        return jsonify({"error": "Purchase item not found"}), 404
    for key, value in data.items():
        setattr(purchase_item, key, value)
    db.session.commit()
    return jsonify({"message": "Purchase item updated"})


@api.route("/api/purchase_items/<int:purchase_item_id>", methods=["DELETE"])
def delete_purchase_item(purchase_item_id):
    purchase_item = PurchaseItem.query.get(purchase_item_id)
    if not purchase_item:
        return jsonify({"error": "Purchase item not found"}), 404
    db.session.delete(purchase_item)
    db.session.commit()
    return jsonify({"message": "Purchase item deleted"})
