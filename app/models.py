from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.db.Integer, primary_key=True)
    name = db.Column(db.db.String(80), unique=True, nullable=False)
    passhash = db.Column(db.db.String(120), nullable=False)
    is_confirmed = db.Column(db.Boolean, default=False, nullable=False)
    is_employee = db.Column(db.Boolean, default=False, nullable=False)
    is_manager = db.Column(db.Boolean, default=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=db.DateTime.now(timezone.utc))

    locations = db.relationship(
        "Location",
        secondary="user_location",
        back_populates="users",
        foreign_keys="[UserLocation.user_id, UserLocation.location_id]",
    )
    purchases = db.relationship("Purchase", back_populates="user")
    stop_list = db.relationship("StopList", back_populates="user")
    stop_list_history = db.relationship("StopListHistory", back_populates="user")


class Location(db.Model):
    __tablename__ = "location"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    tax_id = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=db.DateTime.now(timezone.utc))

    users = db.relationship(
        "User",
        secondary="user_location",
        back_populates="locations",
        foreign_keys="[UserLocation.user_id, UserLocation.location_id]",
    )
    stop_list = db.relationship(
        "StopList", back_populates="location", cascade="all, delete-orphan"
    )
    stop_list_history = db.relationship(
        "StopListHistory", back_populates="location", cascade="all, delete-orphan"
    )


class UserLocation(db.Model):
    __tablename__ = "user_location"

    user_id = db.Column(db.db.Integer, db.ForeignKey("user.id"), primary_key=True)
    location_id = db.Column(
        db.db.Integer, db.ForeignKey("location.id"), primary_key=True
    )
    created_at = db.Column(db.DateTime, default=db.DateTime.now(timezone.utc))


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    price = db.Column(db.Float(asdecimal=True), nullable=False)
    created_at = db.Column(db.DateTime, default=db.DateTime.now(timezone.utc))

    stop_list = db.relationship("StopList", cascade="all, delete-orphan")
    purchases = db.relationship("PurchaseItem")


class StopList(db.Model):
    __tablename__ = "stop_list"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    remaining_quantity = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=db.DateTime.now(timezone.utc))

    product = db.relationship("Product", back_populates="stop_list")
    location = db.relationship("Location", back_populates="stop_list")
    user = db.relationship("User", back_populates="stop_list")


class StopListHistory(db.Model):
    action_enum = ["added", "removed"]

    __tablename__ = "stop_list_history"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    action = db.Column(db.Enum(*action_enum), nullable=False)
    remaining_quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.DateTime.now(timezone.utc))

    product = db.relationship("Product")
    location = db.relationship("Location")
    user = db.relationship("User")


class Customer(db.Model):
    __tablename__ = "customer"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    phone_number = db.Column(db.String, nullable=False)
    delivery_address = db.Column(db.String, nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    block_status = db.Column(db.Boolean, default=False, nullable=False)
    discount = db.Column(db.db.Float(asdecimal=True), default=0)
    note = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=db.DateTime.now(timezone.utc))

    purchases = db.relationship(
        "Purchase", back_populates="customer", cascade="all, delete-orphan"
    )


class Purchase(db.Model):
    status_enum = [
        "accepted",
        "cancelled",
        "preparing",
        "prepared",
        "closed",
        "refunded",
    ]
    type_enum = ["dine-in", "delivery"]

    __tablename__ = "purchase"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    location_id = db.Column(db.String, db.ForeignKey("location.id"), nullable=False)
    promotion_id = db.Column(db.Integer, db.ForeignKey("promotion.id"), nullable=True)
    table_number = db.Column(db.Integer, nullable=True)
    type = db.Column(db.Enum(*type_enum), nullable=False)
    status = db.Column(db.Enum(*status_enum), nullable=False)
    delivery_address = db.Column(db.String, nullable=True)
    total_before_tax = db.Column(db.Float(asdecimal=True), nullable=False)
    tax_amount = db.Column(db.Float(asdecimal=True), nullable=False)
    total = db.Column(db.Float(asdecimal=True), nullable=False)
    created_at = db.Column(db.DateTime, default=db.DateTime.now(timezone.utc))

    customer = db.relationship("Customer", cascade="save-update")
    purchase_items = db.relationship(
        "PurchaseItem", cascade="save-update, delete-orphan"
    )
    user = db.relationship("User", cascade="none")
    promotion = db.relationship("Promotion", cascade="none")


class PurchaseItem(db.Model):
    __tablename__: str = "purchase_item"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey("purchase.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    sale_price = db.Column(db.Float(asdecimal=True), nullable=False)
    created_at = db.Column(db.DateTime, default=db.DateTime.now(timezone.utc))

    purchase = db.relationship("Purchase", back_populates="purchase_items")
    product = db.relationship(
        "Product", back_populates="purchases", overlaps="purchases"
    )


class Promotion(db.Model):
    __tablename__: str = "promotion"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    discount_percentage = db.Column(db.Float(asdecimal=True), nullable=True)
    discount_value = db.Column(db.Integer, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=db.DateTime.now(timezone.utc))
