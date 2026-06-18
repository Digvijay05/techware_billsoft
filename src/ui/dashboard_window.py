"""
Dashboard window – central application hub.

Provides navigation to New Invoice, View Invoices, and other modules.
"""
from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout, QLabel, QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget,
)

from src.ui.invoice_window import InvoiceWindow


class DashboardWindow(QMainWindow):
    """Main dashboard hub after login."""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Dashboard – Techware Billing")
        self.setMinimumSize(800, 500)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        # Title
        title = QLabel("Techware Billing Dashboard")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #0078d4; margin-bottom: 20px;")
        main_layout.addWidget(title)

        # Buttons layout
        btn_layout = QVBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_layout.setSpacing(15)

        self.btn_new_invoice = QPushButton("📄 Create New Invoice")
        self.btn_new_invoice.setMinimumSize(300, 50)
        self.btn_new_invoice.setStyleSheet("font-size: 16px;")
        self.btn_new_invoice.clicked.connect(self._open_new_invoice)
        btn_layout.addWidget(self.btn_new_invoice)

        self.btn_view_invoices = QPushButton("📂 View Past Invoices")
        self.btn_view_invoices.setMinimumSize(300, 50)
        self.btn_view_invoices.setStyleSheet("font-size: 16px;")
        self.btn_view_invoices.clicked.connect(self._open_view_invoices)
        btn_layout.addWidget(self.btn_view_invoices)

        self.btn_logout = QPushButton("🚪 Logout")
        self.btn_logout.setMinimumSize(300, 50)
        self.btn_logout.setStyleSheet("font-size: 16px; background-color: #c42b1c;")
        self.btn_logout.clicked.connect(self.close)
        btn_layout.addWidget(self.btn_logout)

        main_layout.addLayout(btn_layout)
        main_layout.addStretch()

    def _open_new_invoice(self):
        self.invoice_win = InvoiceWindow(self)
        self.invoice_win.show()

    def _open_view_invoices(self):
        QMessageBox.information(
            self, 
            "Coming Soon", 
            "The 'Show Invoices' Qt port is currently under development.\n\n"
            "Please check the original 'show_invoices.py' script for legacy access."
        )
