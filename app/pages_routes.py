from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required
from .perms import admin_required

pages = Blueprint("pages", __name__)


@pages.route("/")
def index():
    return render_template("index.html")


@pages.route("/register")
def register():
    return render_template("register.html")


@pages.route("/app")
@jwt_required()
def app():
    return render_template("app.html")


@pages.route("/admin/unconfirmed_users", methods=["GET"])
@jwt_required()
@admin_required()
def unconfirmed_users():
    return "0"
