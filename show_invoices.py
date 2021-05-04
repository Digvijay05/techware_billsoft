import sqlite3, re

conn = sqlite3.connect("DB\\Invoices.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM INVOICES")
rows = cursor.fetchall()
# print(rows)

conn = sqlite3.connect("DB\\Business.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM ID")
rows = cursor.fetchall()
print(rows)
invoice = rows[0][1]
new_invoice = re.findall(r"[^\W\d_]+|\d+", invoice)
print(new_invoice)
invoice_n = int(new_invoice[1])
invoice_n += 1
print(invoice_n)
invoice_number = str(new_invoice[0] + str(invoice_n))
print(invoice_number)
# self.invoice_n = re.findall(r"[^\W\d_]+|\d+", self.invoice_no)
sql_string = '''UPDATE ID
                SET Id = ?
                WHERE Category = ?'''
cursor.execute(sql_string, ("WF1001", "Invoice"))
cursor.execute("SELECT * FROM ID")
rows = cursor.fetchall()
print(rows)
conn.commit()
conn.close()

conn = sqlite3.connect("DB\\Invoices.db")
cursor = conn.cursor()
cursor.execute("DROP TABLE INVOICES")
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
cursor.execute(query)
cursor.execute("SELECT * FROM INVOICES")
rows = cursor.fetchall()
print(rows)
conn.commit()
conn.close()
