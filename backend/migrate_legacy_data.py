import os
import json
import sqlite3
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# Ensure tables are created
models.Base.metadata.create_all(bind=engine)

def migrate_customers(db: Session, details_dir: str):
    """Migrate customers from individual JSON files in Details directory."""
    if not os.path.exists(details_dir):
        print(f"Details directory {details_dir} not found. Skipping customers.")
        return

    migrated = 0
    for filename in os.listdir(details_dir):
        if filename.endswith(".json") and filename != "bill_number.json":
            filepath = os.path.join(details_dir, filename)
            with open(filepath, 'r') as f:
                try:
                    data = json.load(f)
                    
                    phone = data.get("phonenumber")
                    name = data.get("name")
                    address = data.get("Address", "")

                    if phone and name:
                        # Check if customer already exists
                        existing = db.query(models.Customer).filter(models.Customer.phone == phone).first()
                        if not existing:
                            customer = models.Customer(name=name, phone=phone, address=address)
                            db.add(customer)
                            migrated += 1
                except Exception as e:
                    print(f"Failed to migrate {filename}: {e}")
    db.commit()
    print(f"Migrated {migrated} customers.")

def migrate_items(db: Session, items_db_path: str):
    """Migrate items from legacy Items.db to the new schema."""
    if not os.path.exists(items_db_path):
        print(f"Legacy database {items_db_path} not found. Skipping items.")
        return

    conn = sqlite3.connect(items_db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT Category, Sub_Category, Item_Code, Item_Name, Item_Rate, Item_Qty FROM ITEMS")
        rows = cursor.fetchall()
        
        migrated = 0
        for row in rows:
            category_name = row[0]
            item_code = row[2]
            item_name = row[3]
            item_rate = float(row[4])
            
            # Fetch or create category
            category = db.query(models.Category).filter(models.Category.name == category_name).first()
            if not category:
                category = models.Category(name=category_name)
                db.add(category)
                db.commit()
                db.refresh(category)

            # Check if item exists
            existing_item = db.query(models.Item).filter(models.Item.item_code == item_code).first()
            if not existing_item:
                item = models.Item(
                    name=item_name,
                    item_code=item_code,
                    rate=item_rate,
                    category_id=category.id
                )
                db.add(item)
                migrated += 1
                
        db.commit()
        print(f"Migrated {migrated} items.")
    except Exception as e:
        print(f"Failed to migrate items: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    legacy_details_dir = os.path.join(project_root, "Details")
    legacy_items_db = os.path.join(project_root, "DB", "Items.db")
    
    db = SessionLocal()
    try:
        print("Starting legacy data migration...")
        migrate_customers(db, legacy_details_dir)
        migrate_items(db, legacy_items_db)
        print("Migration complete!")
    finally:
        db.close()
