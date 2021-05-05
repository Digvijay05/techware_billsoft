import json
import os
import re
import sqlite3
import tkinter as tk
from tkinter.constants import *
import tkinter.messagebox as tmsg
import win32com.client
from win32com.universal import com_error

from Digvijay_Algos.custom_widgets import ManageWindow

# conn = sqlite3.connect("DB\\Invoices.db")
# cursor = conn.cursor()
# cursor.execute("SELECT * FROM INVOICES")
# rows = cursor.fetchall()
# print(rows)
#
# conn = sqlite3.connect("DB\\Business.db")
# cursor = conn.cursor()
# cursor.execute("SELECT * FROM ID")
# rows = cursor.fetchall()
# print(rows)
# invoice = rows[0][1]
# new_invoice = re.findall(r"[^\W\d_]+|\d+", invoice)
# print(new_invoice)
# invoice_n = int(new_invoice[1])
# invoice_n += 1
# print(invoice_n)
# invoice_number = str(new_invoice[0] + str(invoice_n))
# print(invoice_number)
# # invoice_n = re.findall(r"[^\W\d_]+|\d+", .invoice_no)
# sql_string = '''UPDATE ID
#                 SET Id = ?
#                 WHERE Category = ?'''
# cursor.execute(sql_string, ("WF1001", "Invoice"))
# cursor.execute("SELECT * FROM ID")
# rows = cursor.fetchall()
# print(rows)
# conn.commit()
# conn.close()
#
# conn = sqlite3.connect("DB\\Invoices.db")
# cursor = conn.cursor()
# cursor.execute("DROP TABLE INVOICES")
# # Preparing Table For Invoices
# query = """CREATE TABLE IF NOT EXISTS INVOICES(
#             id  INTEGER PRIMARY KEY autoincrement,
#             Invoice_Type VARCHAR(500) NOT NULL,
#             Invoice_No VARCHAR(500) NOT NULL,
#             Invoice_Date DATE NOT NULL,
#             POS VARCHAR(500) NOT NULL,
#             Bill_To VARCHAR(500) NOT NULL,
#             Client_Contact INT(10) NOT NULL,
#             Client_Name VARCHAR(500) NOT NULL,
#             Client_Address VARCHAR(5000) NOT NULL,
#             Client_GST VARCHAR(500) NOT NULL,
#             Sold_By VARCHAR(500) NOT NULL,
#             Discount INTEGER NOT NULL,
#             Shipping INTEGER NOT NULL,
#             SubTotal INTEGER NOT NULL,
#             Total INTEGER NOT NULL,
#             Payment_Date DATE NOT NULL,
#             Payment_Mode VARCHAR(500) NOT NULL,
#             Payment_No VARCHAR(500) NOT NULL,
#             Payment_Amount VARCHAR(500) NOT NULL,
#             Client_Balance INTEGER NOT NULL,
#             Remarks VARCHAR(5000) NOT NULL,
#             Delivery_Terms VARCHAR(5000) NOT NULL)
#             """
# cursor.execute(query)
# cursor.execute("SELECT * FROM INVOICES")
# rows = cursor.fetchall()
# print(rows)
# conn.commit()
# conn.close()
from techware_invoice import Invoice

def edit_invoice():
    # Connecting To Database
    conn = sqlite3.connect("DB\\Business.db")
    cursor = conn.cursor()

    # Executing Commands In Cursor
    cursor.execute("SELECT * FROM CATEGORY")

    # Rows of Data
    rows = cursor.fetchall()

    # Initializing Items List
    items = {}

    # Through For Loop
    for id, category in rows:
        # Appending To Items List
        items[category] = {}

    # Initializing Categories List
    categories = {}

    # Through For Loop
    for id, category in rows:
        # Appending To Categories List
        categories[category] = {}
    cursor_row = obj.manage_treeview.custom_treeview.focus()
    contents = obj.manage_treeview.custom_treeview.item(cursor_row)['values']
    # Getting Details From Database
    conn = sqlite3.connect("DB\\Invoices.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM INVOICES where Invoice_No = ?", (contents[5],))
    rows = cursor.fetchone()
    print(rows)
    invoice_window = tk.Toplevel()
    invoice = Invoice(invoice_window)
    invoice.bill_to_var.set(rows[5])
    invoice.update_client()
    invoice.invoice_type_txt.set(rows[1])
    invoice.invoice_no_var.set(rows[2])
    invoice.invoice_date_txt.set_date(rows[3])
    invoice.invoice_place_of_supply_txt.set(rows[4])
    invoice.contact_no_var.set(rows[6])
    invoice.client_name_var.set(rows[7])
    if invoice.client_name_txt.get() != "CASH":
        invoice.client_name_txt.set(rows[7])
    invoice.contact_address_var.set(rows[8])
    invoice.client_gstin_var.set(rows[9])
    invoice.sold_by_txt.set(rows[10])

    with open(f"Details\\{rows[7]}{rows[2]}.json", "r") as outfile:
        items = json.load(outfile)
    number = 1
    for i in categories:
        for j in items[i].keys():
            lis = items[i][j]
            names1 = lis[0]
            category = lis[6]
            sub_category = lis[5]
            rates1 = lis[1]
            units1 = lis[11]
            quantitys1 = lis[2]
            amounts1 = lis[10]
            discounts1 = lis[7]
            taxes1 = lis[8]
            cess1 = lis[9]
            invoice.particulars_treeview.custom_treeview.insert("", END, values=[number, names1, units1, rates1,
                                                                                 quantitys1, discounts1, taxes1, cess1,
                                                                                 amounts1, sub_category, category])
            number += 1

    invoice.discountPrice.set(rows[11])
    invoice.shippingCharges.set(rows[12])
    invoice.subTotalPrice.set(rows[13])
    invoice.totalPrice.set(rows[14])

    invoice.payment_date_txt.set_date(rows[15])
    invoice.payment_mode_txt.set(rows[15])
    invoice.txn_id_var.set(rows[16])
    invoice.payment_amount_var.set(rows[17])
    invoice.payment_balance_var.set(rows[18])
    invoice.remarks_txt.insert(INSERT, rows[20])
    invoice.delivery_terms_txt.insert(INSERT, rows[21])
    invoice.items = items
    invoice.save_btn["text"] = "Update"
    invoice.save_print_btn.destroy()
    invoice.update_total_price()

    def update_invoice():
        ans = tmsg.askquestion("Are you Sure?", f"Are you Sure to Save Invoice No. '{invoice.invoice_no_txt.get()}'")
        if ans == "yes":
            if invoice.bill_to_var.get() == "client":
                if invoice.client_name_txt.get() == "" or invoice.client_address_txt.get() == "" or invoice.contact_no_txt.get() \
                        == "" or invoice.invoice_type_txt.get() == "Select" or invoice.invoice_place_of_supply_txt.get() == \
                        "Select" or invoice.invoice_no_txt.get() == "" or invoice.payment_mode_txt.get() == "Select":
                    # sold_by_txt.get() == "Select" or \
                    tmsg.showerror("Error", "Please Fill All Required Fields!")
                else:
                    print("all checks passed in client")
                    conn = sqlite3.connect("DB\\Invoices.db")
                    cursor = conn.cursor()

                    cwd = os.getcwd()

                    file_path = f"{cwd}\\DB\\INVOICES"

                    if not os.path.exists(file_path):
                        os.makedirs(file_path)

                    # conn.execute("DROP TABLE INVOICES")

                    # Preparing Table For Invoices
                    query = """CREATE TABLE IF NOT EXISTS INVOICES(
                                                                id  INTEGER PRIMARY KEY autoincrement,
                                                                Invoice_Type VARCHAR(500) NOT NULL,
                                                                Invoice_No VARCHAR(500) NOT NULL,
                                                                Invoice_Date DATE NOT NULL,
                                                                POS VARCHAR(500) NOT NULL,
                                                                Bill_To VARCHAR(500) NOT NULL,
                                                                Client_Contact INT(10) NOT NULL,
                                                                Client_Name VARCHAR(500) NOT NULL,
                                                                Client_Address VARCHAR(5000) NOT NULL,
                                                                Client_GST VARCHAR(500) NOT NULL,
                                                                Sold_By VARCHAR(500) NOT NULL,
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
                    update_bill_query = """UPDATE INVOICES 
                    SET
                        Invoice_Type = ?, Invoice_No = ?, Invoice_Date = ?,
                        POS = ?, Bill_To = ?, Client_Contact = ?,
                        Client_Name = ?, Client_Address = ?, Client_GST = ?,
                        Sold_By = ?, Discount = ?, Shipping = ?,
                        SubTotal = ?, Total = ?, Payment_Date = ?,
                        Payment_Mode = ?, Payment_No = ?, Payment_Amount = ?,
                        Client_Balance = ?, Remarks = ?, Delivery_Terms = ?
                    WHERE Invoice_No = ?
                                      """
                    update_bill_values = (invoice.invoice_type_txt.get(), invoice.invoice_no_txt.get(),
                                        invoice.invoice_date_txt.get(), invoice.invoice_place_of_supply_txt.get(),
                                        invoice.bill_to_var.get(), invoice.contact_no_txt.get(),
                                        invoice.client_name_txt.get(),
                                        invoice.client_address_txt.get(), invoice.client_gstin_txt.get(),
                                        invoice.sold_by_txt.get(), invoice.discountPrice.get(),
                                        invoice.shippingCharges.get(), invoice.subTotalPrice.get(),
                                        invoice.totalPrice.get(), invoice.payment_date_txt.get(),
                                        invoice.payment_mode_txt.get(), invoice.txn_id_txt.get(),
                                        invoice.payment_amount_txt.get(), invoice.payment_balance_txt.get(),
                                        invoice.remarks_txt.get("1.0", END), invoice.delivery_terms_txt.get("1.0", END),
                                        invoice.invoice_no_txt.get(),
                                        )
                    cursor.execute(query)
                    cursor.execute(update_bill_query, update_bill_values)
                    cursor.execute("SELECT * FROM INVOICES WHERE Invoice_No = ?", (invoice.invoice_no_txt.get(),))
                    print("done")
                    rows = cursor.fetchall()
                    print(rows)
                    conn.commit()
                    conn.close()
                    save_items = json.dumps(items, indent=len(items))
                    with open(f"Details\\{invoice.client_name_txt.get()}{invoice.invoice_no_txt.get()}.json", "w") as outfile:
                        outfile.write(save_items)
            elif invoice.bill_to_var.get() == "cash":
                if invoice.client_name_txt.get() == "" or invoice.invoice_type_txt.get() == "Select" or \
                            invoice.invoice_place_of_supply_txt.get() == \
                            "Select" or invoice.invoice_no_txt.get() == "" or \
                            invoice.payment_mode_txt.get() == "Select":
                                tmsg.showerror("Error", "Please Fill All Required Fields!")
                else:
                        print("all checks passed in cash")
                        conn = sqlite3.connect("DB\\Invoices.db")
                        cursor = conn.cursor()

                        cwd = os.getcwd()

                        file_path = f"{cwd}\\DB\\INVOICES"

                        if not os.path.exists(file_path):
                            os.makedirs(file_path)

                        # conn.execute("DROP TABLE INVOICES")

                        # Preparing Table For Invoices
                        query = """CREATE TABLE IF NOT EXISTS INVOICES(
                                                                                        id  INTEGER PRIMARY KEY autoincrement,
                                                                                        Invoice_Type VARCHAR(500) NOT NULL,
                                                                                        Invoice_No VARCHAR(500) NOT NULL,
                                                                                        Invoice_Date DATE NOT NULL,
                                                                                        POS VARCHAR(500) NOT NULL,
                                                                                        Bill_To VARCHAR(500) NOT NULL,
                                                                                        Client_Contact INT(10) NOT NULL,
                                                                                        Client_Name VARCHAR(500) NOT NULL,
                                                                                        Client_Address VARCHAR(5000) NOT NULL,
                                                                                        Client_GST VARCHAR(500) NOT NULL,
                                                                                        Sold_By VARCHAR(500) NOT NULL,
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
                        update_bill_query = """UPDATE INVOICES 
                                            SET
                                                Invoice_Type = ?, Invoice_No = ?, Invoice_Date = ?,
                                                POS = ?, Bill_To = ?, Client_Contact = ?,
                                                Client_Name = ?, Client_Address = ?, Client_GST = ?,
                                                Sold_By = ?, Discount = ?, Shipping = ?,
                                                SubTotal = ?, Total = ?, Payment_Date = ?,
                                                Payment_Mode = ?, Payment_No = ?, Payment_Amount = ?,
                                                Client_Balance = ?, Remarks = ?, Delivery_Terms = ?
                                            WHERE Invoice_No = ?
                                                              """
                        update_bill_values = (invoice.invoice_type_txt.get(), invoice.invoice_no_txt.get(),
                                              invoice.invoice_date_txt.get(), invoice.invoice_place_of_supply_txt.get(),
                                              invoice.bill_to_var.get(), invoice.contact_no_txt.get(),
                                              invoice.client_name_txt.get(),
                                              invoice.client_address_txt.get(), invoice.client_gstin_txt.get(),
                                              invoice.sold_by_txt.get(), invoice.discountPrice.get(),
                                              invoice.shippingCharges.get(), invoice.subTotalPrice.get(),
                                              invoice.totalPrice.get(), invoice.payment_date_txt.get(),
                                              invoice.payment_mode_txt.get(), invoice.txn_id_txt.get(),
                                              invoice.payment_amount_txt.get(), invoice.payment_balance_txt.get(),
                                              invoice.remarks_txt.get("1.0", END),
                                              invoice.delivery_terms_txt.get("1.0", END),
                                              invoice.invoice_no_txt.get(),
                                              )
                        cursor.execute(query)
                        cursor.execute(update_bill_query, update_bill_values)
                        cursor.execute("SELECT * FROM INVOICES WHERE Invoice_No = ?", (invoice.invoice_no_txt.get(),))
                        print("done")
                        rows = cursor.fetchall()
                        print(rows)
                        conn.commit()
                        conn.close()
                        save_items = json.dumps(items, indent=len(items))
                        with open(f"Details\\{invoice.client_name_txt.get()}{invoice.invoice_no_txt.get()}.json",
                                  "w") as outfile:
                            outfile.write(save_items)
                        invoice.save_excel()
            else:
                invoice.invoice_root.destroy()

    invoice.save_btn["command"] = update_invoice


def print_invoice():
    cursor_row = obj.manage_treeview.custom_treeview.focus()
    contents = obj.manage_treeview.custom_treeview.item(cursor_row)['values']
    # Getting Details From Database
    conn = sqlite3.connect("DB\\Invoices.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM INVOICES where Invoice_No = ?", (contents[5],))
    rows = cursor.fetchone()

    # Printing Excel File
    # Path to original excel file
    WB_PATH = f"{os.getcwd()}\\Bill Records\\{rows[7]}{rows[2]}.xlsx"

    excel = win32com.client.Dispatch("Excel.Application")

    excel.Visible = False
    try:
        # Open
        wb = excel.Workbooks.Open(WB_PATH)

        # Specify the sheet you want to save by index. 1 is the first (leftmost) sheet.
        ws_index_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        wb.WorkSheets(ws_index_list[0]).Select()

        # Print
        wb.ActiveSheet.PrintOut()
        wb.Save()
        wb.Close()
        excel.Quit()
        # Deleting All Files
        os.remove(WB_PATH)

    except com_error as e:
        print(f"failed. due to {e}")
        return
    else:
        del wb
        del excel


def delete_invoice():
    cursor_row = obj.manage_treeview.custom_treeview.focus()
    contents = obj.manage_treeview.custom_treeview.item(cursor_row)['values']
    # Getting Details From Database
    conn = sqlite3.connect("DB\\Invoices.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM INVOICES where Invoice_No = ?", (contents[5],))
    conn.commit()
    obj.manage_treeview.custom_treeview.delete(*obj.manage_treeview.custom_treeview.get_children())
    cursor.execute(f"SELECT * FROM INVOICES")
    rows = cursor.fetchall()
    number = 1
    for row in rows:
        total = re.findall(r"[^\W\d_]+|\d+", row[14])
        total_amount = total[1]
        payment = re.findall(r"[^\W\d_]+|\d+", row[18])
        payment_d = payment[0]
        payment_due = int(total_amount) - int(payment_d)
        payment = "Rs. " + str(payment_due) + "/-"
        if number % 2 == 0:
            if payment_due == 0:
                obj.manage_treeview.custom_treeview.insert(parent='', index=END, values=[number, "PAID", payment,
                                                                                         row[15],
                                                                                         row[1], row[2], row[6],
                                                                                         row[7], row[8], row[4],
                                                                                         row[9], row[14], row[3]],
                                                           tags="evenrow",
                                                           )
            else:
                obj.manage_treeview.custom_treeview.insert(parent='', index=END, values=[number, "UNPAID", payment,
                                                                                         row[15],
                                                                                         row[1], row[2], row[6],
                                                                                         row[7], row[8], row[4],
                                                                                         row[9], row[14], row[3]],
                                                           tags="evenrow",
                                                           )
        else:
            if payment_due == 0:
                obj.manage_treeview.custom_treeview.insert(parent='', index=END, values=[number, "PAID", payment,
                                                                                         row[15],
                                                                                         row[1], row[2], row[6],
                                                                                         row[7], row[8], row[4],
                                                                                         row[9], row[14], row[3]],
                                                           tags="oddrow",
                                                           )
            else:
                obj.manage_treeview.custom_treeview.insert(parent='', index=END, values=[number, "UNPAID", payment,
                                                                                         row[15],
                                                                                         row[1], row[2], row[6],
                                                                                         row[7], row[8], row[4],
                                                                                         row[9], row[14], row[3]],
                                                           tags="oddrow",
                                                           )
        number += 1
    conn.commit()
    conn.close()


root = tk.Tk()
# Particulars Treeview Dictionary
invoices_dict = {
    "Sr No.": {
        "name": "Sr No.",
        "width": "60"
    },
    "Status": {
        "name": "Status",
        "width": "80"
    },
    "Payment Due": {
        "name": "Payment Due",
        "width": "100"
    },
    "Last Payment On.": {
        "name": "Last Payment On.",
        "width": "120"
    },
    "Invoice-Type": {
        "name": "Invoice-Type",
        "width": "100"
    },
    "Invoice-No.": {
        "name": "Invoice-No.",
        "width": "100"
    },
    "Contact No.": {
        "name": "Contact No.",
        "width": "150"
    },
    "Client Name": {
        "name": "Client Name",
        "width": "200"
    },
    "Address": {
        "name": "Address",
        "width": "150"
    },
    "State(Pos)": {
        "name": "State(Pos)",
        "width": "80"
    },
    "GSTIN": {
        "name": "GSTIN",
        "width": "100"
    },
    "Total Amount": {
        "name": "Total Amount",
        "width": "100"
    },
    "Created On.": {
        "name": "Created On.",
        "width": "120"
    },
}


def reset_invoice():
    obj.manage_treeview.custom_treeview.delete(*obj.manage_treeview.custom_treeview.get_children())
    conn = sqlite3.connect("DB\\Invoices.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM INVOICES")
    rows = cursor.fetchall()
    number = 1
    for row in rows:
        total = re.findall(r"[^\W\d_]+|\d+", row[14])
        total_amount = total[1]
        payment = re.findall(r"[^\W\d_]+|\d+", row[18])
        payment_d = payment[0]
        payment_due = int(total_amount) - int(payment_d)
        payment = "Rs. " + str(payment_due) + "/-"
        if number % 2 == 0:
            if payment_due == 0:
                obj.manage_treeview.custom_treeview.insert(parent='', index=END, values=[number, "PAID", payment,
                                                                                         row[15],
                                                                                         row[1], row[2], row[6],
                                                                                         row[7], row[8], row[4],
                                                                                         row[9], row[14], row[3]],
                                                           tags="evenrow",
                                                           )
            else:
                obj.manage_treeview.custom_treeview.insert(parent='', index=END, values=[number, "UNPAID", payment,
                                                                                         row[15],
                                                                                         row[1], row[2], row[6],
                                                                                         row[7], row[8], row[4],
                                                                                         row[9], row[14], row[3]],
                                                           tags="evenrow",
                                                           )
        else:
            if payment_due == 0:
                obj.manage_treeview.custom_treeview.insert(parent='', index=END, values=[number, "PAID", payment,
                                                                                         row[15],
                                                                                         row[1], row[2], row[6],
                                                                                         row[7], row[8], row[4],
                                                                                         row[9], row[14], row[3]],
                                                           tags="oddrow",
                                                           )
            else:
                obj.manage_treeview.custom_treeview.insert(parent='', index=END, values=[number, "UNPAID", payment,
                                                                                         row[15],
                                                                                         row[1], row[2], row[6],
                                                                                         row[7], row[8], row[4],
                                                                                         row[9], row[14], row[3]],
                                                           tags="oddrow",
                                                           )
        number += 1
    conn.commit()
    conn.close()


def search_invoice():
    obj.manage_treeview.custom_treeview.delete(*obj.manage_treeview.custom_treeview.get_children())
    conn = sqlite3.connect("DB\\Invoices.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM INVOICES WHERE Invoice_No = ?", (obj.client_search_txt.get(),))
    rows = cursor.fetchall()
    number = 1
    for row in rows:
        total = re.findall(r"[^\W\d_]+|\d+", row[14])
        total_amount = total[1]
        payment = re.findall(r"[^\W\d_]+|\d+", row[18])
        payment_d = payment[0]
        payment_due = int(total_amount) - int(payment_d)
        payment = "Rs. " + str(payment_due) + "/-"
        if number % 2 == 0:
            if payment_due == 0:
                obj.manage_treeview.custom_treeview.insert(parent='', index=END, values=[number, "PAID", payment,
                                                                                         row[15],
                                                                                         row[1], row[2], row[6],
                                                                                         row[7], row[8], row[4],
                                                                                         row[9], row[14], row[3]],
                                                           tags="evenrow",
                                                           )
            else:
                obj.manage_treeview.custom_treeview.insert(parent='', index=END, values=[number, "UNPAID", payment,
                                                                                         row[15],
                                                                                         row[1], row[2], row[6],
                                                                                         row[7], row[8], row[4],
                                                                                         row[9], row[14], row[3]],
                                                           tags="evenrow",
                                                           )
        else:
            if payment_due == 0:
                obj.manage_treeview.custom_treeview.insert(parent='', index=END, values=[number, "PAID", payment,
                                                                                         row[15],
                                                                                         row[1], row[2], row[6],
                                                                                         row[7], row[8], row[4],
                                                                                         row[9], row[14], row[3]],
                                                           tags="oddrow",
                                                           )
            else:
                obj.manage_treeview.custom_treeview.insert(parent='', index=END, values=[number, "UNPAID", payment,
                                                                                         row[15],
                                                                                         row[1], row[2], row[6],
                                                                                         row[7], row[8], row[4],
                                                                                         row[9], row[14], row[3]],
                                                           tags="oddrow",
                                                           )
        number += 1
    conn.commit()
    conn.close()


obj = ManageWindow(root, search_frame="Invoices", search_name="Invoice No.", search_function=search_invoice,
                   reset_function=reset_invoice,
                   command_options=[edit_invoice, print_invoice, delete_invoice],
                   database=f"{os.getcwd()}\\DB\\Invoices.db",
                   table_name="INVOICES",
                   command_labels=["Edit", "Print", "Delete"], columns=invoices_dict,
                   )
reset_invoice()
root.mainloop()
