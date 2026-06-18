"""
Authentication controller.

Orchestrates login and registration by calling db_service
and returning results that the UI can act upon (no UI code here).
"""
from __future__ import annotations

from typing import Tuple

from src.services import db_service


def register(
    first_name: str,
    last_name: str,
    contact: str,
    emp_code: str,
    dob: str,
    password: str,
    agreed: bool,
) -> Tuple[bool, str]:
    """
    Validate inputs and register a new user.

    Returns (success, message).
    """
    if not all([first_name, last_name, contact, emp_code, dob, password]):
        return False, "All fields are required."
    if not agreed:
        return False, "Please agree to the Terms & Conditions."
    if db_service.user_exists(emp_code):
        return False, "User already exists. Please log in."

    try:
        db_service.register_user(first_name, last_name, contact, emp_code, dob, password)
        return True, "Registration successful!"
    except Exception as e:
        return False, f"Error: {e}"


def login(emp_code: str, password: str) -> Tuple[bool, str]:
    """
    Validate credentials.

    Returns (success, message).
    """
    if not emp_code or not password:
        return False, "Employee code and password are required."

    user = db_service.authenticate_user(emp_code, password)
    if user:
        return True, f"Welcome, {user['f_name']}!"
    return False, "Invalid credentials."
