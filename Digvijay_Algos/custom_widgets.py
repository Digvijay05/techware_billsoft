import tkinter as tk
from tkinter.ttk import *
from tkinter.constants import *
import sqlite3


class Custom_treeview(Treeview):
    """
    This ttk Treeview is made custom for Any Software
    """

    def __init__(self, edit_command=None, delete_command=None, *args, **kwargs):
        self.column_names = []
        for column in kwargs["columns"].keys():
            for items in kwargs["columns"][column].items():
                if items[0] == 'name':
                    self.column_names.append(items[1])
        print(self.column_names)
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
        self.style.configure("T.Treeview", background="white", foreground="black", fieldbackground="#FFFF88",
                             )
        self.style.map("T.Treeview",
                       background=[("selected", "#00a62d")])
        # Treeview Heading Style
        self.style.map("T.Treeview.Heading",
                       background=[("active", "#00b856",), ("!active", "#26e881",), ("pressed", "#7e8c7a",), ],
                       fieldbackground=[("active", "#9eb099",), ("!active", "white",), ("pressed", "#7e8c7a",), ],
                       foreground=[("active", "#1c1b1b",), ("!active", "black",), ("pressed", "#000000",), ], )

        self.custom_treeview = Treeview(self.treeview_root, style="T.Treeview",
                                        columns=self.column_names, )
        # Vertical Scrollbar
        self.vsb = Scrollbar(self.custom_treeview,
                             orient="vertical",
                             command=self.custom_treeview.yview
                             )
        # Scroll Command For Particulars Treeview
        self.custom_treeview['yscrollcommand'] = self.vsb.set

        # Treeview Headings
        for column in kwargs["columns"].keys():
            for items in kwargs["columns"][column].items():
                if items[0] == 'name':
                    print(items[1])
                    self.custom_treeview.heading(items[1],
                                                 text=items[1])
        self.custom_treeview["displaycolumns"] = (self.column_names)
        self.custom_treeview["show"] = "headings"

        self.columns = {}
        for column in kwargs["columns"]:
            self.column_name = column[0]

        # Treeview Columns
        for column in kwargs["columns"].keys():
            for items in kwargs["columns"][column].items():
                if items[0] == 'width':
                    self.custom_treeview.column("", width=items[1], anchor='center')

        # Tags for Treeview
        self.custom_treeview.tag_configure('oddrow', background="white")
        self.custom_treeview.tag_configure('evenrow', background="#c5dbbf")

        # Packing Vertical Scrollbar
        self.vsb.pack(side=RIGHT, fill=Y)

        # Configuring Vertical Scrollbar
        self.vsb.configure(command=self.custom_treeview.yview)

        # Right-Click Menu
        self.treeview_menu = tk.Menu(self.custom_treeview, tearoff=0)
        self.treeview_menu.add_command(label="Edit", command=edit_command)
        self.treeview_menu.add_command(label="Delete", command=delete_command)

        self.custom_treeview.bind("<<TreeviewSelect>>" and "<ButtonRelease-3>", self.select_item)

    def select_item(self, event):
        """
        It Checks If An Item Is Selected or Not If Selected then it Shows Menu.

        :param event:
        """
        self.cursor_row = self.custom_treeview.focus()
        self.contents = self.custom_treeview.item(self.cursor_row)
        if ('values', '') not in self.contents.items():
            self.treeview_menu.tk_popup(event.x_root, event.y_root)
            self.treeview_menu.grab_release()

    def place(self, **kwargs):
        self.custom_treeview.place(**kwargs)

    def pack(self, **kwargs):
        self.custom_treeview.pack(**kwargs)

    def grid(self, **kwargs):
        self.custom_treeview.grid(**kwargs)


class Link_Text:
    def __init__(self, root, **kwargs):
        self.link_root = root

        self.style = Style(self.link_root)
        # Loading TTK Themes
        self.link_root.tk.eval("""
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
        self.link_root.tk.call("package", "require", 'awthemes')
        self.link_root.tk.call("package", "require", 'awlight')
        # self.root.tk.call("package", "require", 'awbreeze')

        # Using Theme AWLIGHT
        self.style.theme_use('awlight')

        self.style.configure("S.TLabel", background="SystemButtonFace", font=("Calibri", 10, "underline"))

        self.style.map("S.TLabel",
                       foreground=[("!active", "blue"), ("active", "lightblue"), ("pressed", "darkblue")]
                       )

        self.link_lbl = Label(self.link_root, text=kwargs["link_text"], style="S.TLabel", relief=FLAT)
        self.link_lbl.bind("<ButtonRelease-1>", kwargs["link_function"])

# root = tk.Tk()
# obj = Link_Text(root, link_text="Link", link_function="nothing")
# obj.link_lbl.pack(fill=BOTH, expand=1)
# root.mainloop()
