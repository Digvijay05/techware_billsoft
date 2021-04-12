import sqlite3
import time

import wand
from win10toast import ToastNotifier

'''toaster = ToastNotifier()
toaster.show_toast("Hello World!!!",
                   "Python is 10 seconds awsm!",
                   icon_path=None,
                   duration=10)

toaster.show_toast("Example two",
                   "This notification is in it's own thread!",
                   icon_path=None,
                   duration=5,
                   threaded=True)
# Wait for threaded notification to finish
while toaster.notification_active(): time.sleep(0.1)
'''
if __name__ == '__main__':
    # conn = sqlite3.connect("DB\\Items.db")
    # cursor = conn.cursor()
    # cursor.execute("DROP TABLE ITEMS")
    # sql = """CREATE TABLE IF NOT EXISTS ITEMS(
    #                                    id  INTEGER PRIMARY KEY autoincrement,
    #                                    Category VARCHAR(50) NOT NULL,
    #                                    Sub_Category VARCHAR(50) NOT NULL,
    #                                    Item_Code VARCHAR(500) NOT NULL,
    #                                    Item_Name VARCHAR(500) NOT NULL,
    #                                    Item_Rate INTEGER NOT NULL,
    #                                    Item_Qty INTEGER NOT NULL)"""
    # cursor.execute(sql)
    # values1 = [('EXAMPLE', '', 'a', 'a', '500', '5'),
    #           ('EXAMPLE', '', 'b', 'b', '515', '7'),
    #           ('EXAMPLE', '', 'c', 'c', '800', '6'),
    #           ('EXAMPLE', '', 'd', 'd', '545', '17'),
    #           ('EXAMPLE', '', 'e', 'e', '657', '21'),
    #           ('EXAMPLE', '', 'f', 'f', '491', '56'),
    #           ('EXAMPLE', '', 'g', 'g', '561', '87'),
    #           ('EXAMPLE', '', 'g', 'name', '345', '78')]
    # cursor.executemany("""INSERT INTO ITEMS(Category, Sub_Category, Item_Code,
    #      Item_Name, Item_Rate, Item_Qty) VALUES(?,?,?,?,?,?)""", values1)
    # conn.commit()
    # cursor.execute("SELECT * FROM ITEMS")
    # rows = cursor.fetchall()
    # print(rows)
    # conn.close()

    values = [(
        "Digvijay", "", "a", "a", "6351753750", "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "", "a", "a", "'00",
        "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "500"),
        (
            "Ankush", "", "a", "a", "6351753750", "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "", "a", "a", "'00",
            "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "500"),
        (
            "Abhinav", "", "a", "a", "6351753750", "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "", "a", "a", "'00",
            "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "500"),
        (
            "Cyan", "", "a", "a", "6351753750", "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "", "a", "a", "'00",
            "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "500"),
        (
            "Lime", "", "a", "a", "6351753750", "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "", "a", "a", "'00",
            "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "500"),
        (
            "Dhruvil", "", "a", "a", "6351753750", "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "", "a", "a", "'00",
            "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "500"),
        (
            "Raj", "", "a", "a", "6351753750", "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "", "a", "a", "'00",
            "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "500"),
        (
            "Irfan", "", "a", "a", "6351753750", "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "", "a", "a", "'00",
            "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "500"),
        (
            "Dhairya", "", "a", "a", "6351753750", "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "", "a", "a", "'00",
            "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "500"),
        (
            "Het", "", "a", "a", "6351753750", "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "", "a", "a", "'00",
            "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "500"),
        (
            "Happy", "", "a", "a", "6351753750", "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "", "a", "a", "'00",
            "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "500"),
        (
            "HappuSingh", "", "a", "a", "6351753750", "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "", "a", "a", "'00",
            "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "500"),
        (
            "VibhutiNarayan", "", "a", "a", "6351753750", "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "", "a", "a",
            "'00",
            "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "500"),
        (
            "Oggy", "", "a", "a", "6351753750", "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "", "a", "a", "'00",
            "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "500"),
        (
            "Tom", "", "a", "a", "6351753750", "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "", "a", "a", "'00",
            "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "500"),
        (
            "Jerry", "", "a", "a", "6351753750", "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "", "a", "a", "'00",
            "EXAMPLE", "", "a", "a", "500", "EXAMPLE", "500")
    ]

    conn = sqlite3.connect("DB\\Clients.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE CLIENT")

    sql = """CREATE TABLE IF NOT EXISTS CLIENT(
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
                                   Remarks VARCHAR(500) NOT NULL,
                                   Balance VARCHAR(50) NOT NULL)"""

    cursor.execute(sql)

    print(len(values))

    cursor.executemany(
        """insert into CLIENT(Full_Name,DOB,Gender,EMAIL,Contact,City,State,Address,GSTIN,PAN,Contact_Person,
        Contact_Person_Number,Blood_Group,Document_Type,Document_No,Expiry_Date,Issue_Date,Communication_SMS,
        Communication_Email,Sales_Commission,Remarks, Balance) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        values
    )

    conn.commit()
    conn.close()

    conn = sqlite3.connect("DB\\Business.db")
    cursor = conn.cursor()

    sql = """CREATE TABLE IF NOT EXISTS ID(
             no  INTEGER PRIMARY KEY autoincrement,
             Id VARCHAR(50) NOT NULL,
             Category VARCHAR(500) NOT NULL)"""

    conn.execute(sql)

    conn.commit()
    conn.close()
    #
    #
    #
    # # Python program to generate QR code
    # from qrtools import QR
    #
    # # creates the QR object
    # my_QR = QR(data=u"Example")
    #
    # # encodes to a QR code
    # my_QR.encode()
    # print(my_QR.filename)
    #
    # # import win32com.client
    # # from pywintypes import com_error
    # # from wand.image import Image
    # # from wand import exceptions
    # #
    # # # Path to original excel file
    # # WB_PATH = r'C:\Users\Digvijay\Desktop\Ranjan JadavWF1001.xlsx'
    # # # PDF path when saving
    # # PATH_TO_PDF = r'C:\Users\Digvijay\Desktop\YearCalendar.pdf'
    # #
    # # excel = win32com.client.Dispatch("Excel.Application")
    # #
    # # excel.Visible = False
    # #
    # # try:
    # #     print('Start conversion to PDF')
    # #
    # #     # Open
    # #     wb = excel.Workbooks.Open(WB_PATH)
    # #
    # #     # Specify the sheet you want to save by index. 1 is the first (leftmost) sheet.
    # #     ws_index_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # #     wb.WorkSheets(ws_index_list[0]).Select()
    # #
    # #     # Save
    # #     wb.ActiveSheet.ExportAsFixedFormat(0, PATH_TO_PDF)
    # # except com_error as e:
    # #     print('failed.')
    # # else:
    # #     print('Succeeded.')
    # # finally:
    # #     wb.Close()
    # #     excel.Quit()
    # #
    # # f = r'C:\Users\Digvijay\Desktop\sample.pdf.pdf'
    # # try:
    # #     with(Image(filename=f, resolution=120)) as source:
    # #         for i, image in enumerate(source.sequence):
    # #             newfilename = f[:-4] + str(i + 1) + '.png'
    # #             Image(image).save(filename=newfilename)
    # # except wand.exceptions.DelegateError as e:
    # #     print(e)
    #
    # from tkinter import *
    # from tkinter.tix import *
    #
    # root = Tk()
    #
    # MyButtn = Button(root, text="Hello")
    # MyButtn.grid()
    #
    # ToolTp = Balloon()
    # ToolTp.bind_widget(MyButtn, balloonmsg="My ToolTip example")

    # root.mainloop()
