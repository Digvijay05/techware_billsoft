import tkinter as tk
from tkinter.ttk import *
from tkinter.constants import *
import sqlite3


class Custom_treeview:
    """
    This ttk Treeview is made custom for Any Software
    """

    def __init__(self, *args, **kwargs):

        self.treeview_root = kwargs["master"]

        self.style = Style(self.treeview_root)
        # Loading TTK Themes
        self.treeview_root.tk.eval("""
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
        self.treeview_root.tk.call("package", "require", 'awthemes')
        self.treeview_root.tk.call("package", "require", 'awlight')
        # self.root.tk.call("package", "require", 'awbreeze')

        # Using Theme AWLIGHT
        self.style.theme_use('awlight')

        # Treeview Style
        self.style.configure("T.Treeview",background="white", foreground="black", fieldbackground="white",
                             )
        self.style.map("T.Treeview",
                       background=[("selected","#00a62d")])
        # Treeview Heading Style
        self.style.map("T.Treeview.Heading",
                       background=[("active", "#00b856",), ("!active", "#26e881",), ("pressed", "#7e8c7a",), ],
                       fieldbackground=[("active", "#9eb099",), ("!active", "white",), ("pressed", "#7e8c7a",), ],
                       foreground=[("active", "#1c1b1b",), ("!active", "white",), ("pressed", "#000000",), ], )
        # rowheight=[35], font=("Calibri", 15))

        self.custom_treeview = Treeview(self.treeview_root, style="T.Treeview",
                                        columns=kwargs["column_name"], )
        # Vertical Scrollbar
        self.vsb = Scrollbar(self.custom_treeview,
                             orient="vertical",
                             command=self.custom_treeview.yview
                             )
        # Scroll Command For Particulars Treeview
        self.custom_treeview['yscrollcommand'] = self.vsb.set
        # Treeview Headings
        for column in kwargs["column_name"]:
            self.custom_treeview.heading(column, text=column)
        self.custom_treeview["displaycolumns"] = (kwargs["column_name"])
        self.custom_treeview["show"] = "headings"
        # Treeview Columns
        for column in kwargs["column_name"]:
            self.custom_treeview.column(column, width=kwargs["column_width"], anchor='center')

        # Tags for Treeview
        self.custom_treeview.tag_configure('oddrow', background="white")
        self.custom_treeview.tag_configure('evenrow', background="#c5dbbf")

        # Packing Vertical Scrollbar
        self.vsb.pack(side=RIGHT, fill=Y)

        # Configuring Vertical Scrollbar
        self.vsb.configure(command=self.custom_treeview.yview)

        # Packing Particulars Treeview
        self.custom_treeview.pack(fill=BOTH, expand=1)

        self.conn = sqlite3.connect("C:\\Users\\Digvijay\\Desktop\\Techware Billing System\\DB\\Items.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM ITEMS")
        self.rows = self.cursor.fetchall()
        for row in self.rows:
            # Getting The Last Row Of Particulars Treeview
            last_row = len(self.custom_treeview.get_children()) + 1
            print(last_row)
            # Creating Table In Database
            sql = '''CREATE TABLE IF NOT EXISTS ITEMS(
                      0 id  INTEGER PRIMARY KEY,
                      1 Category VARCHAR(50) NOT NULL,
                      2 Sub_Category VARCHAR(50) NOT NULL,
                      3 Item_Code VARCHAR(500) NOT NULL,
                      4 Item_Name VARCHAR(500) NOT NULL,
                      5 Item_Rate INTEGER NOT NULL,
                      6 Item_Qty INTEGER NOT NULL)'''

            # IF ELSE Statement For Getting Last Row And Inserting It To Particulars Treeview
            if last_row != 0:
                if last_row % 2 == 0:
                    self.custom_treeview.insert('', END,
                                                values=(
                                                    last_row, row[4], row[5], row[6], row[3], row[2], row[1]),
                                                tags=('evenrow',))
                else:
                    self.custom_treeview.insert('', END,
                                                values=(
                                                    last_row, row[4], row[5], row[6], row[3], row[2], row[1]),
                                                tags=('oddrow',))
            else:
                self.custom_treeview.insert('', END,
                                            values=(
                                                1, row[4], row[5], row[6], row[3], row[2], row[1]),
                                            tags=('oddrow',))


root = tk.Tk()
obj = Custom_treeview(master=root, column_name=["No.", "Name", "Rate", "Quantity",
                                                "Discount", "Item Code", "Sub-Category", "Category"], column_width=150)
root.mainloop()
