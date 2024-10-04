from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Vendor(db.Model):
    __tablename__ = 'vendors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    contact_details = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    vendor_code = db.Column(db.String, unique=True, nullable=False)
    on_time_delivery_rate = db.Column(db.Float, default=0.0)
    quality_rating_avg = db.Column(db.Float, default=0.0)

class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    po_number = db.Column(db.String, unique=True, nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    delivery_date = db.Column(db.DateTime, nullable=False)
    items = db.Column(db.JSON, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)  # e.g., pending, completed, canceled
    quality_rating = db.Column(db.Float, nullable=True)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    delivered_date = db.Column(db.DateTime, nullable=True)
