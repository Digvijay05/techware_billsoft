import sqlite3
from tkinter import *
import tkinter.ttk as ttk
import pymysql
import tkinter.messagebox as tmsg


class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Window")
        self.root.geometry("1350x700+0+0")
        self.root['bg'] = "white"
        # ==========Bg Image==========

        self.bg_img = PhotoImage(file="Images\\Background.png")
        self.bg = Label(self.root, image=self.bg_img)
        self.bg.place(x=250, y=0, relwidth=1, relheight=1)

        # ===========Left Image==========
        self.left_Image = PhotoImage(file="Images\\Side Image.png")
        self.leftImage = Label(self.root, image=self.left_Image)
        self.leftImage.place(x=80, y=100, width=400, height=500)

        # ===========Register Frame======
        self.frame1 = Frame(self.root, bg="#00bfff")
        self.frame1.place(x=480, y=100, width=700, height=500)

        self.title = Label(self.frame1, text="REGISTER HERE", bg="#00bfff", font=("times new roman", 20, "bold"),
                           fg="white")
        self.title.place(x=50, y=30)

        # ----------------------------------------Row2
        self.f_name = Label(self.frame1, text="First Name", bg="#00bfff", font=("times new roman", 15, "bold"),
                            fg="black")
        self.f_name.place(x=50, y=100)
        self.txt_fname = Entry(self.frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_fname.place(x=50, y=130, width=250)

        self.l_name = Label(self.frame1, text="Last Name", bg="#00bfff", font=("times new roman", 15, "bold"),
                            fg="black").place(
            x=370, y=100)
        self.txt_lname = Entry(self.frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_lname.place(x=370, y=130, width=250)
        # ----------------------------------------Row2
        self.contact = Label(self.frame1, text="Contact No.", bg="#00bfff", font=("times new roman", 15, "bold"),
                             fg="black").place(
            x=50, y=170)
        self.txt_contact = Entry(self.frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_contact.place(x=50, y=200, width=250)

        self.emp_code = Label(self.frame1, text="Employee Code", bg="#00bfff", font=("times new roman", 15, "bold"),
                              fg="black").place(x=370, y=170)
        self.txt_emp = Entry(self.frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_emp.place(x=370, y=200, width=250)

        # ----------------------------------------Row3
        self.dob = Label(self.frame1, text="Date of Birth YYYY-MM-DD", bg="#00bfff",
                         font=("times new roman", 15, "bold"),
                         fg="black") \
            .place(x=50, y=270)
        self.txt_dob = Entry(self.frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_dob.place(x=50, y=300, width=250)

        Password = Label(self.frame1, text="Password", bg="#00bfff", font=("times new roman", 15, "bold"), fg="black") \
            .place(x=370, y=270)
        self.txt_pass = Entry(self.frame1, font=("times new roman", 15), bg="lightgray", show="*")
        self.txt_pass.place(x=370, y=300, width=250)

        # ----------------------------------------Terms
        self.var_chk = IntVar()
        self.chk = Checkbutton(self.frame1, text="I Agree To The Terms & Conditions", variable=self.var_chk,
                               bg="#00bfff", fg="black",
                               onvalue=1, offvalue=0,

                               font=("times new roman", 12, "bold"))
        self.chk.place(x=50, y=330)

        self.reg_btn = Button(self.frame1, text="Register", command=self.register_btn, bd=0, cursor="hand2",
                              font=("times new roman", 20),
                              bg="lightgreen")
        self.reg_btn.place(relx=0.5, y=400, anchor="center", width=180, height=50)

        self.btn_login = Button(self.root, text="Sign In", font=("times new roman", 20), bd=0, cursor="hand2",
                                bg="lightblue", fg="darkblue")
        self.btn_login.place(x=190, y=480, width=180)

    def clear(self):
        self.txt_fname.delete(0, END)
        self.txt_lname.delete(0, END)
        self.txt_contact.delete(0, END)
        self.txt_pass.delete(0, END)
        self.txt_dob.delete(0, END)
        self.txt_emp.delete(0, END)

    def register_btn(self):
        if self.txt_fname.get() == "" or self.txt_contact.get() == "" or self.txt_emp == "" or self.txt_lname.get() == "" or self.txt_dob.get() == "" or self.txt_pass.get() == "":
            tmsg.showerror("Error", "All Fields Are Required", parent=self.root)
        elif self.var_chk.get() == 0:
            tmsg.showerror("Error", "Please Agree to Our Terms & Conditions", parent=self.root)
        else:
            try:
                conn = sqlite3.connect("DB\\users.db")
                cursor = conn.cursor()

                sql = '''CREATE TABLE IF NOT EXISTS USERS(
                   id INTEGER PRIMARY KEY autoincrement,
                   f_name VARCHAR(50) NOT NULL,
                   l_name VARCHAR(50) NOT NULL,
                   contact VARCHAR(10) NOT NULL,
                   emp_code VARCHAR(4) NOT NULL,
                   dob DATE NOT NULL,
                   pass VARCHAR(50) NOT NULL
                )'''
                cursor.execute(sql)
                cursor.execute("select * from USERS where emp_code=?", self.txt_emp.get())
                row = cursor.fetchone()
                print(row)
                if row != None:
                    tmsg.showerror("Error", "User Already Exists, Please Click Login")
                else:
                    cursor.execute(
                        "insert into users(f_name,l_name,contact,emp_code,dob,pass) values(?,?,?,?,?,?)",
                        (
                            self.txt_fname.get(),
                            self.txt_lname.get(),
                            self.txt_contact.get(),
                            self.txt_emp.get(),
                            self.txt_dob.get(),
                            self.txt_pass.get()
                        ))
                    conn.commit()
                    conn.close()
                    tmsg.showinfo("Success", "Registration Successful", parent=self.root)
                    self.clear()
            except Exception as es:
                tmsg.showerror("Error", f"Error due to: {str(es)}", parent=self.root)


root = Tk()
obj = Register(root)
root.mainloop()
