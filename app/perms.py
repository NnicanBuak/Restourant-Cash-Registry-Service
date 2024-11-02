from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from .models import User

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            current_user = get_jwt_identity()
            user = User.query.filter_by(username=current_user['name']).first()

            if not user or not user.is_admin:
                return jsonify({"msg": "Только для администраторов"}), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper

def manager_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            current_user = get_jwt_identity()
            user = User.query.filter_by(name=current_user['name']).first()

            if not user or not (user.is_admin or user.is_manager):
                return jsonify({"msg": "Только для менеджеров и администраторов"}), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper