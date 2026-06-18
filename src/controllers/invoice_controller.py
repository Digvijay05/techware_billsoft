"""
Invoice controller.

Bridges the Invoice UI with service and database layers.
All item manipulation, pricing calculations, and save/export
orchestration live here.
"""
from __future__ import annotations

import json
import os
from typing import Dict, List, Optional, Tuple

from src.models.models import InvoiceData, InvoiceItem
from src.services import db_service, invoice_service


class InvoiceController:
    """
    Stateful controller for a single invoice editing session.

    The UI creates one instance when the Invoice window opens.
    """

    def __init__(self):
        # Items dict:  category → item_key → legacy 12-element list
        self.categories: List[str] = db_service.get_categories()
        self.items: Dict[str, dict] = {c: {} for c in self.categories}

    # ------------------------------------------------------------------ data
    def get_next_invoice_no(self) -> str:
        return db_service.get_next_invoice_no()

    def get_categories(self) -> List[str]:
        return self.categories

    def get_units(self) -> List[str]:
        return db_service.get_units()

    def get_staff_list(self) -> List[str]:
        return db_service.get_staff_list()

    def get_client_names(self) -> List[str]:
        return db_service.get_client_names()

    def get_item_names(self) -> List[str]:
        return db_service.get_item_names()

    def get_client_info(self, name: str) -> Optional[dict]:
        return db_service.get_client_by_name(name)

    def get_item_info(self, name: str) -> Optional[dict]:
        return db_service.get_item_by_name(name)

    # ------------------------------------------------------------- item mgmt
    def add_item(self, item: InvoiceItem) -> None:
        """Add/replace an item in the internal items dict."""
        cat = item.category or "General"
        if cat not in self.items:
            self.items[cat] = {}
        key = item.name
        self.items[cat][key] = item.to_legacy_list()

    def remove_item(self, category: str, name: str) -> None:
        if category in self.items and name in self.items[category]:
            del self.items[category][name]

    # ----------------------------------------------------------- calculations
    @staticmethod
    def calculate_line_amount(rate: float, qty: float,
                              discount_pct: float = 0,
                              tax_pct: float = 0,
                              cess_pct: float = 0) -> float:
        """Return the final line amount after discount, tax, and cess."""
        base = rate * qty
        disc = base * (discount_pct / 100) if discount_pct else 0
        after_disc = base - disc
        tax = after_disc * (tax_pct / 100) if tax_pct else 0
        cess = after_disc * (cess_pct / 100) if cess_pct else 0
        return round(after_disc + tax + cess, 2)

    def calculate_totals(self, shipping: float = 0,
                         global_discount_pct: float = 0) -> dict:
        """
        Walk all items and compute subtotal, discount, total.

        Returns dict with keys: sub_total, discount, shipping, total.
        """
        sub_total = 0.0
        for cat in self.items.values():
            for lis in cat.values():
                sub_total += float(lis[3])  # price after per-item calcs
        discount = sub_total * (global_discount_pct / 100) if global_discount_pct else 0
        total = sub_total - discount + shipping
        return {
            "sub_total": round(sub_total, 2),
            "discount": round(discount, 2),
            "shipping": round(shipping, 2),
            "total": round(total, 2),
        }

    # ----------------------------------------------------------------- save
    def validate_invoice(self, data: InvoiceData) -> Tuple[bool, str]:
        """Basic validation before saving."""
        if data.invoice_type in ("", "Select"):
            return False, "Invoice Type is required."
        if not data.invoice_no:
            return False, "Invoice No. is required."
        if data.place_of_supply in ("", "Select"):
            return False, "Place of Supply is required."
        if data.payment_mode in ("", "Select"):
            return False, "Payment Mode is required."
        if data.bill_to == "client":
            if not data.client_name or not data.client_address or not data.client_contact:
                return False, "Client details are required for Client A/c."
        return True, ""

    def save_invoice(self, data: InvoiceData) -> Tuple[bool, str]:
        """
        Persist the invoice to DB, save items JSON, generate Excel.

        Returns (success, message).
        """
        ok, msg = self.validate_invoice(data)
        if not ok:
            return False, msg

        values = (
            data.invoice_type, data.invoice_no, data.invoice_date,
            data.place_of_supply, data.bill_to, data.client_contact,
            data.client_name, data.client_address, data.client_gstin,
            data.sold_by, data.discount_total, data.shipping_total,
            data.sub_total, data.total, data.payment_date,
            data.payment_mode, data.txn_id, data.payment_amount,
            data.client_balance, data.remarks, data.delivery_terms,
        )
        try:
            db_service.save_invoice(values)
            invoice_service.save_items_json(data.client_name, data.invoice_no, self.items)
            invoice_service.generate_excel(data.invoice_no, self.items, self.categories)
            db_service.increment_invoice_no()
            return True, "Invoice saved successfully!"
        except Exception as e:
            return False, f"Save failed: {e}"

    def update_invoice(self, data: InvoiceData) -> Tuple[bool, str]:
        ok, msg = self.validate_invoice(data)
        if not ok:
            return False, msg
        values = (
            data.invoice_type, data.invoice_no, data.invoice_date,
            data.place_of_supply, data.bill_to, data.client_contact,
            data.client_name, data.client_address, data.client_gstin,
            data.sold_by, data.discount_total, data.shipping_total,
            data.sub_total, data.total, data.payment_date,
            data.payment_mode, data.txn_id, data.payment_amount,
            data.client_balance, data.remarks, data.delivery_terms,
            data.invoice_no,  # WHERE clause
        )
        try:
            db_service.update_invoice(values)
            invoice_service.save_items_json(data.client_name, data.invoice_no, self.items)
            return True, "Invoice updated!"
        except Exception as e:
            return False, f"Update failed: {e}"
