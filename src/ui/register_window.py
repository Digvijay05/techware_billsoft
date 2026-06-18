"""
Registration window – pure PyQt6 UI.

Delegates all logic to auth_controller.
"""
from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox, QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit,
    QMessageBox, QPushButton, QVBoxLayout, QWidget,
)

from src.controllers import auth_controller


class RegisterWindow(QDialog):
    """Modal registration dialog."""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Register – Techware Billing")
        self.setMinimumSize(500, 460)
        self.setModal(True)
        self._build_ui()

    # ── UI ───────────────────────────────────────────────────────────
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(40, 30, 40, 30)
        root.setSpacing(14)

        title = QLabel("Register Here")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #00bfff;")
        root.addWidget(title)

        form = QFormLayout()
        form.setSpacing(10)

        self.fname_input = QLineEdit()
        self.fname_input.setPlaceholderText("First Name")
        form.addRow("First Name:", self.fname_input)

        self.lname_input = QLineEdit()
        self.lname_input.setPlaceholderText("Last Name")
        form.addRow("Last Name:", self.lname_input)

        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("Contact No.")
        form.addRow("Contact No.:", self.contact_input)

        self.emp_code_input = QLineEdit()
        self.emp_code_input.setPlaceholderText("Employee Code")
        form.addRow("Employee Code:", self.emp_code_input)

        self.dob_input = QLineEdit()
        self.dob_input.setPlaceholderText("YYYY-MM-DD")
        form.addRow("Date of Birth:", self.dob_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow("Password:", self.password_input)

        root.addLayout(form)

        # Terms checkbox
        self.terms_check = QCheckBox("I agree to the Terms & Conditions")
        root.addWidget(self.terms_check)

        # Buttons
        btn_row = QHBoxLayout()
        self.register_btn = QPushButton("Register")
        self.register_btn.setProperty("class", "success")
        self.register_btn.clicked.connect(self._on_register)
        btn_row.addWidget(self.register_btn)

        self.login_btn = QPushButton("Back to Login")
        self.login_btn.clicked.connect(self.close)
        btn_row.addWidget(self.login_btn)

        root.addLayout(btn_row)
        root.addStretch()

    # ── Slots ────────────────────────────────────────────────────────
    def _on_register(self):
        success, msg = auth_controller.register(
            first_name=self.fname_input.text().strip(),
            last_name=self.lname_input.text().strip(),
            contact=self.contact_input.text().strip(),
            emp_code=self.emp_code_input.text().strip(),
            dob=self.dob_input.text().strip(),
            password=self.password_input.text().strip(),
            agreed=self.terms_check.isChecked(),
        )
        if success:
            QMessageBox.information(self, "Success", msg)
            self._clear()
        else:
            QMessageBox.warning(self, "Error", msg)

    def _clear(self):
        for w in (self.fname_input, self.lname_input, self.contact_input,
                  self.emp_code_input, self.dob_input, self.password_input):
            w.clear()
        self.terms_check.setChecked(False)
