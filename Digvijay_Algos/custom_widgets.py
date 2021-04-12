import tkinter as tk
from tkinter.ttk import *
from tkinter.constants import *
import sqlite3


class Custom_treeview(Treeview):
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
        self.style.configure("T.Treeview", background="white", foreground="black", fieldbackground="white",
                             )
        self.style.map("T.Treeview",
                       background=[("selected", "#00a62d")])
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

        # Right-Click Menu
        self.treeview_menu = tk.Menu(self.custom_treeview, tearoff=0)
        self.treeview_menu.add_command(label="Edit")
        self.treeview_menu.add_command(label="Delete")

        self.custom_treeview.bind("<ButtonRelease-3>", self.select_item)

    def select_item(self, event):
        """
        It Checks If An Item Is Selected or Not If Selected then it Shows Menu.

        :param event:
        """
        print("Clicked")
        self.cursor_row = self.custom_treeview.focus()
        self.contents = self.custom_treeview.item(self.cursor_row)
        print(self.contents)
        if self.contents == []:
            return
        else:
            try:
                self.treeview_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.treeview_menu.grab_release()

    def place(self, **kwargs):
        self.custom_treeview.place(**kwargs)

    def pack(self, **kwargs):
        self.custom_treeview.pack(**kwargs)

    def grid(self, **kwargs):
        self.custom_treeview.grid(**kwargs)


# root = tk.Tk()
# obj = Custom_treeview(master=root, column_name=["No.", "Name", "Rate", "Quantity",
#                                                 "Discount", "Item Code", "Sub-Category", "Category"], column_width=150)
# root.mainloop()
