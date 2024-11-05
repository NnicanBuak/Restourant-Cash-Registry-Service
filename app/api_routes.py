from . import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from .models import User
from .perms import admin_required

api_blueprint = Blueprint("api", __name__)


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    new_user = User(
        name=data["name"], passhash=generate_password_hash(data["password"])
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User created successfully"}), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(name=data["name"]).first()
    if user and check_password_hash(user.passhash, data["password"]):
        access_token = create_access_token(
            identity={"name": user.name, "is_admin": user.is_admin}
        )
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401


@app.route("/api/admin/confirm_user/<int:user_id>", methods=["GET", "POST"])
@jwt_required()
@admin_required()
def confirm_user(user_id):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"msg": "User not found"}), 404

    user.is_confirmed = True
    db.session.commit()

    return jsonify({"msg": f"Пользователь {user.name} был подтверждён.\n "}), 200
