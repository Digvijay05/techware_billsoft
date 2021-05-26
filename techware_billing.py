import os
import sqlite3
import tkinter.messagebox as tmsg
import tkinter.ttk as ttk
from tkinter import *
from tkinter import scrolledtext, filedialog

import ttkwidgets.autocomplete
from tkcalendar import DateEntry

from Digvijay_Algos.custom_widgets import Add_Staff_Window, Add_Expense_Window, Add_Client_Window, Designation_Window, \
    Category_Window, Unit_Window, Id_Window, Expenses_Window, Manage_Items, Add_Item_Window
from techware_invoice import Invoice
from test2 import Clock, CreateToolTip


class Home:
    def __init__(self, root):
        self.root = root
        self.root.title("Techware BillSoft V1.0")
        self.root.state("zoomed")
        self.root.resizable(0, 0)
        self.root['bg'] = "white"

        self.style = ttk.Style(self.root)

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
        # load the awdark and awlight themes
        self.root.tk.call("package", "require", 'awthemes')
        self.root.tk.call("package", "require", 'awlight')

        self.style.theme_use('awlight')
        self.style = ttk.Style(self.root)
        self.style.configure("C.TButton", font=("Calibri", 12), takefocus=False,
                             shiftrelief=0)
        self.style.map("C.TButton",
                       foreground=[('!active', 'white'), ('pressed', 'white'), ('active', 'white')],
                       background=[('!active', '#11481a'), ('pressed', '#39d44b'), ('active', '#096119')]
                       )

        self.style.map("S.TButton",
                       foreground=[('!active', 'white'), ('pressed', 'white'), ('active', 'white')],
                       background=[('!active', '#00bd61'), ('pressed', '#00e375'), ('active', '#00d16c')]
                       )
        self.style.configure("S.TChkBox", font=("Calibri", 12), takefocus=False)
        self.style.configure("T.Treeview", background="black", fieldbackground="white", foreground="black")

        self.style.configure("T.Treeview.Heading", background="#26e881", foreground="white", rowheight=35,
                             font=("Calibri", 15))

        self.dashboard = Frame(self.root, bg="#00b33c")
        self.dashboard.place(relx=0, rely=0.130, relwidth=0.150, relheight=0.95)
        self.top = Frame(self.root, bg="white", relief=RIDGE, bd=2)
        self.top.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        self.version = Frame(self.root, bg="#094416", relief=RIDGE, bd=1)
        self.version.place(relx=0, rely=0.10, relwidth=0.150, relheight=0.030)
        self.version_lbl = Label(self.version, text="Version. 1.0", font=("Calibri", 10), fg="#f2f2df", bg="#094416")
        self.version_lbl.place(relx=0, rely=0, relwidth=1.0)
        self.bottom = Frame(self.root, bg="lightgray", relief=RIDGE, bd=2)
        self.bottom.place(relx=0.150, rely=0.94, relwidth=0.95, relheight=0.15)
        self.quickInfo = Frame(self.root, bg="#00c814")
        self.quickInfo.place(relx=0.160, rely=0.120, relwidth=0.260, relheight=0.2)
        self.delivery = Frame(self.root)
        self.delivery.place(relx=0.160, rely=0.65, relwidth=0.260, relheight=0.28)

        self.delivery_lbl = Label(self.delivery, bg="#095108", text="DISTRIBUTION IN LAST 30 DAYS", anchor=W, fg="white"
                                  , font=("Calibri", 13))
        self.delivery_lbl.place(relx=0, rely=0, relwidth=1, relheight=0.15)

        self.quickInfo_txt = Label(self.quickInfo, text="QUICK INFO", font=("Calibri", 11), bg="#00c814", fg="white")
        self.quickInfo_txt.place(relx=0.01, rely=0.08)

        self.quickInfo_today = Label(self.quickInfo, text="TODAY", font=("Calibri", 13), bg="#ff6f5e", fg="white")
        self.quickInfo_today.place(relx=0.68, rely=0.05, relwidth=0.3, relheight=0.26)

        self.quickInfo_gross = Label(self.quickInfo, text="GROSS SALE", font=("Calibri", 10), bg="#00c814", fg="white")
        self.quickInfo_gross.place(relx=0.01, rely=0.60)

        self.quickInfo_amo_rec = Label(self.quickInfo, text="AMOUNT RECEIVED", font=("Calibri", 10), bg="#00c814",
                                       fg="white")
        self.quickInfo_amo_rec.place(relx=0.31, rely=0.60)

        self.quickInfo_amo_due = Label(self.quickInfo, text="AMOUNT DUE", font=("Calibri", 10), bg="#00c814",
                                       fg="white")
        self.quickInfo_amo_due.place(relx=0.71, rely=0.60)

        self.newInvoice_image = PhotoImage(file="Images\\New Invoice.png", master=self.root)
        self.newInvoice = ttk.Button(self.root, text="  New Invoice", image=self.newInvoice_image, compound="left",
                                     cursor="hand2", style="C.TButton", command=self.new_invoice_btn)
        self.newInvoice.place(relx=0.160, rely=0.35, relwidth=0.11, relheight=0.06)
        CreateToolTip(self.newInvoice, "Create An Invoice")
        self.newPayment_image = PhotoImage(file="Images\\New Payment.png", master=self.root)
        self.newPayment = ttk.Button(self.root, text="  New Payment", image=self.newPayment_image, compound=LEFT,
                                     cursor="hand2", style="C.TButton", command=self.new_invoice_btn)
        self.newPayment.place(relx=0.310, rely=0.35, relwidth=0.11, relheight=0.06)

        self.newItem_image = PhotoImage(file="Images\\New Item.png", master=self.root)
        self.newItem = ttk.Button(self.root, text="  Add Item", image=self.newItem_image, compound=LEFT,
                                  cursor="hand2", style="S.TButton", command=self.add_item_btn)
        self.newItem.place(relx=0.160, rely=0.43, relwidth=0.11, relheight=0.05)

        self.newExpense_image = PhotoImage(file="Images\\Expense.png", master=self.root)
        self.newExpense = ttk.Button(self.root, text="  Add Expense", image=self.newExpense_image, compound=LEFT,
                                     cursor="hand2", style="S.TButton", command=self.add_expense_btn)
        self.newExpense.place(relx=0.310, rely=0.43, relwidth=0.11, relheight=0.05)

        self.newCustomer_image = PhotoImage(file="Images\\Customer Image.png", master=self.root)
        self.newCustomer = ttk.Button(self.root, text="  Add Customer", image=self.newCustomer_image, compound=LEFT,
                                      cursor="hand2", style="S.TButton", command=self.add_client_btn)
        self.newCustomer.place(relx=0.160, rely=0.50, relwidth=0.11, relheight=0.05)

        self.newStaff_image = PhotoImage(file="Images\\Staff Image.png", master=self.root)
        self.newStaff = ttk.Button(self.root, text="  Add Staff", image=self.newStaff_image, compound=LEFT,
                                   cursor="hand2", style="S.TButton", command=self.add_staff_btn)
        self.newStaff.place(relx=0.310, rely=0.50, relwidth=0.11, relheight=0.05)

        self.paymentIn_image = PhotoImage(file="Images\\Add.png", master=self.root)
        self.paymentIn = ttk.Button(self.root, text="  Payment In", image=self.paymentIn_image, compound=LEFT,
                                    cursor="hand2", style="C.TButton")
        self.paymentIn.place(relx=0.160, rely=0.57, relwidth=0.11, relheight=0.05)

        self.paymentOut_image = PhotoImage(file="Images\\Subtract.png", master=self.root)
        self.paymentOut = ttk.Button(self.root, text="  Payment Out", image=self.paymentOut_image, compound=LEFT,
                                     cursor="hand2", style="C.TButton")
        self.paymentOut.place(relx=0.310, rely=0.57, relwidth=0.11, relheight=0.05)

        self.sale_image = PhotoImage(file="Images\\Sale Image.png", master=self.root)
        # Create a menu button
        self.sale = Menubutton(self.dashboard, image=self.sale_image, cursor="hand2", text="  Sale", fg="white",
                               bg="#00b33c", direction=RIGHT,
                               font=("Calibri", 13), compound=LEFT, anchor="w")
        # Create pull down menu
        self.sale.menu = Menu(self.sale, tearoff=0)
        self.sale["menu"] = self.sale.menu
        self.sale['activebackground'] = "#13551e"
        self.sale['activeforeground'] = "white"
        # Add some commands
        self.sale.menu.add_command(label="New Invoice", command=self.new_invoice_btn, font=("Calibri", 13))
        self.sale.menu.add_command(label="Search and Manage Invoices", font=("Calibri", 13),
                                   command=self.manage_invoices())
        self.sale.menu.add_separator()
        self.sale.menu.add_command(label="New Delivery", font=("Calibri", 13))
        self.sale.menu.add_command(label="Search and Manage Deliveries", font=("Calibri", 13))
        self.sale.menu.add_separator()
        self.sale.menu.add_command(label="New Payments", font=("Calibri", 13))
        self.sale.menu.add_command(label="Search and Manage Payments", font=("Calibri", 13))
        self.sale.place(relx=0, rely=0, relwidth=1, relheight=0.05)

        self.staff_image = PhotoImage(file="Images\\Staff Image.png", master=self.root)
        self.staff = Menubutton(self.dashboard, image=self.staff_image, text="  Staff", fg="white", bg="#00b33c",
                                font=("Calibri", 13), compound=LEFT, anchor="w", direction=RIGHT)
        self.staff.menu = Menu(self.staff, tearoff=0)
        self.staff["menu"] = self.staff.menu
        self.staff['activebackground'] = "#13551e"
        self.staff['activeforeground'] = "white"
        self.staff.menu.add_command(label="Add Staff", command=self.add_staff_btn, font=("Calibri", 14))
        self.staff.menu.add_command(label="Search and Manage Staff", font=("Calibri", 14),
                                    command=self.manage_staff_btn)
        self.staff.place(relx=0, rely=0.05, relwidth=1, relheight=0.05)

        self.customer_image = PhotoImage(file="Images\\Customer Image.png", master=self.root)
        self.customer = Menubutton(self.dashboard, image=self.customer_image, text="  Customer", fg="white",
                                   bg="#00b33c",
                                   font=("Calibri", 13), compound=LEFT, anchor="w", direction=RIGHT)
        self.customer.menu = Menu(self.customer, tearoff=0)
        self.customer["menu"] = self.customer.menu
        self.customer['activebackground'] = "#13551e"
        self.customer['activeforeground'] = "white"
        self.customer.menu.add_command(label="Add Customer", command=self.add_client_btn, font=("Calibri", 14))
        self.customer.menu.add_command(label="Search and Manage Customers", font=("Calibri", 14),
                                       command=self.manage_client_btn)
        self.customer.place(relx=0, rely=0.1, relwidth=1, relheight=0.05)

        self.expense_image = PhotoImage(file="Images\\Expense.png", master=self.root)
        self.expense = Menubutton(self.dashboard, image=self.expense_image, text="  Expenses", fg="white",
                                  bg="#00b33c",
                                  font=("Calibri", 13), compound=LEFT, anchor="w", direction=RIGHT)
        self.expense.menu = Menu(self.expense, tearoff=0)
        self.expense["menu"] = self.expense.menu
        self.expense['activebackground'] = "#13551e"
        self.expense['activeforeground'] = "white"
        self.expense.menu.add_command(label="Add Expense", command=self.add_expense_btn, font=("Calibri", 14))
        self.expense.menu.add_command(label="Search and Manage Expenses", font=("Calibri", 14))
        self.expense.place(relx=0, rely=0.15, relwidth=1, relheight=0.05)

        self.reports_image = PhotoImage(file="Images\\Reports.png", master=self.root)
        self.reports = Menubutton(self.dashboard, image=self.reports_image, text="  Reports", fg="white",
                                  bg="#00b33c", state=DISABLED,
                                  font=("Calibri", 13), compound=LEFT, anchor="w", direction=RIGHT)
        self.reports.menu = Menu(self.reports, tearoff=0)
        self.reports["menu"] = self.reports.menu
        self.reports['activebackground'] = "#13551e"
        self.reports['activeforeground'] = "white"
        self.reports.menu.add_command(label="Daily Reports", command=self.daily_report, font=("Calibri", 13))
        self.reports.menu.add_command(label="Monthly Reports", command=self.monthly_report, font=("Calibri", 13))
        self.reports.menu.add_command(label="Yearly Reports", command=self.yearly_report, font=("Calibri", 13))
        self.reports.menu.add_command(label="Lifetime Report", command=self.lifetime_report, font=("Calibri", 13))
        self.reports.place(relx=0, rely=0.20, relwidth=1, relheight=0.05)

        CreateToolTip(self.reports, f"Coming Soon! Your Reports Are Still Generated in {os.getcwd()}\\Monthly Bills.")

        self.master_image = PhotoImage(file="Images\\Master.png", master=self.root)
        self.master = Menubutton(self.dashboard, image=self.master_image, text="  Master", fg="white",
                                 bg="#00b33c",
                                 font=("Calibri", 13), compound=LEFT, anchor="w", direction=RIGHT)
        self.master.menu = Menu(self.master, tearoff=0)
        self.miscellaneous = Menu(self.master, tearoff=0)
        self.bulk_add = Menu(self.master, tearoff=0)
        self.master["menu"] = self.master.menu
        self.master['activebackground'] = "#13551e"
        self.master['activeforeground'] = "white"
        self.master.menu.add_command(label="Add Product", command=self.add_item_btn, font=("Calibri", 13))
        self.master.menu.add_command(label="Search & Manage Items", command=self.manage_item_btn, font=("Calibri", 13))
        self.master.menu.add_separator()
        self.master.menu.add_command(label="Create Special Ids", command=self.id_add, font=("Calibri", 13))
        self.master.menu.add_cascade(label="Bulk Import", menu=self.bulk_add, font=("Calibri", 13))
        self.master.menu.add_separator()
        self.master.menu.add_command(label="Brand Master", font=("Calibri", 13))
        self.master.menu.add_command(label="Group Master", font=("Calibri", 13))
        self.master.menu.add_command(label="Bank Master", font=("Calibri", 13))
        self.master.menu.add_cascade(label="Miscellaneous", font=("Calibri", 13), menu=self.miscellaneous)
        self.miscellaneous.add_command(label="Unit Master", font=("Calibri", 13), command=self.unit_add)
        self.miscellaneous.add_command(label="Category Master", font=("Calibri", 13), command=self.category_add)
        self.miscellaneous.add_command(label="Expense Master", font=("Calibri", 13), command=self.expense_add)
        self.miscellaneous.add_command(label="Holiday Master", font=("Calibri", 13))
        self.miscellaneous.add_command(label="Designation Master", font=("Calibri", 13), command=self.designation_add)
        self.bulk_add.add_command(label="Import Staff", font=("Calibri", 13))
        self.bulk_add.add_command(label="Import Customers", font=("Calibri", 13))
        self.bulk_add.add_command(label="Import Items", font=("Calibri", 13))
        self.master.place(relx=0, rely=0.25, relwidth=1, relheight=0.05)

        self.tool_image = PhotoImage(file="Images\\Tools.png", master=self.root)
        self.tool = Menubutton(self.dashboard, image=self.tool_image, text="  Tools", fg="white",
                               bg="#00b33c",
                               font=("Calibri", 13), compound=LEFT, anchor="w", direction=RIGHT)
        self.tool.menu = Menu(self.tool, tearoff=0)
        self.tool["menu"] = self.tool.menu
        self.tool['activebackground'] = "#13551e"
        self.tool['activeforeground'] = "white"
        self.tool.menu.add_command(label="GST Calculator", command=self.gst_calc_btn, font=("Calibri", 15))
        self.tool.menu.add_command(label="Discount Calculator", command=self.disc_calc_btn, font=("Calibri", 15))
        self.tool.place(relx=0, rely=0.30, relwidth=1, relheight=0.05)

        self.setting_image = PhotoImage(file="Images\\Settings.png", master=self.root)
        self.setting = Menubutton(self.dashboard, image=self.setting_image, text="  Settings", fg="white",
                                  bg="#00b33c",
                                  font=("Calibri", 13), compound=LEFT, anchor="w", direction=RIGHT)
        self.setting.menu = Menu(self.setting, tearoff=0)
        self.setting["menu"] = self.setting.menu
        self.setting['activebackground'] = "#13551e"
        self.setting['activeforeground'] = "white"
        self.setting.place(relx=0, rely=0.35, relwidth=1, relheight=0.05)
        self.setting.bind("<ButtonRelease-1>", self.setting_btn_btn)

        """self.logo_image = PhotoImage(file="Images/Techware.png")
        self.logo = Label(self.root, image=self.logo_image)
        self.logo.place(relx=0, rely=0)"""

        self.date = Clock(self.dashboard)
        self.date.configure(bg='#00b33c', fg='white', font=("Calibri", 14))
        self.date.place(relx=0, rely=0.75, relwidth=1, relheight=0.05)

    def daily_report(self):
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM DAILY_REPORTS")
        self.rows = self.cursor.fetchall()
        self.daily_report_window = Toplevel()
        self.daily_report_window.title("Daily Report")
        self.daily_report_window.geometry("1152x672+25+12")
        self.daily_report_window.attributes('-toolwindow', 1)
        self.daily_report_window.attributes('-topmost', 'true')
        self.daily_report_window['bg'] = "white"
        self.daily_report_window.focus_force()

        self.daily_report_treeview = ttk.Treeview(self.daily_report_window,
                                                  columns=("Time",
                                                           "No. of Invoices", "Payments Received", "Avg. Invoices/Day",
                                                           "Cost of Expenses", "Avg. Cost of Expenses/Day", "TEST"),
                                                  style="T.Treeview",
                                                  height=len(self.rows))
        self.vsb = Scrollbar(self.daily_report_treeview,
                             orient="vertical",
                             command=self.daily_report_treeview.yview
                             )
        self.hsb = Scrollbar(self.daily_report_treeview,
                             orient="horizontal",
                             command=self.daily_report_treeview.xview
                             )
        self.daily_report_treeview['yscrollcommand'] = self.vsb.set
        self.daily_report_treeview['xscrollcommand'] = self.hsb.set
        self.daily_report_treeview.heading("Time", text="No. of Invoices")
        self.daily_report_treeview.heading("No. of Invoices", text="No. of Invoices")
        self.daily_report_treeview.heading("Payments Received", text="Payments Received")
        self.daily_report_treeview.heading("Avg. Invoices/Day", text="Avg. Invoices/Day")
        self.daily_report_treeview.heading("Cost of Expenses", text="Cost of Expenses")
        self.daily_report_treeview.heading("Avg. Cost of Expenses/Day", text="Avg. Cost of Expenses/Day")
        self.daily_report_treeview.heading("TEST", text="Avg. Cost of Expenses/Day")
        self.daily_report_treeview["displaycolumns"] = ("Time", "No. of Invoices", "Payments Received",
                                                        "Avg. Invoices/Day", "Cost of Expenses",
                                                        "Avg. Cost of Expenses/Day", "TEST")
        self.daily_report_treeview["show"] = "headings"
        self.daily_report_treeview.column("Time", width=150, anchor='center')
        self.daily_report_treeview.column("No. of Invoices", width=150, anchor='center')
        self.daily_report_treeview.column("Payments Received", width=150, anchor='center')
        self.daily_report_treeview.column("Avg. Invoices/Day", width=150, anchor='center')
        self.daily_report_treeview.column("Cost of Expenses", width=150, anchor='center')
        self.daily_report_treeview.column("Avg. Cost of Expenses/Day", width=150, anchor='center')
        self.daily_report_treeview.column("TEST", width=150, anchor='center')

        self.daily_report_treeview.tag_configure('oddrow', background="white")
        self.daily_report_treeview.tag_configure('evenrow', background="#c5dbbf")
        self.count = 0
        for a, b, c, d, e, f in self.rows:
            if self.count % 2 == 0:
                self.daily_report_treeview.insert('', END, values=[a, b, c, d, e, f], tags=("evenrow",))
                self.count += 1
            else:
                self.daily_report_treeview.insert('', END, values=[a, b, c, d, e, f], tags=("oddrow",))
                self.count += 1
        self.vsb.pack(side=RIGHT, fill=Y)
        self.vsb.configure(command=self.daily_report_treeview.yview)
        self.hsb.pack(side=BOTTOM, fill=X)
        self.hsb.configure(command=self.daily_report_treeview.xview)
        self.daily_report_treeview.pack(fill=BOTH, expand=1)

    def monthly_report(self):
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM MONTHLY_REPORTS")
        self.rows = self.cursor.fetchall()
        self.monthly_report_window = Toplevel()
        self.monthly_report_window.title("Daily Report")
        self.monthly_report_window.geometry("1152x672+25+12")
        self.monthly_report_window.attributes('-toolwindow', 1)
        self.monthly_report_window.attributes('-topmost', 'true')
        self.monthly_report_window['bg'] = "white"
        self.monthly_report_window.focus_force()

        self.monthly_report_treeview = ttk.Treeview(self.monthly_report_window,
                                                    columns=("Date",
                                                             "No. of Invoices", "Payments Received",
                                                             "Avg. Invoices/Day",
                                                             "Cost of Expenses", "Avg. Cost of Expenses/Day"),
                                                    style="T.Treeview",
                                                    height=len(self.rows))
        self.vsb = Scrollbar(self.monthly_report_treeview,
                             orient="vertical",
                             command=self.monthly_report_treeview.yview
                             )
        self.hsb = Scrollbar(self.monthly_report_treeview,
                             orient="horizontal",
                             command=self.monthly_report_treeview.xview
                             )
        self.monthly_report_treeview['yscrollcommand'] = self.vsb.set
        self.monthly_report_treeview['xscrollcommand'] = self.hsb.set
        self.monthly_report_treeview.heading("Date", text="Date")
        self.monthly_report_treeview.heading("No. of Invoices", text="No. of Invoices")
        self.monthly_report_treeview.heading("Payments Received", text="Payments Received")
        self.monthly_report_treeview.heading("Avg. Invoices/Day", text="Avg. Invoices/Day")
        self.monthly_report_treeview.heading("Cost of Expenses", text="Cost of Expenses")
        self.monthly_report_treeview.heading("Avg. Cost of Expenses/Day", text="Avg. Cost of Expenses/Day")
        self.monthly_report_treeview["displaycolumns"] = ("No. of Invoices", "Payments Received", "Avg. Invoices/Day",
                                                          "Cost of Expenses", "Avg. Cost of Expenses/Day")
        self.monthly_report_treeview["show"] = "headings"
        self.monthly_report_treeview.column("Date", width=150, anchor='center')
        self.monthly_report_treeview.column("No. of Invoices", width=150, anchor='center')
        self.monthly_report_treeview.column("Payments Received", width=150, anchor='center')
        self.monthly_report_treeview.column("Avg. Invoices/Day", width=150, anchor='center')
        self.monthly_report_treeview.column("Cost of Expenses", width=150, anchor='center')
        self.monthly_report_treeview.column("Avg. Cost of Expenses/Day", width=150, anchor='center')

        self.monthly_report_treeview.tag_configure('oddrow', background="white")
        self.monthly_report_treeview.tag_configure('evenrow', background="#c5dbbf")
        self.count = 0
        for a, b, c, d, e, f in self.rows:
            if self.count % 2 == 0:
                self.monthly_report_treeview.insert('', END, values=[a, b, c, d, e, f], tags=("evenrow",))
                self.count += 1
            else:
                self.monthly_report_treeview.insert('', END, values=[a, b, c, d, e, f], tags=("oddrow",))
                self.count += 1
        self.vsb.pack(side=RIGHT, fill=Y)
        self.vsb.configure(command=self.monthly_report_treeview.yview)
        self.hsb.pack(side=BOTTOM, fill=X)
        self.hsb.configure(command=self.monthly_report_treeview.xview)
        self.monthly_report_treeview.pack(fill=BOTH, expand=1)

    def yearly_report(self):
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM YEARLY_REPORTS")
        self.rows = self.cursor.fetchall()
        self.yearly_report_window = Toplevel()
        self.yearly_report_window.title("Daily Report")
        self.yearly_report_window.geometry("1152x672+25+12")
        self.yearly_report_window.attributes('-toolwindow', 1)
        self.yearly_report_window.attributes('-topmost', 'true')
        self.yearly_report_window['bg'] = "white"
        self.yearly_report_window.focus_force()

        self.yearly_report_treeview = ttk.Treeview(self.yearly_report_window,
                                                   columns=("Date",
                                                            "No. of Invoices", "Payments Received",
                                                            "Avg. Invoices/Day",
                                                            "Cost of Expenses", "Avg. Cost of Expenses/Day"),
                                                   style="T.Treeview",
                                                   height=len(self.rows))
        self.vsb = Scrollbar(self.yearly_report_treeview,
                             orient="vertical",
                             command=self.yearly_report_treeview.yview
                             )
        self.hsb = Scrollbar(self.yearly_report_treeview,
                             orient="horizontal",
                             command=self.yearly_report_treeview.xview
                             )
        self.yearly_report_treeview['yscrollcommand'] = self.vsb.set
        self.yearly_report_treeview['xscrollcommand'] = self.hsb.set
        self.yearly_report_treeview.heading("Date", text="Month")
        self.yearly_report_treeview.heading("No. of Invoices", text="No. of Invoices")
        self.yearly_report_treeview.heading("Payments Received", text="Payments Received")
        self.yearly_report_treeview.heading("Avg. Invoices/Day", text="Avg. Invoices/Day")
        self.yearly_report_treeview.heading("Cost of Expenses", text="Cost of Expenses")
        self.yearly_report_treeview.heading("Avg. Cost of Expenses/Day", text="Avg. Cost of Expenses/Day")
        self.yearly_report_treeview["displaycolumns"] = ("No. of Invoices", "Payments Received", "Avg. Invoices/Day",
                                                         "Cost of Expenses", "Avg. Cost of Expenses/Day")
        self.yearly_report_treeview["show"] = "headings"
        self.yearly_report_treeview.column("Date", width=150, anchor='center')
        self.yearly_report_treeview.column("No. of Invoices", width=150, anchor='center')
        self.yearly_report_treeview.column("Payments Received", width=150, anchor='center')
        self.yearly_report_treeview.column("Avg. Invoices/Day", width=150, anchor='center')
        self.yearly_report_treeview.column("Cost of Expenses", width=150, anchor='center')
        self.yearly_report_treeview.column("Avg. Cost of Expenses/Day", width=150, anchor='center')

        self.yearly_report_treeview.tag_configure('oddrow', background="white")
        self.yearly_report_treeview.tag_configure('evenrow', background="#c5dbbf")
        self.count = 0
        for a, b, c, d, e, f in self.rows:
            if self.count % 2 == 0:
                self.yearly_report_treeview.insert('', END, values=[a, b, c, d, e, f], tags=("evenrow",))
                self.count += 1
            else:
                self.yearly_report_treeview.insert('', END, values=[a, b, c, d, e, f], tags=("oddrow",))
                self.count += 1
        self.vsb.pack(side=RIGHT, fill=Y)
        self.vsb.configure(command=self.yearly_report_treeview.yview)
        self.hsb.pack(side=BOTTOM, fill=X)
        self.hsb.configure(command=self.yearly_report_treeview.xview)
        self.yearly_report_treeview.pack(fill=BOTH, expand=1)

    def lifetime_report(self):
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM LIFETIME_REPORT")
        self.rows = self.cursor.fetchall()
        self.lifetime_report_window = Toplevel()
        self.lifetime_report_window.title("Daily Report")
        self.lifetime_report_window.geometry("1152x672+25+12")
        self.lifetime_report_window.attributes('-toolwindow', 1)
        self.lifetime_report_window.attributes('-topmost', 'true')
        self.lifetime_report_window['bg'] = "white"
        self.lifetime_report_window.focus_force()

        self.lifetime_report_treeview = ttk.Treeview(self.lifetime_report_window,
                                                     columns=("Year",
                                                              "No. of Invoices", "Payments Received",
                                                              "Avg. Invoices/Day",
                                                              "Cost of Expenses", "Avg. Cost of Expenses/Day"),
                                                     style="T.Treeview",
                                                     height=len(self.rows))
        self.vsb = Scrollbar(self.lifetime_report_treeview,
                             orient="vertical",
                             command=self.lifetime_report_treeview.yview
                             )
        self.hsb = Scrollbar(self.lifetime_report_treeview,
                             orient="horizontal",
                             command=self.lifetime_report_treeview.xview
                             )
        self.lifetime_report_treeview['yscrollcommand'] = self.vsb.set
        self.lifetime_report_treeview['xscrollcommand'] = self.hsb.set
        self.lifetime_report_treeview.heading("Date", text="Date")
        self.lifetime_report_treeview.heading("No. of Invoices", text="No. of Invoices")
        self.lifetime_report_treeview.heading("Payments Received", text="Payments Received")
        self.lifetime_report_treeview.heading("Avg. Invoices/Day", text="Avg. Invoices/Day")
        self.lifetime_report_treeview.heading("Cost of Expenses", text="Cost of Expenses")
        self.lifetime_report_treeview.heading("Avg. Cost of Expenses/Day", text="Avg. Cost of Expenses/Day")
        self.lifetime_report_treeview["displaycolumns"] = ("No. of Invoices", "Payments Received", "Avg. Invoices/Day",
                                                           "Cost of Expenses", "Avg. Cost of Expenses/Day")
        self.lifetime_report_treeview["show"] = "headings"
        self.lifetime_report_treeview.column("Date", width=150, anchor='center')
        self.lifetime_report_treeview.column("No. of Invoices", width=150, anchor='center')
        self.lifetime_report_treeview.column("Payments Received", width=150, anchor='center')
        self.lifetime_report_treeview.column("Avg. Invoices/Day", width=150, anchor='center')
        self.lifetime_report_treeview.column("Cost of Expenses", width=150, anchor='center')
        self.lifetime_report_treeview.column("Avg. Cost of Expenses/Day", width=150, anchor='center')

        self.lifetime_report_treeview.tag_configure('oddrow', background="white")
        self.lifetime_report_treeview.tag_configure('evenrow', background="#c5dbbf")
        self.count = 0
        for a, b, c, d, e, f in self.rows:
            if self.count % 2 == 0:
                self.lifetime_report_treeview.insert('', END, values=[a, b, c, d, e, f], tags=("evenrow",))
                self.count += 1
            else:
                self.lifetime_report_treeview.insert('', END, values=[a, b, c, d, e, f], tags=("oddrow",))
                self.count += 1
        self.vsb.pack(side=RIGHT, fill=Y)
        self.vsb.configure(command=self.lifetime_report_treeview.yview)
        self.hsb.pack(side=BOTTOM, fill=X)
        self.hsb.configure(command=self.lifetime_report_treeview.xview)
        self.lifetime_report_treeview.pack(fill=BOTH, expand=1)

    def onExit(self):
        pass

    def add_item_btn(self):
        self.add_item_window = Toplevel(self.root)
        self.item = Add_Item_Window(self.add_item_window)

    def manage_item_btn(self):
        self.manage_item_window = Toplevel(self.root)
        self.items = Manage_Items(self.manage_item_window)

    def expense_add(self):
        self.add_expenses_window = Toplevel(self.root)
        self.expenses = Expenses_Window(self.add_expenses_window)

    def id_add(self):
        self.add_id_window = Toplevel(self.root)
        self.id = Id_Window(self.add_id_window)

    def unit_add(self):
        self.add_unit_window = Toplevel(self.root)
        self.unit = Unit_Window(self.add_unit_window)

    def category_add(self):
        self.add_category_window = Toplevel(self.root)
        self.category = Category_Window(self.add_category_window)

    def designation_add(self):
        self.designation_window = Toplevel(self.root)
        self.desig = Designation_Window(self.designation_window)

    def add_client_btn(self):
        self.add_client_window = Toplevel(self.root)
        self.client = Add_Client_Window(self.add_client_window)

    def new_invoice_btn(self):
        self.invoice_window = Toplevel(self.root)
        self.invoice_frame = Invoice(self.invoice_window)

    def add_staff_btn(self):
        self.add_staff_window = Toplevel(self.root)
        self.staff = Add_Staff_Window(self.add_staff_window, None)

    def add_expense_btn(self):
        self.add_expense_window = Toplevel(self.root)
        self.expense = Add_Expense_Window(self.add_expense_window)

    def gst_calc_btn(self):
        pass

    def disc_calc_btn(self):
        pass

    def setting_btn_btn(self, event):
        print(event)
        self.new_invoice_window = Toplevel()
        self.new_invoice_window.title("Settings")
        self.new_invoice_window.geometry("1152x672+25+12")
        self.new_invoice_window.attributes('-toolwindow', 1)
        self.new_invoice_window.attributes('-topmost', 1)
        self.new_invoice_window.focus_set()

    def save_client_btn(self):
        if self.client_personal_full_name_entry.get() == "" or self.client_personal_dob_entry.get() == "" or self.var_gender.get() == "" or self.client_personal_mobile_no_entry.get() == "" or self.client_personal_state_entry.get() == "":
            tmsg.showerror("Error", "Please Fill all Required Fields", parent=self.add_client_window)
        else:
            self.conn = sqlite3.connect('DB\\Clients.db')
            print(self.conn)
            self.cursor = self.conn.cursor()
            sql = '''CREATE TABLE IF NOT EXISTS CLIENT(
                               id  INTEGER PRIMARY KEY autoincrement,
                               Full_Name VARCHAR(50) NOT NULL,
                               DOB DATE NOT NULL,
                               Gender VARCHAR(50) NOT NULL,
                               EMAIL VARCHAR(100) NOT NULL,
                               Contact INT(10) NOT NULL,
                               City VARCHAR(100) NOT NULL,
                               State VARCHAR(100) NOT NULL,
                               Address VARCHAR(5000) NOT NULL,
                               GSTIN VARCHAR(100) NOT NULL,
                               PAN  VARCHAR(100) NOT NULL,
                               Contact_Person VARCHAR(100) NOT NULL,
                               Contact_Person_Number INT(10) NOT NULL,
                               Blood_Group VARCHAR(50) NOT NULL,
                               Document_Type VARCHAR(50) NOT NULL,
                               Document_No VARCHAR(5000) NOT NULL,
                               Expiry_Date DATE NOT NULL,
                               Issue_Date DATE NOT NULL,
                               Communication_SMS VARCHAR(50) NOT NULL,
                               Communication_Email VARCHAR(50) NOT NULL,
                               Sales_Commission VARCHAR(50) NOT NULL,
                               Remarks VARCHAR(500) NOT NULL)'''

            self.cursor.execute(sql)

            self.cursor.execute(
                """insert into CLIENT(Full_Name,DOB,Gender,EMAIL,Contact,City,State,Address,GSTIN,PAN,Contact_Person,
                Contact_Person_Number,Blood_Group,Document_Type,Document_No,Expiry_Date,Issue_Date,Communication_SMS,
                Communication_Email,Sales_Commission,Remarks) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    self.client_personal_full_name_entry.get(),
                    self.client_personal_dob_entry.get(),
                    self.var_gender.get(),
                    self.client_personal_email_entry.get(),
                    self.client_personal_mobile_no_entry.get(),
                    self.client_personal_city_entry.get(),
                    self.client_personal_state_entry.get(),
                    self.client_personal_address_entry.get('1.0', END),
                    self.client_tax_gstin_no_entry.get(),
                    self.client_tax_pan_no_entry.get(),
                    self.client_emergency_con_person_txt.get(),
                    self.client_emergency_con_no_txt.get(),
                    self.client_emergency_bl_gr_txt.get(),
                    self.client_id_information_doc_type_txt.get(),
                    self.client_id_information_doc_no_txt.get(),
                    self.client_id_information_exp_date_txt.get(),
                    self.client_id_information_iss_date_txt.get(),
                    self.chk_sms.get(),
                    self.chk_ema.get(),
                    self.chk_sale.get(),
                    self.client_other_information_remark_txt.get('1.0', END),
                ))
            self.conn.commit()
            self.conn.close()
            tmsg.showinfo("Success", f"Client '{self.client_personal_full_name_entry.get()} Added to Database.'")

    def save_staff_btn(self):
        if self.staff_personal_full_name_entry.get() == "" or self.staff_personal_dob_entry.get() == "" or self.var_gender.get() == "" or self.staff_personal_mobile_no_entry.get() == "" or self.staff_personal_emp_code_entry.get() == "" or self.staff_personal_address_entry.get(
                '1.0', END) == "":

            tmsg.showerror("Error", "Please Fill All Required Details", parent=self.add_staff_window)
        else:
            self.ans = tmsg.askquestion("Are you Sure?",
                                        f"Are you sure to You want ot create Staff '{self.staff_personal_full_name_entry.get()}'"
                                        , parent=self.add_staff_window)
            if self.ans == 'yes':
                self.conn = sqlite3.connect('DB\\Employee.db')
                self.cursor = self.conn.cursor()

                sql = '''CREATE TABLE IF NOT EXISTS STAFF(
                                   id  INTEGER PRIMARY KEY autoincrement,
                                   Full_Name VARCHAR(50) NOT NULL,
                                   DOB DATE NOT NULL,
                                   Gender VARCHAR(50) NOT NULL,
                                   EMAIL VARCHAR(100) NOT NULL,
                                   Contact INT(10) NOT NULL,
                                   Employee_Code VARCHAR(100) NOT NULL,
                                   Address VARCHAR(5000) NOT NULL,
                                   Join_date VARCHAR(100) NOT NULL,
                                   Designation  VARCHAR(100) NOT NULL,
                                   Contact_Person VARCHAR(100) NOT NULL,
                                   Contact_Person_Number INT(10) NOT NULL,
                                   Blood_Group VARCHAR(50) NOT NULL,
                                   Document_Type VARCHAR(50) NOT NULL,
                                   Document_No VARCHAR(5000) NOT NULL,
                                   Expiry_Date DATE NOT NULL,
                                   Issue_Date DATE NOT NULL,
                                   Communication_SMS VARCHAR(50) NOT NULL,
                                   Communication_Email VARCHAR(50) NOT NULL,
                                   Sales_Commission VARCHAR(50) NOT NULL,
                                   Remarks VARCHAR(500) NOT NULL)'''

                self.cursor.execute(sql)

                self.cursor.execute(
                    """insert into STAFF(Full_Name,DOB,Gender,EMAIL,Contact,Employee_Code,Address,Join_date,
                    Designation,Contact_Person, Contact_Person_Number,Blood_Group,Document_Type,Document_No,Expiry_Date,
                    Issue_Date,Communication_SMS, Communication_Email,Sales_Commission,Remarks) VALUES (?,?,?,?,?,?,?,?,?,?,
                    ?,?,?,?,?,?,?,?,?,?)""",
                    (
                        self.staff_personal_full_name_entry.get(),
                        self.staff_personal_dob_entry.get(),
                        self.var_gender.get(),
                        self.staff_personal_email_entry.get(),
                        self.staff_personal_mobile_no_entry.get(),
                        self.staff_personal_emp_code_entry.get(),
                        self.staff_personal_address_entry.get('1.0', END),
                        self.staff_staff_joining_date_entry.get(),
                        self.staff_staff_designation_entry.get(),
                        self.staff_emergency_con_person_txt.get(),
                        self.staff_emergency_con_no_txt.get(),
                        self.staff_emergency_bl_gr_txt.get(),
                        self.staff_id_information_doc_type_txt.get(),
                        self.staff_id_information_doc_no_txt.get(),
                        self.staff_id_information_exp_date_txt.get(),
                        self.staff_id_information_iss_date_txt.get(),
                        self.chk_sms.get(),
                        self.chk_ema.get(),
                        self.chk_sale.get(),
                        self.staff_other_information_remark_txt.get('1.0', END),
                    ))
                self.conn.commit()
                self.conn.close()
                tmsg.showinfo("Success", f"Employee '{self.staff_personal_full_name_entry.get()} Added to Database.'")

    def delete_staff_btn(self):
        if self.staff_search_txt.get() == "":
            tmsg.showerror("Error", "Please Enter Employee Code", parent=self.search_staff_window)
        else:
            self.conn = sqlite3.connect('DB\\Employee.db')
            self.cursor = self.conn.cursor()

            sqlite_update_query = """DELETE FROM STAFF where Employee_Code = ?"""

            self.cursor.execute(sqlite_update_query, (self.staff_search_txt.get(),))

            self.staff_table.delete(*self.staff_table.get_children())

            self.cursor.execute("SELECT * FROM STAFF")
            self.rows = self.cursor.fetchall()
            self.count = 0
            for id, Full_Name, DOB, Gender, EMAIL, Contact, Employee_Code, Address, Join_date, Designation, \
                Contact_Person, Contact_Person_Number, Blood_Group, Document_Type, Document_No, Expiry_Date, \
                Issue_Date, Communication_SMS, Communication_Email, Sales_Commission, Remarks in self.rows:
                if self.count % 2 == 0:
                    self.staff_table.insert('', END,
                                            values=(Employee_Code, Full_Name, Address, Contact, Contact, Designation),
                                            tags=('evenrow',))
                    self.count += 1
                else:
                    self.staff_table.insert('', END,
                                            values=(Employee_Code, Full_Name, Address, Contact, Contact, Designation),
                                            tags=('oddrow',))
                    self.count += 1
            self.conn.commit()
            self.conn.close()

    def search_staff_btn(self):
        if self.staff_search_txt.get() == "":
            tmsg.showerror("Error", "Please Enter Employee Code", parent=self.search_staff_window)
        else:
            self.conn = sqlite3.connect('DB\\Employee.db')
            self.cursor = self.conn.cursor()

            sqlite_update_query = """SELECT * from STAFF where Employee_Code = ?"""

            self.cursor.execute(sqlite_update_query, (self.staff_search_txt.get(),))

            self.rows = self.cursor.fetchone()

            self.staff_table.delete(*self.staff_table.get_children())
            self.staff_table.insert('', END,
                                    values=(self.rows[6],
                                            self.rows[1],
                                            self.rows[7],
                                            self.rows[5],
                                            self.rows[5],
                                            self.rows[9]),
                                    tags=('oddrow',))

    def imageopen(self):
        self.root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                        filetypes=(("png files", "*.png"), ("all files", "*.*")))
        print(root.filename)
        self.client_photo = PhotoImage(file=f"{root.filename}")
        self.client_photo_label['image'] = self.client_photo

    def manage_staff_btn(self):
        self.conn = sqlite3.connect('DB\\Employee.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM STAFF")
        self.rows = self.cursor.fetchall()

        self.search_staff_window = Toplevel()
        self.search_staff_window.title("Search Staff")
        self.search_staff_window.geometry("1152x672+25+12")
        self.search_staff_window.attributes('-toolwindow', 1)
        self.search_staff_window.attributes('-topmost', 'true')
        self.search_staff_window.focus_force()

        self.staff_table_search = LabelFrame(self.search_staff_window, text="Search")
        self.staff_table_search.place(relx=0.02, rely=0.01, relwidth=0.75, relheight=0.19)

        self.staff_search_lbl = Label(self.staff_table_search, text="Employee Code", font=("Calibri", 12))
        self.staff_search_lbl.place(relx=0.01, rely=0.52)

        self.staff_search_txt = ttk.Entry(self.staff_table_search, font=("Calibri", 12))
        self.staff_search_txt.place(relx=0.42, rely=0.52, relwidth=0.55)

        self.staff_search_btn = ttk.Button(self.search_staff_window, text="Search", style="C.TButton",
                                           command=self.search_staff_btn)
        self.staff_search_btn.place(relx=0.80, rely=0.095)

        self.staff_delete_btn = ttk.Button(self.search_staff_window, text="Delete", style="C.TButton",
                                           command=self.delete_staff_btn)
        self.staff_delete_btn.place(relx=0.90, rely=0.095)

        self.staff_table_frame = LabelFrame(self.search_staff_window, text="Existing Employee(s)")
        self.staff_table_frame.place(relx=0, rely=0.2, relwidth=1, relheight=0.7)

        if self.rows != []:
            self.staff_table = ttk.Treeview(self.staff_table_frame, style="T.Treeview",
                                            columns=(
                                                "Employee ID", "Name", "Address",
                                                "State", "Contact", "Designation",
                                                "Status"), height=len(self.rows))
            self.vsb = Scrollbar(self.staff_table,
                                 orient="vertical",
                                 command=self.staff_table.yview
                                 )

            self.staff_table['yscrollcommand'] = self.vsb.set
            self.staff_table.heading("Employee ID", text="Employee ID")
            self.staff_table.heading("Name", text="Name")
            self.staff_table.heading("Address", text="Address")
            self.staff_table.heading("State", text="State")
            self.staff_table.heading("Contact", text="Contact")
            self.staff_table.heading("Designation", text="Designation")
            self.staff_table.heading("Status", text="Status")
            self.staff_table["displaycolumns"] = ("Employee ID", "Name", "Address",
                                                  "Contact", "Designation", "Status")
            self.staff_table["show"] = "headings"
            self.staff_table.column("Employee ID", width=150, anchor='center')
            self.staff_table.column("Name", width=150, anchor='center')
            self.staff_table.column("Address", width=150, anchor='center')
            self.staff_table.column("Contact", width=150, anchor='center')
            self.staff_table.column("Designation", width=150, anchor='center')
            self.staff_table.column("Status", width=150, anchor='center')

            self.staff_table.tag_configure('oddrow', background="white")
            self.staff_table.tag_configure('evenrow', background="#c5dbbf")

            self.count = 0
            for id, Full_Name, DOB, Gender, EMAIL, Contact, Employee_Code, Address, Join_date, Designation, \
                Contact_Person, Contact_Person_Number, Blood_Group, Document_Type, Document_No, Expiry_Date, \
                Issue_Date, Communication_SMS, Communication_Email, Sales_Commission, Remarks in self.rows:
                if self.count % 2 == 0:
                    self.staff_table.insert('', END,
                                            values=(Employee_Code, Full_Name, Address, Contact, Contact, Designation),
                                            tags=('evenrow',))
                    self.count += 1
                else:
                    self.staff_table.insert('', END,
                                            values=(Employee_Code, Full_Name, Address, Contact, Contact, Designation),
                                            tags=('oddrow',))
                    self.count += 1

            self.vsb.pack(side=RIGHT, fill=Y)
            self.vsb.configure(command=self.staff_table.yview)
            self.staff_table.pack(fill=BOTH, expand=1)
        else:
            self.img = PhotoImage(file="Images\\Search not found.png")
            self.img1 = Label(self.staff_table_frame, image=self.img)
            self.img1.place(relx=0.5, rely=0.5, anchor=CENTER)

        """self.staff_search_notebook = ttk.Notebook(self.search_staff_window)
        self.other = Frame(self.staff_search_notebook, bd=3)
        self.staff_profile_notebook.add(self.other, text="Other")
        self.staff_search_notebook.place(relx=0.83, rely=0.2, relwidth=0.15, relheight=0.7)"""

    def delete_client_btn(self):
        if self.client_search_txt.get() == "":
            tmsg.showerror("Error", "Please Enter Client Name")
        else:
            self.conn = sqlite3.connect('DB\\Clients.db')
            self.cursor = self.conn.cursor()

            sqlite_update_query = """DELETE FROM CLIENT where Full_Name = ?"""

            self.cursor.execute(sqlite_update_query, (self.client_search_txt.get(),))

            self.client_table.delete(*self.client_table.get_children())

            self.cursor.execute("SELECT * FROM CLIENT")
            self.rows = self.cursor.fetchall()
            self.count = 0
            for No, Full_Name, DOB, Gender, EMAIL, Contact, City, State, Address, GSTIN, PAN, Contact_Person, Contact_Person_Number, Blood_Group, Document_Type, Document_No, Expiry_Date, Issue_Date, Communication_SMS, Communication_Email, Sales_Commission, Remarks in self.rows:
                if self.count % 2 == 0:
                    self.client_table.insert('', END,
                                             values=(No, Full_Name, Address, City, State, Contact, GSTIN),
                                             tags=('evenrow',))
                    print(Contact)
                    self.count += 1
                else:
                    self.client_table.insert('', END,
                                             values=(No, Full_Name, Address, City, State, Contact, GSTIN),
                                             tags=('oddrow',))
                    print(Contact)
                    self.count += 1
            self.conn.commit()
            self.conn.close()

    def search_client_btn(self):
        if self.client_search_txt.get() == "":
            tmsg.showerror("Error", "Please Enter Client Name")
        else:
            self.conn = sqlite3.connect('DB\\Clients.db')
            self.cursor = self.conn.cursor()

            sqlite_update_query = """SELECT * from CLIENT where Full_Name = ?"""

            self.cursor.execute(sqlite_update_query, (self.client_search_txt.get(),))

            self.rows = self.cursor.fetchone()

            self.client_table.delete(*self.client_table.get_children())
            self.client_table.insert('', END,
                                     values=(self.rows[0],
                                             self.rows[1],
                                             self.rows[8],
                                             self.rows[6],
                                             self.rows[7],
                                             self.rows[5],
                                             self.rows[5],
                                             self.rows[9]),
                                     tags=('oddrow',))
            self.conn.commit()
            self.conn.close()

    def manage_client_btn(self):
        self.conn = sqlite3.connect('DB\\Clients.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM CLIENT")
        self.rows = self.cursor.fetchall()

        self.search_client_window = Toplevel()
        self.search_client_window.title("Search Client")
        self.search_client_window.geometry("1152x672+25+12")
        self.search_client_window.attributes('-toolwindow', 1)
        self.search_client_window.attributes('-topmost', 'true')
        self.search_client_window.focus_force()

        self.client_table_search = LabelFrame(self.search_client_window, text="Search")
        self.client_table_search.place(relx=0.02, rely=0.01, relwidth=0.75, relheight=0.19)

        self.client_search_lbl = Label(self.client_table_search, text="Client Name", font=("Calibri", 12))
        self.client_search_lbl.place(relx=0.01, rely=0.52)

        self.client_search_txt = ttk.Entry(self.client_table_search, font=("Calibri", 12))
        self.client_search_txt.place(relx=0.42, rely=0.52, relwidth=0.55)

        self.client_search_btn = ttk.Button(self.search_client_window, text="Search", style="C.TButton",
                                            command=self.search_client_btn)
        self.client_search_btn.place(relx=0.80, rely=0.095)

        self.client_delete_btn = ttk.Button(self.search_client_window, text="Delete", style="C.TButton",
                                            command=self.delete_client_btn)
        self.client_delete_btn.place(relx=0.90, rely=0.095)

        self.client_table_frame = LabelFrame(self.search_client_window, text="Existing Client(s)")
        self.client_table_frame.place(relx=0, rely=0.2, relwidth=1, relheight=0.7)

        if self.rows != []:
            self.client_table = ttk.Treeview(self.client_table_frame, style="T.Treeview",
                                             columns=(
                                                 "No.", "Name", "Address",
                                                 "City", "State", "Contact",
                                                 "GSTIN"), height=len(self.rows))
            self.vsb = Scrollbar(self.client_table,
                                 orient="vertical",
                                 command=self.client_table.yview
                                 )
            self.client_table['yscrollcommand'] = self.vsb.set
            self.client_table.heading("No.", text="No.")
            self.client_table.heading("Name", text="Name")
            self.client_table.heading("Address", text="Address")
            self.client_table.heading("City", text="City")
            self.client_table.heading("State", text="State")
            self.client_table.heading("Contact", text="Contact")
            self.client_table.heading("GSTIN", text="GSTIN")
            self.client_table["displaycolumns"] = ("No.", "Name", "Address",
                                                   "City", "State", "Contact", "GSTIN")
            self.client_table["show"] = "headings"
            self.client_table.column("No.", width=150, anchor='center')
            self.client_table.column("Name", width=150, anchor='center')
            self.client_table.column("Address", width=150, anchor='center')
            self.client_table.column("City", width=150, anchor='center')
            self.client_table.column("State", width=150, anchor='center')
            self.client_table.column("Contact", width=150, anchor='center')
            self.client_table.column("GSTIN", width=150, anchor='center')

            self.client_table.tag_configure('oddrow', background="white")
            self.client_table.tag_configure('evenrow', background="#c5dbbf")

            self.count = 0
            print(self.rows)
            for row in self.rows:
                if self.count % 2 == 0:
                    self.client_table.insert('', END,
                                             values=(row[0], row[1], row[8], row[6], row[7], row[5], row[9]),
                                             tags=('evenrow',))
                    self.count += 1
                else:
                    self.client_table.insert('', END,
                                             values=(row[0], row[1], row[8], row[6], row[7], row[5], row[9]),
                                             tags=('oddrow',))
                    self.count += 1
            self.vsb.pack(side=RIGHT, fill=Y)
            self.vsb.configure(command=self.client_table.yview)
            self.client_table.pack(fill=BOTH, expand=1)
        else:
            self.img = PhotoImage(file="Images\\Search not found.png")
            self.img1 = Label(self.client_table_frame, image=self.img)
            self.img1.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.conn.commit()
        self.conn.close()

    def manage_invoices(self):
        pass


root = Tk()
obj = Home(root)
root.mainloop()
