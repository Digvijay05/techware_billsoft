"""
Login window – pure PyQt6 UI.

Delegates all authentication logic to auth_controller.
"""
from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QDialog, QHBoxLayout, QLabel, QLineEdit, QMessageBox,
    QPushButton, QVBoxLayout, QWidget,
)

from src.controllers import auth_controller


class LoginWindow(QDialog):
    """Modal login dialog."""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Login – Techware Billing")
        self.setMinimumSize(420, 340)
        self.setModal(True)
        self._logged_in = False
        self._build_ui()

    # ── UI construction ──────────────────────────────────────────────
    def _build_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(40, 30, 40, 30)
        root_layout.setSpacing(16)

        # Title
        title = QLabel("Log In")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #0078d4;")
        root_layout.addWidget(title)

        # Employee code
        self.emp_code_input = QLineEdit()
        self.emp_code_input.setPlaceholderText("Enter your Employee Code…")
        root_layout.addWidget(QLabel("Employee Code"))
        root_layout.addWidget(self.emp_code_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your Password…")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        root_layout.addWidget(QLabel("Password"))
        root_layout.addWidget(self.password_input)

        # Buttons
        btn_row = QHBoxLayout()
        self.login_btn = QPushButton("Log In")
        self.login_btn.setProperty("class", "success")
        self.login_btn.clicked.connect(self._on_login)
        btn_row.addWidget(self.login_btn)

        self.register_btn = QPushButton("Sign Up")
        self.register_btn.clicked.connect(self._on_register)
        btn_row.addWidget(self.register_btn)

        root_layout.addLayout(btn_row)
        root_layout.addStretch()

        # Allow pressing Enter to log in
        self.password_input.returnPressed.connect(self._on_login)

    # ── Slots ────────────────────────────────────────────────────────
    def _on_login(self):
        emp = self.emp_code_input.text().strip()
        pwd = self.password_input.text().strip()
        success, msg = auth_controller.login(emp, pwd)
        if success:
            QMessageBox.information(self, "Success", msg)
            self._logged_in = True
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", msg)

    def _on_register(self):
        from src.ui.register_window import RegisterWindow
        dlg = RegisterWindow(self)
        dlg.exec()

    # ── Public API ───────────────────────────────────────────────────
    @property
    def logged_in(self) -> bool:
        return self._logged_in
