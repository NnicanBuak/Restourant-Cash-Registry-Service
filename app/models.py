from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, Enum, Date, DateTime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default='client')

class Category(db.Model):
    __tablename__: str = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    products = relationship('Product', back_populates='category')

class Product(db.Model):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    price = Column(Float(asdecimal=True), nullable=False)
    quantity = Column(Integer, nullable=False)

    category = relationship('Category', back_populates='products')
    stop_list = relationship('StopList', back_populates='product')
    purchase_items = relationship('PurchaseItem', back_populates='product')

class StopList(db.Model):
    __tablename__ = 'stop_list'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    remaining_quantity = Column(Integer, nullable=False)
    date_added = Column(DateTime, default=datetime.now(timezone.utc))

    product = relationship('Product', back_populates='stop_list')

class StopListHistory(db.Model):
    __tablename__ = 'stop_list_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)
    action = Column(Enum("added", "removed"), nullable=False)
    quantity = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))

    product = relationship('Product')
    employee = relationship('Employee')

class Customer(db.Model):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    delivery_address = Column(String, nullable=False)
    birthday = Column(Date, nullable=True)
    block_status = Column(Boolean, default=False)
    discount = Column(Float(asdecimal=True), default=0)
    note = Column(String, nullable=True)

    purchases = relationship('Purchase', back_populates='customer')

class Purchase(db.Model):
    __tablename__: str = 'purchase'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)
    total_before_tax = Column(Float(asdecimal=True), nullable=False)
    tax_amount = Column(Float(asdecimal=True), nullable=False)
    date = Column(DateTime, default=datetime.now(timezone.utc))
    location = Column(String, nullable=False)
    total = Column(Float(asdecimal=True), nullable=False)
    table_number = Column(Integer, nullable=True)
    delivery_address = Column(String, nullable=True)
    promotion_id = Column(Integer, ForeignKey('promotion.id'), nullable=True)
    status = Column(Enum("accepted", "cancelled", "preparing", "prepared", "closed", "refunded"), nullable=False)
    type = Column(Enum("dine-in", "delivery"), nullable=False)

    customer = relationship('Customer', back_populates='purchases')
    employee = relationship('Employee')
    purchase_items = relationship('PurchaseItem', back_populates='purchase')

class PurchaseItem(db.Model):
    __tablename__: str = 'purchase_item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    purchase_id = Column(Integer, ForeignKey('purchase.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    sale_price = Column(Float(asdecimal=True), nullable=False)

    purchase = relationship('Purchase', back_populates='purchase_items')
    product = relationship('Product')

class Employee(db.Model):
    __tablename__: str = 'employee'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    position = Column(String, nullable=False)

    stop_list_history = relationship('StopListHistory', back_populates='employee')

class Promotion(db.Model):
    __tablename__: str = 'promotion'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    discount_percentage = Column(Float(asdecimal=True), nullable=True)
    discount_value = Column(Integer, nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

class BranchInfo(db.Model):
    __tablename__: str = 'branch_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    tax_id = Column(String, nullable=False)
    address = Column(String, nullable=False)
