import os
import re
import tkinter as tk
from tkinter.ttk import *
from tkinter.constants import *
import sqlite3


class Custom_treeview(Treeview):
    """
    This ttk Treeview is made custom for Any Software
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.command_labels = kwargs["command_labels"]
        self.command_options = [command for command in kwargs["command_options"]]
        self.commands = list(zip(self.command_labels, self.command_options))
        self.column_names = []
        for column in kwargs["columns"].keys():
            for items in kwargs["columns"][column].items():
                if items[0] == 'name':
                    self.column_names.append(items[1])

        self.treeview_root = kwargs["master"]
        self.command_labels = kwargs["command_labels"]

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
        self.style.configure("T.Treeview", background="white", foreground="black", fieldbackground="#FFFF88")
        self.style.map("T.Treeview",
                       background=[("selected", "#00a62d")])
        # Treeview Heading Style
        # self.style.map("T.Treeview.Heading", font="Times New Roman 1")
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
        # Horizontal Scrollbar
        self.hsb = Scrollbar(self.custom_treeview,
                             orient="horizontal",
                             command=self.custom_treeview.xview
                             )
        # Scroll Command For Particulars Treeview
        self.custom_treeview['yscrollcommand'] = self.vsb.set
        self.custom_treeview['xscrollcommand'] = self.hsb.set

        # Treeview Headings
        for column in kwargs["columns"].keys():
            for items in kwargs["columns"][column].items():
                if items[0] == 'name':
                    self.custom_treeview.heading(items[1],
                                                 text=items[1])
        self.custom_treeview["displaycolumns"] = self.column_names
        self.custom_treeview["show"] = "headings"

        self.columns = {}
        for column in kwargs["columns"]:
            self.column_name = column[0]

        # Treeview Columns
        for column in kwargs["columns"].keys():
            for items in kwargs["columns"][column].items():
                if items[0] == 'width':
                    self.custom_treeview.column(column, width=items[1], minwidth=items[1],
                                                anchor='center', stretch=0)

        # Tags for Treeview
        self.custom_treeview.tag_configure('oddrow', background="white")
        self.custom_treeview.tag_configure('evenrow', background="#c5dbbf")

        # Packing Vertical Scrollbar
        self.vsb.pack(side=RIGHT, fill=Y)
        self.hsb.pack(side=BOTTOM, fill=X)

        # Configuring Vertical Scrollbar
        self.vsb.configure(command=self.custom_treeview.yview)
        self.hsb.configure(command=self.custom_treeview.xview)

        # Right-Click Menu
        self.treeview_menu = tk.Menu(self.custom_treeview, tearoff=0)
        for i, j in self.commands:
            self.treeview_menu.add_command(label=i, command=j)
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


class Required_Text:
    def __init__(self, root, **kwargs):
        self.required_root = root

        self.style = Style(self.required_root)
        # Loading TTK Themes
        self.required_root.tk.eval("""
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
        self.required_root.tk.call("package", "require", 'awthemes')
        self.required_root.tk.call("package", "require", 'awlight')
        # self.root.tk.call("package", "require", 'awbreeze')

        # Using Theme AWLIGHT
        self.style.theme_use('awlight')

        self.style.configure("Required.TLabel", background="SystemButtonFace", font=("Calibri", 10))

        self.style.map("Required.TLabel",
                       foreground=[("!active", "red"), ("active", "red"), ("pressed", "red")]
                       )
        self.style.configure("Required_Text.TLabel", background="SystemButtonFace", font=("Calibri", 10))

        self.required_frame = Frame(self.required_root)
        self.required_lbl = Label(self.required_root, text=kwargs["required_text"], style="Required_Text.TLabel")
        self.required_str = Label(self.required_lbl, text="*", style="Required.TLabel")
        self.required_str.place(relx=0.865, rely=0)


class ManageWindow:
    def __init__(self, root, *args, **kwargs):
        self.manage_root = root
        self.style = Style(self.manage_root)
        # Loading TTK Themes
        self.manage_root.tk.eval("""
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
        self.manage_root.tk.call("package", "require", 'awthemes')
        self.manage_root.tk.call("package", "require", 'awlight')
        # self.root.tk.call("package", "require", 'awbreeze')

        # Using Theme AWLIGHT
        self.style.theme_use('awlight')

        self.style.configure("S.TLabelframe", background="SystemButtonFace")
        self.style.configure("S.TLabelframe.Label", background="SystemButtonFace")
        self.style.configure("S.TLabel", background="SystemButtonFace")
        self.style.map("Red.TButton",
                       background=[("!active", "#ff0000"), ("active", "#ba0000"), ("pressed", "#800000")],
                       foreground=[("!active", "white"), ("active", "white"), ("pressed", "white"), ]
                       )
        self.style.map("Green.TButton",
                       background=[("!active", "#20bf00"), ("active", "#25db00"), ("pressed", "#27e800")],
                       foreground=[("!active", "white"), ("active", "white"), ("pressed", "white"), ]
                       )
        self.manage_root.title(f"Manage {kwargs['search_frame']}")
        self.manage_root.geometry("%sx%s+125+50" % (1100, 600))
        self.manage_root.attributes('-toolwindow', 1)
        self.manage_root.attributes('-topmost', 1)

        self.search_frame = LabelFrame(self.manage_root, text="Search " + kwargs["search_frame"],
                                       style="S.TLabelframe")
        self.search_frame.place(relx=0.02, rely=0.01, relwidth=0.75, relheight=0.1)

        self.client_search_lbl = Label(self.search_frame, text=kwargs["search_name"], font=("Calibri", 12),
                                       style="S.TLabel")
        self.client_search_lbl.place(relx=0.01, rely=0.1)

        self.client_search_txt = Entry(self.search_frame, font=("Calibri", 12))
        self.client_search_txt.place(relx=0.12, rely=0.1, relwidth=0.88)

        self.search_btn = Button(self.manage_root, text="Search", style="Green.TButton",
                                 command=kwargs["search_function"])
        self.search_btn.place(relx=0.80, rely=0.05)

        self.reset_btn = Button(self.manage_root, text="Reset", style="Red.TButton",
                                command=kwargs["reset_function"])
        self.reset_btn.place(relx=0.90, rely=0.05)

        self.manage_treeview_frame = LabelFrame(self.manage_root, text="Recent Invoice(s)", style="S.TLabelframe")
        self.manage_treeview_frame.place(relx=0.005, rely=0.39, relwidth=0.99, relheight=0.59)

        self.manage_treeview = Custom_treeview(master=self.manage_treeview_frame,
                                               columns=kwargs["columns"], command_labels=kwargs["command_labels"],
                                               command_options=kwargs["command_options"])
        self.manage_treeview.place(relx=0, rely=0, relwidth=1, relheight=1)
        print(kwargs["database"])

    def insert(self, **kwargs):
        self.manage_treeview.custom_treeview.insert(**kwargs)

# root = tk.Tk()
# # Particulars Treeview Dictionary
# invoices_dict = {
#     "Sr No.": {
#         "name": "Sr No.",
#         "width": "60"
#     },
#     "Status": {
#         "name": "Status",
#         "width": "80"
#     },
#     "Payment Due": {
#         "name": "Payment Due",
#         "width": "100"
#     },
#     "Last Payment On.": {
#         "name": "Last Payment On.",
#         "width": "120"
#     },
#     "Invoice-Type": {
#         "name": "Invoice-Type",
#         "width": "100"
#     },
#     "Invoice-No.": {
#         "name": "Invoice-No.",
#         "width": "100"
#     },
#     "Contact No.": {
#         "name": "Contact No.",
#         "width": "150"
#     },
#     "Client Name": {
#         "name": "Client Name",
#         "width": "200"
#     },
#     "Address": {
#         "name": "Address",
#         "width": "150"
#     },
#     "State(Pos)": {
#         "name": "State(Pos)",
#         "width": "80"
#     },
#     "GSTIN": {
#         "name": "GSTIN",
#         "width": "100"
#     },
#     "Total Amount": {
#         "name": "Total Amount",
#         "width": "100"
#     },
#     "Created On.": {
#         "name": "Created On.",
#         "width": "120"
#     },
# }
# obj = ManageWindow(root, search_frame="Invoices", search_name="Invoice No.", search_function="nothing",
#                    reset_function="nothing",
#                    command_options=["edit_item", "delete_item"], database=f"{os.getcwd()}\\DB\\Invoices.db",
#                    table_name="INVOICES",
#                    command_labels=["Edit", "Delete"], columns=invoices_dict,
#                    )
# root.mainloop()
