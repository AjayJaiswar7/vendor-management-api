from app import app, db
from models import Vendor, PurchaseOrder
from datetime import datetime

with app.app_context():
    db.create_all()

    # Add sample vendors
    vendor1 = Vendor(
        name="Vendor A",
        contact_details="123456789",
        address="123 Street",
        vendor_code="VENDOR_A",
        on_time_delivery_rate=90.0,
        quality_rating_avg=4.5
    )
    vendor2 = Vendor(
        name="Vendor B",
        contact_details="987654321",
        address="456 Avenue",
        vendor_code="VENDOR_B",
        on_time_delivery_rate=85.0,
        quality_rating_avg=4.0
    )
    
    db.session.add(vendor1)
    db.session.add(vendor2)
    
    # Add sample purchase orders
    po1 = PurchaseOrder(
        po_number="PO001",
        vendor_id=1,
        order_date=datetime.utcnow(),
        delivery_date=datetime.utcnow(),
        items={"item1": {"name": "Item A", "price": 100}},
        quantity=10,
        status="completed",
        quality_rating=4.5
    )
    
    po2 = PurchaseOrder(
        po_number="PO002",
        vendor_id=2,
        order_date=datetime.utcnow(),
        delivery_date=datetime.utcnow(),
        items={"item2": {"name": "Item B", "price": 150}},
        quantity=5,
        status="completed",
        quality_rating=4.0
    )
    
    db.session.add(po1)
    db.session.add(po2)
    
    db.session.commit()
    print("Database and tables created with sample data.")
