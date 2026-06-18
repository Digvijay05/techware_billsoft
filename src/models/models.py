"""
Data models for the Techware Billing System.
Pure Python dataclasses — no UI or DB dependencies.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class User:
    """Represents a registered employee / user."""
    id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""
    contact: str = ""
    emp_code: str = ""
    dob: str = ""
    password: str = ""


@dataclass
class InvoiceItem:
    """A single line-item inside an invoice."""
    name: str = ""
    unit: str = ""
    rate: float = 0.0
    quantity: float = 0.0
    discount_pct: float = 0.0
    tax_pct: float = 0.0
    cess_pct: float = 0.0
    amount: float = 0.0
    category: str = ""
    sub_category: str = ""
    description: str = ""
    serial_number: str = ""

    # The legacy system stores 12-element lists per item.
    # Index mapping (from techware_invoice.py):
    #  0  name
    #  1  rate
    #  2  quantity
    #  3  price (after tax)
    #  4  discount_amount
    #  5  sub_category
    #  6  category
    #  7  discount_pct
    #  8  tax_pct
    #  9  cess_pct
    # 10  amount (= rate * qty)
    # 11  unit

    def to_legacy_list(self) -> list:
        """Serialize to the 12-element list format used by the JSON files."""
        price = self.amount  # final amount after discount / tax
        discount_amount = self.rate * self.quantity * (self.discount_pct / 100) if self.discount_pct else 0
        base_amount = self.rate * self.quantity
        return [
            self.name,           # 0
            self.rate,           # 1
            self.quantity,       # 2
            price,               # 3
            discount_amount,     # 4
            self.sub_category,   # 5
            self.category,       # 6
            self.discount_pct,   # 7
            self.tax_pct,        # 8
            self.cess_pct,       # 9
            base_amount,         # 10
            self.unit,           # 11
        ]


@dataclass
class InvoiceData:
    """
    Aggregate of all data that constitutes one invoice.
    Used to pass data between controller ↔ service layers.
    """
    invoice_type: str = ""
    invoice_no: str = ""
    invoice_date: str = ""
    place_of_supply: str = ""
    bill_to: str = "cash"           # "cash" | "client"
    client_contact: str = ""
    client_name: str = ""
    client_address: str = ""
    client_gstin: str = ""
    sold_by: str = ""
    discount_total: str = "0"
    shipping_total: str = "0"
    sub_total: str = "0"
    total: str = "0"
    payment_date: str = ""
    payment_mode: str = ""
    txn_id: str = ""
    payment_amount: str = "0"
    client_balance: str = "0"
    remarks: str = ""
    delivery_terms: str = ""

    # Nested items dict keyed by category → item_key → legacy list
    items: dict = field(default_factory=dict)
