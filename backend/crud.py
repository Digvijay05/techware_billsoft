from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from hashlib import sha256
import models, schemas


# ===========================================================================
# Customers
# ===========================================================================
def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customer_by_phone(db: Session, phone: str):
    return db.query(models.Customer).filter(models.Customer.phone == phone).first()

def get_customers(db: Session, skip: int = 0, limit: int = 100, search: str = ""):
    q = db.query(models.Customer)
    if search:
        q = q.filter(
            models.Customer.name.ilike(f"%{search}%") |
            models.Customer.phone.ilike(f"%{search}%")
        )
    return q.order_by(models.Customer.id.desc()).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: int, data: schemas.CustomerUpdate):
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return None
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(db_customer, key, val)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int):
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return False
    db.delete(db_customer)
    db.commit()
    return True


# ===========================================================================
# Categories & Items
# ===========================================================================
def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, name: str):
    cat = models.Category(name=name)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

def get_items(db: Session, skip: int = 0, limit: int = 100, search: str = "", category_id: int = None):
    q = db.query(models.Item)
    if search:
        q = q.filter(
            models.Item.name.ilike(f"%{search}%") |
            models.Item.item_code.ilike(f"%{search}%")
        )
    if category_id:
        q = q.filter(models.Item.category_id == category_id)
    return q.order_by(models.Item.id.desc()).offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, data: schemas.ItemUpdate):
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(db_item, key, val)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id)
    if not db_item:
        return False
    db.delete(db_item)
    db.commit()
    return True


# ===========================================================================
# Invoices
# ===========================================================================
def get_invoices(db: Session, skip: int = 0, limit: int = 100, status: str = None, search: str = ""):
    q = db.query(models.Invoice)
    if status:
        q = q.filter(models.Invoice.status == status)
    if search:
        q = q.filter(
            models.Invoice.bill_number.ilike(f"%{search}%")
        )
    return q.order_by(models.Invoice.id.desc()).offset(skip).limit(limit).all()

def get_invoice(db: Session, invoice_id: int):
    return db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()

def get_invoice_by_bill_number(db: Session, bill_number: str):
    return db.query(models.Invoice).filter(models.Invoice.bill_number == bill_number).first()

def create_invoice(db: Session, invoice: schemas.InvoiceCreate):
    db_customer = get_customer_by_phone(db, phone=invoice.customer_phone)
    if not db_customer:
        raise ValueError(f"Customer with phone {invoice.customer_phone} not found")

    invoice_data = invoice.model_dump(exclude={"customer_phone", "items"})
    db_invoice = models.Invoice(customer_id=db_customer.id, **invoice_data)
    db.add(db_invoice)
    db.flush()

    for item in invoice.items:
        db_item = models.InvoiceItem(
            invoice_id=db_invoice.id,
            item_id=item.item_id,
            quantity=item.quantity,
            rate=item.rate,
            price=item.price,
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def update_invoice(db: Session, invoice_id: int, data: schemas.InvoiceUpdate):
    db_invoice = get_invoice(db, invoice_id)
    if not db_invoice:
        return None
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(db_invoice, key, val)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def delete_invoice(db: Session, invoice_id: int):
    db_invoice = get_invoice(db, invoice_id)
    if not db_invoice:
        return False
    db.delete(db_invoice)
    db.commit()
    return True


# ===========================================================================
# Staff
# ===========================================================================
def get_staff_list(db: Session, skip: int = 0, limit: int = 100, search: str = ""):
    q = db.query(models.Staff)
    if search:
        q = q.filter(
            models.Staff.full_name.ilike(f"%{search}%") |
            models.Staff.employee_code.ilike(f"%{search}%") |
            models.Staff.contact.ilike(f"%{search}%")
        )
    return q.order_by(models.Staff.id.desc()).offset(skip).limit(limit).all()

def get_staff(db: Session, staff_id: int):
    return db.query(models.Staff).filter(models.Staff.id == staff_id).first()

def create_staff(db: Session, staff: schemas.StaffCreate):
    db_staff = models.Staff(**staff.model_dump())
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff

def update_staff(db: Session, staff_id: int, data: schemas.StaffUpdate):
    db_staff = get_staff(db, staff_id)
    if not db_staff:
        return None
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(db_staff, key, val)
    db.commit()
    db.refresh(db_staff)
    return db_staff

def delete_staff(db: Session, staff_id: int):
    db_staff = get_staff(db, staff_id)
    if not db_staff:
        return False
    db.delete(db_staff)
    db.commit()
    return True


# ===========================================================================
# Expenses
# ===========================================================================
def get_expenses(db: Session, skip: int = 0, limit: int = 100, category: str = None):
    q = db.query(models.Expense)
    if category:
        q = q.filter(models.Expense.category == category)
    return q.order_by(models.Expense.id.desc()).offset(skip).limit(limit).all()

def get_expense(db: Session, expense_id: int):
    return db.query(models.Expense).filter(models.Expense.id == expense_id).first()

def create_expense(db: Session, expense: schemas.ExpenseCreate):
    db_expense = models.Expense(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def delete_expense(db: Session, expense_id: int):
    db_expense = get_expense(db, expense_id)
    if not db_expense:
        return False
    db.delete(db_expense)
    db.commit()
    return True


# ===========================================================================
# Users (Auth)
# ===========================================================================
def _hash_password(password: str) -> str:
    return sha256(password.encode()).hexdigest()

def get_user_by_code(db: Session, employee_code: str):
    return db.query(models.User).filter(models.User.employee_code == employee_code).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        contact=user.contact,
        employee_code=user.employee_code,
        hashed_password=_hash_password(user.password),
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, employee_code: str, password: str):
    user = get_user_by_code(db, employee_code)
    if user and user.hashed_password == _hash_password(password):
        return user
    return None


# ===========================================================================
# Lookup Tables (Units, Designations, Expense Categories)
# ===========================================================================
def get_units(db: Session):
    return db.query(models.Unit).all()

def create_unit(db: Session, name: str):
    u = models.Unit(name=name)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

def delete_unit(db: Session, unit_id: int):
    u = db.query(models.Unit).filter(models.Unit.id == unit_id).first()
    if not u:
        return False
    db.delete(u)
    db.commit()
    return True

def get_designations(db: Session):
    return db.query(models.Designation).all()

def create_designation(db: Session, name: str):
    d = models.Designation(name=name)
    db.add(d)
    db.commit()
    db.refresh(d)
    return d

def delete_designation(db: Session, designation_id: int):
    d = db.query(models.Designation).filter(models.Designation.id == designation_id).first()
    if not d:
        return False
    db.delete(d)
    db.commit()
    return True

def get_expense_categories(db: Session):
    return db.query(models.ExpenseCategory).all()

def create_expense_category(db: Session, name: str):
    c = models.ExpenseCategory(name=name)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


# ===========================================================================
# Reports / Dashboard
# ===========================================================================
def get_dashboard_stats(db: Session) -> schemas.DashboardStats:
    total_sales = db.query(func.coalesce(func.sum(models.Invoice.total_amount), 0)).scalar()
    total_invoices = db.query(func.count(models.Invoice.id)).scalar()
    total_customers = db.query(func.count(models.Customer.id)).scalar()
    total_items = db.query(func.count(models.Item.id)).scalar()
    unpaid_invoices = db.query(func.count(models.Invoice.id)).filter(
        models.Invoice.status == "UNPAID"
    ).scalar()
    total_expenses = db.query(func.coalesce(func.sum(models.Expense.amount), 0)).scalar()

    return schemas.DashboardStats(
        total_sales=float(total_sales),
        total_invoices=total_invoices,
        total_customers=total_customers,
        total_items=total_items,
        unpaid_invoices=unpaid_invoices,
        total_expenses=float(total_expenses),
    )

def get_report_summary(db: Session, start_date: datetime, end_date: datetime) -> schemas.ReportSummary:
    invoices = db.query(models.Invoice).filter(
        models.Invoice.created_at >= start_date,
        models.Invoice.created_at <= end_date,
    )

    total_revenue = invoices.with_entities(
        func.coalesce(func.sum(models.Invoice.total_amount), 0)
    ).scalar()

    invoice_count = invoices.count()
    paid_count = invoices.filter(models.Invoice.status == "PAID").count()
    unpaid_count = invoices.filter(models.Invoice.status == "UNPAID").count()

    total_expenses = db.query(
        func.coalesce(func.sum(models.Expense.amount), 0)
    ).filter(
        models.Expense.date >= start_date,
        models.Expense.date <= end_date,
    ).scalar()

    return schemas.ReportSummary(
        total_revenue=float(total_revenue),
        total_expenses=float(total_expenses),
        net_profit=float(total_revenue) - float(total_expenses),
        invoice_count=invoice_count,
        paid_count=paid_count,
        unpaid_count=unpaid_count,
    )
