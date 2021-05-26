import json
import os
import re
import sqlite3
import tkinter as tk
import tkinter.messagebox as tmsg
from tkinter import scrolledtext
from tkinter.constants import *
from tkinter.ttk import *

import ttkwidgets.autocomplete
import win32com.client
from tkcalendar import DateEntry
import win32com.universal




class Custom_treeview(Treeview):
    """
    This ttk Treeview is made custom for Any Software
    """

    def __init__(self, **kwargs):
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

        # Menubutton style
        self.style.configure("Menu.TMenubutton", background="white", foreground="black", font=("Calibri", 8))

        # Treeview Style
        self.style.configure("T.Treeview", background="white", foreground="black", fieldbackground="#FFFF88",
                             rowheight=40)
        self.style.map("T.Treeview",
                       background=[("selected", "#00a62d")])
        # Treeview Heading Style
        # self.style.configure("T.Treeview.Heading")
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
        self.treeview_menu = tk.Menu(self.custom_treeview, tearoff=0,
                                     background="white", foreground="black")
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
        # # Loading TTK Themes
        # self.link_root.tk.eval("""
        #                         set base_theme_dir C:/Users/Digvijay/Downloads/awthemes-10.2.0/awthemes-10.2.0
        #
        #                         package ifneeded awthemes 10.2.0 \
        #                             [list source [file join $base_theme_dir awthemes.tcl]]
        #                         package ifneeded colorutils 4.8 \
        #                             [list source [file join $base_theme_dir colorutils.tcl]]
        #                         package ifneeded awdark 7.7 \
        #                             [list source [file join $base_theme_dir awdark.tcl]]
        #                         package ifneeded awlight 7.9 \
        #                             [list source [file join $base_theme_dir awlight.tcl]]
        #                         package ifneeded awbreeze 7.9 \
        #                             [list source [file join $base_theme_dir awbreeze.tcl]]
        #                         """)
        #
        # # Load The Awdark And Awlight Themes
        # self.link_root.tk.call("package", "require", 'awthemes')
        # self.link_root.tk.call("package", "require", 'awlight')
        # # self.root.tk.call("package", "require", 'awbreeze')
        #
        # # Using Theme AWLIGHT
        # self.style.theme_use('awlight')

        self.style.configure("S.TLabel", background="#FFFFFF", font=("Calibri", 10, "underline"))

        self.style.map("S.TLabel",
                       foreground=[("!active", "#0000FF"), ("active", "#FF0000"), ("pressed", "#FFee00",)]

                       )
        self.link_lbl = Label(self.link_root, text=kwargs["link_text"], style="S.TLabel", relief=FLAT)
        self.link_lbl.bind("<ButtonRelease-1>", kwargs["link_function"])
        self.link_lbl.bind("Enter", lambda: self.style.configure("S.TLabel", foreground="#FF0000"))
        self.link_lbl.bind("Leave", lambda: self.style.configure("S.TLabel", foreground="#0000FF"))


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


class Add_Client_Window:
    def __init__(self, root):
        self.add_client_window = root
        self.add_client_window.title("Add Customer")
        self.add_client_window.geometry("1152x672+25+12")
        self.add_client_window.attributes('-toolwindow', 1)
        self.add_client_window.attributes('-topmost', 1)
        self.add_client_window.focus_set()
        self.client_photo_lbl = tk.LabelFrame(master=self.add_client_window, text="Customer Photo")
        self.client_photo_lbl.place(relx=0.01, rely=0.01, relwidth=0.17, relheight=0.3)
        self.client_photo = tk.PhotoImage(file="Images\\Staff Photo.png")
        print(self.client_photo.height())
        self.client_photo_label = tk.Label(self.client_photo_lbl, image=self.client_photo)
        self.client_photo_label.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.client_photo_add_btn_image = tk.PhotoImage(file="Images\\Upload.png")
        self.client_photo_add_btn = tk.Button(self.client_photo_lbl, image=self.client_photo_add_btn_image, bd=0, )
        # command=self.imageopen)
        self.client_photo_add_btn.place(relx=0.01, rely=0.8)

        self.client_photo_capture_btn_image = tk.PhotoImage(file="Images\\Capture.png")
        self.client_photo_capture_btn = tk.Button(self.client_photo_lbl, image=self.client_photo_capture_btn_image,
                                                  bd=0)
        self.client_photo_capture_btn.place(relx=0.25, rely=0.8)

        self.client_photo_reset_btn_image = tk.PhotoImage(file="Images\\Reset Camera.png")
        self.client_photo_reset_btn = tk.Button(self.client_photo_lbl, image=self.client_photo_reset_btn_image, bd=0)
        self.client_photo_reset_btn.place(relx=0.50, rely=0.8)

        self.client_photo_cancel_btn_image = tk.PhotoImage(file="Images\\Cancel Camera.png")
        self.client_photo_cancel_btn = tk.Button(self.client_photo_lbl, image=self.client_photo_cancel_btn_image, bd=0)
        self.client_photo_cancel_btn.place(relx=0.75, rely=0.8)

        self.client_profile_notebook = Notebook(self.add_client_window)
        self.client_profile_notebook.place(relx=0.20, rely=0.01, relwidth=1, relheight=1)
        self.tab1 = tk.Frame(self.client_profile_notebook, bd=3)
        self.client_profile_notebook.add(self.tab1, text="Profile")

        self.client_personal_information_lbl = tk.LabelFrame(master=self.tab1, text="Customer Details")
        self.client_personal_information_lbl.place(relx=0.01, rely=0.01, relwidth=0.4, relheight=0.7)

        # Variables
        self.client_personal_full_name_var = tk.StringVar()
        self.client_personal_email_var = tk.StringVar()
        self.client_personal_mobile_no_var = tk.StringVar()
        self.client_personal_city_var = tk.StringVar()
        self.client_tax_gstin_no_var = tk.StringVar()
        self.client_tax_pan_no_var = tk.StringVar()
        self.client_emergency_con_person_var = tk.StringVar()
        self.client_emergency_con_no_var = tk.StringVar()
        self.client_id_information_doc_no_var = tk.StringVar()
        self.client_other_information_balance_var = tk.StringVar()

        self.client_personal_full_name_lbl = tk.Label(self.client_personal_information_lbl, text="Full Name*",
                                                      font=("Calibri", 12))
        self.client_personal_full_name_lbl.place(relx=0.1, rely=0.05)

        self.client_personal_full_name_entry = Entry(self.client_personal_information_lbl,
                                                     textvariable=self.client_personal_full_name_var)
        self.client_personal_full_name_entry.place(relx=0.35, rely=0.05, relwidth=0.55)

        self.client_personal_dob_lbl = tk.Label(self.client_personal_information_lbl, text="DOB*",
                                                font=("Calibri", 12))
        self.client_personal_dob_lbl.place(relx=0.1, rely=0.15)

        self.client_personal_dob_entry = DateEntry(self.client_personal_information_lbl)
        self.client_personal_dob_entry.place(relx=0.35, rely=0.15, relwidth=0.55)

        self.client_personal_gender_lbl = tk.Label(self.client_personal_information_lbl, text="Gender*",
                                                   font=("Calibri", 12))
        self.client_personal_gender_lbl.place(relx=0.1, rely=0.25)

        self.var_gender = tk.StringVar()
        self.male = Radiobutton(self.client_personal_information_lbl, text="Male", variable=self.var_gender,
                                value="Male")
        self.male.place(relx=0.35, rely=0.25)

        self.female = Radiobutton(self.client_personal_information_lbl, text="Female", variable=self.var_gender,
                                  value="Female")
        self.female.place(relx=0.55, rely=0.25)

        self.client_personal_email_lbl = tk.Label(self.client_personal_information_lbl, text="Email ID",
                                                  font=("Calibri", 12))
        self.client_personal_email_lbl.place(relx=0.1, rely=0.35)

        self.client_personal_email_entry = Entry(self.client_personal_information_lbl,
                                                 textvariable=self.client_personal_email_var)

        self.client_personal_email_entry.place(relx=0.35, rely=0.35, relwidth=0.55)

        self.client_personal_mobile_no_lbl = tk.Label(self.client_personal_information_lbl, text="Mobile No.*",
                                                      font=("Calibri", 12))
        self.client_personal_mobile_no_lbl.place(relx=0.1, rely=0.45)

        self.client_personal_mobile_no_entry = Entry(self.client_personal_information_lbl,
                                                     textvariable=self.client_personal_mobile_no_var)
        self.client_personal_mobile_no_entry.place(relx=0.35, rely=0.45, relwidth=0.55)

        self.client_personal_city_lbl = tk.Label(self.client_personal_information_lbl, text="City",
                                                 font=("Calibri", 12))
        self.client_personal_city_lbl.place(relx=0.1, rely=0.55)

        self.client_personal_city_entry = Entry(self.client_personal_information_lbl,
                                                textvariable=self.client_personal_city_var)
        self.client_personal_city_entry.place(relx=0.35, rely=0.55, relwidth=0.55)

        self.client_personal_state_lbl = tk.Label(self.client_personal_information_lbl, text="State.*",
                                                  font=("Calibri", 12))
        self.client_personal_state_lbl.place(relx=0.1, rely=0.65)

        self.client_personal_state_entry = ttkwidgets.autocomplete.AutocompleteCombobox(
            self.client_personal_information_lbl,
            completevalues=["Select",
                            "Andaman and Nicobar",
                            "Andhra Pradesh",
                            "Arunachal Pradesh",
                            "Assam",
                            "Bihar",
                            "Chandigarh",
                            "Chhattisgarh",
                            "Dadra and Nagar Haveli",
                            "Daman and Diu",
                            "Delhi",
                            "Goa",
                            "Gujarat",
                            "Haryana",
                            "Himachal Pradesh",
                            "Jammu & Kashmir",
                            "Jharkhand",
                            "Karnataka",
                            "Kerala",
                            "Lakshadweep",
                            "Madhya Pradesh",
                            "Maharashtra",
                            "Manipur",
                            "Meghalaya",
                            "Mizoram",
                            "Nagaland",
                            "Odisha",
                            "Puducherry",
                            "Punjab",
                            "Rajashthan",
                            "Sikkim",
                            "Tamil Nadu",
                            "Telangana",
                            "Tripura",
                            "Uttar Pradesh",
                            "Uttarakhand",
                            "West Bengal"])
        self.client_personal_state_entry.current(29)
        self.client_personal_state_entry.place(relx=0.35, rely=0.65, relwidth=0.55)

        self.client_personal_address_lbl = tk.Label(self.client_personal_information_lbl, text="Address*",
                                                    font=("Calibri", 12))
        self.client_personal_address_lbl.place(relx=0.1, rely=0.75)

        self.client_personal_address_entry = scrolledtext.ScrolledText(self.client_personal_information_lbl,
                                                                       font=("Calibri", 12))
        self.client_personal_address_entry.place(relx=0.35, rely=0.75, relwidth=0.55, relheight=0.15)

        self.client_tax_information_lbl = tk.LabelFrame(master=self.tab1, text="Tax Details")
        self.client_tax_information_lbl.place(relx=0.01, rely=0.72, relwidth=0.4, relheight=0.2)

        self.client_tax_gstin_no_lbl = tk.Label(self.client_tax_information_lbl, text="GSTIN No.",
                                                font=("Calibri", 13))
        self.client_tax_gstin_no_lbl.place(relx=0.1, rely=0.1)
        self.client_tax_gstin_no_entry = Entry(self.client_tax_information_lbl, font=("Calibri", 12),
                                               textvariable=self.client_tax_gstin_no_var)
        self.client_tax_gstin_no_entry.place(relx=0.4, rely=0.14, relwidth=0.5)

        self.client_tax_pan_no_lbl = tk.Label(self.client_tax_information_lbl, text="PAN No.",
                                              font=("Calibri", 13))
        self.client_tax_pan_no_lbl.place(relx=0.1, rely=0.7)
        self.client_tax_pan_no_entry = Entry(self.client_tax_information_lbl, font=("Calibri", 12),
                                             textvariable=self.client_tax_pan_no_var)
        self.client_tax_pan_no_entry.place(relx=0.4, rely=0.7, relwidth=0.5)

        self.client_emergency_information = tk.LabelFrame(self.client_profile_notebook, text="Emergency Contact")
        self.client_emergency_information.place(relx=0.45, rely=0.05, relwidth=0.33, relheight=0.25)

        self.client_emergency_con_person = tk.Label(self.client_emergency_information, text="Contact Person",
                                                    font=("Calibri", 12))
        self.client_emergency_con_person.place(relx=0.02, rely=0.1)

        self.client_emergency_con_person_txt = Entry(self.client_emergency_information, font=("Calibri", 12),
                                                     textvariable=self.client_emergency_con_person_var)
        self.client_emergency_con_person_txt.place(relx=0.345, rely=0.1, relwidth=0.6)

        self.client_emergency_con_no = tk.Label(self.client_emergency_information, text="Contact No.",
                                                font=("Calibri", 12))
        self.client_emergency_con_no.place(relx=0.02, rely=0.335)

        self.client_emergency_con_no_txt = Entry(self.client_emergency_information, font=("Calibri", 12),
                                                 textvariable=self.client_emergency_con_no_var)
        self.client_emergency_con_no_txt.place(relx=0.345, rely=0.335, relwidth=0.6)

        self.client_emergency_bl_gr = tk.Label(self.client_emergency_information, text="Blood Group",
                                               font=("Calibri", 12))
        self.client_emergency_bl_gr.place(relx=0.02, rely=0.560)

        self.client_emergency_bl_gr_txt = Combobox(self.client_emergency_information, font=("Calibri", 12),
                                                   text="Select",
                                                   state="readonly",
                                                   values=(
                                                       "Select", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"))
        self.client_emergency_bl_gr_txt.current(0)
        self.client_emergency_bl_gr_txt.place(relx=0.345, rely=0.560, relwidth=0.6)

        self.client_id_information = tk.LabelFrame(self.client_profile_notebook, text="Identity Information")
        self.client_id_information.place(relx=0.45, rely=0.33, relwidth=0.33, relheight=0.25)

        self.client_id_information_doc_type_lbl = tk.Label(self.client_id_information, text="Document Type",
                                                           font=("Calibri", 12))

        self.client_id_information_doc_type_lbl.place(relx=0.02, rely=0.1)

        self.doc_chk = tk.StringVar()

        self.client_id_information_doc_type_txt = Combobox(self.client_id_information, text="Document Type",
                                                           font=("Calibri", 12), textvariable=self.doc_chk,
                                                           state="readonly",
                                                           values=(
                                                               "Select",
                                                               "Aadhar Card",
                                                               "PAN Card",
                                                               "Driving License",
                                                               "Government ID",
                                                               "Voter ID Card"
                                                           ))

        self.client_id_information_doc_type_txt.bind("<<ComboboxSelected>>", self.activateCheck_doc_client)

        self.client_id_information_doc_type_txt.current(0)

        self.chk_exp = tk.IntVar()
        self.chk_iss = tk.IntVar()

        self.client_id_information_doc_type_txt.place(relx=0.345, rely=0.1, relwidth=0.6)

        self.client_id_information_doc_no = tk.Label(self.client_id_information, text="Document No.",
                                                     font=("Calibri", 12))
        self.client_id_information_doc_no.place(relx=0.02, rely=0.335)

        self.client_id_information_doc_no_txt = Entry(self.client_id_information, font=("Calibri", 12),
                                                      state=DISABLED,
                                                      textvariable=self.client_id_information_doc_no_var)
        self.client_id_information_doc_no_txt.place(relx=0.345, rely=0.335, relwidth=0.6)

        self.client_id_information_exp_date = tk.Label(self.client_id_information, text="Expiry Date.",
                                                       font=("Calibri", 12))
        self.client_id_information_exp_date.place(relx=0.02, rely=0.560)

        self.client_id_information_exp_date_txt = DateEntry(self.client_id_information, font=("Calibri", 12),
                                                            state=DISABLED)

        self.client_id_information_exp_app_chk = Checkbutton(self.client_id_information, variable=self.chk_exp
                                                             , text="Applicable", onvalue=1, offvalue=0,
                                                             command=self.activateCheck_expiry_client)
        self.client_id_information_exp_app_chk.place(relx=0.345, rely=0.560)

        self.client_id_information_exp_date_txt.place(relx=0.645, rely=0.560, relwidth=0.3)

        self.client_id_information_iss_date = tk.Label(self.client_id_information, text="Issue Date",
                                                       font=("Calibri", 12))
        self.client_id_information_iss_date.place(relx=0.02, rely=0.775)

        self.client_id_information_iss_date_txt = DateEntry(self.client_id_information, font=("Calibri", 12),
                                                            state=DISABLED)
        self.client_id_information_iss_date_txt.place(relx=0.645, rely=0.775, relwidth=0.3)

        self.client_id_information_iss_app_chk = Checkbutton(self.client_id_information, variable=self.chk_iss
                                                             , text="Applicable", onvalue=1, offvalue=0,
                                                             command=self.activateCheck_issue_client)
        self.client_id_information_iss_app_chk.place(relx=0.345, rely=0.775)

        self.client_other_information = tk.LabelFrame(self.client_profile_notebook, text="Other Details")
        self.client_other_information.place(relx=0.45, rely=0.60, relwidth=0.33, relheight=0.30)

        self.client_other_information_com = tk.Label(self.client_other_information, text="Communication",
                                                     font=("Calibri", 12))
        self.client_other_information_com.place(relx=0.02, rely=0.1)

        self.chk_sms = tk.IntVar()
        self.chk_ema = tk.IntVar()

        self.client_other_information_com_sms_chk = Checkbutton(self.client_other_information, variable=self.chk_sms
                                                                , text="SMS")
        self.client_other_information_com_sms_chk.place(relx=0.345, rely=0.1)
        self.chk_sms.set(1)

        self.client_other_information_com_ema_chk = Checkbutton(self.client_other_information, variable=self.chk_ema
                                                                , text="Email")
        self.chk_ema.set(1)
        self.client_other_information_com_ema_chk.place(relx=0.645, rely=0.1)

        self.client_other_information_sale = tk.Label(self.client_other_information, text="Sales Commission",
                                                      font=("Calibri", 12))
        self.client_other_information_sale.place(relx=0.02, rely=0.335)

        self.chk_sale = tk.StringVar()

        self.client_other_information_com_sms_chk = Radiobutton(self.client_other_information,
                                                                variable=self.chk_sale
                                                                , value="Yes", text="Yes")
        self.client_other_information_com_sms_chk.place(relx=0.345, rely=0.335)

        self.client_other_information_com_ema_chk = Radiobutton(self.client_other_information,
                                                                variable=self.chk_sale
                                                                , value="No", text="No")
        self.client_other_information_com_ema_chk.place(relx=0.645, rely=0.335)

        self.client_other_information_balance = tk.Label(self.client_other_information,
                                                         text="Balance",
                                                         font=("Calibri", 12))
        self.client_other_information_balance.place(relx=0.02, rely=0.560)

        self.client_other_information_balance_txt = Entry(self.client_other_information, font=("Calibri", 12),
                                                          textvariable=self.client_other_information_balance_var)
        self.client_other_information_balance_txt.place(relx=0.345, rely=0.560)

        self.client_other_information_remark = tk.Label(self.client_other_information,
                                                        text="Remarks/Notes",
                                                        font=("Calibri", 12))
        self.client_other_information_remark.place(relx=0.02, rely=0.785)

        self.client_other_information_remark_txt = scrolledtext.ScrolledText(self.client_other_information,
                                                                             font=("Calibri", 12))
        self.client_other_information_remark_txt.place(relx=0.345, rely=0.785, relwidth=0.6, relheight=0.2)

        self.client_save_btn = Button(self.tab1, text="Save", command=self.save_client_btn, style="C.TButton")
        self.client_save_btn.place(relx=0.60, rely=0.93)

    def activateCheck_expiry_client(self):
        if self.chk_exp.get() == 0:
            print(self.chk_exp.get())
            self.client_id_information_exp_date_txt.config(state=DISABLED)
        elif self.chk_exp.get() == 1:
            print(self.chk_exp.get())
            self.client_id_information_exp_date_txt.config(state=NORMAL)

    def activateCheck_issue_client(self):
        if self.chk_iss.get() == 0:
            print(self.chk_iss.get())
            self.client_id_information_iss_date_txt.config(state=DISABLED)
        elif self.chk_iss.get() == 1:
            print(self.chk_iss.get())
            self.client_id_information_iss_date_txt.config(state=NORMAL)

    def activateCheck_doc_client_event(self, event):
        print(event)
        self.activateCheck_doc_client()

    def activateCheck_doc_client(self):
        if self.doc_chk.get() == "Select" or self.doc_chk.get() == "":
            print(self.doc_chk.get())
            self.client_id_information_doc_no_txt.config(state=DISABLED)
        else:
            print(self.doc_chk.get())
            self.client_id_information_doc_no_txt.config(state=NORMAL)

    def save_client_btn(self):
        if self.client_personal_full_name_entry.get() == "" or self.client_personal_dob_entry.get() == "" or self.var_gender.get() == "" or self.client_personal_mobile_no_entry.get() == "" or self.client_personal_state_entry.get() == "":
            tmsg.showerror("Error", "Please Fill all Required Fields", parent=self.add_client_window)
        else:
            self.conn = sqlite3.connect('DB\\Clients.db')
            print(self.conn)
            self.cursor = self.conn.cursor()
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

            self.cursor.execute(sql)

            self.cursor.execute(
                """insert into CLIENT(Full_Name,DOB,Gender,EMAIL,Contact,City,State,Address,GSTIN,PAN,Contact_Person,
        Contact_Person_Number,Blood_Group,Document_Type,Document_No,Expiry_Date,Issue_Date,Communication_SMS,
        Communication_Email,Sales_Commission,Remarks, Balance) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
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
                    self.client_other_information_balance_txt.get()
                ))
            self.conn.commit()
            self.conn.close()
            tmsg.showinfo("Success", f"Client '{self.client_personal_full_name_entry.get()} Added to Database.'")


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
        self.manage_root.focus_force()

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

    def insert(self, **kwargs):
        self.manage_treeview.custom_treeview.insert(**kwargs)


class Add_Staff_Window:
    def __init__(self, root, reset_staff):
        self.reset_staff = reset_staff
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM DESIGNATION")
        rows = self.cursor.fetchall()
        self.add_staff_window = root
        self.add_staff_window.title("Add Staff")
        self.add_staff_window.geometry("1152x672+25+12")
        self.add_staff_window.attributes('-toolwindow', 1)
        self.add_staff_window.attributes('-topmost', 1)
        self.add_staff_window.focus_set()
        self.staff_photo_lbl = tk.LabelFrame(master=self.add_staff_window, text="Staff Photo")
        self.staff_photo_lbl.place(relx=0.01, rely=0.01, relwidth=0.17, relheight=0.3)
        self.staff_photo = tk.PhotoImage(file="Images\\Staff Photo.png")
        self.staff_photo_label = tk.Label(self.staff_photo_lbl, image=self.staff_photo)
        self.staff_photo_label.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.staff_photo_add_btn_image = tk.PhotoImage(file="Images\\Upload.png")
        self.staff_photo_add_btn = tk.Button(self.staff_photo_lbl, image=self.staff_photo_add_btn_image, bd=0, )
        # command=self.insert_photo)
        self.staff_photo_add_btn.place(relx=0.01, rely=0.8)

        self.staff_photo_capture_btn_image = tk.PhotoImage(file="Images\\Capture.png")
        self.staff_photo_capture_btn = tk.Button(self.staff_photo_lbl, image=self.staff_photo_capture_btn_image, bd=0, )
        # command=self.capture_photo)
        self.staff_photo_capture_btn.place(relx=0.25, rely=0.8)

        self.staff_photo_reset_btn_image = tk.PhotoImage(file="Images\\Reset Camera.png")
        self.staff_photo_reset_btn = tk.Button(self.staff_photo_lbl, image=self.staff_photo_reset_btn_image, bd=0)
        self.staff_photo_reset_btn.place(relx=0.50, rely=0.8)

        self.staff_photo_cancel_btn_image = tk.PhotoImage(file="Images\\Cancel Camera.png")
        self.staff_photo_cancel_btn = tk.Button(self.staff_photo_lbl, image=self.staff_photo_cancel_btn_image, bd=0)

        self.staff_photo_cancel_btn.place(relx=0.75, rely=0.8)
        self.staff_profile_notebook = Notebook(self.add_staff_window)
        self.staff_profile_notebook.place(relx=0.20, rely=0.01, relwidth=1, relheight=1)
        self.tab1 = tk.Frame(self.staff_profile_notebook, bd=3)
        self.staff_profile_notebook.add(self.tab1, text="Profile")
        self.staff_staff_information_lbl = tk.LabelFrame(master=self.tab1, text="Staff Information")
        self.staff_staff_information_lbl.place(relx=0.01, rely=0.01, relwidth=0.4, relheight=0.2)

        self.staff_staff_joining_date_lbl = tk.Label(self.staff_staff_information_lbl, text="Joining Date",
                                                     font=("Calibri", 13))
        self.staff_staff_joining_date_lbl.place(relx=0.1, rely=0.1)
        self.staff_staff_joining_date_entry = DateEntry(self.staff_staff_information_lbl, width=12, background='white',
                                                        foreground='black', borderwidth=2, font=("Calibri", 12))
        self.staff_staff_joining_date_entry.place(relx=0.4, rely=0.14, relwidth=0.5)

        self.staff_staff_designation_lbl = tk.Label(self.staff_staff_information_lbl, text="Designation",
                                                    font=("Calibri", 13))
        self.staff_staff_designation_lbl.place(relx=0.1, rely=0.7)
        self.staff_staff_designation_entry = Combobox(self.staff_staff_information_lbl, font=("Calibri", 12))
        self.staff_staff_designation_entry.place(relx=0.4, rely=0.7, relwidth=0.5)

        result = []
        for i, designation in rows:
            result.append(designation)
        self.staff_staff_designation_entry['values'] = result

        self.staff_personal_information_lbl = tk.LabelFrame(master=self.tab1, text="Personal Information")
        self.staff_personal_information_lbl.place(relx=0.01, rely=0.25, relwidth=0.4, relheight=0.7)

        self.staff_personal_full_name_lbl = tk.Label(self.staff_personal_information_lbl, text="Full Name*",
                                                     font=("Calibri", 12))
        self.staff_personal_full_name_lbl.place(relx=0.1, rely=0.05)

        # Full Name Entry Variable
        self.staff_personal_full_name_var = tk.StringVar()

        self.staff_personal_full_name_entry = Entry(self.staff_personal_information_lbl,
                                                    textvariable=self.staff_personal_full_name_var)
        self.staff_personal_full_name_entry.place(relx=0.35, rely=0.05, relwidth=0.55)

        self.staff_personal_emp_code_lbl = tk.Label(self.staff_personal_information_lbl, text="Employee Code*",
                                                    font=("Calibri", 12))
        self.staff_personal_emp_code_lbl.place(relx=0.1, rely=0.15)

        # Employee Code Entry Variable
        self.staff_personal_emp_code_var = tk.StringVar()

        self.staff_personal_emp_code_entry = Entry(self.staff_personal_information_lbl,
                                                   textvariable=self.staff_personal_emp_code_var)
        self.staff_personal_emp_code_entry.place(relx=0.35, rely=0.15, relwidth=0.55)

        self.staff_personal_gender_lbl = tk.Label(self.staff_personal_information_lbl, text="Gender*",
                                                  font=("Calibri", 12))
        self.staff_personal_gender_lbl.place(relx=0.1, rely=0.25)

        self.var_gender = tk.StringVar()
        self.male = Radiobutton(self.staff_personal_information_lbl, text="Male", variable=self.var_gender,
                                value="Male")
        self.male.place(relx=0.35, rely=0.25)

        self.female = Radiobutton(self.staff_personal_information_lbl, text="Female", variable=self.var_gender,
                                  value="Female")
        self.female.place(relx=0.55, rely=0.25)

        self.staff_personal_email_lbl = tk.Label(self.staff_personal_information_lbl, text="Email ID",
                                                 font=("Calibri", 12))
        self.staff_personal_email_lbl.place(relx=0.1, rely=0.35)

        # Email Variable
        self.staff_personal_email_var = tk.StringVar()

        self.staff_personal_email_entry = Entry(self.staff_personal_information_lbl,
                                                textvariable=self.staff_personal_email_var)

        self.staff_personal_email_entry.place(relx=0.35, rely=0.35, relwidth=0.55)

        self.staff_personal_dob_lbl = tk.Label(self.staff_personal_information_lbl, text="DOB*",
                                               font=("Calibri", 12))
        self.staff_personal_dob_lbl.place(relx=0.1, rely=0.45)

        # Employee Code Entry Variable
        self.staff_personal_dob_var = tk.StringVar()

        self.staff_personal_dob_entry = Entry(self.staff_personal_information_lbl,
                                              textvariable=self.staff_personal_dob_var)
        self.staff_personal_dob_entry.place(relx=0.35, rely=0.45, relwidth=0.55)

        self.staff_personal_mobile_no_lbl = tk.Label(self.staff_personal_information_lbl, text="Mobile No.*",
                                                     font=("Calibri", 12))
        self.staff_personal_mobile_no_lbl.place(relx=0.1, rely=0.55)

        # Mobile No. Variable
        self.staff_personal_mobile_no_var = tk.StringVar()

        self.staff_personal_mobile_no_entry = Entry(self.staff_personal_information_lbl,
                                                    textvariable=self.staff_personal_mobile_no_var)
        self.staff_personal_mobile_no_entry.place(relx=0.35, rely=0.55, relwidth=0.55)

        self.staff_personal_address_lbl = tk.Label(self.staff_personal_information_lbl, text="Address*",
                                                   font=("Calibri", 12))
        self.staff_personal_address_lbl.place(relx=0.1, rely=0.65)

        self.staff_personal_address_entry = scrolledtext.ScrolledText(self.staff_personal_information_lbl,
                                                                      font=("Calibri", 12))
        self.staff_personal_address_entry.place(relx=0.35, rely=0.65, relwidth=0.55, relheight=0.15)

        self.staff_emergency_information = tk.LabelFrame(self.staff_profile_notebook, text="Emergency Contact")
        self.staff_emergency_information.place(relx=0.45, rely=0.05, relwidth=0.33, relheight=0.25)

        self.staff_emergency_con_person = tk.Label(self.staff_emergency_information, text="Contact Person",
                                                   font=("Calibri", 12))
        self.staff_emergency_con_person.place(relx=0.02, rely=0.1)

        # Emergency Contact Person Variable
        self.staff_emergency_con_person_var = tk.StringVar()

        self.staff_emergency_con_person_txt = Entry(self.staff_emergency_information, font=("Calibri", 12),
                                                    textvariable=self.staff_emergency_con_person_var)
        self.staff_emergency_con_person_txt.place(relx=0.345, rely=0.1, relwidth=0.6)

        self.staff_emergency_con_no = tk.Label(self.staff_emergency_information, text="Contact No.",
                                               font=("Calibri", 12))
        self.staff_emergency_con_no.place(relx=0.02, rely=0.335)

        # Emergency Contact Person Number Variable
        self.staff_emergency_con_no_var = tk.StringVar()

        self.staff_emergency_con_no_txt = Entry(self.staff_emergency_information, font=("Calibri", 12),
                                                textvariable=self.staff_emergency_con_no_var)
        self.staff_emergency_con_no_txt.place(relx=0.345, rely=0.335, relwidth=0.6)

        self.staff_emergency_bl_gr = tk.Label(self.staff_emergency_information, text="Blood Group",
                                              font=("Calibri", 12))
        self.staff_emergency_bl_gr.place(relx=0.02, rely=0.560)

        self.staff_emergency_bl_gr_txt = Combobox(self.staff_emergency_information, font=("Calibri", 12),
                                                  text="Select",
                                                  state="readonly",
                                                  values=(
                                                      "Select", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"))
        self.staff_emergency_bl_gr_txt.current(0)
        self.staff_emergency_bl_gr_txt.place(relx=0.345, rely=0.560, relwidth=0.6)

        self.staff_id_information = tk.LabelFrame(self.staff_profile_notebook, text="Identity Information")
        self.staff_id_information.place(relx=0.45, rely=0.33, relwidth=0.33, relheight=0.25)

        self.staff_id_information_doc_type_lbl = tk.Label(self.staff_id_information, text="Document Type",
                                                          font=("Calibri", 12))

        self.staff_id_information_doc_type_lbl.place(relx=0.02, rely=0.1)

        self.doc_chk = tk.StringVar()

        self.staff_id_information_doc_type_txt = Combobox(self.staff_id_information, text="Document Type",
                                                          font=("Calibri", 12), textvariable=self.doc_chk,
                                                          state="readonly",
                                                          values=(
                                                              "Select",
                                                              "Aadhar Card",
                                                              "PAN Card",
                                                              "Driving License",
                                                              "Government ID",
                                                              "Voter ID Card"
                                                          ))

        self.staff_id_information_doc_type_txt.bind("<<ComboboxSelected>>", self.activateCheck_doc_staff_event)

        self.staff_id_information_doc_type_txt.current(0)

        self.chk_exp = tk.IntVar()
        self.chk_iss = tk.IntVar()

        self.staff_id_information_doc_type_txt.place(relx=0.345, rely=0.1, relwidth=0.6)

        self.staff_id_information_doc_no = tk.Label(self.staff_id_information, text="Document No.",
                                                    font=("Calibri", 12))
        self.staff_id_information_doc_no.place(relx=0.02, rely=0.335)

        # Document No Variable
        self.staff_id_information_doc_no_var = tk.StringVar()

        self.staff_id_information_doc_no_txt = Entry(self.staff_id_information, font=("Calibri", 12),
                                                     state=DISABLED, textvariable=self.staff_id_information_doc_no_var)
        self.staff_id_information_doc_no_txt.place(relx=0.345, rely=0.335, relwidth=0.6)

        self.staff_id_information_exp_date = tk.Label(self.staff_id_information, text="Expiry Date.",
                                                      font=("Calibri", 12))
        self.staff_id_information_exp_date.place(relx=0.02, rely=0.560)

        self.staff_id_information_exp_date_txt = DateEntry(self.staff_id_information, font=("Calibri", 12),
                                                           state=DISABLED)

        self.staff_id_information_exp_app_chk = Checkbutton(self.staff_id_information, variable=self.chk_exp
                                                            , text="Applicable", onvalue=1, offvalue=0,
                                                            command=self.activateCheck_expiry_staff)
        self.staff_id_information_exp_app_chk.place(relx=0.345, rely=0.560)

        self.staff_id_information_exp_date_txt.place(relx=0.645, rely=0.560, relwidth=0.3)

        self.staff_id_information_iss_date = tk.Label(self.staff_id_information, text="Issue Date",
                                                      font=("Calibri", 12))
        self.staff_id_information_iss_date.place(relx=0.02, rely=0.775)

        self.staff_id_information_iss_date_txt = DateEntry(self.staff_id_information, font=("Calibri", 12),
                                                           state=DISABLED)
        self.staff_id_information_iss_date_txt.place(relx=0.645, rely=0.775, relwidth=0.3)

        self.staff_id_information_iss_app_chk = Checkbutton(self.staff_id_information, variable=self.chk_iss
                                                            , text="Applicable", onvalue=1, offvalue=0,
                                                            command=self.activateCheck_issue_staff)
        self.staff_id_information_iss_app_chk.place(relx=0.345, rely=0.775)

        self.staff_other_information = tk.LabelFrame(self.staff_profile_notebook, text="Other Details")
        self.staff_other_information.place(relx=0.45, rely=0.60, relwidth=0.33, relheight=0.30)

        self.staff_other_information_com = tk.Label(self.staff_other_information, text="Communication",
                                                    font=("Calibri", 12))
        self.staff_other_information_com.place(relx=0.02, rely=0.1)

        self.chk_sms = tk.IntVar()
        self.chk_ema = tk.IntVar()

        self.staff_other_information_com_sms_chk = Checkbutton(self.staff_other_information, variable=self.chk_sms
                                                               , text="SMS")
        self.staff_other_information_com_sms_chk.place(relx=0.345, rely=0.1)
        self.chk_sms.set(1)

        self.staff_other_information_com_ema_chk = Checkbutton(self.staff_other_information, variable=self.chk_ema
                                                               , text="Email")
        self.chk_ema.set(1)
        self.staff_other_information_com_ema_chk.place(relx=0.645, rely=0.1)

        self.staff_other_information_sale = tk.Label(self.staff_other_information, text="Sales Commission",
                                                     font=("Calibri", 12))
        self.staff_other_information_sale.place(relx=0.02, rely=0.335)

        self.chk_sale = tk.StringVar()

        self.staff_other_information_sale_yes_chk = Radiobutton(self.staff_other_information, variable=self.chk_sale
                                                                , value="Yes", text="Yes")
        self.staff_other_information_sale_yes_chk.place(relx=0.345, rely=0.335)

        self.staff_other_information_sale_no_chk = Radiobutton(self.staff_other_information, variable=self.chk_sale
                                                               , value="No", text="No")
        self.staff_other_information_sale_no_chk.place(relx=0.645, rely=0.335)

        self.staff_other_information_remark = tk.Label(self.staff_other_information,
                                                       text="Remarks/Notes",
                                                       font=("Calibri", 12))
        self.staff_other_information_remark.place(relx=0.02, rely=0.560)

        self.staff_other_information_remark_txt = scrolledtext.ScrolledText(self.staff_other_information,
                                                                            font=("Calibri", 12))
        self.staff_other_information_remark_txt.place(relx=0.345, rely=0.560, relwidth=0.6, relheight=0.4)

        self.staff_save_btn = Button(self.tab1, text="Save", command=self.save_staff_btn)
        self.staff_save_btn.place(relx=0.60, rely=0.95)

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
                self.add_staff_window.destroy()
                self.reset_staff()

    def activateCheck_expiry_staff(self):
        if self.chk_exp.get() == 0:
            self.staff_id_information_exp_date_txt.config(state=DISABLED)
        elif self.chk_exp.get() == 1:
            self.staff_id_information_exp_date_txt.config(state=NORMAL)

    def activateCheck_issue_staff(self):
        if self.chk_iss.get() == 0:
            self.staff_id_information_iss_date_txt.config(state=DISABLED)
        elif self.chk_iss.get() == 1:
            self.staff_id_information_iss_date_txt.config(state=NORMAL)

    def activateCheck_doc_staff_event(self, event):
        self.activateCheck_doc_staff()

    def activateCheck_doc_staff(self):
        if self.doc_chk.get() == "Select" or self.doc_chk.get() == "":
            self.staff_id_information_doc_no_txt.config(state=DISABLED)
        else:
            self.staff_id_information_doc_no_txt.config(state=NORMAL)


class Manage_Staff:
    def __init__(self, root):
        self.staff_root = root
        self.staff_dict = {
            "Staff Id": {
                "name": "Staff Id",
                "width": "100"
            },
            "Staff Name": {
                "name": "Staff Name",
                "width": "200"
            },
            "Address": {
                "name": "Address",
                "width": "500"
            },
            "Contact No.": {
                "name": "Contact No.",
                "width": "180"
            },
            "Designation": {
                "name": "Designation",
                "width": "200"
            },
            "Department": {
                "name": "Department",
                "width": "200"
            },
            "Status": {
                "name": "Status",
                "width": "180"
            }
        }
        self.manage = ManageWindow(self.staff_root, search_frame="Employees", search_name="Staff Id",
                                   search_function=self.search_staff,
                                   reset_function=self.reset_staff,
                                   command_options=[self.edit_staff, self.delete_staff],
                                   command_labels=["View/ Edit/ Modify", "Delete"], columns=self.staff_dict,
                                   )

    def search_staff(self):
        if self.manage.client_search_txt.get() == "":
            tmsg.showerror("Error", "Please Enter Employee Code", parent=self.manage.manage_root)
        else:
            conn = sqlite3.connect('DB\\Employee.db')
            cursor = conn.cursor()

            sqlite_update_query = """SELECT * from STAFF where Employee_Code = ?"""

            cursor.execute(sqlite_update_query, (self.manage.client_search_txt.get(),))
            rows = cursor.fetchall()
            if rows != []:
                count = 1
                for id, Full_Name, DOB, Gender, EMAIL, Contact, Employee_Code, Address, Join_date, Designation, \
                    Contact_Person, Contact_Person_Number, Blood_Group, Document_Type, Document_No, Expiry_Date, \
                    Issue_Date, Communication_SMS, Communication_Email, Sales_Commission, Remarks in rows:
                    address = Address
                    address1 = address.splitlines()
                    final_address = " "
                    print(address1)
                    final_address.join(address1[i] for i in range(len(address1)))
                    print(final_address)
                    if count % 2 == 0:
                        self.manage.manage_treeview.custom_treeview.insert('', END,
                                                                           values=(
                                                                               Employee_Code, Full_Name, Address,
                                                                               Contact,
                                                                               Designation,
                                                                               "Department", "Active"),
                                                                           tags=('evenrow',))
                        count += 1
                    else:
                        self.manage.manage_treeview.custom_treeview.insert('', END,
                                                                           values=(
                                                                               Employee_Code, Full_Name, Address,
                                                                               Contact,
                                                                               Designation,
                                                                               "Department", "Active"),
                                                                           tags=('oddrow',))
                        count += 1
            else:
                tmsg.showerror("Error", "Employee Not Found. \nPlease Check The Code!",
                               parent=self.manage.manage_root)

    def reset_staff(self):
        conn = sqlite3.connect('DB\\Employee.db')
        cursor = conn.cursor()
        self.manage.manage_treeview.custom_treeview.delete(
            *self.manage.manage_treeview.custom_treeview.get_children())
        cursor.execute("SELECT * FROM STAFF")
        rows = cursor.fetchall()
        count = 1
        if rows != []:
            for id, Full_Name, DOB, Gender, EMAIL, Contact, Employee_Code, Address, Join_date, Designation, \
                Contact_Person, Contact_Person_Number, Blood_Group, Document_Type, Document_No, Expiry_Date, \
                Issue_Date, Communication_SMS, Communication_Email, Sales_Commission, Remarks in rows:
                address = Address
                address1 = address.splitlines()
                final_address = " "
                print(address1)
                final_address.join(address1[i] for i in range(len(address1)))
                print(final_address)
                if count % 2 == 0:
                    self.manage.manage_treeview.custom_treeview.insert('', END,
                                                                       values=(
                                                                           Employee_Code, Full_Name, Address,
                                                                           Contact,
                                                                           Designation,
                                                                           "Department", "Active"),
                                                                       tags=('evenrow',))
                    count += 1
                else:
                    self.manage.manage_treeview.custom_treeview.insert('', END,
                                                                       values=(
                                                                           Employee_Code, Full_Name, Address,
                                                                           Contact,
                                                                           Designation,
                                                                           "Department", "Active"),
                                                                       tags=('oddrow',))
                    count += 1
        else:
            ans = tmsg.askquestion("Please Add Staff", "No Employees Found! \n\n Would You Like To Add Employees Now?",
                                   icon="error", master=self.staff_root)
            if ans == "yes":
                employee_root = tk.Toplevel(self.staff_root)
                employee = Add_Staff_Window(employee_root, self.reset_staff)
            else:
                self.manage.manage_root.destroy()
        conn.commit()
        conn.close()

    def edit_staff(self):
        cursor_row = self.manage.manage_treeview.custom_treeview.focus()
        contents = self.manage.manage_treeview.custom_treeview.item(cursor_row)['values']
        # Getting Details From Database
        conn = sqlite3.connect("DB\\Employee.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM STAFF where Employee_Code = ?", (contents[0],))
        rows = cursor.fetchone()
        if rows is not None or []:
            employee_root = tk.Toplevel(self.staff_root)
            employee = Add_Staff_Window(employee_root, self.reset_staff)
            employee.staff_personal_full_name_var.set(rows[1])
            employee.staff_personal_dob_var.set(rows[2])
            employee.var_gender.set(rows[3])
            employee.staff_personal_email_var.set(rows[4])
            employee.staff_personal_mobile_no_var.set(rows[5])
            employee.staff_personal_emp_code_var.set(rows[6])
            employee.staff_personal_address_entry.insert(INSERT, rows[7])
            employee.staff_staff_joining_date_entry.set_date(rows[8])
            employee.staff_staff_designation_entry.set(rows[9])
            employee.staff_emergency_con_person_var.set(rows[10])
            employee.staff_emergency_con_no_var.set(rows[11])
            employee.staff_emergency_bl_gr_txt.set(rows[12])
            employee.staff_id_information_doc_type_txt.set(rows[13])
            employee.activateCheck_doc_staff()
            employee.staff_id_information_doc_no_var.set(rows[14])
            if rows[15] != "":
                employee.chk_exp.set(1)
                employee.staff_id_information_exp_date_txt.set_date(rows[15])
            if rows[16] != "":
                employee.chk_iss.set(1)
                employee.staff_id_information_iss_date_txt.set_date(rows[16])
            employee.chk_ema.set(rows[17])
            employee.chk_ema.set(rows[18])
            employee.chk_sale.set(rows[19])
            employee.staff_other_information_remark_txt.insert(INSERT, rows[20])

            def update_staff():
                if employee.staff_personal_full_name_entry.get() == "" or employee.staff_personal_dob_entry.get() == "" or employee.var_gender.get() == "" or employee.staff_personal_mobile_no_entry.get() == "" or employee.staff_personal_emp_code_entry.get() == "" or employee.staff_personal_address_entry.get(
                        '1.0', END) == "":

                    tmsg.showerror("Error", "Please Fill All Required Details", parent=employee.add_staff_window)
                else:
                    employee.ans = tmsg.askquestion("Are you Sure?",
                                                    f"Are you sure to You want ot Update Employee '{employee.staff_personal_full_name_entry.get()}' "
                                                    , parent=employee.add_staff_window)
                    if employee.ans == 'yes':
                        employee.conn = sqlite3.connect('DB\\Employee.db')
                        employee.cursor = employee.conn.cursor()

                        employee.cursor.execute(
                            """UPDATE STAFF
                            SET Full_Name = ?,DOB = ?,Gender = ?,
                            EMAIL = ?,Contact = ?,Employee_Code = ?,
                            Address = ?,Join_date = ?,Designation = ?,
                            Contact_Person = ?, Contact_Person_Number = ?,Blood_Group = ?,
                            Document_Type = ?,Document_No = ?,Expiry_Date = ?,
                            Issue_Date = ?,Communication_SMS = ?, Communication_Email = ?,
                            Sales_Commission = ?,Remarks = ?
                            WHERE Employee_Code = ?""",
                            (
                                employee.staff_personal_full_name_entry.get(),
                                employee.staff_personal_dob_entry.get(),
                                employee.var_gender.get(),
                                employee.staff_personal_email_entry.get(),
                                employee.staff_personal_mobile_no_entry.get(),
                                employee.staff_personal_emp_code_entry.get(),
                                employee.staff_personal_address_entry.get('1.0', END),
                                employee.staff_staff_joining_date_entry.get(),
                                employee.staff_staff_designation_entry.get(),
                                employee.staff_emergency_con_person_txt.get(),
                                employee.staff_emergency_con_no_txt.get(),
                                employee.staff_emergency_bl_gr_txt.get(),
                                employee.staff_id_information_doc_type_txt.get(),
                                employee.staff_id_information_doc_no_txt.get(),
                                employee.staff_id_information_exp_date_txt.get(),
                                employee.staff_id_information_iss_date_txt.get(),
                                employee.chk_sms.get(),
                                employee.chk_ema.get(),
                                employee.chk_sale.get(),
                                employee.staff_other_information_remark_txt.get('1.0', END),
                                employee.staff_personal_emp_code_entry.get(),
                            ))
                        employee.conn.commit()
                        employee.conn.close()
                        tmsg.showinfo("Success",
                                      f"Employee '{employee.staff_personal_full_name_entry.get()} Updated.'",
                                      master=employee.add_staff_window)
                        employee.add_staff_window.destroy()
                        self.reset_staff()

            employee.staff_save_btn["text"] = "Update"
            employee.staff_save_btn["command"] = update_staff
        else:
            tmsg.showerror("Error", "There was A Problem Opening Staff Window!", master=self.manage.manage_root)
            self.reset_staff()
        conn.commit()
        conn.close()

    def delete_staff(self):
        cursor_row = self.manage.manage_treeview.custom_treeview.focus()
        contents = self.manage.manage_treeview.custom_treeview.item(cursor_row)['values']
        # Getting Details From Database
        conn = sqlite3.connect("DB\\Employee.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM STAFF where Employee_Code = ?", (contents[0],))
        conn.commit()
        conn.close()
        self.reset_staff()


class Manage_Customer:
    def __init__(self, root):
        self.client_dict = {
            "Sr No.": {
                "name": "Sr No.",
                "width": "100"
            },
            "Customer Name": {
                "name": "Customer Name",
                "width": "200"
            },
            "Address": {
                "name": "Address",
                "width": "500"
            },
            "Contact No.": {
                "name": "Contact No.",
                "width": "180"
            },
            "State": {
                "name": "State",
                "width": "200"
            },
            "GSTIN": {
                "name": "GSTIN",
                "width": "200"
            },
            "Bank Balance": {
                "name": "Bank Balance",
                "width": "180"
            }
        }

        self.manage = ManageWindow(root, search_frame="Customers", search_name="Customer Name",
                                   search_function=self.search_client,
                                   reset_function=self.reset_client,
                                   command_options=[self.edit_client, self.delete_staff],
                                   command_labels=["View/ Edit/ Modify", "Delete"], columns=self.client_dict,
                                   )

    def search_client(self):
        if self.manage.client_search_txt.get() == "":
            tmsg.showerror("Error", "Please Enter Customer Name", parent=self.manage.manage_root)
        else:
            conn = sqlite3.connect('DB\\Clients.db')
            cursor = conn.cursor()

            sqlite_update_query = """SELECT * from CLIENT where Client_Name = ?"""

            cursor.execute(sqlite_update_query, (self.manage.client_search_txt.get(),))
            rows = cursor.fetchall()
            if rows != []:
                print(rows)
                count = 1
                for id, Full_Name, DOB, Gender, EMAIL, Contact, City, State, Address, GSTIN, \
                    PAN, Contact_Person, Contact_Person_Number, Blood_Group, Document_Type, Document_No, \
                    Expiry_Date, Issue_Date, Communication_SMS, Communication_Email, Sales_Commission, Remarks, Balance in rows:
                    print(State)
                    address = Address
                    address1 = address.splitlines()
                    final_address = " "
                    final_address.join(address1[i] for i in range(len(address1)))
                    if count % 2 == 0:
                        self.manage.manage_treeview.custom_treeview.insert('', END,
                                                                           values=(
                                                                               count, Full_Name, Address, Contact,
                                                                               State,
                                                                               GSTIN, Balance),
                                                                           tags=('evenrow',))
                        count += 1
                    else:
                        self.manage.manage_treeview.custom_treeview.insert('', END,
                                                                           values=(
                                                                               count, Full_Name, Address, Contact,
                                                                               State,
                                                                               GSTIN, Balance),
                                                                           tags=('oddrow',))
                        count += 1
            else:
                tmsg.showerror("Error", "Customer Not Found. \nPlease Check The Name!", parent=self.manage.manage_root)
                self.reset_client()

    def reset_client(self):
        conn = sqlite3.connect('DB\\Clients.db')
        cursor = conn.cursor()
        self.manage.manage_treeview.custom_treeview.delete(*self.manage.manage_treeview.custom_treeview.get_children())
        cursor.execute("SELECT * FROM CLIENT")
        rows = cursor.fetchall()
        count = 1
        if rows != []:
            for id, Full_Name, DOB, Gender, EMAIL, Contact, City, State, Address, GSTIN, \
                PAN, Contact_Person, Contact_Person_Number, Blood_Group, Document_Type, Document_No, \
                Expiry_Date, Issue_Date, Communication_SMS, Communication_Email, Sales_Commission, Remarks, Balance in rows:
                print(State)
                address = Address
                address1 = address.splitlines()
                final_address = " "
                final_address.join(address1[i] for i in range(len(address1)))
                if count % 2 == 0:
                    self.manage.manage_treeview.custom_treeview.insert('', END,
                                                                       values=(
                                                                           count, Full_Name, Address, Contact,
                                                                           State,
                                                                           GSTIN, Balance),
                                                                       tags=('evenrow',))
                    count += 1
                else:
                    self.manage.manage_treeview.custom_treeview.insert('', END,
                                                                       values=(
                                                                           count, Full_Name, Address, Contact,
                                                                           State,
                                                                           GSTIN, Balance),
                                                                       tags=('oddrow',))
                    count += 1
        else:
            ans = tmsg.askquestion("Please Add Staff",
                                   "No Customers Found! \n\n Would You Like To Add Customers Now?",
                                   icon="error", master=self.manage.manage_root)
            if ans == "yes":
                client_root = tk.Toplevel(self.manage.manage_root)
                client = Add_Client_Window(client_root)
            else:
                self.manage.manage_root.destroy()
        conn.commit()
        conn.close()

    def edit_client(self):
        cursor_row = self.manage.manage_treeview.custom_treeview.focus()
        contents = self.manage.manage_treeview.custom_treeview.item(cursor_row)['values']
        # Getting Details From Database
        conn = sqlite3.connect("DB\\Clients.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CLIENT where Full_Name = ?", (contents[1],))
        rows = cursor.fetchone()
        if rows is not None or []:
            client_root = tk.Toplevel(self.manage.manage_root)
            client = Add_Client_Window(client_root)
            client.client_personal_full_name_var.set(rows[1])
            client.client_personal_dob_entry.set_date(rows[2])
            client.var_gender.set(rows[3])
            client.client_personal_email_var.set(rows[4])
            client.client_personal_mobile_no_var.set(rows[5])
            client.client_personal_city_var.set(rows[6])
            client.client_personal_state_entry.set(rows[7])
            client.client_personal_address_entry.insert(INSERT, rows[8])
            client.client_tax_gstin_no_var.set(rows[9])
            client.client_tax_pan_no_var.set(rows[10])
            client.client_emergency_con_person_var.set(rows[11])
            client.client_emergency_con_no_var.set(rows[12])
            client.client_emergency_bl_gr_txt.set(rows[13])
            client.client_id_information_doc_type_txt.set(rows[14])
            client.activateCheck_doc_client()
            client.client_id_information_doc_no_var.set(rows[15])
            if rows[16] != "":
                client.chk_exp.set(1)
                client.client_id_information_exp_date_txt.set_date(rows[16])
            if rows[17] != "":
                client.chk_iss.set(1)
                client.client_id_information_iss_date_txt.set_date(rows[17])
            client.chk_ema.set(rows[18])
            client.chk_ema.set(rows[19])
            client.chk_sale.set(rows[20])
            client.client_other_information_remark_txt.insert(INSERT, rows[21])
            client.client_other_information_balance_var.set(rows[22])

            def update_client():
                if client.client_personal_full_name_entry.get() == "" or client.client_personal_dob_entry.get() == "" or client.var_gender.get() == "" or client.client_personal_mobile_no_entry.get() == "" or client.client_personal_address_entry.get(
                        '1.0', END) == "":

                    tmsg.showerror("Error", "Please Fill All Required Details", parent=client.add_client_window)
                else:
                    client.ans = tmsg.askquestion("Are you Sure?",
                                                  f"Are you sure to You want ot Update Employee '{client.client_personal_full_name_entry.get()}' "
                                                  , parent=client.add_client_window)
                    if client.ans == 'yes':
                        client.conn = sqlite3.connect('DB\\Clients.db')
                        client.cursor = client.conn.cursor()

                        client.cursor.execute(
                            """UPDATE CLIENT
                            SET Full_Name = ?,DOB = ?,Gender = ?,
                            EMAIL = ?,Contact = ?,City = ?,
                            State = ?,Address = ?,GSTIN = ?,
                            PAN = ?, Contact_Person = ?,Contact_Person_Number = ?,
                            Blood_Group = ?,Document_Type = ?,Document_No = ?,
                            Expiry_Date = ?,Issue_Date = ?, Communication_SMS = ?,
                            Communication_Email = ?,Sales_Commission = ?, Remarks = ?, Balance = ?
                            WHERE Full_Name = ?""",
                            (
                                client.client_personal_full_name_entry.get(),
                                client.client_personal_dob_entry.get(),
                                client.var_gender.get(),
                                client.client_personal_email_entry.get(),
                                client.client_personal_mobile_no_entry.get(),
                                client.client_personal_city_entry.get(),
                                client.client_personal_state_entry.get(),
                                client.client_personal_address_entry.get('1.0', END),
                                client.client_tax_gstin_no_entry.get(),
                                client.client_tax_pan_no_entry.get(),
                                client.client_emergency_con_person_txt.get(),
                                client.client_emergency_con_no_txt.get(),
                                client.client_emergency_bl_gr_txt.get(),
                                client.client_id_information_doc_type_txt.get(),
                                client.client_id_information_doc_no_txt.get(),
                                client.client_id_information_exp_date_txt.get(),
                                client.client_id_information_iss_date_txt.get(),
                                client.chk_sms.get(),
                                client.chk_ema.get(),
                                client.chk_sale.get(),
                                client.client_other_information_remark_txt.get('1.0', END),
                                client.client_other_information_balance_txt.get(),
                                client.client_personal_full_name_entry.get(),
                            ))
                        client.conn.commit()
                        client.conn.close()
                        tmsg.showinfo("Success",
                                      f"Employee '{client.client_personal_full_name_entry.get()} Updated.'",
                                      master=client.add_client_window)
                        client.add_client_window.destroy()
                        self.reset_client()

            client.client_save_btn["text"] = "Update"
            client.client_save_btn["command"] = update_client
        else:
            tmsg.showerror("Error", "There was A Problem Opening Staff Window!", master=self.manage.manage_root)
            self.reset_client()
        conn.commit()
        conn.close()

    def delete_staff(self):
        cursor_row = self.manage.manage_treeview.custom_treeview.focus()
        contents = self.manage.manage_treeview.custom_treeview.item(cursor_row)['values']
        # Getting Details From Database
        conn = sqlite3.connect("DB\\Clients.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM CLIENT where Full_Name = ?", (contents[1],))
        conn.commit()
        conn.close()
        self.reset_client()


class Manage_Invoice:
    from techware_invoice import Invoice
    def __init__(self, root):
        self.invoices_root = root
        self.invoices_dict = {
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
        self.invoice = ManageWindow(self.invoices_root, search_frame="Invoices", search_name="Invoice No.",
                                    search_function=self.search_invoice,
                                    reset_function=self.reset_invoice,
                                    command_options=[self.edit_invoice, self.print_invoice, self.delete_invoice],
                                    database=f"{os.getcwd()}\\DB\\Invoices.db",
                                    table_name="INVOICES",
                                    command_labels=["Edit", "Print", "Delete"], columns=self.invoices_dict,
                                    )

    def edit_invoice(self):
        # Connecting To Database
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()

        # Executing Commands In Cursor
        self.cursor.execute("SELECT * FROM CATEGORY")

        # Rows of Data
        self.rows = self.cursor.fetchall()

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
        cursor_row = self.invoice.manage_treeview.custom_treeview.focus()
        contents = self.invoice.manage_treeview.custom_treeview.item(cursor_row)['values']
        # Getting Details From Database
        self.conn = sqlite3.connect("DB\\Invoices.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM INVOICES where Invoice_No = ?", (contents[5],))
        self.rows = self.cursor.fetchone()
        self.invoice_window = tk.Toplevel()
        self.invoic = Invoice(self.invoice_window)
        self.invoic.bill_to_var.set(self.rows[5])
        self.invoic.update_client()
        self.invoic.invoice_type_txt.set(self.rows[1])
        self.invoic.invoice_no_var.set(self.rows[2])
        self.invoic.invoice_date_txt.set_date(self.rows[3])
        self.invoic.invoice_place_of_supply_txt.set(self.rows[4])
        self.invoic.contact_no_var.set(self.rows[6])
        self.invoic.client_name_var.set(self.rows[7])
        if self.invoic.client_name_txt.get() != "CASH":
            self.invoic.client_name_txt.set(self.rows[7])
        self.invoic.contact_address_var.set(self.rows[8])
        self.invoic.client_gstin_var.set(self.rows[9])
        self.invoic.sold_by_txt.set(self.rows[10])

        with open(f"Details\\{self.rows[7]}{self.rows[2]}.json", "r") as outfile:
            self.items = json.load(outfile)
        self.number = 1
        for i in self.categories:
            for j in self.items[i].keys():
                lis = self.items[i][j]
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
                self.invoic.particulars_treeview.custom_treeview.insert("", END,
                                                                        values=[self.number, names1, units1, rates1,
                                                                                quantitys1, discounts1, taxes1,
                                                                                cess1,
                                                                                amounts1, sub_category, category])
                self.number += 1

        self.invoic.discountPrice.set(self.rows[11])
        self.invoic.shippingCharges.set(self.rows[12])
        self.invoic.subTotalPrice.set(self.rows[13])
        self.invoic.totalPrice.set(self.rows[14])

        self.invoic.payment_date_txt.set_date(self.rows[15])
        self.invoic.payment_mode_txt.set(self.rows[15])
        self.invoic.txn_id_var.set(self.rows[16])
        self.invoic.payment_amount_var.set(self.rows[17])
        self.invoic.payment_balance_var.set(self.rows[18])
        self.invoic.remarks_txt.insert(INSERT, self.rows[20])
        self.invoic.delivery_terms_txt.insert(INSERT, self.rows[21])
        self.invoic.items = self.items
        self.invoic.save_btn["text"] = "Update"
        self.invoic.save_print_btn.destroy()
        self.invoic.update_total_price()

        def update_invoice():
            self.ans = tmsg.askquestion("Are you Sure?",
                                        f"Are you Sure to Save Invoice No. '{self.invoic.invoice_no_txt.get()}'")
            if self.ans == "yes":
                if self.invoic.bill_to_var.get() == "client":
                    if self.invoic.client_name_txt.get() == "" or self.invoic.client_address_txt.get() == "" or self.invoic.contact_no_txt.get() \
                            == "" or self.invoic.invoice_type_txt.get() == "Select" or self.invoic.invoice_place_of_supply_txt.get() == \
                            "Select" or self.invoic.invoice_no_txt.get() == "" or self.invoic.payment_mode_txt.get() == "Select":
                        # sold_by_txt.get() == "Select" or \
                        tmsg.showerror("Error", "Please Fill All Required Fields!", master=self.invoices_root)
                    else:
                        print("all checks passed in client")
                        self.conn = sqlite3.connect("DB\\Invoices.db")
                        self.cursor = self.conn.cursor()

                        self.cwd = os.getcwd()

                        self.file_path = f"{self.cwd}\\DB\\INVOICES"

                        if not os.path.exists(self.file_path):
                            os.makedirs(self.file_path)

                        # conn.execute("DROP TABLE INVOICES")

                        # Preparing Table For Invoices
                        self.query = """CREATE TABLE IF NOT EXISTS INVOICES(
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
                        self.update_bill_query = """UPDATE INVOICES 
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
                        self.update_bill_values = (self.invoic.invoice_type_txt.get(), self.invoic.invoice_no_txt.get(),
                                                   self.invoic.invoice_date_txt.get(),
                                                   self.invoic.invoice_place_of_supply_txt.get(),
                                                   self.invoic.bill_to_var.get(), self.invoic.contact_no_txt.get(),
                                                   self.invoic.client_name_txt.get(),
                                                   self.invoic.client_address_txt.get(),
                                                   self.invoic.client_gstin_txt.get(),
                                                   self.invoic.sold_by_txt.get(), self.invoic.discountPrice.get(),
                                                   self.invoic.shippingCharges.get(), self.invoic.subTotalPrice.get(),
                                                   self.invoic.totalPrice.get(), self.invoic.payment_date_txt.get(),
                                                   self.invoic.payment_mode_txt.get(), self.invoic.txn_id_txt.get(),
                                                   self.invoic.payment_amount_txt.get(),
                                                   self.invoic.payment_balance_txt.get(),
                                                   self.invoic.remarks_txt.get("1.0", END),
                                                   self.invoic.delivery_terms_txt.get("1.0", END),
                                                   self.invoic.invoice_no_txt.get(),
                                                   )
                        self.cursor.execute(self.query)
                        self.cursor.execute(self.update_bill_query, self.update_bill_values)
                        self.cursor.execute("SELECT * FROM INVOICES WHERE Invoice_No = ?",
                                            (self.invoic.invoice_no_txt.get(),))
                        self.rows = self.cursor.fetchall()
                        self.conn.commit()
                        self.conn.close()
                        self.save_items = json.dumps(self.items, indent=len(self.items))
                        with open(
                                f"Details\\{self.invoic.client_name_txt.get()}{self.invoic.invoice_no_txt.get()}.json",
                                "w") as outfile:
                            outfile.write(self.save_items)
                elif self.invoic.bill_to_var.get() == "cash":
                    if self.invoic.client_name_txt.get() == "" or self.invoic.invoice_type_txt.get() == "Select" or \
                            self.invoic.invoice_place_of_supply_txt.get() == \
                            "Select" or self.invoic.invoice_no_txt.get() == "" or \
                            self.invoic.payment_mode_txt.get() == "Select":
                        tmsg.showerror("Error", "Please Fill All Required Fields!", master=self.invoices_root)
                    else:
                        print("all checks passed in cash")
                        self.conn = sqlite3.connect("DB\\Invoices.db")
                        self.cursor = self.conn.cursor()

                        self.cwd = os.getcwd()

                        self.file_path = f"{self.cwd}\\DB\\INVOICES"

                        if not os.path.exists(self.file_path):
                            os.makedirs(self.file_path)

                        # conn.execute("DROP TABLE INVOICES")

                        # Preparing Table For Invoices
                        self.query = """CREATE TABLE IF NOT EXISTS INVOICES(
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
                        self.update_bill_query = """UPDATE INVOICES 
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
                        self.update_bill_values = (
                            self.invoic.invoice_type_txt.get(), self.invoic.invoice_no_txt.get(),
                            self.invoic.invoice_date_txt.get(), self.invoic.invoice_place_of_supply_txt.get(),
                            self.invoic.bill_to_var.get(), self.invoic.contact_no_txt.get(),
                            self.invoic.client_name_txt.get(),
                            self.invoic.client_address_txt.get(), self.invoic.client_gstin_txt.get(),
                            self.invoic.sold_by_txt.get(), self.invoic.discountPrice.get(),
                            self.invoic.shippingCharges.get(), self.invoic.subTotalPrice.get(),
                            self.invoic.totalPrice.get(), self.invoic.payment_date_txt.get(),
                            self.invoic.payment_mode_txt.get(), self.invoic.txn_id_txt.get(),
                            self.invoic.payment_amount_txt.get(), self.invoic.payment_balance_txt.get(),
                            self.invoic.remarks_txt.get("1.0", END),
                            self.invoic.delivery_terms_txt.get("1.0", END),
                            self.invoic.invoice_no_txt.get(),
                        )
                        self.cursor.execute(self.query)
                        self.cursor.execute(self.update_bill_query, self.update_bill_values)
                        self.cursor.execute("SELECT * FROM INVOICES WHERE Invoice_No = ?",
                                            (self.invoic.invoice_no_txt.get(),))
                        self.rows = self.cursor.fetchall()
                        self.conn.commit()
                        self.conn.close()
                        self.save_items = json.dumps(self.items, indent=len(self.items))
                        with open(
                                f"Details\\{self.invoic.client_name_txt.get()}{self.invoic.invoice_no_txt.get()}.json",
                                "w") as outfile:
                            outfile.write(self.save_items)
                        self.invoic.save_excel()
                else:
                    self.invoic.invoice_root.destroy()

        self.invoic.save_btn["command"] = update_invoice

    def print_invoice(self):
        cursor_row = self.invoice.manage_treeview.custom_treeview.focus()
        contents = self.invoice.manage_treeview.custom_treeview.item(cursor_row)['values']
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

    def delete_invoice(self):
        cursor_row = self.invoice.manage_treeview.custom_treeview.focus()
        contents = self.invoice.manage_treeview.custom_treeview.item(cursor_row)['values']
        # Getting Details From Database
        conn = sqlite3.connect("DB\\Invoices.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM INVOICES where Invoice_No = ?", (contents[5],))
        conn.commit()
        conn.close()
        self.reset_invoice()

    def reset_invoice(self):
        self.invoice.manage_treeview.custom_treeview.delete(
            *self.invoice.manage_treeview.custom_treeview.get_children())
        self.conn = sqlite3.connect("DB\\Invoices.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"SELECT * FROM INVOICES")
        self.rows = self.cursor.fetchall()
        self.number = 1
        for row in self.rows:
            self.total = re.findall(r"[^\W\d_]+|\d+", row[14])
            self.total_amount = self.total[1]
            self.payment = re.findall(r"[^\W\d_]+|\d+", row[18])
            self.payment_d = self.payment[0]
            self.payment_due = int(self.total_amount) - int(self.payment_d)
            self.payment = "Rs. " + str(self.payment_due) + "/-"
            if self.number % 2 == 0:
                if self.payment_due == 0:
                    self.invoice.manage_treeview.custom_treeview.insert(parent='', index=END,
                                                                        values=[self.number, "PAID", self.payment,
                                                                                row[15],
                                                                                row[1], row[2], row[6],
                                                                                row[7], row[8], row[4],
                                                                                row[9], row[14], row[3]],
                                                                        tags="evenrow",
                                                                        )
                else:
                    self.invoice.manage_treeview.custom_treeview.insert(parent='', index=END,
                                                                        values=[self.number, "UNPAID", self.payment,
                                                                                row[15],
                                                                                row[1], row[2], row[6],
                                                                                row[7], row[8], row[4],
                                                                                row[9], row[14], row[3]],
                                                                        tags="evenrow",
                                                                        )
            else:
                if self.payment_due == 0:
                    self.invoice.manage_treeview.custom_treeview.insert(parent='', index=END,
                                                                        values=[self.number, "PAID", self.payment,
                                                                                row[15],
                                                                                row[1], row[2], row[6],
                                                                                row[7], row[8], row[4],
                                                                                row[9], row[14], row[3]],
                                                                        tags="oddrow",
                                                                        )
                else:
                    self.invoice.manage_treeview.custom_treeview.insert(parent='', index=END,
                                                                        values=[self.number, "UNPAID", self.payment,
                                                                                row[15],
                                                                                row[1], row[2], row[6],
                                                                                row[7], row[8], row[4],
                                                                                row[9], row[14], row[3]],
                                                                        tags="oddrow",
                                                                        )
            self.number += 1
        self.conn.commit()
        self.conn.close()

    def search_invoice(self):
        self.invoice.manage_treeview.custom_treeview.delete(
            *self.invoice.manage_treeview.custom_treeview.get_children())
        self.conn = sqlite3.connect("DB\\Invoices.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM INVOICES WHERE Invoice_No = ?", (self.invoice.client_search_txt.get(),))
        self.rows = self.cursor.fetchall()
        self.number = 1
        self.conn.commit()
        self.conn.close()
        if self.rows != None or []:
            for row in self.rows:
                self.total = re.findall(r"[^\W\d_]+|\d+", row[14])
                self.total_amount = self.total[1]
                self.payment = re.findall(r"[^\W\d_]+|\d+", row[18])
                self.payment_d = self.payment[0]
                self.payment_due = int(self.total_amount) - int(self.payment_d)
                self.payment = "Rs. " + str(self.payment_due) + "/-"
                if self.number % 2 == 0:
                    if self.payment_due == 0:
                        self.invoice.manage_treeview.custom_treeview.insert(parent='', index=END,
                                                                            values=[self.number, "PAID", self.payment,
                                                                                    row[15],
                                                                                    row[1], row[2], row[6],
                                                                                    row[7], row[8], row[4],
                                                                                    row[9], row[14], row[3]],
                                                                            tags="evenrow",
                                                                            )
                    else:
                        self.invoice.manage_treeview.custom_treeview.insert(parent='', index=END,
                                                                            values=[self.number, "UNPAID", self.payment,
                                                                                    row[15],
                                                                                    row[1], row[2], row[6],
                                                                                    row[7], row[8], row[4],
                                                                                    row[9], row[14], row[3]],
                                                                            tags="evenrow",
                                                                            )
                else:
                    if self.payment_due == 0:
                        self.invoice.manage_treeview.custom_treeview.insert(parent='', index=END,
                                                                            values=[self.number, "PAID", self.payment,
                                                                                    row[15],
                                                                                    row[1], row[2], row[6],
                                                                                    row[7], row[8], row[4],
                                                                                    row[9], row[14], row[3]],
                                                                            tags="oddrow",
                                                                            )
                    else:
                        self.invoice.manage_treeview.custom_treeview.insert(parent='', index=END,
                                                                            values=[self.number, "UNPAID", self.payment,
                                                                                    row[15],
                                                                                    row[1], row[2], row[6],
                                                                                    row[7], row[8], row[4],
                                                                                    row[9], row[14], row[3]],
                                                                            tags="oddrow",
                                                                            )
                self.number += 1
            else:
                tmsg.showerror("Invoice Not Found", "Please Check The Invoice No.", master=self.invoices_root)
                self.reset_invoice()


class Small_Manage_Window:
    def __init__(self, root, **kwargs):
        self.small_manage_root = root
        self.small_manage_root.title(kwargs["search_frame"])
        self.small_manage_root.geometry("600x500+417+54")
        self.small_manage_root.attributes('-toolwindow', 1)
        self.small_manage_root.attributes('-topmost', 1)
        self.small_manage_root.focus_set()
        self.small_manage_lbl = tk.LabelFrame(self.small_manage_root, text=kwargs["label_frame_name"],
                                              font=("Calibri", 12))
        self.small_manage_lbl.place(relx=0.025, rely=0.01, relwidth=0.95, relheight=0.2)

        self.small_manage_search_lbl = tk.Label(self.small_manage_lbl, text=kwargs["search_name"],
                                                font=("Calibri", 12))
        self.small_manage_search_lbl.place(relx=0.01, rely=0.25)

        self.small_manage_search_txt = Entry(self.small_manage_lbl,
                                             font=("Calibri", 12))
        self.small_manage_search_txt.place(relx=0.35, rely=0.25, relwidth=0.55)

        self.small_manage_save_btn = Button(self.small_manage_root, text="Save", style="S.TButton",
                                            command=kwargs["save_function"])

        self.small_manage_save_btn.place(relx=0.65, rely=0.22, relheight=0.07, relwidth=0.25)

        self.small_manage_treeview_frame = tk.LabelFrame(self.small_manage_root, text=kwargs["treeview_lbl"],
                                                         font=("Calibri", 12))
        self.small_manage_treeview_frame.place(relx=0.025, rely=0.3, relwidth=0.95, relheight=0.70)

        self.small_manage_treeview = Custom_treeview(master=self.small_manage_treeview_frame,
                                                     columns=kwargs["columns"],
                                                     command_labels=kwargs["command_labels"],
                                                     command_options=kwargs["command_options"])


class Edit_Window:
    def __init__(self, root, **kwargs):
        self.edit_root = root
        self.edit_root.geometry("400x100+417+54")
        self.edit_root.attributes('-toolwindow', 1)
        self.edit_root.attributes('-topmost', 1)
        self.edit_lbl = tk.LabelFrame(self.edit_root, text=kwargs["label_frame_name"],
                                      font=("Calibri", 12))
        self.edit_lbl.place(relx=0.025, rely=0.01, relwidth=0.95, relheight=0.95)

        self.edit_search_lbl = tk.Label(self.edit_lbl, text=kwargs["search_name"],
                                        font=("Calibri", 12))
        self.edit_search_lbl.place(relx=0.01, rely=0.25)

        self.edit_search_var = tk.StringVar()

        self.edit_search_txt = Entry(self.edit_lbl,
                                     font=("Calibri", 12), textvariable=self.edit_search_var)
        self.edit_search_txt.place(relx=0.35, rely=0.25, relwidth=0.55)

        self.edit_save_btn = Button(self.edit_lbl, text="Save", style="S.TButton",
                                    command=kwargs["save_function"])

        self.edit_save_btn.place(relx=0.65, rely=0.65, relwidth=0.25)


class Designation_Window:
    def __init__(self, root):
        self.designation_root = root
        self.invoices_dict = {
            "Sr No.": {
                "name": "Sr No.",
                "width": "275"
            },
            "Designation": {
                "name": "Designation",
                "width": "275"
            }
        }
        self.designation = Small_Manage_Window(self.designation_root, search_name="Designation",
                                               search_frame="Designation",
                                               save_function=self.save_designation, command_labels=["Edit", "Delete"],
                                               command_options=[self.edit_designation, self.delete_designation],
                                               columns=self.invoices_dict,
                                               treeview_lbl="Existing Data", label_frame_name="Add Designation")
        self.reset_designation()
        self.designation.small_manage_treeview.custom_treeview.pack(fill=BOTH, expand=1)

    def delete_designation(self):
        self.cursor_row = self.designation.small_manage_treeview.custom_treeview.focus()
        self.contents = self.designation.small_manage_treeview.custom_treeview.item(self.cursor_row)['values']
        # Getting Details From Database
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("DELETE FROM DESIGNATION where designation = ?", (self.contents[1],))
        self.conn.commit()
        self.conn.close()
        self.reset_designation()

    def save_designation(self):
        self.ans = tmsg.askquestion("Are you Sure?",
                                    f"Are you sure to add '{self.designation.small_manage_search_txt.get()}'"
                                    , parent=self.designation.small_manage_root)
        if self.ans == "yes":
            self.conn = sqlite3.connect("DB\\Business.db")
            self.cursor = self.conn.cursor()
            sql = """SELECT * FROM DESIGNATION WHERE designation = ?"""
            self.cursor.execute(sql, (self.designation.small_manage_search_txt.get(),))
            rows = self.cursor.fetchone()

            print(rows)
            if rows is None:
                self.cursor.execute("insert into DESIGNATION(designation) VALUES(?)",
                                    (self.designation.small_manage_search_txt.get(),))
                tmsg.showinfo("Success", f"'{self.designation.small_manage_search_txt.get()}' Successfully Added!",
                              parent=self.designation.small_manage_root)
                self.conn.commit()
                self.conn.close()
                self.reset_designation()
            else:
                tmsg.showerror("Error", "Designation already exists",
                               parent=self.designation.small_manage_root)

    def edit_designation(self):
        self.cursor_row = self.designation.small_manage_treeview.custom_treeview.focus()
        self.contents = self.designation.small_manage_treeview.custom_treeview.item(self.cursor_row)['values']
        self.edit_window = tk.Toplevel(self.designation_root)
        self.edit_frame = Edit_Window(self.edit_window, search_name="Designation",
                                      save_function=self.update_designation, label_frame_name="Edit Designation")
        self.edit_frame.edit_search_var.set(self.contents[1])

    def update_designation(self):
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM DESIGNATION WHERE designation = ?", (self.contents[1],))
        self.rows = self.cursor.fetchone()
        self.sql = '''UPDATE DESIGNATION
                      SET designation = ?
                      WHERE id = ?'''
        self.cursor.execute(self.sql, (self.edit_frame.edit_search_var.get(), self.rows[0]))
        self.conn.commit()
        self.conn.close()
        tmsg.showinfo("Success", "Designation Saved!", parent=self.edit_frame.edit_root)
        self.edit_frame.edit_root.destroy()
        self.reset_designation()

    def reset_designation(self):
        self.designation.small_manage_treeview.custom_treeview.delete(
            *self.designation.small_manage_treeview.custom_treeview.get_children())
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM DESIGNATION")
        self.rows = self.cursor.fetchall()
        count = 1
        for row in self.rows:
            if count % 2 != 0:
                self.designation.small_manage_treeview.custom_treeview.insert('', END, values=(row[0], row[1]),
                                                                              tags=("oddrow",))

            else:
                self.designation.small_manage_treeview.custom_treeview.insert('', END, values=(row[0], row[1]),
                                                                              tags=("evenrow",))
            count += 1


class Category_Window:
    def __init__(self, root):
        self.category_root = root
        self.category_dict = {
            "Sr No.": {
                "name": "Sr No.",
                "width": "275"
            },
            "Category": {
                "name": "Category",
                "width": "275"
            }
        }
        self.category = Small_Manage_Window(self.category_root, search_name="Category",
                                            search_frame="Add Category",
                                            save_function=self.save_category, command_labels=["Edit", "Delete"],
                                            command_options=[self.edit_category, self.delete_category],
                                            columns=self.category_dict,
                                            treeview_lbl="Existing Data", label_frame_name="Add Category")
        self.reset_category()
        self.category.small_manage_treeview.custom_treeview.pack(fill=BOTH, expand=1)

    def delete_category(self):
        self.cursor_row = self.category.small_manage_treeview.custom_treeview.focus()
        self.contents = self.category.small_manage_treeview.custom_treeview.item(self.cursor_row)['values']
        # Getting Details From Database
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("DELETE FROM CATEGORY where Category = ?", (self.contents[1],))
        self.conn.commit()
        self.conn.close()
        self.reset_category()

    def save_category(self):
        self.ans = tmsg.askquestion("Are you Sure?",
                                    f"Are you sure to add '{self.category.small_manage_search_txt.get()}'"
                                    , parent=self.category.small_manage_root)
        if self.ans == "yes":
            self.conn = sqlite3.connect("DB\\Business.db")
            self.cursor = self.conn.cursor()
            sql = """SELECT * FROM CATEGORY WHERE Category = ?"""
            self.cursor.execute(sql, (self.category.small_manage_search_txt.get(),))
            rows = self.cursor.fetchone()

            print(rows)
            if rows is None:
                self.cursor.execute("insert into CATEGORY(Category) VALUES(?)",
                                    (self.category.small_manage_search_txt.get(),))
                tmsg.showinfo("Success", f"'{self.category.small_manage_search_txt.get()}' Successfully Added!",
                              parent=self.category.small_manage_root)
                self.conn.commit()
                self.conn.close()
                self.reset_category()
            else:
                tmsg.showerror("Error", "Category already exists",
                               parent=self.category.small_manage_root)

    def edit_category(self):
        self.cursor_row = self.category.small_manage_treeview.custom_treeview.focus()
        self.contents = self.category.small_manage_treeview.custom_treeview.item(self.cursor_row)['values']
        self.edit_window = tk.Toplevel(self.category_root)
        self.edit_frame = Edit_Window(self.edit_window, search_name="Category",
                                      save_function=self.update_category, label_frame_name="Edit Category")
        self.edit_frame.edit_search_var.set(self.contents[1])

    def update_category(self):
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM CATEGORY WHERE Category = ?", (self.contents[1],))
        self.rows = self.cursor.fetchone()
        self.sql = '''UPDATE CATEGORY
                      SET Category = ?
                      WHERE id = ?'''
        self.cursor.execute(self.sql, (self.edit_frame.edit_search_var.get(), self.rows[0]))
        self.conn.commit()
        self.conn.close()
        tmsg.showinfo("Success", "Category Saved!", parent=self.edit_frame.edit_root)
        self.edit_frame.edit_root.destroy()
        self.reset_category()

    def reset_category(self):
        self.category.small_manage_treeview.custom_treeview.delete(
            *self.category.small_manage_treeview.custom_treeview.get_children())
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM CATEGORY")
        self.rows = self.cursor.fetchall()
        count = 1
        for row in self.rows:
            if count % 2 != 0:
                self.category.small_manage_treeview.custom_treeview.insert('', END, values=(row[0], row[1]),
                                                                           tags=("oddrow",))

            else:
                self.category.small_manage_treeview.custom_treeview.insert('', END, values=(row[0], row[1]),
                                                                           tags=("evenrow",))
            count += 1


class Unit_Window:
    def __init__(self, root):
        self.unit_root = root
        self.unit_dict = {
            "Sr No.": {
                "name": "Sr No.",
                "width": "275"
            },
            "Unit": {
                "name": "Unit",
                "width": "275"
            }
        }
        self.unit = Small_Manage_Window(self.unit_root, search_name="Unit",
                                        search_frame="Add Unit",
                                        save_function=self.save_unit, command_labels=["Edit", "Delete"],
                                        command_options=[self.edit_unit, self.delete_unit],
                                        columns=self.unit_dict,
                                        treeview_lbl="Existing Data", label_frame_name="Add Unit")
        self.reset_unit()
        self.unit.small_manage_treeview.custom_treeview.pack(fill=BOTH, expand=1)

    def delete_unit(self):
        self.cursor_row = self.unit.small_manage_treeview.custom_treeview.focus()
        self.contents = self.unit.small_manage_treeview.custom_treeview.item(self.cursor_row)['values']
        # Getting Details From Database
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("DELETE FROM UNIT where Unit = ?", (self.contents[1],))
        self.conn.commit()
        self.conn.close()
        self.reset_unit()

    def save_unit(self):
        self.ans = tmsg.askquestion("Are you Sure?",
                                    f"Are you sure to add '{self.unit.small_manage_search_txt.get()}'"
                                    , parent=self.unit.small_manage_root)
        if self.ans == "yes":
            self.conn = sqlite3.connect("DB\\Business.db")
            self.cursor = self.conn.cursor()
            sql = """SELECT * FROM UNIT WHERE Unit = ?"""
            self.cursor.execute(sql, (self.unit.small_manage_search_txt.get(),))
            rows = self.cursor.fetchone()

            print(rows)
            if rows is None:
                self.cursor.execute("insert into UNIT(Unit) VALUES(?)",
                                    (self.unit.small_manage_search_txt.get(),))
                tmsg.showinfo("Success", f"'{self.unit.small_manage_search_txt.get()}' Successfully Added!",
                              parent=self.unit.small_manage_root)
                self.conn.commit()
                self.conn.close()
                self.reset_unit()
            else:
                tmsg.showerror("Error", "Unit already exists",
                               parent=self.unit.small_manage_root)

    def edit_unit(self):
        self.cursor_row = self.unit.small_manage_treeview.custom_treeview.focus()
        self.contents = self.unit.small_manage_treeview.custom_treeview.item(self.cursor_row)['values']
        self.edit_window = tk.Toplevel(self.unit_root)
        self.edit_frame = Edit_Window(self.edit_window, search_name="Unit",
                                      save_function=self.update_unit, label_frame_name="Edit Unit")
        self.edit_frame.edit_search_var.set(self.contents[1])

    def update_unit(self):
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM UNIT WHERE Unit = ?", (self.contents[1],))
        self.rows = self.cursor.fetchone()
        self.sql = '''UPDATE UNIT
                      SET Unit = ?
                      WHERE id = ?'''
        self.cursor.execute(self.sql, (self.edit_frame.edit_search_var.get(), self.rows[0]))
        self.conn.commit()
        self.conn.close()
        tmsg.showinfo("Success", "Unit Saved!", parent=self.edit_frame.edit_root)
        self.edit_frame.edit_root.destroy()
        self.reset_unit()

    def reset_unit(self):
        self.unit.small_manage_treeview.custom_treeview.delete(
            *self.unit.small_manage_treeview.custom_treeview.get_children())
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM UNIT")
        self.rows = self.cursor.fetchall()
        count = 1
        for row in self.rows:
            if count % 2 != 0:
                self.unit.small_manage_treeview.custom_treeview.insert('', END, values=(row[0], row[1]),
                                                                       tags=("oddrow",))

            else:
                self.unit.small_manage_treeview.custom_treeview.insert('', END, values=(row[0], row[1]),
                                                                       tags=("evenrow",))
            count += 1


class Id_Window:
    def __init__(self, root):
        self.id_root = root
        self.id_dict = {
            "Sr No.": {
                "name": "Sr No.",
                "width": "200"
            },
            "Category": {
                "name": "Category",
                "width": "200"
            },
            "Id": {
                "name": "Id",
                "width": "175"
            }
        }
        self.id = Small_Manage_Window(self.id_root, search_name="Id",
                                      search_frame="Add Id",
                                      save_function=self.save_id, command_labels=["Edit", "Delete"],
                                      command_options=[self.edit_id, self.delete_id],
                                      columns=self.id_dict,
                                      treeview_lbl="Existing Data", label_frame_name="Add Id")
        self.id.small_manage_category_lbl = tk.Label(self.id.small_manage_lbl, text="Category",
                                                     font=("Calibri", 12))
        self.id.small_manage_category_txt = Entry(self.id.small_manage_lbl,
                                                  font=("Calibri", 12))

        self.id.small_manage_search_lbl.place(relx=0.01, rely=0.05)
        self.id.small_manage_search_txt.place(relx=0.35, rely=0.05, relwidth=0.55)

        self.id.small_manage_category_lbl.place(relx=0.01, rely=0.55)
        self.id.small_manage_category_txt.place(relx=0.35, rely=0.55, relwidth=0.55)
        self.reset_id()
        self.id.small_manage_treeview.custom_treeview.pack(fill=BOTH, expand=1)

    def delete_id(self):
        self.cursor_row = self.id.small_manage_treeview.custom_treeview.focus()
        self.contents = self.id.small_manage_treeview.custom_treeview.item(self.cursor_row)['values']
        # Getting Details From Database
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("DELETE FROM ID where Id = ?", (self.contents[2],))
        self.conn.commit()
        self.conn.close()
        self.reset_id()

    def save_id(self):
        self.ans = tmsg.askquestion("Are you Sure?",
                                    f"Are you sure to add '{self.id.small_manage_search_txt.get()}'"
                                    , parent=self.id.small_manage_root)
        if self.ans == "yes":
            self.conn = sqlite3.connect("DB\\Business.db")
            self.cursor = self.conn.cursor()
            sql = """SELECT * FROM ID WHERE Id = ?"""
            self.cursor.execute(sql, (self.id.small_manage_search_txt.get(),))
            rows = self.cursor.fetchone()

            print(rows)
            if rows is None:
                self.cursor.execute("insert into ID(Id, Category) VALUES(?,?)",
                                    (self.id.small_manage_search_txt.get(), self.id.small_manage_category_txt.get()))
                tmsg.showinfo("Success", f"'{self.id.small_manage_search_txt.get()}' Successfully Added!",
                              parent=self.id.small_manage_root)
                self.conn.commit()
                self.conn.close()
                self.reset_id()
            else:
                tmsg.showerror("Error", "Id already exists",
                               parent=self.id.small_manage_root)

    def edit_id(self):
        self.cursor_row = self.id.small_manage_treeview.custom_treeview.focus()
        self.contents = self.id.small_manage_treeview.custom_treeview.item(self.cursor_row)['values']
        self.edit_window = tk.Toplevel(self.id_root)
        self.edit_frame = Edit_Window(self.edit_window, search_name="Id",
                                      save_function=self.update_id, label_frame_name="Edit Id")
        self.edit_frame.edit_search_var.set(self.contents[2])
        self.edit_frame.edit_search_txt.place(relx=0.35, rely=0.25, relwidth=0.2525)
        self.edit_frame.edit_category_var = tk.StringVar(master=self.edit_frame.edit_lbl)
        self.edit_frame.edit_category_txt = Entry(self.edit_frame.edit_lbl, font=("Calibri", 12),
                                                  textvariable=self.edit_frame.edit_category_var)
        self.edit_frame.edit_category_txt.place(relx=0.7025, rely=0.25, relwidth=0.2525)
        self.edit_frame.edit_category_var.set(self.contents[1])

    def update_id(self):
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM ID WHERE Id = ?", (self.contents[2],))
        self.rows = self.cursor.fetchone()
        self.sql = '''UPDATE ID
                      SET Id = ?, Category = ?
                      WHERE no = ?'''
        self.cursor.execute(self.sql, (self.edit_frame.edit_search_var.get(), self.edit_frame.edit_category_var.get(),
                                       self.rows[0]))
        self.conn.commit()
        self.conn.close()
        tmsg.showinfo("Success", "Id Saved!", parent=self.edit_frame.edit_root)
        self.edit_frame.edit_root.destroy()
        self.reset_id()

    def reset_id(self):
        self.id.small_manage_treeview.custom_treeview.delete(
            *self.id.small_manage_treeview.custom_treeview.get_children())
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM ID")
        self.rows = self.cursor.fetchall()
        count = 1
        for row in self.rows:
            if count % 2 != 0:
                self.id.small_manage_treeview.custom_treeview.insert('', END, values=(row[0], row[2], row[1]),
                                                                     tags=("oddrow",))

            else:
                self.id.small_manage_treeview.custom_treeview.insert('', END, values=(row[0], row[2], row[1]),
                                                                     tags=("evenrow",))
            count += 1


class Expenses_Window:
    def __init__(self, root):
        self.expense_root = root
        self.expense_dict = {
            "Sr No.": {
                "name": "Sr No.",
                "width": "275"
            },
            "Expense": {
                "name": "Expense",
                "width": "275"
            }
        }
        self.expense = Small_Manage_Window(self.expense_root, search_name="Expense",
                                           search_frame="Add Expense",
                                           save_function=self.save_expense, command_labels=["Edit", "Delete"],
                                           command_options=[self.edit_expense, self.delete_expense],
                                           columns=self.expense_dict,
                                           treeview_lbl="Existing Data", label_frame_name="Add Expense")
        self.reset_expense()
        self.expense.small_manage_treeview.custom_treeview.pack(fill=BOTH, expand=1)

    def delete_expense(self):
        self.cursor_row = self.expense.small_manage_treeview.custom_treeview.focus()
        self.contents = self.expense.small_manage_treeview.custom_treeview.item(self.cursor_row)['values']
        # Getting Details From Database
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("DELETE FROM EXPENSE where Espense = ?", (self.contents[1],))
        self.conn.commit()
        self.conn.close()
        self.reset_expense()

    def save_expense(self):
        self.ans = tmsg.askquestion("Are you Sure?",
                                    f"Are you sure to add '{self.expense.small_manage_search_txt.get()}'"
                                    , parent=self.expense.small_manage_root)
        if self.ans == "yes":
            self.conn = sqlite3.connect("DB\\Business.db")
            self.cursor = self.conn.cursor()
            sql = """SELECT * FROM EXPENSE WHERE Expense = ?"""
            self.cursor.execute(sql, (self.expense.small_manage_search_txt.get(),))
            rows = self.cursor.fetchone()

            print(rows)
            if rows is None:
                self.cursor.execute("insert into EXPENSE(Expense) VALUES(?)",
                                    (self.expense.small_manage_search_txt.get(),))
                tmsg.showinfo("Success", f"'{self.expense.small_manage_search_txt.get()}' Successfully Added!",
                              parent=self.expense.small_manage_root)
                self.conn.commit()
                self.conn.close()
                self.reset_expense()
            else:
                tmsg.showerror("Error", "Expense already exists",
                               parent=self.expense.small_manage_root)

    def edit_expense(self):
        self.cursor_row = self.expense.small_manage_treeview.custom_treeview.focus()
        self.contents = self.expense.small_manage_treeview.custom_treeview.item(self.cursor_row)['values']
        self.edit_window = tk.Toplevel(self.expense_root)
        self.edit_frame = Edit_Window(self.edit_window, search_name="Expense",
                                      save_function=self.update_expense, label_frame_name="Edit Expense")
        self.edit_frame.edit_search_var.set(self.contents[1])

    def update_expense(self):
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM EXPENSE WHERE Expense = ?", (self.contents[1],))
        self.rows = self.cursor.fetchone()
        self.sql = '''UPDATE EXPENSE
                      SET Expense = ?
                      WHERE id = ?'''
        self.cursor.execute(self.sql, (self.edit_frame.edit_search_var.get(), self.rows[0]))
        self.conn.commit()
        self.conn.close()
        tmsg.showinfo("Success", "Expense Saved!", parent=self.edit_frame.edit_root)
        self.edit_frame.edit_root.destroy()
        self.reset_expense()

    def reset_expense(self):
        self.expense.small_manage_treeview.custom_treeview.delete(
            *self.expense.small_manage_treeview.custom_treeview.get_children())
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM Expense")
        self.rows = self.cursor.fetchall()
        count = 1
        for row in self.rows:
            if count % 2 != 0:
                self.expense.small_manage_treeview.custom_treeview.insert('', END, values=(row[0], row[1]),
                                                                          tags=("oddrow",))

            else:
                self.expense.small_manage_treeview.custom_treeview.insert('', END, values=(row[0], row[1]),
                                                                          tags=("evenrow",))
            count += 1


class Manage_Items:
    def __init__(self, root):
        self.item_root = root
        self.items_dict = {
            "Sr No.": {
                "name": "Sr No.",
                "width": "175"
            },
            "Item Name": {
                "name": "Item Name",
                "width": "175"
            },
            "Item Rate": {
                "name": "Item Rate",
                "width": "175"
            },
            "Item Quantity": {
                "name": "Item Quantity",
                "width": "175"
            },
            "Sub-Category": {
                "name": "Sub-Category",
                "width": "175"
            },
            "Category": {
                "name": "Category",
                "width": "200"
            }
        }
        self.manage = ManageWindow(self.item_root, search_frame="Items", search_name="Item Name",
                                   search_function=self.search_items,
                                   reset_function=self.reset_items,
                                   command_options=[self.edit_items, self.delete_items],
                                   command_labels=["View/ Edit/ Modify", "Delete"], columns=self.items_dict,
                                   )
        self.reset_items()

    def search_items(self):
        if self.manage.client_search_txt.get() == "":
            tmsg.showerror("Error", "Please Enter Item Name", parent=self.manage.manage_root)
        else:
            self.conn = sqlite3.connect('DB\\Items.db')
            self.cursor = self.conn.cursor()

            sqlite_update_query = """SELECT * from ITEMS where Item_Name = ?"""

            self.cursor.execute(sqlite_update_query, (self.manage.client_search_txt.get(),))
            self.rows = self.cursor.fetchall()
            if self.rows != []:
                count = 1
                for id, Category, Sub_Category, Item_Code, Item_Name, Item_Rate, Item_Qty in self.rows:
                    if count % 2 == 0:
                        self.manage.manage_treeview.custom_treeview.insert('', END,
                                                                           values=(
                                                                               count, Item_Name, Item_Rate, Item_Qty,
                                                                               Sub_Category, Category),
                                                                           tags=('evenrow',))
                        count += 1
                    else:
                        self.manage.manage_treeview.custom_treeview.insert('', END,
                                                                           values=(
                                                                               count, Item_Name, Item_Rate, Item_Qty,
                                                                               Sub_Category, Category),
                                                                           tags=('oddrow',))
                        count += 1
            else:
                tmsg.showerror("Error", "Item Not Found. \nPlease Check The Name!",
                               parent=self.manage.manage_root)

    def reset_items(self):
        self.conn = sqlite3.connect('DB\\Items.db')
        self.cursor = self.conn.cursor()
        self.manage.manage_treeview.custom_treeview.delete(
            *self.manage.manage_treeview.custom_treeview.get_children())
        self.cursor.execute("SELECT * FROM ITEMS")
        self.rows = self.cursor.fetchall()
        count = 1
        if self.rows != [] or None:
            for id, Category, Sub_Category, Item_Code, Item_Name, Item_Rate, Item_Qty in self.rows:
                if count % 2 == 0:
                    self.manage.manage_treeview.custom_treeview.insert('', END,
                                                                       values=(
                                                                           count, Item_Name, Item_Rate, Item_Qty,
                                                                           Sub_Category, Category),
                                                                       tags=('evenrow',))
                    count += 1
                else:
                    self.manage.manage_treeview.custom_treeview.insert('', END,
                                                                       values=(
                                                                           count, Item_Name, Item_Rate, Item_Qty,
                                                                           Sub_Category, Category),
                                                                       tags=('oddrow',))
                    count += 1
        else:
            ans = tmsg.askquestion("Please Add Item", "No Items Found! \n\n Would You Like To Add Items Now?",
                                   icon="error", master=self.item_root)
            if ans == "yes":
                employee_root = tk.Toplevel(self.item_root)
                employee = Add_Item_Window(employee_root)
            else:
                self.manage.manage_root.destroy()
        self.conn.commit()
        self.conn.close()

    def edit_items(self):
        cursor_row = self.manage.manage_treeview.custom_treeview.focus()
        contents = self.manage.manage_treeview.custom_treeview.item(cursor_row)['values']
        # Getting Details From Database
        conn = sqlite3.connect("DB\\Items.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ITEMS where Item_Name = ?", (contents[1],))
        rows = cursor.fetchone()
        if rows is not None or []:
            items_root = tk.Toplevel(self.item_root)
            item = Add_Item_Window(items_root)
            item.category_txt.set(rows[1])
            item.sub_category_txt.set(rows[2])
            item.item_code_var.set(rows[3])
            item.item_name_var.set(rows[4])
            item.item_rate_var.set(rows[5])
            item.item_qty_var.set(rows[6])

            def update_items():
                if item.item_rate_var.get() == "" or item.item_name_var.get() == "" or item.category_txt.get() == "" \
                        or item.category_txt.get() == "Select":

                    tmsg.showerror("Error", "Please Fill All Required Details", parent=item.add_item_window)
                else:
                    item.ans = tmsg.askquestion("Are you Sure?",
                                                f"Are you sure to You want ot Update Item '{item.item_name_var.get()}' "
                                                , parent=item.add_item_window)
                    if item.ans == 'yes':
                        item.conn = sqlite3.connect('DB\\Items.db')
                        item.cursor = item.conn.cursor()

                        item.cursor.execute(
                            """UPDATE ITEMS
                            SET Category = ?,Sub_Category = ?,Item_Code = ?,
                            Item_Name = ?,Item_Rate = ?,Item_Qty = ?
                            WHERE Item_Name = ?""",
                            (
                                item.category_txt.get(),
                                item.sub_category_txt.get(),
                                item.item_code_var.set(rows[3]),
                                item.item_name_var.set(rows[4]),
                                item.item_rate_var.set(rows[5]),
                                item.item_qty_var.set(rows[6]),
                                item.item_name_var.set(rows[4]),
                            ))
                        item.conn.commit()
                        item.conn.close()
                        tmsg.showinfo("Success",
                                      f"Employee '{item.item_name_var.get()} Updated.'",
                                      master=item.add_item_window)
                        item.add_item_window.destroy()
                        self.reset_items()

            item.save_btn["text"] = "Update"
            item.save_btn["command"] = update_items
        else:
            tmsg.showerror("Error", "There was A Problem Opening Items Window!", master=self.manage.manage_root)
            self.reset_items()
        conn.commit()
        conn.close()

    def delete_items(self):
        cursor_row = self.manage.manage_treeview.custom_treeview.focus()
        contents = self.manage.manage_treeview.custom_treeview.item(cursor_row)['values']
        # Getting Details From Database
        conn = sqlite3.connect("DB\\Items.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ITEMS where Item_Name = ?", (contents[1],))
        conn.commit()
        conn.close()
        self.reset_items()


class Add_Item_Window:
    def __init__(self, root):
        # Variables
        self.item_code_var = tk.StringVar()
        self.item_name_var = tk.StringVar()
        self.item_qty_var = tk.StringVar()
        self.item_rate_var = tk.StringVar()
        self.add_item_window = root
        self.add_item_window.title("Add Item")
        self.add_item_window.geometry("1152x200+50+150")
        self.add_item_window.attributes('-toolwindow', 1)
        self.add_item_window.attributes('-topmost', 1)
        self.add_item_window.focus_set()
        self.category_lbl = tk.Label(self.add_item_window, text="Category *", font=("Calibri", 12))
        self.category_lbl.place(relx=0.01, rely=0.1)
        self.category_txt = Combobox(self.add_item_window, font=("Calibri", 12), values=["Select"])
        self.category_txt.place(relx=0.1, rely=0.1, relwidth=0.15)
        self.category_txt.current(0)
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM CATEGORY")
        self.rows = self.cursor.fetchall()
        self.values = ["Select"]
        for id, category in self.rows:
            self.values.append(category)

        self.category_txt['values'] = self.values

        self.sub_category_lbl = tk.Label(self.add_item_window, text="Sub-Category", font=("Calibri", 12))
        self.sub_category_lbl.place(relx=0.28, rely=0.1)
        self.sub_category_txt = Combobox(self.add_item_window, font=("Calibri", 12), values=["Select"])
        self.sub_category_txt.place(relx=0.37, rely=0.1, relwidth=0.15)
        self.sub_category_txt.current(0)

        self.item_code_lbl = tk.Label(self.add_item_window, text="Item Code", font=("Calibri", 12))
        self.item_code_lbl.place(relx=0.01, rely=0.3)
        self.item_code_txt = Entry(self.add_item_window, font=("Calibri", 12), textvariable=self.item_code_var)
        self.item_code_txt.place(relx=0.1, rely=0.3, relwidth=0.15)

        self.item_name_lbl = tk.Label(self.add_item_window, text="Item Name *", font=("Calibri", 12))
        self.item_name_lbl.place(relx=0.28, rely=0.3)
        self.item_name_txt = Entry(self.add_item_window, font=("Calibri", 12), textvariable=self.item_name_var)
        self.item_name_txt.place(relx=0.37, rely=0.3, relwidth=0.15)

        self.item_qty_lbl = tk.Label(self.add_item_window, text="Item Quantity", font=("Calibri", 12))
        self.item_qty_lbl.place(relx=0.01, rely=0.5)
        self.item_qty_txt = Entry(self.add_item_window, font=("Calibri", 12), textvariable=self.item_qty_var)
        self.item_qty_txt.place(relx=0.1, rely=0.5, relwidth=0.15)

        self.item_rate_lbl = tk.Label(self.add_item_window, text="Item Rate *", font=("Calibri", 12))
        self.item_rate_lbl.place(relx=0.28, rely=0.5)
        self.item_rate_txt = Entry(self.add_item_window, font=("Calibri", 12), textvariable=self.item_rate_var)
        self.item_rate_txt.place(relx=0.37, rely=0.5, relwidth=0.15)

        self.save_btn = Button(self.add_item_window, text="Save", style="C.TButton", command=self.save_item)
        self.save_btn.place(relx=0.87, rely=0.7)

    def save_item(self):
        if self.category_txt.get() == "Select" or self.item_name_txt.get() == "" or self.item_rate_txt.get() == "":
            tmsg.showerror("Error", "Please Fill All Required Fields.", parent=self.add_item_window)
        else:
            ans = tmsg.askquestion("Are You Sure?", f"Are You Sure To Add '{self.item_name_txt.get()}'",
                                   parent=self.add_item_window)
            if ans == "yes":
                self.conn = sqlite3.connect("DB\\Items.db")
                self.cursor = self.conn.cursor()
                sql = """CREATE TABLE IF NOT EXISTS ITEMS(
                                   id  INTEGER PRIMARY KEY autoincrement,
                                   Category VARCHAR(50) NOT NULL,
                                   Sub_Category VARCHAR(50) NOT NULL,
                                   Item_Code VARCHAR(500) NOT NULL,
                                   Item_Name VARCHAR(500) NOT NULL,
                                   Item_Rate INTEGER NOT NULL,
                                   Item_Qty INTEGER NOT NULL)"""
                self.cursor.execute(sql)

                sql1 = """INSERT INTO ITEMS(Category,Sub_Category,Item_Code,Item_Name,Item_Rate,Item_Qty) VALUES(?,?,?,?,
                ?,?) """

                self.cursor.execute(sql1, (self.category_txt.get(),
                                           self.sub_category_txt.get(),
                                           self.item_code_txt.get(),
                                           self.item_name_txt.get(),
                                           self.item_rate_txt.get(),
                                           self.item_qty_txt.get()))
                self.conn.commit()
                self.conn.close()
                tmsg.showinfo("Success", f"Item '{self.item_name_txt.get()}' Successfully Added To Database.",
                              parent=self.add_item_window)
                self.add_item_window.destroy()


class Add_Expense_Window:
    def __init__(self, root):
        # Variables
        self.paid_to_var = tk.StringVar()
        self.payment_ref_var = tk.StringVar()
        self.paid_by_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.add_expense_window = root
        self.add_expense_window.title("Add Expense")
        self.add_expense_window.geometry("700x350+200+150")
        self.add_expense_window.attributes('-toolwindow', 1)
        self.add_expense_window.attributes('-topmost', 1)
        self.add_expense_window.focus_set()

        self.expense_frame = tk.LabelFrame(self.add_expense_window, text="Expense Details")
        self.expense_frame.place(relx=0.05, rely=0.05, relwidth=0.90, relheight=0.8)
        self.date_lbl = tk.Label(self.expense_frame, text="Date", font=("Calibri", 10))
        self.date_lbl.place(relx=0.05, rely=0.05)
        # self.category_lbl.required_str.place(relx=0.01, rely=0.1)
        self.date_txt = DateEntry(self.expense_frame, font=("Calibri", 12), date_pattern="dd-mm-yy")
        self.date_txt.place(relx=0.2, rely=0.05, relwidth=0.25)
        self.date_txt.set_date(self.date_txt.get_date())

        self.category_lbl = Required_Text(self.expense_frame, required_text="Expense Type   ")
        # self.category_lbl.style.configure("Required.TLabel", background="SystemButtonFace", font=("Calibri", 12))
        self.category_lbl.required_lbl.place(relx=0.05, rely=0.25)
        self.category_lbl.required_frame.place(relx=0.05, rely=0.25)
        # self.category_lbl.required_str.place(relx=0.01, rely=0.1)
        self.category_txt = Combobox(self.expense_frame, font=("Calibri", 12), values=self.reset_category())
        self.category_txt.place(relx=0.2, rely=0.25, relwidth=0.25)
        self.category_txt.bind("<<ComboboxSelected>>", self.check_category_event)
        self.category_txt.bind("<FocusOut>", self.check_category_event)

        self.amount_lbl = Required_Text(self.expense_frame, required_text="Amount   ")
        self.amount_lbl.required_lbl.place(relx=0.05, rely=0.45)
        self.amount_lbl.required_frame.place(relx=0.05, rely=0.45)
        # self.amount_lbl.style.configure("Required.TLabel", background="SystemButtonFace", font=("Calibri", 12))
        self.amount_txt = Entry(self.expense_frame, font=("Calibri", 12), textvariable=self.amount_var)
        self.amount_txt.place(relx=0.2, rely=0.45, relwidth=0.25)

        self.paid_to_lbl = Required_Text(self.expense_frame, required_text="Paid To   ")
        self.paid_to_lbl.required_lbl.place(relx=0.05, rely=0.65)
        self.paid_to_lbl.required_frame.place(relx=0.05, rely=0.65)
        # self.paid_to_lbl.style.configure("Required.TLabel", background="SystemButtonFace", font=("Calibri", 12))
        self.paid_to_txt = Entry(self.expense_frame, font=("Calibri", 12), textvariable=self.paid_to_var)
        self.paid_to_txt.place(relx=0.2, rely=0.65, relwidth=0.25)

        self.pay_mode_lbl = Required_Text(self.expense_frame, required_text="Pay Mode   ")
        self.pay_mode_lbl.required_lbl.place(relx=0.05, rely=0.85)
        self.pay_mode_lbl.required_frame.place(relx=0.05, rely=0.85)
        # self.pay_mode_lbl.style.configure("Required.TLabel", background="SystemButtonFace", font=("Calibri", 12))

        self.pay_mode_list = ["Select", "Cash", "Voucher", "Cheque", "Demand Draft", "Mobile Wallet", "Bank Transfer"]

        self.pay_mode_txt = Combobox(self.expense_frame, font=("Calibri", 12), values=self.pay_mode_list,
                                     state='readonly')
        self.pay_mode_txt.place(relx=0.2, rely=0.85, relwidth=0.25)
        self.pay_mode_txt.bind("<<ComboboxSelected>>", self.check_mode_event)

        self.payment_ref_lbl = tk.Label(self.expense_frame, text="Payment Ref No.", font=("Calibri", 10))
        self.payment_ref_lbl.place(relx=0.5, rely=0.05)
        self.payment_ref_txt = Entry(self.expense_frame, font=("Calibri", 12), textvariable=self.payment_ref_var,
                                     state=DISABLED)
        self.payment_ref_txt.place(relx=0.7, rely=0.05, relwidth=0.25)

        self.paid_by_lbl = Required_Text(self.expense_frame, required_text="Paid By   ")
        self.paid_by_lbl.required_lbl.place(relx=0.5, rely=0.25)
        self.paid_by_lbl.required_frame.place(relx=0.5, rely=0.25)
        # self.paid_by_lbl.style.configure("Required.TLabel", background="SystemButtonFace", font=("Calibri", 12))
        self.paid_by_txt = Entry(self.expense_frame, font=("Calibri", 12), textvariable=self.paid_by_var)
        self.paid_by_txt.place(relx=0.7, rely=0.25, relwidth=0.25)

        self.remarks_lbl = tk.Label(self.expense_frame, text="Remarks", font=("Calibri", 10))
        self.remarks_lbl.place(relx=0.5, rely=0.45)
        self.remarks_txt = scrolledtext.ScrolledText(self.expense_frame, font=("Calibri", 12))
        self.remarks_txt.place(relx=0.7, rely=0.45, relwidth=0.25, relheight=0.5)

        self.save_btn = Button(self.add_expense_window, text="Save", style="C.TButton", command=self.save_expense)
        self.save_btn.place(relx=0.87, rely=0.87)

    def check_category(self):
        if self.category_txt.get() != "":
            self.conn = sqlite3.connect("DB\\Business.db")
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT * FROM EXPENSE where Expense = ?", (self.category_txt.get(),))
            self.rows = self.cursor.fetchone()
            if self.rows != None:
                return
            else:
                self.ans = tmsg.askquestion("User Confirmation",
                                            f"{self.category_txt.get()} is not Added To Database. \n\nWould You Like To Add {self.category_txt.get()} To Database?",
                                            parent=self.add_expense_window)
                if self.ans == "yes":
                    self.cursor.execute("INSERT INTO EXPENSE(Expense) VALUES(?)", (self.category_txt.get(),))
                    self.conn.commit()
                    self.conn.close()
                    self.category_txt['values'] = self.reset_category()
        else:
            return

    def check_category_event(self, event):
        self.check_category()

    def reset_category(self):
        self.category_list = []
        self.conn = sqlite3.connect("DB\\Business.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM EXPENSE")
        self.rows = self.cursor.fetchall()
        for row in self.rows:
            self.category_list.append(row[1])
        return self.category_list

    def check_mode(self):
        if self.pay_mode_txt.get() == "Select" or self.pay_mode_txt.get() == "Cash":
            self.payment_ref_txt['state'] = "disabled"
            self.payment_ref_var.set("")
        else:
            self.payment_ref_var.set("")
            self.payment_ref_txt['state'] = "enabled"

    def check_mode_event(self, event):
        self.check_mode()

    def save_expense(self):
        if self.category_txt.get() == "" or self.amount_txt.get() == "" or self.paid_to_txt.get() == "" or self.pay_mode_txt.get() == "Select" or self.paid_by_txt.get() == "":
            tmsg.showerror("Error", "Please Fill All Required Fields.", parent=self.add_expense_window)
        else:
            ans = tmsg.askquestion("Are You Sure?", f"Are You Sure To Add '{self.category_txt.get()}'",
                                   parent=self.add_expense_window)
            if ans == "yes":
                self.conn = sqlite3.connect("DB\\Expenses.db")
                self.cursor = self.conn.cursor()
                # self.cursor.execute("DROP TABLE EXPENSES")
                sql = '''CREATE TABLE IF NOT EXISTS EXPENSES(
                                   id  INTEGER PRIMARY KEY autoincrement,
                                   Expense_Type VARCHAR(50) NOT NULL,
                                   Amount INTEGER NOT NULL,
                                   Paid_To VARCHAR(500) NOT NULL,
                                   Payment_Mode VARCHAR(500) NOT NULL,
                                   Payment_Ref VARCHAR(500) NOT NULL,
                                   Paid_By VARCHAR(500) NOT NULL,
                                   Date DATE NOT NULL,
                                   Remarks VARCHAR(500) NOT NULL)'''
                self.cursor.execute(sql)
                sql1 = """INSERT INTO EXPENSES(Expense_Type,Amount,Paid_To,Payment_Mode,Payment_Ref,Paid_By,Date,
                Remarks) VALUES(?,?,?,?,?,?,?,?) """
                self.cursor.execute(sql1, (self.category_txt.get(),
                                           self.amount_txt.get(),
                                           self.paid_to_txt.get(),
                                           self.pay_mode_txt.get(),
                                           self.payment_ref_txt.get(),
                                           self.paid_by_txt.get(),
                                           self.date_txt.get_date(),
                                           self.remarks_txt.get("1.0", END),
                                           ))
                self.conn.commit()
                self.conn.close()
                tmsg.showinfo("Success", f"Item '{self.category_txt.get()}' Successfully Added To Database.",
                              parent=self.add_expense_window)
                self.add_expense_window.destroy()


class Techware_Start_Window:
    def __init__(self, root):
        self.start_root = root
        self.start_root.geometry("751x470+299+109")
        self.start_root.attributes('-toolwindow', 1)
        self.start_root.attributes('-topmost', 1)
        self.start_root.focus_force()
        self.start_root.resizable(0, 0)
        # self.start_root.config(background="#FFFFFF")
        self.start_root.title("Techware BillSoft 1.0")
        self.style = Style(self.start_root)
        self.style.configure("Start.TLabel", foreground="#a8a894", background="white",
                             font=("Helvetica", 15))

        self.style.configure("Start2.TLabel", foreground="#000000", background="SystemButtonFace",
                             font=("Calibri", 10))

        self.style.configure("Start.TRadiobutton", foreground="black", background="SystemButtonFace",
                             font=("Calibri", 12))

        self.style.configure("Start.TLabelframe", borderwidth=3, relief=GROOVE)
        self.style.configure("Start.TFrame", background="white")
        self.style.configure("Start1.TFrame", background="darkgrey")
        self.header_frame = Frame(self.start_root, style="Start.TFrame")
        self.header_title = Label(self.header_frame, text="Let's Simplify Your Business", style="Start.TLabel")
        self.header_title.place(relx=0.62, rely=0.35)
        self.web_link = Link_Text(self.header_frame, link_text="https://www.spyderwebtech.com/techware",
                                  link_function=lambda e: self.web_link.style.configure("S.TLabel", foreground="#FFee00"))
        self.web_link.link_lbl.place(relx=0.65, rely=0.65)
        self.header_frame.place(relx=0, rely=0, relwidth=1, relheight=0.21)

        self.select_version_frame = Labelframe(self.start_root, text="Select Version", style="Start.TLabelframe")
        self.select_version_frame.place(relx=0.025, rely=0.2205, relwidth=0.9525, relheight=0.56)
        self.select_version_var = tk.StringVar()
        self.select_version_free = Radiobutton(self.select_version_frame, text="Free Limited Version",
                                               style="Start.TRadiobutton", value="free",
                                               variable=self.select_version_var)
        self.select_version_free.place(relx=0.15, rely=0.2205)

        self.select_version_free.line_1 = Label()

        self.link_version_frame = Frame(self.start_root, style="Start1.TFrame")
        self.link_version_frame.place(relx=0.025, rely=0.7805, relwidth=0.9525, relheight=0.05)


class Manage_Expenses:
    def __init__(self, root):
        self.expense_dict = {
            "Sr No.": {
                "name": "Sr No.",
                "width": "100"
            },
            "Date": {
                "name": "Date",
                "width": "150"
            },
            "Type": {
                "name": "Type",
                "width": "200"
            },
            "Amount": {
                "name": "Amount",
                "width": "150"
            },
            "Paid To": {
                "name": "Paid To",
                "width": "250"
            },
            "Remarks": {
                "name": "Remarks",
                "width": "300"
            },
            "Pay Mode": {
                "name": "Pay Mode",
                "width": "150"
            },
            "Payment Ref. No.": {
                "name": "Payment Ref. No.",
                "width": "200"
            },
            "Paid By": {
                "name": "Paid By",
                "width": "250"
            },
        }

        self.expense = ManageWindow(root, search_frame="Expenses", search_name="Expense Name",
                                    search_function=self.search_expense,
                                    reset_function=self.reset_expense,
                                    command_options=[self.edit_expense, self.delete_expense],
                                    command_labels=["View/ Edit/ Modify", "Delete"], columns=self.expense_dict,
                                    )
        self.reset_expense()

    def search_expense(self):
        if self.expense.client_search_txt.get() == "":
            tmsg.showerror("Error", "Please Enter Expense Name", parent=self.expense.manage_root)
        else:
            conn = sqlite3.connect('DB\\Expenses.db')
            cursor = conn.cursor()

            sqlite_update_query = """SELECT * from EXPENSES where Expense_Type = ?"""

            cursor.execute(sqlite_update_query, (self.expense.client_search_txt.get(),))
            rows = cursor.fetchall()
            if rows != []:
                print(rows)
                count = 1
                for id, Expense_Type, Amount, Paid_To, Payment_Mode, Payment_Ref, Paid_By, Date, Remarks in rows:
                    if count % 2 == 0:
                        self.expense.manage_treeview.custom_treeview.insert('', END,
                                                                            values=(
                                                                                count, Date, Expense_Type, Amount,
                                                                                Paid_To,
                                                                                Remarks, Payment_Mode, Payment_Ref,
                                                                                Paid_By),
                                                                            tags=('evenrow',))
                        count += 1
                    else:
                        self.expense.manage_treeview.custom_treeview.insert('', END,
                                                                            values=(
                                                                                count, Date, Expense_Type, Amount,
                                                                                Paid_To,
                                                                                Remarks, Payment_Mode, Payment_Ref,
                                                                                Paid_By),
                                                                            tags=('oddrow',))
                        count += 1
            else:
                tmsg.showerror("Error", "Expense Not Found. \nPlease Check The Name!", parent=self.expense.manage_root)
                self.reset_expense()

    def reset_expense(self):
        conn = sqlite3.connect('DB\\Expenses.db')
        cursor = conn.cursor()
        self.expense.manage_treeview.custom_treeview.delete(
            *self.expense.manage_treeview.custom_treeview.get_children())
        cursor.execute("SELECT * FROM EXPENSES")
        rows = cursor.fetchall()
        count = 1
        print(rows)
        if rows != []:
            for id, Expense_Type, Amount, Paid_To, Payment_Mode, Payment_Ref, Paid_By, Date, Remarks in rows:
                if count % 2 == 0:
                    self.expense.manage_treeview.custom_treeview.insert('', END,
                                                                        values=(
                                                                            count, Date, Expense_Type, Amount,
                                                                            Paid_To,
                                                                            Remarks, Payment_Mode, Payment_Ref,
                                                                            Paid_By),
                                                                        tags=('evenrow',))
                    count += 1
                else:
                    self.expense.manage_treeview.custom_treeview.insert('', END,
                                                                        values=(
                                                                            count, Date, Expense_Type, Amount,
                                                                            Paid_To,
                                                                            Remarks, Payment_Mode, Payment_Ref,
                                                                            Paid_By),
                                                                        tags=('oddrow',))
                    count += 1
        else:
            ans = tmsg.askquestion("Please Add Expense",
                                   "No Expenses Found! \n\n Would You Like To Add Expenses Now?",
                                   icon="error", master=self.expense.manage_root)
            if ans == "yes":
                expense_root = tk.Toplevel(self.expense.manage_root)
                exp = Add_Expense_Window(expense_root)
            else:
                self.expense.manage_root.destroy()
        conn.commit()
        conn.close()

    def edit_expense(self):
        cursor_row = self.expense.manage_treeview.custom_treeview.focus()
        contents = self.expense.manage_treeview.custom_treeview.item(cursor_row)['values']
        # Getting Details From Database
        conn = sqlite3.connect("DB\\Expenses.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM EXPENSES where Expense_Type = ?", (contents[1],))
        rows = cursor.fetchone()
        if rows is not None or []:
            expense_root = tk.Toplevel(self.expense.manage_root)
            exp = Add_Expense_Window(expense_root)
            exp.category_txt.set(rows[1])
            exp.amount_var.set(rows[2])
            exp.paid_to_var.set(rows[3])
            exp.pay_mode_txt.set(rows[4])
            exp.payment_ref_var.set(rows[5])
            exp.paid_by_var.set(rows[6])
            exp.date_txt.set_date(rows[7])
            exp.remarks_txt.insert(INSERT, rows[8])

            def update_expense():
                if exp.category_txt.get() == "" or exp.amount_txt.get() == "" or exp.paid_to_txt.get() == "" or exp.pay_mode_txt.get() == "Select" or exp.paid_by_txt.get() == "":
                    tmsg.showerror("Error", "Please Fill All Required Details", parent=exp.add_expense_window)
                else:
                    exp.ans = tmsg.askquestion("Are you Sure?",
                                               f"Are you sure to You want ot Update Employee '{exp.category_txt.get()}' "
                                               , parent=exp.add_expense_window)
                    if exp.ans == 'yes':
                        exp.conn = sqlite3.connect('DB\\Clients.db')
                        exp.cursor = exp.conn.cursor()

                        exp.cursor.execute(
                            """UPDATE CLIENT
                            SET 
                            Expense_Type = ?,Amount = ?,Paid_To = ?,
                            Payment_Mode = ?,Payment_Ref = ?,Paid_By = ?,
                            Date = ?,Remarks = ?
                            WHERE 
                            Expense_Type = ?""",
                            (
                                exp.category_txt.get(),
                                exp.amount_var.get(),
                                exp.paid_to_var.get(),
                                exp.pay_mode_txt.get(),
                                exp.payment_ref_var.get(),
                                exp.paid_by_var.get(),
                                exp.date_txt.get_date(),
                                exp.remarks_txt.get('1.0', END),
                                exp.category_txt.get(),
                            ))
                        exp.conn.commit()
                        exp.conn.close()
                        tmsg.showinfo("Success",
                                      f"Expense '{exp.category_txt.get()} Updated.'",
                                      master=exp.add_expense_window)
                        exp.add_expense_window.destroy()
                        self.reset_expense()

            exp.save_btn["text"] = "Update"
            exp.save_btn["command"] = update_expense
        else:
            tmsg.showerror("Error", "There was A Problem Opening Staff Window!", master=self.expense.manage_root)
            self.reset_expense()
        conn.commit()
        conn.close()

    def delete_expense(self):
        cursor_row = self.expense.manage_treeview.custom_treeview.focus()
        contents = self.expense.manage_treeview.custom_treeview.item(cursor_row)['values']
        # Getting Details From Database
        conn = sqlite3.connect("DB\\Expenses.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM EXPENSES where Expense_Type = ?", (contents[1],))
        conn.commit()
        conn.close()
        self.reset_expense()


root = tk.Tk()
obj = Techware_Start_Window(root)
root.mainloop()
