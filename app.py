from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from models import db, Vendor, PurchaseOrder
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vendors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# Vendor Management
@app.route('/api/vendors/', methods=['POST'])
def create_vendor():
    data = request.get_json()
    new_vendor = Vendor(**data)
    db.session.add(new_vendor)
    db.session.commit()
    return jsonify(new_vendor.id), 201

@app.route('/api/vendors/', methods=['GET'])
def list_vendors():
    vendors = Vendor.query.all()
    return jsonify([{ "id": v.id, "name": v.name, "vendor_code": v.vendor_code } for v in vendors])

@app.route('/api/vendors/<int:vendor_id>/', methods=['GET'])
def get_vendor(vendor_id):
    vendor = Vendor.query.get(vendor_id)
    if vendor is None:
        abort(404)
    return jsonify({
        "id": vendor.id,
        "name": vendor.name,
        "contact_details": vendor.contact_details,
        "address": vendor.address,
        "vendor_code": vendor.vendor_code,
        "on_time_delivery_rate": vendor.on_time_delivery_rate,
        "quality_rating_avg": vendor.quality_rating_avg
    })

@app.route('/api/vendors/<int:vendor_id>/', methods=['PUT'])
def update_vendor(vendor_id):
    vendor = Vendor.query.get(vendor_id)
    if vendor is None:
        abort(404)
    data = request.get_json()
    for key, value in data.items():
        setattr(vendor, key, value)
    db.session.commit()
    return jsonify({"message": "Vendor updated"}), 200

@app.route('/api/vendors/<int:vendor_id>/', methods=['DELETE'])
def delete_vendor(vendor_id):
    vendor = Vendor.query.get(vendor_id)
    if vendor is None:
        abort(404)
    db.session.delete(vendor)
    db.session.commit()
    return jsonify({"message": "Vendor deleted"}), 204

# Purchase Order Management
@app.route('/api/purchase_orders/', methods=['POST'])
def create_purchase_order():
    data = request.get_json()
    new_order = PurchaseOrder(**data)
    db.session.add(new_order)
    db.session.commit()

    # Update Vendor Performance Metrics
    update_vendor_performance(new_order.vendor_id)
    
    return jsonify(new_order.id), 201

@app.route('/api/purchase_orders/', methods=['GET'])
def list_purchase_orders():
    vendor_id = request.args.get('vendor_id', type=int)
    if vendor_id:
        orders = PurchaseOrder.query.filter_by(vendor_id=vendor_id).all()
    else:
        orders = PurchaseOrder.query.all()
    return jsonify([{ "id": o.id, "po_number": o.po_number } for o in orders])

@app.route('/api/purchase_orders/<int:po_id>/', methods=['GET'])
def get_purchase_order(po_id):
    order = PurchaseOrder.query.get(po_id)
    if order is None:
        abort(404)
    return jsonify({
        "id": order.id,
        "po_number": order.po_number,
        "vendor_id": order.vendor_id,
        "order_date": order.order_date.isoformat(),
        "delivery_date": order.delivery_date.isoformat(),
        "items": order.items,
        "quantity": order.quantity,
        "status": order.status,
        "quality_rating": order.quality_rating,
        "issue_date": order.issue_date.isoformat(),
        "delivered_date": order.delivered_date.isoformat() if order.delivered_date else None
    })

@app.route('/api/purchase_orders/<int:po_id>/', methods=['PUT'])
def update_purchase_order(po_id):
    order = PurchaseOrder.query.get(po_id)
    if order is None:
        abort(404)
    data = request.get_json()
    for key, value in data.items():
        setattr(order, key, value)
    db.session.commit()

    # Update Vendor Performance Metrics
    update_vendor_performance(order.vendor_id)

    return jsonify({"message": "Purchase Order updated"}), 200

@app.route('/api/purchase_orders/<int:po_id>/', methods=['DELETE'])
def delete_purchase_order(po_id):
    order = PurchaseOrder.query.get(po_id)
    if order is None:
        abort(404)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Purchase Order deleted"}), 204

@app.route('/api/vendors/<int:vendor_id>/performance', methods=['GET'])
def get_vendor_performance(vendor_id):
    vendor = Vendor.query.get(vendor_id)
    if vendor is None:
        abort(404)

    completed_orders = PurchaseOrder.query.filter_by(vendor_id=vendor_id, status='completed').all()
    total_orders = len(completed_orders)
    if total_orders == 0:
        return jsonify({"on_time_delivery_rate": 0, "quality_rating_avg": 0})

    on_time_count = sum(1 for order in completed_orders if order.delivered_date and order.delivered_date <= order.delivery_date)
    on_time_delivery_rate = (on_time_count / total_orders) * 100

    quality_rating_sum = sum(order.quality_rating for order in completed_orders if order.quality_rating is not None)
    quality_rating_avg = quality_rating_sum / total_orders if total_orders > 0 else 0

    return jsonify({
        "on_time_delivery_rate": on_time_delivery_rate,
        "quality_rating_avg": quality_rating_avg
    })

def update_vendor_performance(vendor_id):
    completed_orders = PurchaseOrder.query.filter_by(vendor_id=vendor_id, status='completed').all()
    total_orders = len(completed_orders)
    if total_orders == 0:
        return

    on_time_count = sum(1 for order in completed_orders if order.delivered_date and order.delivered_date <= order.delivery_date)
    on_time_delivery_rate = (on_time_count / total_orders) * 100

    quality_rating_sum = sum(order.quality_rating for order in completed_orders if order.quality_rating is not None)
    quality_rating_avg = quality_rating_sum / total_orders if total_orders > 0 else 0

    vendor = Vendor.query.get(vendor_id)
    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.quality_rating_avg = quality_rating_avg
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
