from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


# ---------------------------------------------------------------------------
# Customer
# ---------------------------------------------------------------------------
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, default="")
    address = Column(String, default="")
    gst_number = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    invoices = relationship("Invoice", back_populates="customer")


# ---------------------------------------------------------------------------
# Category
# ---------------------------------------------------------------------------
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    items = relationship("Item", back_populates="category")


# ---------------------------------------------------------------------------
# Item
# ---------------------------------------------------------------------------
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    item_code = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    rate = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)  # stock quantity

    category = relationship("Category", back_populates="items")


# ---------------------------------------------------------------------------
# Invoice
# ---------------------------------------------------------------------------
class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_type = Column(String, default="GST")  # GST, NON-GST, ESTIMATE
    bill_number = Column(String, unique=True, index=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    sub_total = Column(Float, default=0.0)
    status = Column(String, default="UNPAID")  # UNPAID, PAID, DELIVERED
    operation_type = Column(String, default="RETAIL")  # RETAIL, WHOLESALE, AGENT
    discount_amount = Column(Float, default=0.0)
    shipping_amount = Column(Float, default=0.0)
    gst_amount = Column(Float, default=0.0)
    payment_mode = Column(String, default="CASH")  # CASH, UPI, CARD, CHEQUE
    payment_amount = Column(Float, default=0.0)
    payment_reference = Column(String, default="")
    remarks = Column(Text, default="")
    delivery_terms = Column(Text, default="")
    sold_by = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    delivery_date = Column(DateTime)

    customer = relationship("Customer", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")


# ---------------------------------------------------------------------------
# Invoice Line Item
# ---------------------------------------------------------------------------
class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    rate = Column(Float, nullable=False)
    price = Column(Float, nullable=False)  # rate * quantity

    invoice = relationship("Invoice", back_populates="items")
    item = relationship("Item")


# ---------------------------------------------------------------------------
# Staff / Employee
# ---------------------------------------------------------------------------
class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    dob = Column(String, default="")
    gender = Column(String, default="")
    email = Column(String, default="")
    contact = Column(String, default="")
    employee_code = Column(String, unique=True, index=True)
    address = Column(String, default="")
    join_date = Column(String, default="")
    designation = Column(String, default="")
    contact_person = Column(String, default="")
    contact_person_number = Column(String, default="")
    blood_group = Column(String, default="")
    document_type = Column(String, default="")
    document_no = Column(String, default="")
    expiry_date = Column(String, default="")
    issue_date = Column(String, default="")
    sales_commission = Column(String, default="")
    remarks = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


# ---------------------------------------------------------------------------
# Expense
# ---------------------------------------------------------------------------
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, default="")
    date = Column(DateTime, default=datetime.utcnow)


# ---------------------------------------------------------------------------
# User (Authentication)
# ---------------------------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, default="")
    contact = Column(String, default="")
    employee_code = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="cashier")  # admin, cashier, manager
    created_at = Column(DateTime, default=datetime.utcnow)


# ---------------------------------------------------------------------------
# Lookup Tables
# ---------------------------------------------------------------------------
class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)


class Designation(Base):
    __tablename__ = "designations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)


class ExpenseCategory(Base):
    __tablename__ = "expense_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)


class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(String, default="")
