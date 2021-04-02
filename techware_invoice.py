# Importing Packages
import json
import os
import sqlite3
import time
import re
from datetime import date, timedelta
from tkinter import *
from tkinter import messagebox as tmsg
from tkinter import ttk, scrolledtext

import openpyxl.drawing.image
import wand
import wand.image
import win32com
import win32com.client
from openpyxl import load_workbook
from pywintypes import com_error
from tkcalendar import DateEntry
from ttkwidgets.autocomplete import *
from wand import exceptions


class Invoice:

    # Initializing The Invoice
    def __init__(self, root):
        # Root Window
        self.root = root
        self.root = root
        w, h = self.root.winfo_screenwidth(), root.winfo_screenheight()
        self.root.title("Unsaved Invoice")
        # root.geometry("%dx%d+92+12" % (1183, 684))
        self.root['bg'] = "white"
        self.root.state("zoomed")
        self.root.resizable(0, 0)

        # Style Of TTK
        self.style = ttk.Style(self.root)

        # Loading TTK Themes
        self.root.tk.eval("""
                set base_theme_dir C:/Users/Digvijay/Downloads/awthemes-10.2.0/awthemes-10.2.0

                package ifneeded awthemes 10.2.0 \
                    [list source [file join $base_theme_dir awthemes.tcl]]
                package ifneeded colorutils 4.8 \
                    [list source [file join $base_theme_dir colorutils.tcl]]
                package ifneeded awdark 7.7 \
                    [list source [file join $base_theme_dir awdark.tcl]]
                package ifneeded awlight 7.9 \
                    [list source [file join $base_theme_dir awlight.tcl]]
                package ifneeded awbreeze 7.9 \
                    [list source [file join $base_theme_dir awbreeze.tcl]]
                """)

        # Load The Awdark And Awlight Themes
        self.root.tk.call("package", "require", 'awthemes')
        self.root.tk.call("package", "require", 'awlight')
        # self.root.tk.call("package", "require", 'awbreeze')

        # Using Theme AWLIGHT
        self.style.theme_use('awlight')

        # Showing All The Themes
        # print(self.style.theme_names())

        # Button Style 1
        self.style.configure("C.TButton", font=("Calibri", 12), takefocus=False,
                             shiftrelief=0)
        self.style.map("C.TButton",
                       foreground=[('!active', 'white'), ('pressed', 'white'), ('active', 'white')],
                       background=[('!active', '#11481a'), ('pressed', '#39d44b'), ('active', '#096119')]
                       )

        # Button Style 2
        self.style.map("S.TButton",
                       foreground=[('!active', 'white'), ('pressed', 'white'), ('active', 'white')],
                       background=[('!active', '#00bd61'), ('pressed', '#00e375'), ('active', '#00d16c')]
                       )

        # CheckButton Style
        self.style.configure('Red.TCheckbutton', font=("Calibri", 12), takefocus=False, background="white",
                             selectcolor="white", lightcolor="white", darkcolor="white", padding=[5, 0, 1, 2],
                             focusthickness=0, borderwidth=0, relief='none')
        self.style.map('Red.TCheckbutton',
                       background=[('!active', 'white'), ('pressed', 'white'), ('active', 'white')],
                       foreground=[('!active', 'black'), ('pressed', 'black'), ('active', 'black')])

        # Frame Style
        self.style.map('Retail.TFrame',
                       background=[('!active', 'black'), ('pressed', 'white'), ('active', 'white')])

        # Label Style
        self.style.map('Retail.TLabel',
                       background=[('!active', 'black'), ('pressed', 'white'), ('active', 'white')])

        # Treeview Style
        self.style.configure("T.Treeview", background="black", fieldbackground="white", foreground="black")

        # Treeview Heading Style
        self.style.configure("T.Treeview.Heading", background="#26e881", foreground="white",
                             rowheight=35, font=("Calibri", 15))

        # Invoice Information Frame
        self.invoice_information_lbl = LabelFrame(self.root, text="Invoice Information", bg="white")
        self.invoice_information_lbl.place(relx=0, rely=0, relwidth=1, relheight=0.15)

        # Variable for Contact No.
        self.contact_no_var = StringVar()

        # Variable for Contact Address
        self.contact_address_var = StringVar()

        # Invoice Type Label
        self.invoice_type_lbl = Label(self.invoice_information_lbl, text="Invoice Type *", font=("Calibri", 10),
                                      bg="white")
        self.invoice_type_lbl.place(relx=0, rely=0)

        # Invoice Type ComboBox
        self.invoice_type_txt = ttk.Combobox(self.invoice_information_lbl, font=("Calibri", 12),
                                             values=["Select", "GST",
                                                     "Non-GST", "Bill of Supply"])
        self.invoice_type_txt.place(relx=0, rely=0.2, relwidth=0.1)
        self.invoice_type_txt.current(0)

        # Invoice No. Variable
        self.invoice_no_var = StringVar()

        # Invoice No. Label
        self.invoice_no_lbl = Label(self.invoice_information_lbl, text="Invoice-No.", font=("Calibri", 10), bg="white")
        self.invoice_no_lbl.place(relx=0.125, rely=0)

        # Invoice No. Entry
        self.invoice_no_txt = ttk.Entry(self.invoice_information_lbl, font=("Calibri", 12),
                                        textvariable=self.invoice_no_var)
        self.invoice_no_txt.place(relx=0.125, rely=0.2, relwidth=0.1)

        # Adding Invoice No. Dynamically
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.sql_string = '''SELECT * FROM ID where Category = ?'''
        self.cursor.execute(self.sql_string, ("Invoice",))
        self.rows = self.cursor.fetchall()
        print(self.rows)
        self.invoice_no_var.set(self.rows[0][1])

        # Date Label
        self.invoice_date_lbl = Label(self.invoice_information_lbl, text="Date", font=("Calibri", 10), bg="white")
        self.invoice_date_lbl.place(relx=0.250, rely=0)

        # Date Entry
        self.invoice_date_txt = DateEntry(self.invoice_information_lbl, font=("Calibri", 12))
        self.invoice_date_txt.place(relx=0.250, rely=0.2, relwidth=0.1)

        # Sold By Label
        self.sold_by_lbl = Label(self.invoice_information_lbl, text="Sold By", font=("Calibri", 10), bg="white")
        self.sold_by_lbl.place(relx=0.375, rely=0)

        # Sold By ComboBox
        self.sold_by_txt = ttk.Combobox(self.invoice_information_lbl, font=("Calibri", 12), values=["Select"],
                                        state='readonly')
        self.sold_by_txt.place(relx=0.375, rely=0.2, relwidth=0.1)
        self.sold_by_txt.current(0)

        # Contact Label
        self.contact_no_lbl = Label(self.invoice_information_lbl, text="Contact *", font=("Calibri", 10), bg="white")
        self.contact_no_lbl.place(relx=0, rely=0.5)

        # Contact Entry
        self.contact_no_txt = ttk.Entry(self.invoice_information_lbl, font=("Calibri", 12),
                                        textvariable=self.contact_no_var)
        self.contact_no_txt.place(relx=0, rely=0.7, relwidth=0.1)

        # # Retail Options Label
        # self.retail_options_lbl = Label(self.invoice_information_lbl, text="Retail", font=("Calibri", 10, "underline"),
        #                                 fg='darkblue', bg="white")
        # self.retail_options_lbl.place(relx=0.125, rely=0.5)
        # self.retail_options_lbl.bind("<ButtonRelease-1>", self.retail_options)

        # Client Name Label
        self.client_name_lbl = Label(self.invoice_information_lbl, text="Client Name *", font=("Calibri", 10),
                                     bg="white")
        self.client_name_lbl.place(relx=0.150, rely=0.5)

        # Client Name Entry
        self.client_name_txt = AutocompleteCombobox(self.invoice_information_lbl, completevalues=["Select"],
                                                    font=("Calibri", 12))
        self.client_name_txt.place(relx=0.125, rely=0.7, relwidth=0.1)

        self.conn = sqlite3.connect("DB\\Clients.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT * FROM CLIENT")

        self.rows = self.cursor.fetchall()

        self.clients = []

        for i in range(0, int(len(self.rows))):
            self.client = self.rows[i][1]
            self.clients.append(self.client)

        self.client_name_txt.config(completevalues=self.clients)

        self.client_name_txt.bind("<<ComboboxSelected>>", self.client_info_add)

        # Client Address Label
        self.client_address_lbl = Label(self.invoice_information_lbl, text="Client Address *", font=("Calibri", 10),
                                        bg="white")
        self.client_address_lbl.place(relx=0.250, rely=0.5)

        # Client Address Entry
        self.client_address_txt = ttk.Entry(self.invoice_information_lbl, font=("Calibri", 12),
                                            textvariable=self.contact_address_var)
        self.client_address_txt.place(relx=0.250, rely=0.7, relwidth=0.1)

        # Particulars Frame
        self.particulars_lbl = LabelFrame(self.root, text="Particulars", bg="white")
        self.particulars_lbl.place(relx=0, rely=0.15, relwidth=1, relheight=0.51)

        # Bar Code / QR Code
        self.bar_var = StringVar()
        self.bar_var.set("bar code")

        # Bar Code RadioButton
        self.bar_code_radio = Radiobutton(self.particulars_lbl, text="Bar Code",
                                          font=("Calibri", 12), bg="white", value="bar code",
                                          variable=self.bar_var)
        self.bar_code_radio.place(relx=0, rely=0)

        # QR Code RadioButton
        self.bar_code_radio = Radiobutton(self.particulars_lbl, text="QR Code",
                                          font=("Calibri", 12), bg="white", value="qr code",
                                          variable=self.bar_var)
        self.bar_code_radio.place(relx=0.065, rely=0)

        # Bar Code Entry
        self.item_code_txt = ttk.Entry(self.particulars_lbl, font=("Calibri", 12))
        self.item_code_txt.place(relx=0, rely=0.1, relwidth=0.13)

        # Item Name Label
        self.item_name_lbl = Label(self.particulars_lbl, text="Item Name *", font=("Calibri", 10), bg="white")
        self.item_name_lbl.place(relx=0.150, rely=0)

        # Item Name Entry
        self.item_name_txt = AutocompleteCombobox(self.particulars_lbl, font=("Calibri", 12))
        self.item_name_txt.place(relx=0.150, rely=0.05, relwidth=0.2)

        self.conn = sqlite3.connect("DB\\Items.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT * FROM ITEMS")

        self.rows = self.cursor.fetchall()

        self.items_names = []

        for i in range(0, int(len(self.rows))):
            self.items_name = self.rows[i][4]
            self.items_names.append(self.items_name)

        self.item_name_txt.config(completevalues=self.items_names)

        self.item_name_txt.bind("<<ComboboxSelected>>", self.item_info_add)

        # Item Units Label
        self.item_units_lbl = Label(self.particulars_lbl, text="Unit *", font=("Calibri", 10), bg="white")
        self.item_units_lbl.place(relx=0.420, rely=0)

        # Item Units Entry
        self.item_units_txt = AutocompleteCombobox(self.particulars_lbl, font=("Calibri", 12))
        self.item_units_txt.place(relx=0.420, rely=0.05, relwidth=0.04)

        self.units = []

        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT * FROM UNIT")

        for i in self.rows:
            self.units.append(i[1])
            print(i)

        self.item_units_txt.config(completevalues=self.units)

        self.conn = sqlite3.connect("DB\\Items.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT * FROM ITEMS")

        self.rows = self.cursor.fetchall()

        self.units_names = []

        for i in range(0, int(len(self.rows))):
            self.units_name = self.rows[i][1]
            self.units_names.append(self.items_name)

        self.item_name_txt.config(completevalues=self.units_names)

        # Item Rate Label
        self.item_rate_lbl = Label(self.particulars_lbl, text="Item Rate *", font=("Calibri", 10), bg="white")
        self.item_rate_lbl.place(relx=0.490, rely=0)

        # Item Rate Entry
        self.item_rate_txt = ttk.Entry(self.particulars_lbl, font=("Calibri", 12))
        self.item_rate_txt.place(relx=0.490, rely=0.05, relwidth=0.06)

        # Item Quantity Label
        self.item_qty_lbl = Label(self.particulars_lbl, text="Item Quantity", font=("Calibri", 10), bg="white")
        self.item_qty_lbl.place(relx=0.560, rely=0)

        # Item Quantity Entry
        self.item_qty_txt = ttk.Entry(self.particulars_lbl, font=("Calibri", 12))
        self.item_qty_txt.place(relx=0.560, rely=0.05, relwidth=0.06)

        # Discount Label
        self.discount_lbl = Label(self.particulars_lbl, text="Discount", font=("Calibri", 10), bg="white")
        self.discount_lbl.place(relx=0.630, rely=0)

        # Discount Entry
        self.discount_txt = ttk.Entry(self.particulars_lbl, font=("Calibri", 12))
        self.discount_txt.place(relx=0.630, rely=0.05, relwidth=0.06)

        # Category Label
        self.category_lbl = Label(self.particulars_lbl, text="Category *", font=("Calibri", 10), bg="white")
        self.category_lbl.place(relx=0.700, rely=0)

        # Category ComboBox
        self.category_txt = ttk.Combobox(self.particulars_lbl, font=("Calibri", 12), values=["Select"],
                                         state='readonly')
        self.category_txt.place(relx=0.700, rely=0.05, relwidth=0.06)
        self.category_txt.current(0)

        # Connecting To Database
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()

        # Executing Commands In Cursor
        self.cursor.execute("SELECT * FROM CATEGORY")

        # Rows of Data
        self.rows = self.cursor.fetchall()

        # Giving Rows To Values
        self.values = ["Select"]

        # Through For Loop
        for id, category in self.rows:
            # Appending To Values
            self.values.append(category)

        # Giving Values to Category ComboBox
        self.category_txt['values'] = self.values

        # Initializing Items List
        self.items = {}

        # Through For Loop
        for id, category in self.rows:
            # Appending To Items List
            self.items[category] = {}

        # Initializing Categories List
        self.categories = {}

        # Through For Loop
        for id, category in self.rows:
            # Appending To Categories List
            self.categories[category] = {}

        # Sub-Category Label
        self.sub_category_lbl = Label(self.particulars_lbl, text="Sub-Category", font=("Calibri", 10), bg="white")
        self.sub_category_lbl.place(relx=0.770, rely=0)

        # Sub-Category ComboBox
        self.sub_category_txt = ttk.Combobox(self.particulars_lbl, font=("Calibri", 12), values=["Select"])
        self.sub_category_txt.place(relx=0.770, rely=0.05, relwidth=0.06)
        self.sub_category_txt.current(0)

        '''# Item Code Label
        self.item_code_lbl = Label(self.particulars_lbl, text="Item Code", font=("Calibri", 10), bg="white")
        self.item_code_lbl.place(relx=0.600, rely=0)

        # Item Code Entry
        self.item_code_txt = ttk.Entry(self.particulars_lbl, font=("Calibri", 12))
        self.item_code_txt.place(relx=0.600, rely=0.05, relwidth=0.1)'''

        # Add Particulars Button
        self.add_particular_btn = ttk.Button(self.particulars_lbl, text="Add", style="S.TButton",
                                             command=self.add_particular_func)
        self.add_particular_btn.place(relx=0.95, rely=0.2)

        '''# List Particulars Button
        self.list_particular_btn = ttk.Button(self.particulars_lbl, text="List", style="S.TButton",
                                              command=self.select_from_menu)
        self.list_particular_btn.place(relx=0.95, rely=0.2)'''

        # Description Label
        self.description_lbl = Label(self.particulars_lbl, text="Description", font=("Calibri", 10), bg="white")
        self.description_lbl.place(relx=0, rely=0.4)

        # Description Entry
        self.description_txt = scrolledtext.ScrolledText(self.particulars_lbl, font=("Calibri", 12))
        self.description_txt.place(relx=0, rely=0.45, relwidth=1, relheight=0.1)

        # Particulars Treeview Frame
        self.particulars_treeview_frame = Frame(self.particulars_lbl)
        self.particulars_treeview_frame.place(relx=0, rely=0.6, relwidth=1, relheight=0.6)

        # Particulars Treeview
        self.particulars_treeview = ttk.Treeview(self.particulars_treeview_frame, style="T.Treeview",
                                                 columns=(
                                                     "No.", "Name", "Rate",
                                                     "Quantity", "Item Code", "Sub-Category", "Category"), )
        # height=len(self.rows))

        # Vertical Scrollbar
        self.vsb = Scrollbar(self.particulars_treeview,
                             orient="vertical",
                             command=self.particulars_treeview.yview
                             )

        # Scroll Command For Particulars Treeview
        self.particulars_treeview['yscrollcommand'] = self.vsb.set

        # Treeview Headings
        self.particulars_treeview.heading("No.", text="No.")
        self.particulars_treeview.heading("Name", text="Name")
        self.particulars_treeview.heading("Rate", text="Rate")
        self.particulars_treeview.heading("Quantity", text="Quantity")
        self.particulars_treeview.heading("Item Code", text="Item Code")
        self.particulars_treeview.heading("Sub-Category", text="Sub-Category")
        self.particulars_treeview.heading("Category", text="Category")
        self.particulars_treeview["displaycolumns"] = ("No.", "Name", "Rate",
                                                       "Quantity", "Item Code", "Sub-Category", "Category")
        self.particulars_treeview["show"] = "headings"

        # Treeview Columns
        self.particulars_treeview.column("No.", width=150, anchor='center')
        self.particulars_treeview.column("Name", width=150, anchor='center')
        self.particulars_treeview.column("Rate", width=150, anchor='center')
        self.particulars_treeview.column("Quantity", width=150, anchor='center')
        self.particulars_treeview.column("Item Code", width=150, anchor='center')
        self.particulars_treeview.column("Sub-Category", width=150, anchor='center')
        self.particulars_treeview.column("Category", width=150, anchor='center')

        # Tags for Treeview
        self.particulars_treeview.tag_configure('oddrow', background="white")
        self.particulars_treeview.tag_configure('evenrow', background="#c5dbbf")

        # Packing Vertical Scrollbar
        self.vsb.pack(side=RIGHT, fill=Y)

        # Configuring Vertical Scrollbar
        self.vsb.configure(command=self.particulars_treeview.yview)

        # Packing Particulars Treeview
        self.particulars_treeview.pack(fill=BOTH, expand=1)

        # Payment Frame
        self.payment_lbl = LabelFrame(self.root, text="Payment", bg="white")
        self.payment_lbl.place(relx=0.55, rely=0.66, relwidth=0.22, relheight=0.33)

        # Payment Date Label
        self.payment_date_lbl = Label(self.payment_lbl, text="Date", bg="white", font=("Calibri", 12))
        self.payment_date_lbl.place(relx=0, rely=0.01)

        # Payment Date Entry
        self.payment_date_txt = DateEntry(self.payment_lbl, font=("Calibri", 12))
        self.payment_date_txt.place(relx=0.3, rely=0.01, relwidth=0.6)

        # Payment Mode Label
        self.payment_mode_lbl = Label(self.payment_lbl, text="Mode", bg="white", font=("Calibri", 12))
        self.payment_mode_lbl.place(relx=0, rely=0.2)

        # Payment Mode ComboBox
        self.payment_mode_txt = ttk.Combobox(self.payment_lbl, font=("Calibri", 12), values=["Select", "Cash",
                                                                                             "Cheque", "Card",
                                                                                             "Demand Draft",
                                                                                             "Mobile Wallet",
                                                                                             "Bank Transfer"],
                                             state='readonly', style="TCombobox")
        self.payment_mode_txt.current(0)
        self.payment_mode_txt.place(relx=0.3, rely=0.2, relwidth=0.6)

        # Txn. Id Label
        self.txn_id_lbl = Label(self.payment_lbl, text="Txn. Id", bg="white", font=("Calibri", 12))
        self.txn_id_lbl.place(relx=0, rely=0.4)

        # Txn. Id Entry
        self.txn_id_txt = ttk.Entry(self.payment_lbl, font=("Calibri", 12), state='disabled')
        self.txn_id_txt.place(relx=0.3, rely=0.4, relwidth=0.6)

        # Payment Amount Label
        self.payment_amount_lbl = Label(self.payment_lbl, text="Amount", bg="white", font=("Calibri", 12))
        self.payment_amount_lbl.place(relx=0, rely=0.6)

        # Payment Amount Variable
        self.payment_amount_var = StringVar()

        # Payment Amount Entry
        self.payment_amount_txt = ttk.Entry(self.payment_lbl, text="", font=("Calibri", 12))
        self.payment_amount_txt.place(relx=0.3, rely=0.6, relwidth=0.6)

        # Payment Balance Label
        self.payment_balance_lbl = Label(self.payment_lbl, text="Balance", bg="white", font=("Calibri", 12))
        self.payment_balance_lbl.place(relx=0, rely=0.8)

        # Payment Amount Entry
        self.payment_balance_txt = ttk.Entry(self.payment_lbl, font=("Calibri", 12), state='disabled')
        self.payment_balance_txt.place(relx=0.3, rely=0.8, relwidth=0.6)

        # Variable for Discount CheckButton
        self.discount_var = IntVar()

        # Discount CheckButton
        self.discount_chkbox = ttk.Checkbutton(self.root, text="Apply Discount To All",
                                               variable=self.discount_var, onvalue=1, offvalue=0, takefocus=False,
                                               style='Red.TCheckbutton', command=self.add_discount)

        # Packing Discount CheckButton
        self.discount_chkbox.place(relx=0.11, rely=0.77)

        # Variable for Discount CheckButton
        self.shipping_var = IntVar()
        self.shipping_var.set(1)

        # Shipping CheckButton
        self.shipping_chkbox = ttk.Checkbutton(self.root, text="Add Shipping",
                                               variable=self.shipping_var, onvalue=1, offvalue=0, takefocus=False,
                                               style='Red.TCheckbutton', command=self.add_shipping)
        # self.add_shipping()

        # Packing Shipping CheckButton
        self.shipping_chkbox.place(relx=0.33, rely=0.77)

        # Delivery Terms Frame
        self.delivery_terms_lbl = LabelFrame(self.root, text="Delivery Terms", bg="white")
        self.delivery_terms_lbl.place(relx=0.25, rely=0.88, relwidth=0.22, relheight=0.1)

        # Delivery Terms Entry
        self.delivery_terms_txt = scrolledtext.ScrolledText(self.delivery_terms_lbl, font=("Calibri", 12))
        self.delivery_terms_txt.pack(fill=BOTH, expand=1)

        # Remarks Frame
        self.remarks_lbl = LabelFrame(self.root, text="Remarks(Private Use)", bg="white")
        self.remarks_lbl.place(relx=0.01, rely=0.88, relwidth=0.22, relheight=0.1)

        # Remarks Entry
        self.remarks_txt = scrolledtext.ScrolledText(self.remarks_lbl, font=("Calibri", 12))
        self.remarks_txt.pack(fill=BOTH, expand=1)
        self.root.update_idletasks()

        # Total Amount Frame
        self.total_amount_frame = LabelFrame(self.root, text="Total Amount", bg="white")
        self.total_amount_frame.place(relx=0.78, rely=0.66, relwidth=0.22, relheight=0.2)

        # Total Price Variable
        self.totalPrice = StringVar()

        # Discount Price Variable
        self.discountPrice = StringVar()

        # Shipping Charges Variable
        self.shippingCharges = StringVar()

        # Subtotal Amount Variable
        self.subTotalPrice = StringVar()

        # Total Amount Label
        self.total_amount_lbl = Label(self.total_amount_frame, text="SubTotal:-", font=("Calibri", 13), bg="white")
        self.total_amount_lbl.place(relx=0, rely=0)

        # Total Amount TXT
        self.total_amount_txt = Label(self.total_amount_frame, text="", textvariable=self.subTotalPrice, bg="white",
                                      font=("Calibri", 13))
        self.total_amount_txt.place(relx=0.3, rely=0)

        # Shipping Charges Label
        self.shipping_charges_lbl = Label(self.total_amount_frame, text="Shipping:-", font=("Calibri", 13), bg="white")
        self.shipping_charges_lbl.place(relx=0, rely=0.25)

        # Shipping Charges TXT
        self.shippingCharges_txt = Label(self.total_amount_frame, text="", textvariable=self.shippingCharges,
                                         bg="white", font=("Calibri", 13))
        self.shippingCharges_txt.place(relx=0.3, rely=0.25)

        # Discount Amount Label
        self.discount_amount_lbl = Label(self.total_amount_frame, text="Discount:-", font=("Calibri", 13), bg="white")
        self.discount_amount_lbl.place(relx=0, rely=0.50)

        # Discount Amount TXT
        self.discount_amount_txt = Label(self.total_amount_frame, text="", textvariable=self.discountPrice, bg="white",
                                         font=("Calibri", 13))
        self.discount_amount_txt.place(relx=0.3, rely=0.50)

        # Total Amount Label
        self.total_amount_lbl = Label(self.total_amount_frame, text="Total:-", font=("Calibri", 13), bg="white")
        self.total_amount_lbl.place(relx=0, rely=0.75)

        # Total Amount TXT
        self.total_amount_txt = Label(self.total_amount_frame, text="", textvariable=self.totalPrice, bg="white",
                                      font=("Calibri", 13))
        self.total_amount_txt.place(relx=0.3, rely=0.75)

        # Save Button
        self.save_btn = ttk.Button(self.root, text="Save", style="S.TButton", command=self.save_operation)
        self.save_btn.place(relx=0.8, rely=0.88)

        # Save & Print Button
        self.save_print_btn = ttk.Button(self.root, text="Save & Print", style="S.TButton",
                                         command=self.print_operation)
        self.save_print_btn.place(relx=0.9, rely=0.88)

    # Adding Items Info
    def item_info_add(self, event):
        self.conn = sqlite3.connect("DB\\Items.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT * FROM ITEMS where Item_Name = ?", (self.client_name_txt.get(),))
        self.rows = self.cursor.fetchone()

        self.category_name = self.rows[5]
        self.sub_category_name = self.rows[8]
        self.item_code_name = self.rows[5]
        self.item_name_name = self.rows[8]
        self.item_rate_name = self.rows[5]
        self.item_qty_name = self.rows[8]

        self.contact_no_var.set(self.client_contact)
        self.contact_address_var.set(self.client_address)

    # Adding Client Info
    def client_info_add(self, event):
        self.conn = sqlite3.connect("DB\\Clients.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT * FROM CLIENT where Full_Name = ?", (self.client_name_txt.get(),))
        self.rows = self.cursor.fetchone()

        self.client_contact = self.rows[5]
        self.client_address = self.rows[8]

        self.contact_no_var.set(self.client_contact)
        self.contact_address_var.set(self.client_address)

    # Retail Options Window Function
    # def retail_options(self, event):
    #
    #     # Retail Options Window
    #     self.retail_options_window = Toplevel()
    #     self.retail_options_window.overrideredirect(True)
    #     self.retail_options_window.geometry("500x300+400+200")
    #
    #     # Dict for Retail Option Values
    #     self.retail_options = ["Retail", "Agent", "Wholesale"]
    #
    #     # Retail Frame
    #     self.retail_frame = ttk.Frame(self.retail_options_window, style="Retail.TFrame")
    #     self.retail_frame.pack(fill=BOTH, side=TOP, anchor=N, expand=1)
    #
    #     # Retail Button
    #     self.retail_lbl = ttk.Button(self.retail_frame, text=self.retail_options[0], command=self.retail_operation
    #                                  , style="S.TButton")
    #     self.retail_lbl.pack(fill=BOTH, side=TOP, expand=1)
    #
    #     # Agent Frame
    #     self.agent_frame = ttk.Frame(self.retail_options_window, style="Retail.TFrame")
    #     self.agent_frame.pack(fill=BOTH, side=TOP, anchor=N, expand=1)
    #
    #     # Agent Button
    #     self.agent_lbl = ttk.Button(self.retail_frame, text=self.retail_options[1], command=self.agent_operation
    #                                 , style="S.TButton")
    #     self.agent_lbl.pack(fill=BOTH, side=TOP, expand=1)
    #
    #     # Wholesale Frame
    #     self.wholesale_frame = ttk.Frame(self.retail_options_window, style="Retail.TFrame")
    #     self.wholesale_frame.pack(fill=BOTH, side=TOP, anchor=N, expand=1)
    #
    #     # Wholesale Button
    #     self.wholesale_lbl = ttk.Button(self.retail_frame, text=self.retail_options[2], command=self.wholesale_operation
    #                                     , style="S.TButton")
    #     self.wholesale_lbl.pack(fill=BOTH, side=TOP, expand=1)

    # # Retail Button Function
    # def retail_operation(self):
    #     self.retail_options_lbl.config(text="Retail")
    #     self.retail_options_window.destroy()
    #
    # # Agent Button Function
    # def agent_operation(self):
    #     self.retail_options_lbl.config(text="Agent")
    #     self.retail_options_window.destroy()
    #
    # # Wholesale Button Function
    # def wholesale_operation(self):
    #     self.retail_options_lbl.config(text="Wholesale")
    #     self.retail_options_window.destroy()

    # Adding Discount Option
    def add_discount(self):

        # IF ELSE Statement For Adding And Removing Discount Entries According to CheckButton
        if self.discount_var.get() == 1:
            self.discount_charges_txt = ttk.Entry(self.root, font=("Calibri", 12))
            self.discount_charges_txt.place(relx=0.24, rely=0.77, relwidth=0.05)
            self.discount_charges_txt.bind("<KeyRelease>", self.update_total_price_event)
        else:
            self.discount_charges_txt.destroy()

    def update_total_price_event(self, event):
        self.subPrice = 0
        self.totalprice = 0
        for i in self.categories.keys():
            for j in self.items[i].keys():
                self.subPrice += int(self.items[i][j][3])
        if self.subPrice == 0:
            self.subTotalPrice.set("")
        else:
            self.subTotalPrice.set("Rs." + str(self.subPrice) + " /-")
            self.payment_amount_var.set(str(self.subPrice))
        print(self.discount_var.get())
        if self.discount_var.get() == 1:
            self.discountPrice.set(str(self.discount_charges_txt.get()))
        else:
            self.discountPrice.set(str(0))
        if self.shipping_var.get() == 1:
            if self.shipping_charges_sel.get() != "Select":
                self.shippingCharges.set(str(self.shipping_charges_sel.get()))
            else:
                self.shippingCharges.set(str(self.shipping_charges_txt.get()))
        else:
            self.shippingCharges.set(str(0))
        if self.totalprice == 0:
            try:
                self.totalprice = str(
                    int(self.subPrice) - int(self.discountPrice.get()) + int(self.shippingCharges.get()))
                self.totalPrice.set(self.totalprice)
            except Exception as e:
                self.totalprice = 0
                self.shippingCharges.set(0)
                self.totalPrice.set(self.totalprice)

    # Saving Bills
    def save_operation(self):
        self.conn = sqlite3.connect("DB\\Invoices.db")
        self.cursor = self.conn.cursor()

        self.cwd = os.getcwd()

        self.file_path = f"{self.cwd}\\DB\\INVOICES"

        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)
        print(self.items)

        self.conn.execute("DROP TABLE INVOICES")

        # Preparing Table For Invoices
        self.query = """CREATE TABLE IF NOT EXISTS INVOICES(
                        id  INTEGER PRIMARY KEY autoincrement,
                        Invoice_Type VARCHAR(500) NOT NULL,
                        Invoice_No VARCHAR(500) NOT NULL,
                        Invoice_Date DATE NOT NULL,
                        Sold_By VARCHAR(500) NOT NULL,
                        Client_Contact INT(10) NOT NULL,
                        Client_Type VARCHAR(500) NOT NULL,
                        Client_Name VARCHAR(500) NOT NULL,
                        Client_Address VARCHAR(5000) NOT NULL,
                        Discount INTEGER NOT NULL,
                        Shipping INTEGER NOT NULL,
                        SubTotal INTEGER NOT NULL,
                        Total INTEGER NOT NULL,
                        Payment_Date DATE NOT NULL,
                        Payment_Mode VARCHAR(500) NOT NULL,
                        Payment_No VARCHAR(500) NOT NULL,
                        Payment_Amount VARCHAR(500) NOT NULL,
                        Client_Balance INTEGER NOT NULL,
                        Remarks VARCHAR(5000) NOT NULL,
                        Delivery_Terms VARCHAR(5000) NOT NULL)
                     """
        self.save_bill_query = """INSERT INTO INVOICES(Invoice_Type, Invoice_No, Invoice_Date,
                                                        Sold_By, Client_Contact, Client_Type,
                                                        Client_Name, Client_Address, Discount,
                                                        Shipping, SubTotal, Total, Payment_Date, Payment_Mode,
                                                        Payment_No, Payment_Amount, Client_Balance,
                                                        Remarks, Delivery_Terms) 
                                                        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        self.save_bill_values = (self.invoice_type_txt.get(), self.invoice_no_txt.get(),
                                 self.invoice_date_txt.get(), self.sold_by_txt.get(),
                                 self.contact_no_txt.get(), self.retail_options_lbl.cget("text"),
                                 self.client_name_txt.get(), self.client_address_txt.get(),
                                 self.discountPrice.get(), self.shippingCharges.get(),
                                 self.subTotalPrice.get(), self.totalPrice.get(),
                                 self.payment_date_txt.get(), self.payment_mode_txt.get(),
                                 self.txn_id_txt.get(), self.payment_amount_txt.get(),
                                 self.payment_balance_txt.get(), self.remarks_txt.get("1.0", END),
                                 self.delivery_terms_txt.get("1.0", END)
                                 )
        self.cursor.execute(self.query)
        self.cursor.execute(self.save_bill_query, self.save_bill_values)
        self.conn.commit()
        self.conn.close()
        self.save_items = json.dumps(self.items, indent=len(self.items))
        with open(f"Details\\{self.client_name_txt.get()}{self.invoice_no_txt.get()}.json", "w") as outfile:
            outfile.write(self.save_items)
        self.save_excel()
        self.temp = re.compile('([a-zA-Z]+)([0-9]+)')
        self.res = self.temp.match(self.invoice_no_var.get()).groups()
        self.invoice_no = int(self.res[1])
        self.invoice_no += 1
        self.invoice_number = str(self.res[0]) + str(self.invoice_no)
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.sql_string = '''UPDATE ID where Category = ?
                             SET Id = ?'''
        self.sql_string_query = ("Invoice", self.invoice_number)
        self.conn.commit()
        self.conn.close()

    # Saving Excel Function
    def save_excel(self):

        # Getting Details From Database
        self.conn = sqlite3.connect("DB\\Invoices.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM INVOICES where Invoice_No = ?", (self.invoice_no_txt.get(),))
        self.rows = self.cursor.fetchone()

        # Excel File Starting
        self.xlWorkBook = load_workbook(f"Images\\Workbook_2.xlsx")
        self.xlSheet = self.xlWorkBook.active
        del self.xlWorkBook['Invoice']._images[0]
        self.xlSheet.title = "Invoice"
        self.headerxl = ["No.", "Name", "Rate", "Quantity", "Price", "Total Price:- ",  # + totalPrice.get()
                         str(date.today())]
        self.delivery_date = str(date.today() + timedelta(4))
        self.col = 0
        self.row = 0
        self.img = openpyxl.drawing.image.Image('Images\\Logo.png')
        self.img.anchor = "F1"
        self.img.width = 213.165312
        self.img.height = 91.0866144
        self.xlSheet.add_image(self.img)
        self.xlSheet.cell(row=self.row + 9, column=self.col + 1, value=f"Customer Name:- {self.rows[7]}")
        self.xlSheet.cell(row=self.row + 10, column=self.col + 1, value=f"Customer Contact No:- {self.rows[5]}")
        self.xlSheet.cell(row=self.row + 12, column=self.col + 1, value=self.rows[8])
        self.xlSheet.cell(row=self.row + 9, column=self.col + 5, value=self.headerxl[6])
        self.xlSheet.cell(row=self.row + 6, column=self.col + 7, value=self.headerxl[6])
        self.xlSheet.cell(row=self.row + 6, column=self.col + 5, value=self.rows[2])
        self.xlSheet.cell(row=self.row + 11, column=self.col + 5, value=str(self.delivery_date))
        self.xlSheet.cell(row=self.row + 32, column=self.col + 7, value=self.rows[11])
        self.xlSheet.print_area = 'A1:G42'
        self.xlSheet.print_options.verticalCentered = True
        self.xlSheet.print_options.horizontalCentered = True
        self.row1 = 17

        for i in self.categories:
            for j in self.items[i].keys():
                self.lis = self.items[i][j]
                self.names1 = self.lis[0]
                self.rates1 = self.lis[1]
                self.units1 = self.lis[7]
                self.quantitys1 = self.lis[2]
                self.prices1 = self.lis[3]
                self.xlSheet.cell(row=self.row1, column=self.col + 1, value=self.names1)
                self.xlSheet.cell(row=self.row1, column=self.col + 5, value=self.quantitys1)
                self.xlSheet.cell(row=self.row1, column=self.col + 6, value=self.rates1)
                self.xlSheet.cell(row=self.row1, column=self.col + 7, value=self.units1)
                self.xlSheet.cell(row=self.row1, column=self.col + 8, value=self.prices1)
                self.row1 = self.row1 + 1

        self.xlWorkBook.save(f"Bill Records\\{self.rows[7]}{self.rows[2]}.xlsx")
        self.xlWorkBook.close()

    def print_excel(self):

        # Getting Details From Database
        self.conn = sqlite3.connect("DB\\Invoices.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM INVOICES where Invoice_No = ?", (self.invoice_no_txt.get(),))
        self.rows = self.cursor.fetchone()

        # Saving As PNG To Preview
        # Path to original excel file
        self.WB_PATH = f"{os.getcwd()}\\Bill Records\\{self.rows[7]}{self.rows[2]}.xlsx"
        # PDF path when saving
        self.PATH_TO_PDF = f"{os.getcwd()}\\Bill Records\\{self.rows[7]}{self.rows[2]}.pdf"

        self.excel = win32com.client.Dispatch("Excel.Application")

        self.excel.Visible = False

        try:
            print('Start conversion to PDF')

            # Open
            self.wb = self.excel.Workbooks.Open(self.WB_PATH)

            # Specify the sheet you want to save by index. 1 is the first (leftmost) sheet.
            self.ws_index_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            self.wb.WorkSheets(self.ws_index_list[0]).Select()

            # Save
            self.wb.ActiveSheet.ExportAsFixedFormat(0, self.PATH_TO_PDF)
        except com_error as e:
            print(f"failed. due to {e}")
            return
        else:
            self.wb.Close()
            self.excel.Quit()

        self.f = f"{os.getcwd()}\\Bill Records\\{self.rows[7]}{self.rows[2]}.pdf"
        self.newfilename = ""
        try:
            with(wand.image.Image(filename=self.f, resolution=120)) as source:
                for i, image in enumerate(source.sequence):
                    self.newfilename = self.f[:-4] + str(i + 1) + '.png'
                    wand.image.Image(image).save(filename=self.newfilename)
        except wand.exceptions.DelegateError as e:
            print(e)

    # Saving & Printing Bills
    def print_operation(self):
        self.ans = tmsg.askquestion("Are You Sure?", "Are You Sure To Print Bill?")
        if self.ans == "yes":
            # Loading Start
            self.loading_start = time.time()
            self.loading_screen = Tk()
            self.loading_screen.overrideredirect(True)
            self.loading_screen.focus_set()
            self.loading_bar = ttk.Progressbar(self.loading_screen, orient=HORIZONTAL, length=200,
                                               mode="determinate", maximum=100, value=20)
            self.loading_bar.pack()
            # Save Function
            self.save_operation()
            self.loading_bar.step(50)
            # Print Function
            self.print_excel()
            self.root.update_idletasks()
            self.invoice = self.invoice_no_txt.get()
            # Destroying Root Window
            self.root.destroy()
            del self.root
            self.loading_bar.step(30)
            self.loading_screen.destroy()

            # Loading End
            self.loading_end = time.time()

            # Print Preview Window
            self.print_preview_window = Tk()
            self.print_preview_window['bg'] = "white"

            self.print_frame = Frame(self.print_preview_window, bg="white")
            self.print_frame.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)

            self.print_btn = ttk.Button(self.print_preview_window, text="Print", style="S.TButton",
                                        command=self.print_button)
            self.print_btn.place(relx=0, rely=0.1)
            try:
                self.print_image = PhotoImage(file=self.newfilename)
                print(self.newfilename)
                self.print_page = Label(self.print_frame, image=self.print_image)
                self.print_page.pack(anchor=CENTER, fill=BOTH)
            except Exception as e:
                print(e)

    # Print Button
    def print_button(self):
        # Getting Details From Database
        self.conn = sqlite3.connect("DB\\Invoices.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM INVOICES where Invoice_No = ?", (self.invoice,))
        self.rows = self.cursor.fetchone()

        # Printing Excel File
        # Path to original excel file
        self.WB_PATH = f"{os.getcwd()}\\Bill Records\\{self.rows[7]}{self.rows[2]}.xlsx"

        self.excel = win32com.client.Dispatch("Excel.Application")

        self.excel.Visible = False
        try:
            print('Start Printing')

            # Open
            self.wb = self.excel.Workbooks.Open(self.WB_PATH)

            # Specify the sheet you want to save by index. 1 is the first (leftmost) sheet.
            self.ws_index_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            self.wb.WorkSheets(self.ws_index_list[0]).Select()

            # Print
            self.wb.ActiveSheet.PrintOut()

            # Deleting All Files
            os.remove(self.WB_PATH)
            os.remove(self.newfilename)
            os.remove(self.f)

        except com_error as e:
            print(f"failed. due to {e}")
            return
        else:
            self.print_preview_window.destroy()
            self.wb.Save(True)
            self.wb.Close()
            self.excel.Quit()
            del self.print_preview_window
            del self.wb
            del self.excel

    def update_total_price(self):
        self.subPrice = 0
        self.totalprice = 0
        for i in self.categories.keys():
            for j in self.items[i].keys():
                self.subPrice += int(self.items[i][j][3])
        if self.subPrice == 0:
            self.subTotalPrice.set("")
        else:
            self.subTotalPrice.set("Rs." + str(self.subPrice) + " /-")
            self.payment_amount_var.set(str(self.subPrice))
        print(self.discount_var.get())
        if self.discount_var.get() == 1:
            self.discountPrice.set(str(self.discount_charges_txt.get()))
        else:
            self.discountPrice.set(str(0))
        if self.shipping_var.get() == 1:
            if self.shipping_charges_sel.get() != "Select":
                self.shippingCharges.set(str(self.shipping_charges_sel.get()))
            else:
                self.shippingCharges.set(str(self.shipping_charges_txt.get()))
        else:
            self.shippingCharges.set(str(0))
        if self.totalprice == 0:
            try:
                self.totalprice = str(
                    int(self.subPrice) - int(self.discountPrice.get()) + int(self.shippingCharges.get()))
                self.totalPrice.set(self.totalprice)
            except Exception as e:
                self.totalprice = 0
                self.shippingCharges.set(0)
                self.totalPrice.set(self.totalprice)

    # Getting Object Entries From Outside
    def get_object(self, object):
        get_objec = object
        try:
            get_objec.get()
        except Exception as e:
            print(e)
        return get_objec

    # Setting Object Entries From Outside
    def set_object(self, object, value):
        set_objec = object
        try:
            set_objec.set(value)
        except Exception as e:
            print(e)
        return set_objec

    # Adding Shipping Entries
    def add_shipping(self):

        # IF ELSE Statement For Adding And Removing Shipping Entries According to CheckButton
        if self.shipping_var.get() == 1:
            self.shipping_charges_txt = ttk.Entry(self.root, font=("Calibri", 12))
            self.shipping_charges_txt.place(relx=0.43, rely=0.77, relwidth=0.05)
            self.shipping_charges_sel = ttk.Combobox(self.root, values=["Select", "10", "15", "25", "50"])
            self.shipping_charges_sel.place(relx=0.49, rely=0.77, relwidth=0.05)
            self.shipping_charges_sel.current(0)
            self.shipping_charges_txt.bind("<KeyRelease>", self.update_total_price_event)
            self.shipping_charges_sel.bind("<<ComboboxSelected>>", self.update_total_price_event)
        else:
            self.shipping_charges_txt.destroy()
            self.shipping_charges_sel.destroy()

    def add_shipping_percent(self):
        self.shippingCharges.set(str(self.shipping_charges_sel.get()))
        self.update_shipping_charges()

    # Adding Shipping Charges Amount in ShippingCharges TXT
    def update_shipping_charges(self):
        self.shipping = self.shipping_charges_sel.get()
        self.price = self.totalPrice.get()

    # Adding Particulars To Particulars Treeview
    def add_particular_func(self):
        if self.category_txt.get() == "Select" or self.item_name_txt.get() == "" or self.item_rate_txt.get() == "" or self.item_units_txt.get() == "":
            tmsg.showerror("Error", "Please Fill All Required Fields.", parent=self.root)
        else:
            # Variables For Getting Row Values
            name = self.item_name_txt.get()
            rate = self.item_rate_txt.get()
            qty = self.item_qty_txt.get()
            item_code = self.item_code_txt.get()
            sub_category = self.sub_category_txt.get()
            category = self.category_txt.get()
            unit = self.item_units_txt.get()

            # IF Statement For Checking If Name Already Exist in Order
            if name in self.items[category].keys():
                tmsg.showinfo("Error", "Item already exist in your order")
                return
            # IF Statement For Checking If Quantity Is Digit in Order
            if not qty.isdigit():
                tmsg.showinfo("Error", "Please Enter Valid Quantity")
                return

            # Getting Items in List Variable
            self.lis = [name, rate, qty, str(int(rate) * int(qty)), item_code, sub_category, category, unit]
            self.items[category][name] = self.lis

            # Getting The Last Row Of Particulars Treeview
            last_row = len(self.particulars_treeview.get_children(""))

            # IF ELSE Statement For Getting Last Row And Inserting It To Particulars Treeview
            if last_row != 0:
                self.particulars_treeview.insert('', END,
                                                 values=(last_row, name, rate, qty, item_code, sub_category, category),
                                                 tags=('oddrow',))
                self.update_total_price()
            else:
                self.particulars_treeview.insert('', END,
                                                 values=(1, name, rate, qty, item_code, sub_category, category),
                                                 tags=('oddrow',))
                self.update_total_price()

    # Item Menu Function
    def select_from_menu(self):

        # Connecting to Database
        self.conn = sqlite3.connect('DB\\Items.db')
        self.cursor = self.conn.cursor()

        # Item Menu Window
        self.item_menu = Toplevel()

        # Style For TTK
        self.style = ttk.Style(self.item_menu)

        # Using Theme AWLIGHT
        self.style.theme_use('awlight')

        # Treeview Style
        self.style.configure("T.Treeview", background="black", fieldbackground="white", foreground="black")

        # Treeview Heading Style
        self.style.configure("T.Treeview.Heading", background="#26e881", foreground="white", rowheight=35,
                             font=("Calibri", 15))

        # Functions For Item Menu Window
        self.item_menu.title("Product Menu")
        self.item_menu.geometry("600x600+100+12")
        self.item_menu.attributes('-topmost', 1)
        self.item_menu.attributes('-toolwindow', 1)
        self.item_menu.focus_force()

        # Treeview For Items
        self.item_treeview = ttk.Treeview(self.item_menu, style="T.Treeview",
                                          columns=(
                                              "No.", "Name", "Rate",
                                              "Quantity", "Item Code", "Sub-Category", "Category"), )
        # height=len(self.rows))

        # Vertical Scrollbar
        self.vsb = Scrollbar(self.item_treeview,
                             orient="vertical",
                             command=self.item_treeview.yview
                             )

        # Horizontal Scrollbar
        self.hsb = Scrollbar(self.item_treeview,
                             orient="horizontal",
                             command=self.item_treeview.xview
                             )

        # Scroll Command For Treeview
        self.item_treeview['yscrollcommand'] = self.vsb.set
        self.item_treeview['xscrollcommand'] = self.hsb.set

        # Heading For Treeview
        self.item_treeview.heading("No.", text="No.")
        self.item_treeview.heading("Name", text="Name")
        self.item_treeview.heading("Rate", text="Rate")
        self.item_treeview.heading("Quantity", text="Quantity")
        self.item_treeview.heading("Item Code", text="Item Code")
        self.item_treeview.heading("Sub-Category", text="Sub-Category")
        self.item_treeview.heading("Category", text="Category")
        self.item_treeview["displaycolumns"] = ("No.", "Name", "Rate",
                                                "Quantity", "Item Code", "Sub-Category", "Category")
        self.item_treeview["show"] = "headings"

        # Columns For Treeview
        self.item_treeview.column("No.", width=150, anchor='center')
        self.item_treeview.column("Name", width=150, anchor='center')
        self.item_treeview.column("Rate", width=150, anchor='center')
        self.item_treeview.column("Quantity", width=150, anchor='center')
        self.item_treeview.column("Item Code", width=150, anchor='center')
        self.item_treeview.column("Sub-Category", width=150, anchor='center')
        self.item_treeview.column("Category", width=150, anchor='center')

        # Tags For Treeview
        self.item_treeview.tag_configure('oddrow', background="white")
        self.item_treeview.tag_configure('evenrow', background="#c5dbbf")

        # Creating Table In Database
        sql = '''CREATE TABLE IF NOT EXISTS ITEMS(
           id  INTEGER PRIMARY KEY,
           Category VARCHAR(50) NOT NULL,
           Sub_Category VARCHAR(50) NOT NULL,
           Item_Code VARCHAR(500) NOT NULL,
           Item_Name VARCHAR(500) NOT NULL,
           Item_Rate INTEGER NOT NULL,
           Item_Qty INTEGER NOT NULL)'''

        # Fake Data For Database
        values = [('EXAMPLE', '', 'a', 'a', '500', '5'),
                  ('EXAMPLE', '', 'b', 'b', '515', '7'),
                  ('EXAMPLE', '', 'c', 'c', '800', '6'),
                  ('EXAMPLE', '', 'd', 'd', '545', '17'),
                  ('EXAMPLE', '', 'e', 'e', '657', '21'),
                  ('EXAMPLE', '', 'f', 'f', '491', '56'),
                  ('EXAMPLE', '', 'g', 'g', '561', '87'),
                  ('EXAMPLE', '', 'g', 'name', '345', '78')]
        # Commands For Inserting Fake Data In Items Treeview
        '''self.cursor.executemany("""INSERT INTO ITEMS(Category, Sub_Category, Item_Code,
         Item_Name, Item_Rate, Item_Qty) VALUES(?,?,?,?,?,?)""", values)'''
        # For Deleting Items From Treeview For Delete Button TESTING
        '''self.cursor.execute("DELETE FROM ITEMS WHERE Category = ?", 'a')
        self.cursor.execute("DELETE FROM ITEMS WHERE Category = ?", 'g')'''

        # Selecting Items From Database For Treeview
        self.cursor.execute("SELECT  * FROM ITEMS")

        # Rows Of Data
        self.rows = self.cursor.fetchall()

        # Deleting Table ITEMS
        # self.conn.execute("DROP TABLE ITEMS")

        # Executing SQLITE Commands
        self.cursor.execute(sql)

        # Inserting Data Into Treeview
        self.count = 0
        self.nu = 1

        # Through For Loop
        for a, b, c, d, e, f, g in self.rows:
            # IF ELSE Statements For Striped Treeview
            if self.count % 2 == 0:
                self.item_treeview.insert('', END,
                                          values=(self.nu, e, f, g, d, c, b),
                                          tags=('evenrow',))
                self.count += 1
                self.nu += 1
            else:
                self.item_treeview.insert('', END,
                                          values=(self.nu, e, f, g, d, c, b),
                                          tags=('oddrow',))
                self.count += 1
                self.nu += 1

        # Packing Vertical Scrollbar
        self.vsb.pack(side=RIGHT, fill=Y)

        # Packing Horizontal Scrollbar
        self.hsb.pack(side=BOTTOM, fill=X)

        # Configuring Scrollbars For Treeview
        self.vsb.configure(command=self.item_treeview.yview)
        self.hsb.configure(command=self.item_treeview.xview)

        # Packing Item Treeview
        self.item_treeview.pack(fill=BOTH, expand=1)

        # Add Item Button
        self.add_item_btn = ttk.Button(self.item_menu, text="Add Item", compound=LEFT,
                                       cursor="hand2", style="S.TButton", command=self.add_item_to_menu)
        self.add_item_btn.pack(anchor=W)

    # Adding Items To Particulars Treeview from Item Treeview
    def add_item_to_menu(self):

        # Getting The Last Row Of Particulars Treeview
        last_row = len(self.particulars_treeview.get_children())

        print(last_row)

        # Giving Variable For Focusing Treeview
        cursor_row = self.item_treeview.focus()

        # Using Focus Variable To Get Item Values
        contents = self.item_treeview.item(cursor_row)

        # Variable For Storing Item Values
        row = contents['values']

        # Variables For Getting Row Values
        name = row[1]
        rate = row[2]
        qty = row[3]
        item_code = row[4]
        sub_category = row[5]
        category = row[6]

        # IF Statement For Checking If Name Already Exist in Order
        if name in self.items[category].keys():
            tmsg.showinfo("Error", "Item already exist in your order")
            return

        # IF Statement For Checking If Quantity Is Digit in Order
        '''if not qty.isdigit():
            tmsg.showinfo("Error", "Please Enter Valid Quantity")
            return'''

        # Getting Items in List Variable
        self.lis = [name, rate, qty, str(int(rate) * int(qty)), item_code, sub_category, category]
        self.items[category][name] = self.lis
        # IF ELSE Statement For Getting Last Row And Inserting It To Particulars Treeview
        if last_row != 0:
            print(str(1))
            self.particulars_treeview.insert('', END,
                                             values=(
                                                 str(last_row + 1), name, rate, qty,
                                                 item_code, sub_category, category),
                                             tags=('oddrow',))
            self.update_total_price()
        else:
            print(str(2))
            self.particulars_treeview.insert('', END,
                                             values=(1, name, rate, qty, item_code, sub_category, category),
                                             tags=('oddrow',))
            self.update_total_price()


'''# Testing Invoice Class
# Root Window
root = Tk()
# Invoice Class
obj = Invoice(root)
root1 = obj.shipping_var
obj.get_object(root1)
obj.set_object(root1, 0)
# Loop For Running Root Window
root.mainloop()'''
