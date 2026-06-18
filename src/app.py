"""
Application entry point.

Creates the QApplication, shows the login dialog,
then opens the main invoice window on success.
"""
from __future__ import annotations

import os
import sys

# Ensure the project root is on sys.path so that ``from src.…`` works
# regardless of where the script is invoked from.
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from PyQt6.QtWidgets import QApplication

from src.services import db_service
from src.ui.login_window import LoginWindow
from src.ui.dashboard_window import DashboardWindow
from src.utils.constants import APP_STYLESHEET


def main():
    # Bootstrap DB schemas on first run
    db_service.ensure_schemas()

    app = QApplication(sys.argv)
    app.setApplicationName("Techware Billing System")
    app.setStyleSheet(APP_STYLESHEET)

    # ── Login gate ──
    login = LoginWindow()
    if login.exec() and login.logged_in:
        window = DashboardWindow()
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
