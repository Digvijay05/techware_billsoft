import os
import shutil
import sqlite3
import time

from progress.bar import IncrementalBar

print("started")

with IncrementalBar('Processing', max=7) as bar:
    print(bar.start())
    print(bar.progress * 100)
    # ======================Designation Resetter-Start===============================
    conn = sqlite3.connect("DB\\Business.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE DESIGNATION")
    sql = """CREATE TABLE IF NOT EXISTS DESIGNATION(
                                   id  INTEGER PRIMARY KEY autoincrement,
                                   designation VARCHAR(500) NOT NULL)"""
    cursor.execute(sql)
    # ======================Designation Resetter End==================================
    print(bar.next())
    # ======================Designation Inserter Start================================
    sql1 = """INSERT INTO DESIGNATION(designation) VALUES(?)"""
    cursor.execute(sql1, ("Store Manager",))
    cursor.execute(sql1, ("Store Executive",))
    cursor.execute(sql1, ("Logistics Executive",))
    conn.commit()
    conn.close()
    # ======================Designation Inserter End==================================
    bar.next()
    print(bar.progress * 100)
    # ======================Staff Resetter Start======================================
    conn = sqlite3.connect("DB\\Employee.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE STAFF")
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
    cursor.execute(sql)
    conn.commit()
    conn.close()
    # ======================Staff Resetter End========================================
    bar.next()
    print(bar.progress * 100)
    # ======================Items Resetter Start======================================
    conn = sqlite3.connect("DB\\Items.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE ITEMS")
    sql = """CREATE TABLE IF NOT EXISTS ITEMS(
                                       id  INTEGER PRIMARY KEY autoincrement,
                                       Category VARCHAR(50) NOT NULL,
                                       Sub_Category VARCHAR(50) NOT NULL,
                                       Item_Code VARCHAR(500) NOT NULL,
                                       Item_Name VARCHAR(500) NOT NULL,
                                       Item_Rate INTEGER NOT NULL,
                                       Item_Qty INTEGER NOT NULL)"""
    cursor.execute(sql)
    conn.commit()
    conn.close()
    # ======================Items Resetter End==========================================
    print(bar.progress * 100)
    # ======================Category Resetter Start======================================
    conn = sqlite3.connect("DB\\Business.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE Category")
    sql = """CREATE TABLE IF NOT EXISTS CATEGORY(
                                   id  INTEGER PRIMARY KEY autoincrement,
                                   Category VARCHAR(500) NOT NULL)"""
    cursor.execute(sql)
    conn.commit()
    conn.close()
    # ======================Category Resetter End========================================
    bar.next()
    print(bar.progress * 100)
    # ======================Expense Resetter Start=======================================
    conn = sqlite3.connect("DB\\Business.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE EXPENSE")
    sql = """CREATE TABLE IF NOT EXISTS EXPENSE(
                                   id  INTEGER PRIMARY KEY autoincrement,
                                   Expense VARCHAR(500) NOT NULL)"""
    cursor.execute(sql)
    conn.commit()
    conn.close()
    # ======================Expense Resetter End=========================================
    bar.next()
    print(bar.progress * 100)
    # ======================Unit Resetter Start==========================================
    conn = sqlite3.connect("DB\\Business.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE UNIT")
    conn.commit()
    sql = """CREATE TABLE IF NOT EXISTS UNIT(
                                   id  INTEGER PRIMARY KEY autoincrement,
                                   Unit VARCHAR(500) NOT NULL)"""
    cursor.execute(sql)
    conn.commit()
    conn.close()
    # ======================Unit Resetter End============================================
    bar.next()
    # ======================Invoice Resetter Start=======================================
    conn = sqlite3.connect("DB\\Invoices.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS INVOICES")
    sql = """CREATE TABLE IF NOT EXISTS INVOICES(
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
    cursor.execute(sql)
    conn.commit()
    conn.close()
    shutil.rmtree("DB\\INVOICES", ignore_errors=True)
    os.mkdir("DB\\INVOICES")
    bar.next()
    # ======================Invoice Resetter End=========================================

    # ======================ID Resetter Start============================================
    conn = sqlite3.connect("DB\\Business.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE ID")
    sql = """
             CREATE TABLE IF NOT EXISTS ID(
                                    id INTEGER PRIMARY KEY autoincrement,
                                    category VARCHAR(500) NOT NULL,
                                    id VARCHAR(500) NOT NULL)"""
    cursor.execute(sql)
    bar.finish()
    print(bar.progress * 100)
    print("done")
