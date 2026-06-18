"""
Application-wide QSS (Qt Style Sheet) and constants.
"""

# Indian states list for Place of Supply dropdown
INDIAN_STATES = [
    "Select",
    "Andaman and Nicobar", "Andhra Pradesh", "Arunachal Pradesh",
    "Assam", "Bihar", "Chandigarh", "Chhattisgarh",
    "Dadra and Nagar Haveli", "Daman and Diu", "Delhi", "Goa",
    "Gujarat", "Haryana", "Himachal Pradesh", "Jammu & Kashmir",
    "Jharkhand", "Karnataka", "Kerala", "Lakshadweep",
    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya",
    "Mizoram", "Nagaland", "Odisha", "Puducherry", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal",
]

PAYMENT_MODES = [
    "Select", "Cash", "Cheque", "Card",
    "Demand Draft", "Mobile Wallet", "Bank Transfer",
]

INVOICE_TYPES = ["Select", "GST", "Non-GST", "Bill of Supply"]

# -----------------------------------------------------------------
# Application-wide QSS
# -----------------------------------------------------------------
APP_STYLESHEET = """
/* ── Global ── */
QWidget {
    font-family: "Segoe UI", "Calibri", sans-serif;
    font-size: 13px;
    color: #222222;
}

/* ── Main window / dialogs ── */
QMainWindow, QDialog {
    background-color: #f5f7fa;
}

/* ── Group boxes (replacing LabelFrame) ── */
QGroupBox {
    font-weight: bold;
    border: 1px solid #c0c0c0;
    border-radius: 6px;
    margin-top: 12px;
    padding: 14px 8px 8px 8px;
    background: #ffffff;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 14px;
    padding: 0 6px;
    color: #333;
}

/* ── Labels ── */
QLabel {
    color: #222222;
}

/* ── Line edits ── */
QLineEdit, QComboBox, QDateEdit, QSpinBox {
    border: 1px solid #bbb;
    border-radius: 4px;
    padding: 4px 8px;
    background: white;
    color: #222222;
    min-height: 28px;
}
QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
    border: 1.5px solid #0078d4;
}

/* ── Buttons (primary) ── */
QPushButton {
    border: none;
    border-radius: 5px;
    padding: 8px 18px;
    font-weight: 600;
    color: white;
    background-color: #0078d4;
    min-height: 32px;
}
QPushButton:hover {
    background-color: #106ebe;
}
QPushButton:pressed {
    background-color: #005a9e;
}
QPushButton:disabled {
    background-color: #cccccc;
    color: #888;
}

/* ── Success button ── */
QPushButton[class="success"] {
    background-color: #11481a;
}
QPushButton[class="success"]:hover {
    background-color: #096119;
}

/* ── Danger button ── */
QPushButton[class="danger"] {
    background-color: #c42b1c;
}
QPushButton[class="danger"]:hover {
    background-color: #a31b10;
}

/* ── Table ── */
QTableWidget {
    border: 1px solid #ccc;
    gridline-color: #e0e0e0;
    alternate-background-color: #f0f4f8;
    selection-background-color: #cce4f7;
    selection-color: #000;
    background: white;
}
QHeaderView::section {
    background-color: #e8ecef;
    padding: 6px;
    border: 1px solid #ccc;
    font-weight: 600;
}

/* ── Check boxes ── */
QCheckBox {
    spacing: 6px;
}

/* ── Radio buttons ── */
QRadioButton {
    spacing: 6px;
}

/* ── Scroll area ── */
QTextEdit {
    border: 1px solid #bbb;
    border-radius: 4px;
    padding: 4px;
    background: white;
    color: #222222;
}
"""
