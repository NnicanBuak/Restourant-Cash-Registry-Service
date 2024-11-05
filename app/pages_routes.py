from . import app, db
from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required
from .perms import admin_required

pages_blueprint = Blueprint("pages", __name__)


@app.route("/")
def index_page():
    return render_template("index.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/app")
@jwt_required()
def app_page():
    return "0"


@app.route("/admin/unconfirmed_users", methods=["GET"])
@jwt_required()
@admin_required()
def unconfirmed_users_page():
    return "0"
