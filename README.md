# Techware BillSoft (Legacy Python Application)

A robust, local-first Point of Sale (POS) and billing management desktop application built using Python, Tkinter, and SQLite. This repository contains the source code for the original desktop application designed for offline business operations.

## Architecture

The application is a monolithic desktop client built natively in Python. It relies heavily on Tkinter for the graphical user interface and SQLite for local, serverless database management. The project uses customized Tkinter widgets for advanced UI behaviors and interacts with the Windows COM API for Microsoft Excel integration and reporting.

### Core Modules

*   **`techware_billing.py`**: The main entry point and dashboard GUI. This module orchestrates the application's root window, menu system, and high-level navigation, providing access to all secondary operations.
*   **`techware_invoice.py`**: Handles the complex business logic and GUI for invoice creation. It manages real-time cart calculations, customer data retrieval, tax application, and saving the finalized invoice records directly to the local SQLite databases.
*   **`show_invoices.py`**: Provides the interface for invoice management. This module allows users to search, filter, view, print, and delete existing invoices from the database.
*   **`reset_software.py`**: A database management and schema reset utility. It contains the data definition language (DDL) necessary to drop and recreate the SQLite tables (e.g., Business, Clients, Invoices, Items, Employee), effectively resetting the software to a clean slate.
*   **`save_excel.py` & `save_reports.py`**: Reporting modules that leverage `openpyxl` and `win32com.client`. They automate the generation of financial reports, export data to Excel spreadsheets, and handle the layout and saving of these records.

### Foundational Dependencies

The core modules depend on several foundational algorithms and custom UI components:

*   **`Digvijay_Algos/custom_widgets.py`**: A foundational UI library specific to this project. It contains subclasses of standard Tkinter widgets (like `Custom_treeview`, `Link_Text`, `Required_Text`) and entirely new composite windows (e.g., `Add_Staff_Window`, `Manage_Items`, `Manage_Invoice`). This encapsulates complex UI behavior and ensures a consistent design language across the application.
*   **`test2.py`**: Contains helper utilities such as custom `Clock` widgets and `CreateToolTip` classes for enhancing the user experience within the Tkinter dashboard.

## Technology Stack

*   **Language:** Python 3.x
*   **GUI Framework:** Tkinter (with `ttk`, `awthemes` for styling, and `tkcalendar` for date inputs)
*   **Database:** SQLite3
*   **Reporting & Automation:** `openpyxl`, `win32com.client` (Microsoft Excel Interop), `wand` (ImageMagick binding for Python)
*   **UI Addons:** `ttkwidgets.autocomplete`

## Database Structure

The application segments data across multiple SQLite database files (stored under `DB/`) for modularity:
*   `Business.db`: Company settings and configurations.
*   `Clients.db`: Customer CRM and details.
*   `Invoices.db`: Billing records, invoice line items, and transaction history.
*   `Items.db`: Inventory, product catalog, and pricing.
*   `Employee.db`: Staff records and tracking.

## Getting Started

The project can be executed locally by running the main dashboard script via a Python interpreter:

```cmd
python techware_billing.py
```

It can also be packaged into a standalone Windows executable using PyInstaller, leveraging the included `Techware Billing System.spec` file.
