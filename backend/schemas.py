from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


# ---------------------------------------------------------------------------
# Customer
# ---------------------------------------------------------------------------
class CustomerBase(BaseModel):
    name: str
    phone: str
    email: Optional[str] = ""
    address: Optional[str] = ""
    gst_number: Optional[str] = ""

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    gst_number: Optional[str] = None

class Customer(CustomerBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# Category
# ---------------------------------------------------------------------------
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# Item
# ---------------------------------------------------------------------------
class ItemBase(BaseModel):
    name: str
    item_code: Optional[str] = None
    rate: float
    quantity: Optional[int] = 0

class ItemCreate(ItemBase):
    category_id: int

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    item_code: Optional[str] = None
    rate: Optional[float] = None
    quantity: Optional[int] = None
    category_id: Optional[int] = None

class Item(ItemBase):
    id: int
    category_id: int
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# Invoice Item (line item)
# ---------------------------------------------------------------------------
class InvoiceItemBase(BaseModel):
    item_id: int
    quantity: int
    rate: float
    price: float

class InvoiceItemCreate(BaseModel):
    item_id: int
    quantity: int
    rate: float
    price: float

class InvoiceItem(InvoiceItemBase):
    id: int
    invoice_id: int
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# Invoice
# ---------------------------------------------------------------------------
class InvoiceBase(BaseModel):
    invoice_type: str = "GST"
    bill_number: str
    total_amount: float
    sub_total: float = 0.0
    status: str = "UNPAID"
    operation_type: str = "RETAIL"
    discount_amount: float = 0.0
    shipping_amount: float = 0.0
    gst_amount: float = 0.0
    payment_mode: str = "CASH"
    payment_amount: float = 0.0
    payment_reference: str = ""
    remarks: str = ""
    delivery_terms: str = ""
    sold_by: str = ""

class InvoiceCreate(InvoiceBase):
    customer_phone: str  # Look up customer by phone
    items: List[InvoiceItemCreate]

class InvoiceUpdate(BaseModel):
    status: Optional[str] = None
    payment_mode: Optional[str] = None
    payment_amount: Optional[float] = None
    payment_reference: Optional[str] = None
    discount_amount: Optional[float] = None
    shipping_amount: Optional[float] = None
    remarks: Optional[str] = None
    delivery_terms: Optional[str] = None
    delivery_date: Optional[datetime] = None

class Invoice(InvoiceBase):
    id: int
    customer_id: int
    created_at: datetime
    delivery_date: Optional[datetime] = None
    items: List[InvoiceItem] = []
    model_config = ConfigDict(from_attributes=True)

class InvoiceWithCustomer(Invoice):
    """Invoice response that includes customer info."""
    customer: Optional[Customer] = None


# ---------------------------------------------------------------------------
# Staff
# ---------------------------------------------------------------------------
class StaffBase(BaseModel):
    full_name: str
    dob: str = ""
    gender: str = ""
    email: str = ""
    contact: str = ""
    employee_code: Optional[str] = None
    address: str = ""
    join_date: str = ""
    designation: str = ""
    contact_person: str = ""
    contact_person_number: str = ""
    blood_group: str = ""
    document_type: str = ""
    document_no: str = ""
    expiry_date: str = ""
    issue_date: str = ""
    sales_commission: str = ""
    remarks: str = ""

class StaffCreate(StaffBase):
    pass

class StaffUpdate(BaseModel):
    full_name: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    contact: Optional[str] = None
    address: Optional[str] = None
    designation: Optional[str] = None
    remarks: Optional[str] = None

class Staff(StaffBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# Expense
# ---------------------------------------------------------------------------
class ExpenseBase(BaseModel):
    category: str
    amount: float
    description: str = ""

class ExpenseCreate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: int
    date: datetime
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# User (Auth)
# ---------------------------------------------------------------------------
class UserBase(BaseModel):
    first_name: str
    last_name: str = ""
    contact: str = ""
    employee_code: str
    role: str = "cashier"

class UserCreate(UserBase):
    password: str  # plain text; will be hashed before storage

class UserLogin(BaseModel):
    employee_code: str
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: User


# ---------------------------------------------------------------------------
# Lookup Tables
# ---------------------------------------------------------------------------
class LookupBase(BaseModel):
    name: str

class LookupCreate(LookupBase):
    pass

class Lookup(LookupBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------
class ReportSummary(BaseModel):
    total_revenue: float = 0.0
    total_expenses: float = 0.0
    net_profit: float = 0.0
    invoice_count: int = 0
    paid_count: int = 0
    unpaid_count: int = 0

class DashboardStats(BaseModel):
    total_sales: float = 0.0
    total_invoices: int = 0
    total_customers: int = 0
    total_items: int = 0
    unpaid_invoices: int = 0
    total_expenses: float = 0.0
