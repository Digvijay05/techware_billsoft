"""
Invoice window – the core of the billing application.

Pure PyQt6 UI.  All business logic is delegated to InvoiceController.
Replaces the 1 800-line monolithic techware_invoice.py.
"""
from __future__ import annotations

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox, QComboBox, QDateEdit, QDialog, QFormLayout,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMessageBox, QPushButton, QRadioButton,
    QSizePolicy, QTableWidget, QTableWidgetItem, QTextEdit,
    QVBoxLayout, QWidget,
)

from src.controllers.invoice_controller import InvoiceController
from src.models.models import InvoiceData, InvoiceItem
from src.utils.constants import INDIAN_STATES, INVOICE_TYPES, PAYMENT_MODES


# ─── Worker thread for heavy I/O ────────────────────────────────────
class _SaveWorker(QThread):
    finished = pyqtSignal(bool, str)

    def __init__(self, ctrl: InvoiceController, data: InvoiceData):
        super().__init__()
        self.ctrl = ctrl
        self.data = data

    def run(self):
        ok, msg = self.ctrl.save_invoice(self.data)
        self.finished.emit(ok, msg)


# ─── Main Invoice Window ────────────────────────────────────────────
class InvoiceWindow(QMainWindow):
    """Full invoice creation / editing window."""

    TABLE_COLUMNS = [
        "No.", "Name", "Unit", "Rate", "Quantity",
        "Discount %", "Tax %", "CESS %", "Amount",
        "Sub-Category", "Category",
    ]

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("New Invoice – Techware Billing")
        self.resize(1200, 720)
        self.ctrl = InvoiceController()
        self._item_counter = 0
        self._build_ui()
        self._populate_dropdowns()

    # ================================================================
    # UI CONSTRUCTION
    # ================================================================
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(10, 10, 10, 10)

        main_layout.addWidget(self._build_invoice_info())
        main_layout.addWidget(self._build_particulars(), stretch=1)

        bottom = QHBoxLayout()
        bottom.addWidget(self._build_remarks(), stretch=1)
        bottom.addWidget(self._build_delivery_terms(), stretch=1)
        bottom.addWidget(self._build_payment(), stretch=1)
        bottom.addWidget(self._build_totals(), stretch=1)
        main_layout.addLayout(bottom)
        main_layout.addLayout(self._build_action_buttons())

    # ── Invoice Information ─────────────────────────────────────────
    def _build_invoice_info(self) -> QGroupBox:
        grp = QGroupBox("Invoice Information")
        grid = QGridLayout(grp)
        grid.setSpacing(8)

        # Row 0
        grid.addWidget(QLabel("Invoice Type *"), 0, 0)
        self.invoice_type_combo = QComboBox()
        self.invoice_type_combo.addItems(INVOICE_TYPES)
        grid.addWidget(self.invoice_type_combo, 1, 0)

        grid.addWidget(QLabel("Invoice No. *"), 0, 1)
        self.invoice_no_edit = QLineEdit()
        grid.addWidget(self.invoice_no_edit, 1, 1)

        grid.addWidget(QLabel("Date"), 0, 2)
        self.invoice_date_edit = QDateEdit()
        self.invoice_date_edit.setCalendarPopup(True)
        from PyQt6.QtCore import QDate
        self.invoice_date_edit.setDate(QDate.currentDate())
        grid.addWidget(self.invoice_date_edit, 1, 2)

        grid.addWidget(QLabel("Place of Supply *"), 0, 3)
        self.pos_combo = QComboBox()
        self.pos_combo.addItems(INDIAN_STATES)
        self.pos_combo.setCurrentIndex(29)  # default Uttar Pradesh
        self.pos_combo.setEditable(True)
        grid.addWidget(self.pos_combo, 1, 3)

        # Bill To radio
        grid.addWidget(QLabel("Bill To *"), 0, 4)
        bill_to_w = QWidget()
        bill_h = QHBoxLayout(bill_to_w)
        bill_h.setContentsMargins(0, 0, 0, 0)
        self.client_radio = QRadioButton("Client A/c")
        self.cash_radio = QRadioButton("Cash A/c")
        self.cash_radio.setChecked(True)
        self.client_radio.toggled.connect(self._on_bill_to_changed)
        bill_h.addWidget(self.client_radio)
        bill_h.addWidget(self.cash_radio)
        grid.addWidget(bill_to_w, 1, 4)

        # Row 2
        grid.addWidget(QLabel("Contact *"), 2, 0)
        self.contact_edit = QLineEdit()
        grid.addWidget(self.contact_edit, 3, 0)

        grid.addWidget(QLabel("Client Name *"), 2, 1)
        self.client_name_combo = QComboBox()
        self.client_name_combo.setEditable(True)
        self.client_name_combo.currentTextChanged.connect(self._on_client_selected)
        grid.addWidget(self.client_name_combo, 3, 1)

        grid.addWidget(QLabel("Client Address"), 2, 2)
        self.client_address_edit = QLineEdit()
        grid.addWidget(self.client_address_edit, 3, 2)

        grid.addWidget(QLabel("Client GSTIN"), 2, 3)
        self.client_gstin_edit = QLineEdit()
        grid.addWidget(self.client_gstin_edit, 3, 3)

        grid.addWidget(QLabel("Sold By"), 2, 4)
        self.sold_by_combo = QComboBox()
        grid.addWidget(self.sold_by_combo, 3, 4)

        return grp

    # ── Particulars (items table + input row) ───────────────────────
    def _build_particulars(self) -> QGroupBox:
        grp = QGroupBox("Particulars")
        layout = QVBoxLayout(grp)

        # Input row
        input_grid = QGridLayout()
        input_grid.setSpacing(6)

        input_grid.addWidget(QLabel("Item Code"), 0, 0)
        self.item_code_edit = QLineEdit()
        input_grid.addWidget(self.item_code_edit, 1, 0)

        input_grid.addWidget(QLabel("Item Name *"), 0, 1)
        self.item_name_combo = QComboBox()
        self.item_name_combo.setEditable(True)
        self.item_name_combo.currentTextChanged.connect(self._on_item_selected)
        input_grid.addWidget(self.item_name_combo, 1, 1)

        input_grid.addWidget(QLabel("Unit *"), 0, 2)
        self.unit_combo = QComboBox()
        self.unit_combo.setEditable(True)
        input_grid.addWidget(self.unit_combo, 1, 2)

        input_grid.addWidget(QLabel("Quantity *"), 0, 3)
        self.qty_edit = QLineEdit()
        self.qty_edit.setPlaceholderText("0")
        input_grid.addWidget(self.qty_edit, 1, 3)

        input_grid.addWidget(QLabel("Rate *"), 0, 4)
        self.rate_edit = QLineEdit()
        self.rate_edit.setPlaceholderText("0.00")
        input_grid.addWidget(self.rate_edit, 1, 4)

        input_grid.addWidget(QLabel("Category"), 0, 5)
        self.category_combo = QComboBox()
        input_grid.addWidget(self.category_combo, 1, 5)

        input_grid.addWidget(QLabel("Sub-Cat"), 0, 6)
        self.sub_category_combo = QComboBox()
        self.sub_category_combo.setEditable(True)
        input_grid.addWidget(self.sub_category_combo, 1, 6)

        input_grid.addWidget(QLabel("Disc %"), 0, 7)
        self.discount_edit = QLineEdit()
        self.discount_edit.setPlaceholderText("0")
        input_grid.addWidget(self.discount_edit, 1, 7)

        input_grid.addWidget(QLabel("Tax %"), 0, 8)
        self.tax_edit = QLineEdit()
        self.tax_edit.setPlaceholderText("0")
        input_grid.addWidget(self.tax_edit, 1, 8)

        input_grid.addWidget(QLabel("CESS %"), 0, 9)
        self.cess_edit = QLineEdit()
        self.cess_edit.setPlaceholderText("0")
        input_grid.addWidget(self.cess_edit, 1, 9)

        input_grid.addWidget(QLabel("Amount"), 0, 10)
        self.amount_label = QLabel("0.00")
        self.amount_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        input_grid.addWidget(self.amount_label, 1, 10)

        self.add_btn = QPushButton("Add")
        self.add_btn.setProperty("class", "success")
        self.add_btn.setFixedWidth(70)
        self.add_btn.clicked.connect(self._on_add_item)
        input_grid.addWidget(self.add_btn, 1, 11)

        layout.addLayout(input_grid)

        # Description & serial
        desc_row = QHBoxLayout()
        desc_row.addWidget(QLabel("Description:"))
        self.description_edit = QLineEdit()
        desc_row.addWidget(self.description_edit, stretch=4)
        desc_row.addWidget(QLabel("Serial No.:"))
        self.serial_edit = QLineEdit()
        desc_row.addWidget(self.serial_edit, stretch=1)
        layout.addLayout(desc_row)

        # Table
        self.items_table = QTableWidget(0, len(self.TABLE_COLUMNS))
        self.items_table.setHorizontalHeaderLabels(self.TABLE_COLUMNS)
        self.items_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.items_table.setAlternatingRowColors(True)
        self.items_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.items_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.items_table, stretch=1)

        # Delete button
        del_row = QHBoxLayout()
        del_row.addStretch()
        self.delete_item_btn = QPushButton("Delete Selected")
        self.delete_item_btn.setProperty("class", "danger")
        self.delete_item_btn.clicked.connect(self._on_delete_item)
        del_row.addWidget(self.delete_item_btn)
        layout.addLayout(del_row)

        # Live calc listeners
        for w in (self.qty_edit, self.rate_edit, self.discount_edit,
                  self.tax_edit, self.cess_edit):
            w.textChanged.connect(self._update_live_amount)

        return grp

    # ── Payment section ──────────────────────────────────────────────
    def _build_payment(self) -> QGroupBox:
        grp = QGroupBox("Payment")
        form = QFormLayout(grp)
        form.setSpacing(8)

        self.payment_date_edit = QDateEdit()
        self.payment_date_edit.setCalendarPopup(True)
        from PyQt6.QtCore import QDate
        self.payment_date_edit.setDate(QDate.currentDate())
        form.addRow("Date:", self.payment_date_edit)

        self.payment_mode_combo = QComboBox()
        self.payment_mode_combo.addItems(PAYMENT_MODES)
        self.payment_mode_combo.currentTextChanged.connect(self._on_payment_mode_changed)
        form.addRow("Mode *:", self.payment_mode_combo)

        self.txn_id_edit = QLineEdit()
        self.txn_id_edit.setEnabled(False)
        form.addRow("Txn Id:", self.txn_id_edit)

        self.payment_amount_edit = QLineEdit()
        self.payment_amount_edit.setPlaceholderText("0")
        form.addRow("Amount:", self.payment_amount_edit)

        self.balance_label = QLabel("0")
        self.balance_label.setStyleSheet("font-weight: bold;")
        form.addRow("Balance:", self.balance_label)

        return grp

    # ── Totals ────────────────────────────────────────────────────────
    def _build_totals(self) -> QGroupBox:
        grp = QGroupBox("Total Amount")
        form = QFormLayout(grp)
        self.subtotal_label = QLabel("0.00")
        self.subtotal_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        form.addRow("SubTotal:", self.subtotal_label)

        self.shipping_label = QLabel("0.00")
        form.addRow("Shipping:", self.shipping_label)

        self.discount_total_label = QLabel("0.00")
        form.addRow("Discount:", self.discount_total_label)

        self.total_label = QLabel("0.00")
        self.total_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #0078d4;")
        form.addRow("Total:", self.total_label)

        # Checkboxes
        self.apply_discount_check = QCheckBox("Apply Discount to All")
        form.addRow(self.apply_discount_check)

        self.add_shipping_check = QCheckBox("Add Shipping")
        self.add_shipping_check.setChecked(True)
        form.addRow(self.add_shipping_check)

        return grp

    # ── Remarks ───────────────────────────────────────────────────────
    def _build_remarks(self) -> QGroupBox:
        grp = QGroupBox("Remarks (Private)")
        layout = QVBoxLayout(grp)
        self.remarks_edit = QTextEdit()
        self.remarks_edit.setMaximumHeight(80)
        layout.addWidget(self.remarks_edit)
        return grp

    # ── Delivery Terms ────────────────────────────────────────────────
    def _build_delivery_terms(self) -> QGroupBox:
        grp = QGroupBox("Delivery Terms")
        layout = QVBoxLayout(grp)
        self.delivery_terms_edit = QTextEdit()
        self.delivery_terms_edit.setMaximumHeight(80)
        layout.addWidget(self.delivery_terms_edit)
        return grp

    # ── Action Buttons ────────────────────────────────────────────────
    def _build_action_buttons(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.addStretch()

        self.save_btn = QPushButton("💾  Save Invoice")
        self.save_btn.setProperty("class", "success")
        self.save_btn.setMinimumWidth(160)
        self.save_btn.clicked.connect(self._on_save)
        row.addWidget(self.save_btn)

        self.save_print_btn = QPushButton("🖨️  Save & Print")
        self.save_print_btn.setMinimumWidth(160)
        self.save_print_btn.clicked.connect(self._on_save_and_print)
        row.addWidget(self.save_print_btn)

        return row

    # ================================================================
    # POPULATE DROPDOWNS
    # ================================================================
    def _populate_dropdowns(self):
        self.invoice_no_edit.setText(self.ctrl.get_next_invoice_no())

        cats = self.ctrl.get_categories()
        self.category_combo.addItems(["Select"] + cats)

        units = self.ctrl.get_units()
        self.unit_combo.addItems(units)

        staff = self.ctrl.get_staff_list()
        self.sold_by_combo.addItems(["Select"] + staff)

        clients = self.ctrl.get_client_names()
        self.client_name_combo.addItems(clients)

        items = self.ctrl.get_item_names()
        self.item_name_combo.addItems(items)

    # ================================================================
    # SLOTS
    # ================================================================
    def _on_bill_to_changed(self, checked: bool):
        is_client = self.client_radio.isChecked()
        self.client_address_edit.setEnabled(is_client)
        self.client_gstin_edit.setEnabled(is_client)
        if not is_client:
            self.client_name_combo.setCurrentText("CASH")
            self.client_address_edit.clear()
            self.client_gstin_edit.clear()
            self.contact_edit.clear()

    def _on_client_selected(self, name: str):
        info = self.ctrl.get_client_info(name)
        if info:
            self.contact_edit.setText(str(info.get("Contact", "")))
            self.client_address_edit.setText(info.get("Address", ""))
            self.client_gstin_edit.setText(info.get("GSTIN", ""))

    def _on_item_selected(self, name: str):
        info = self.ctrl.get_item_info(name)
        if info:
            self.rate_edit.setText(str(info.get("Item_Rate", "")))

    def _on_payment_mode_changed(self, mode: str):
        needs_txn = mode not in ("Select", "Cash")
        self.txn_id_edit.setEnabled(needs_txn)

    def _update_live_amount(self):
        try:
            rate = float(self.rate_edit.text() or 0)
            qty = float(self.qty_edit.text() or 0)
            disc = float(self.discount_edit.text() or 0)
            tax = float(self.tax_edit.text() or 0)
            cess = float(self.cess_edit.text() or 0)
            amt = InvoiceController.calculate_line_amount(rate, qty, disc, tax, cess)
            self.amount_label.setText(f"{amt:.2f}")
        except ValueError:
            self.amount_label.setText("—")

    # ── Add / Delete items ───────────────────────────────────────────
    def _on_add_item(self):
        name = self.item_name_combo.currentText().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Item Name is required.")
            return
        try:
            rate = float(self.rate_edit.text() or 0)
            qty = float(self.qty_edit.text() or 0)
        except ValueError:
            QMessageBox.warning(self, "Error", "Rate and Quantity must be numbers.")
            return

        disc = float(self.discount_edit.text() or 0)
        tax = float(self.tax_edit.text() or 0)
        cess = float(self.cess_edit.text() or 0)
        amount = InvoiceController.calculate_line_amount(rate, qty, disc, tax, cess)

        item = InvoiceItem(
            name=name,
            unit=self.unit_combo.currentText(),
            rate=rate,
            quantity=qty,
            discount_pct=disc,
            tax_pct=tax,
            cess_pct=cess,
            amount=amount,
            category=self.category_combo.currentText(),
            sub_category=self.sub_category_combo.currentText(),
            description=self.description_edit.text(),
            serial_number=self.serial_edit.text(),
        )
        self.ctrl.add_item(item)
        self._item_counter += 1

        row = self.items_table.rowCount()
        self.items_table.insertRow(row)
        vals = [
            str(self._item_counter), name, item.unit, f"{rate:.2f}",
            f"{qty:.1f}", f"{disc:.1f}", f"{tax:.1f}", f"{cess:.1f}",
            f"{amount:.2f}", item.sub_category, item.category,
        ]
        for col, val in enumerate(vals):
            self.items_table.setItem(row, col, QTableWidgetItem(val))

        self._recalculate_totals()
        self._clear_item_inputs()

    def _on_delete_item(self):
        row = self.items_table.currentRow()
        if row < 0:
            return
        name = self.items_table.item(row, 1).text()
        cat = self.items_table.item(row, 10).text()
        self.ctrl.remove_item(cat, name)
        self.items_table.removeRow(row)
        self._recalculate_totals()

    def _clear_item_inputs(self):
        self.item_code_edit.clear()
        self.item_name_combo.setCurrentIndex(0)
        self.qty_edit.clear()
        self.rate_edit.clear()
        self.discount_edit.clear()
        self.tax_edit.clear()
        self.cess_edit.clear()
        self.description_edit.clear()
        self.serial_edit.clear()
        self.amount_label.setText("0.00")

    # ── Totals ───────────────────────────────────────────────────────
    def _recalculate_totals(self):
        shipping = 0.0  # could be editable in the future
        totals = self.ctrl.calculate_totals(shipping=shipping)
        self.subtotal_label.setText(f"{totals['sub_total']:.2f}")
        self.discount_total_label.setText(f"{totals['discount']:.2f}")
        self.shipping_label.setText(f"{totals['shipping']:.2f}")
        self.total_label.setText(f"Rs. {totals['total']:.2f} /-")

    # ── Save ─────────────────────────────────────────────────────────
    def _collect_data(self) -> InvoiceData:
        totals = self.ctrl.calculate_totals()
        return InvoiceData(
            invoice_type=self.invoice_type_combo.currentText(),
            invoice_no=self.invoice_no_edit.text().strip(),
            invoice_date=self.invoice_date_edit.date().toString("yyyy-MM-dd"),
            place_of_supply=self.pos_combo.currentText(),
            bill_to="client" if self.client_radio.isChecked() else "cash",
            client_contact=self.contact_edit.text().strip(),
            client_name=self.client_name_combo.currentText().strip(),
            client_address=self.client_address_edit.text().strip(),
            client_gstin=self.client_gstin_edit.text().strip(),
            sold_by=self.sold_by_combo.currentText(),
            discount_total=str(totals["discount"]),
            shipping_total=str(totals["shipping"]),
            sub_total=str(totals["sub_total"]),
            total=f"Rs. {totals['total']}/-",
            payment_date=self.payment_date_edit.date().toString("yyyy-MM-dd"),
            payment_mode=self.payment_mode_combo.currentText(),
            txn_id=self.txn_id_edit.text().strip(),
            payment_amount=self.payment_amount_edit.text().strip() or "0",
            client_balance=self.balance_label.text(),
            remarks=self.remarks_edit.toPlainText(),
            delivery_terms=self.delivery_terms_edit.toPlainText(),
        )

    def _on_save(self):
        reply = QMessageBox.question(
            self, "Confirm",
            f"Save Invoice '{self.invoice_no_edit.text()}'?",
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        data = self._collect_data()
        self.save_btn.setEnabled(False)
        self.save_btn.setText("Saving…")

        self._worker = _SaveWorker(self.ctrl, data)
        self._worker.finished.connect(self._on_save_done)
        self._worker.start()

    def _on_save_done(self, ok: bool, msg: str):
        self.save_btn.setEnabled(True)
        self.save_btn.setText("💾  Save Invoice")
        if ok:
            QMessageBox.information(self, "Success", msg)
            self.close()
        else:
            QMessageBox.warning(self, "Error", msg)

    def _on_save_and_print(self):
        # Save first, then print
        self._on_save()
