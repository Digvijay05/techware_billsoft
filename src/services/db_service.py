"""
Centralized SQLite service.

Every database interaction across the application goes through this module.
All queries use parameterized placeholders to prevent SQL injection.
"""
from __future__ import annotations

import os
import sqlite3
from typing import Any, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Resolve the DB directory relative to the project root, NOT the cwd.
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_DIR = os.path.join(_PROJECT_ROOT, "DB")


def _db_path(name: str) -> str:
    """Return the absolute path to a database file inside DB/."""
    return os.path.join(DB_DIR, name)


def _connect(db_name: str) -> sqlite3.Connection:
    """Open a connection to the given DB file (row_factory enabled)."""
    conn = sqlite3.connect(_db_path(db_name))
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------------------------------------------------
# Schema bootstrap (idempotent)
# ---------------------------------------------------------------------------

_USERS_DDL = """
CREATE TABLE IF NOT EXISTS USERS (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    f_name    VARCHAR(50)  NOT NULL,
    l_name    VARCHAR(50)  NOT NULL,
    contact   VARCHAR(10)  NOT NULL,
    emp_code  VARCHAR(4)   NOT NULL,
    dob       DATE         NOT NULL,
    pass      VARCHAR(50)  NOT NULL
)
"""

_INVOICES_DDL = """
CREATE TABLE IF NOT EXISTS INVOICES (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    Invoice_Type    VARCHAR(500)  NOT NULL,
    Invoice_No      VARCHAR(500)  NOT NULL,
    Invoice_Date    DATE          NOT NULL,
    POS             VARCHAR(500)  NOT NULL,
    Bill_To         VARCHAR(500)  NOT NULL,
    Client_Contact  INT(10)       NOT NULL,
    Client_Name     VARCHAR(500)  NOT NULL,
    Client_Address  VARCHAR(5000) NOT NULL,
    Client_GST      VARCHAR(500)  NOT NULL,
    Sold_By         VARCHAR(500)  NOT NULL,
    Discount        INTEGER       NOT NULL,
    Shipping        INTEGER       NOT NULL,
    SubTotal        INTEGER       NOT NULL,
    Total           INTEGER       NOT NULL,
    Payment_Date    DATE          NOT NULL,
    Payment_Mode    VARCHAR(500)  NOT NULL,
    Payment_No      VARCHAR(500)  NOT NULL,
    Payment_Amount  VARCHAR(500)  NOT NULL,
    Client_Balance  INTEGER       NOT NULL,
    Remarks         VARCHAR(5000) NOT NULL,
    Delivery_Terms  VARCHAR(5000) NOT NULL
)
"""


def ensure_schemas() -> None:
    """Create tables if they do not already exist."""
    with _connect("users.db") as conn:
        conn.execute(_USERS_DDL)
    with _connect("Invoices.db") as conn:
        conn.execute(_INVOICES_DDL)


# ---------------------------------------------------------------------------
# User operations
# ---------------------------------------------------------------------------

def user_exists(emp_code: str) -> bool:
    with _connect("users.db") as conn:
        conn.execute(_USERS_DDL)
        row = conn.execute("SELECT 1 FROM USERS WHERE emp_code = ?", (emp_code,)).fetchone()
        return row is not None


def register_user(f_name: str, l_name: str, contact: str,
                  emp_code: str, dob: str, password: str) -> None:
    with _connect("users.db") as conn:
        conn.execute(_USERS_DDL)
        conn.execute(
            "INSERT INTO USERS (f_name, l_name, contact, emp_code, dob, pass) VALUES (?,?,?,?,?,?)",
            (f_name, l_name, contact, emp_code, dob, password),
        )
        conn.commit()


def authenticate_user(emp_code: str, password: str) -> Optional[dict]:
    """Return a dict of user data if credentials match, else None."""
    with _connect("users.db") as conn:
        conn.execute(_USERS_DDL)
        row = conn.execute(
            "SELECT * FROM USERS WHERE emp_code = ? AND pass = ?",
            (emp_code, password),
        ).fetchone()
        if row:
            return dict(row)
    return None


# ---------------------------------------------------------------------------
# Business / lookup operations
# ---------------------------------------------------------------------------

def get_next_invoice_no() -> str:
    """Read the current invoice number from Business.db → ID table."""
    with _connect("Business.db") as conn:
        row = conn.execute("SELECT * FROM ID WHERE Category = ?", ("Invoice",)).fetchone()
        return row["Id"] if row else "INV1001"


def increment_invoice_no() -> str:
    """Increment the invoice number in Business.db and return the new value."""
    import re
    current = get_next_invoice_no()
    parts = re.findall(r"[^\W\d_]+|\d+", current)
    prefix = parts[0] if parts else "INV"
    num = int(parts[1]) + 1 if len(parts) > 1 else 1001
    new_no = f"{prefix}{num}"
    with _connect("Business.db") as conn:
        conn.execute("UPDATE ID SET Id = ? WHERE Category = ?", (new_no, "Invoice"))
        conn.commit()
    return new_no


def get_categories() -> List[str]:
    """Return list of category names from Business.db → CATEGORY table."""
    with _connect("Business.db") as conn:
        rows = conn.execute("SELECT * FROM CATEGORY").fetchall()
        return [r["Category"] if "Category" in r.keys() else r[1] for r in rows]


def get_units() -> List[str]:
    """Return list of unit names from Business.db → UNIT table."""
    with _connect("Business.db") as conn:
        rows = conn.execute("SELECT * FROM UNIT").fetchall()
        return [r[1] for r in rows]


def get_staff_list() -> List[str]:
    """Return list of employee codes from Employee.db → STAFF table."""
    with _connect("Employee.db") as conn:
        rows = conn.execute("SELECT * FROM STAFF").fetchall()
        return [r[6] for r in rows]


def get_client_names() -> List[str]:
    """Return list of client names from Clients.db → CLIENT table."""
    with _connect("Clients.db") as conn:
        rows = conn.execute("SELECT * FROM CLIENT").fetchall()
        return [r["Full_Name"] if "Full_Name" in r.keys() else r[1] for r in rows]


def get_client_by_name(name: str) -> Optional[dict]:
    """Return full client row as dict."""
    with _connect("Clients.db") as conn:
        row = conn.execute("SELECT * FROM CLIENT WHERE Full_Name = ?", (name,)).fetchone()
        return dict(row) if row else None


def get_item_names() -> List[str]:
    """Return all item names from Items.db → ITEMS table."""
    with _connect("Items.db") as conn:
        rows = conn.execute("SELECT * FROM ITEMS").fetchall()
        return [r[4] for r in rows]


def get_item_by_name(name: str) -> Optional[dict]:
    """Return full item row as dict by item name."""
    with _connect("Items.db") as conn:
        row = conn.execute("SELECT * FROM ITEMS WHERE Item_Name = ?", (name,)).fetchone()
        return dict(row) if row else None


# ---------------------------------------------------------------------------
# Invoice CRUD
# ---------------------------------------------------------------------------

def save_invoice(data: tuple) -> None:
    """Insert a new invoice row into Invoices.db."""
    with _connect("Invoices.db") as conn:
        conn.execute(_INVOICES_DDL)
        conn.execute(
            """INSERT INTO INVOICES (
                Invoice_Type, Invoice_No, Invoice_Date, POS, Bill_To,
                Client_Contact, Client_Name, Client_Address, Client_GST,
                Sold_By, Discount, Shipping, SubTotal, Total,
                Payment_Date, Payment_Mode, Payment_No, Payment_Amount,
                Client_Balance, Remarks, Delivery_Terms
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            data,
        )
        conn.commit()


def update_invoice(data: tuple) -> None:
    """Update an existing invoice. Last element of *data* must be the Invoice_No."""
    with _connect("Invoices.db") as conn:
        conn.execute(_INVOICES_DDL)
        conn.execute(
            """UPDATE INVOICES SET
                Invoice_Type=?, Invoice_No=?, Invoice_Date=?, POS=?, Bill_To=?,
                Client_Contact=?, Client_Name=?, Client_Address=?, Client_GST=?,
                Sold_By=?, Discount=?, Shipping=?, SubTotal=?, Total=?,
                Payment_Date=?, Payment_Mode=?, Payment_No=?, Payment_Amount=?,
                Client_Balance=?, Remarks=?, Delivery_Terms=?
            WHERE Invoice_No=?""",
            data,
        )
        conn.commit()


def get_invoice_by_no(invoice_no: str) -> Optional[dict]:
    with _connect("Invoices.db") as conn:
        conn.execute(_INVOICES_DDL)
        row = conn.execute("SELECT * FROM INVOICES WHERE Invoice_No = ?", (invoice_no,)).fetchone()
        return dict(row) if row else None


def get_all_invoices() -> List[dict]:
    with _connect("Invoices.db") as conn:
        conn.execute(_INVOICES_DDL)
        rows = conn.execute("SELECT * FROM INVOICES").fetchall()
        return [dict(r) for r in rows]


def delete_invoice_by_no(invoice_no: str) -> None:
    with _connect("Invoices.db") as conn:
        conn.execute("DELETE FROM INVOICES WHERE Invoice_No = ?", (invoice_no,))
        conn.commit()


def get_staff_by_code(code: str) -> Optional[dict]:
    with _connect("Employee.db") as conn:
        row = conn.execute("SELECT * FROM STAFF WHERE Employee_Code = ?", (code,)).fetchone()
        return dict(row) if row else None
