from tkinter import *
from tkinter import ttk


class Placeholder_State(object):
    __slots__ = 'normal_color', 'normal_font', 'placeholder_text', 'placeholder_color', 'placeholder_font', 'with_placeholder'


def add_placeholder_to(entry, placeholder, color="grey", font=None, show=None):
    normal_color = entry.cget("foreground")
    normal_font = entry.cget("font")

    if font is None:
        font = normal_font

    state = Placeholder_State()
    state.normal_color = normal_color
    state.normal_font = normal_font
    state.placeholder_color = color
    state.placeholder_font = font
    state.placeholder_text = placeholder
    state.with_placeholder = True

    def on_focusin(event, entry=entry, state=state):
        if state.with_placeholder:
            entry.delete(0, "end")
            entry.config(foreground=state.normal_color, font=state.normal_font)

            state.with_placeholder = False

    def on_focusout(event, entry=entry, state=state):
        if entry.get() == '':
            entry.insert(0, state.placeholder_text)
            entry.config(foreground=state.placeholder_color, font=state.placeholder_font)

            state.with_placeholder = True

    entry.insert(0, placeholder)
    entry.config(foreground=color, font=font)

    entry.bind('<FocusIn>', on_focusin, add="+")
    entry.bind('<FocusOut>', on_focusout, add="+")

    entry.placeholder_state = state

    return state


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Window")
        self.root.geometry("1350x700+0+0")
        self.root['bg'] = "white"
        self.bg_image = PhotoImage(file="Images\\Background.png")
        self.background_label = Label(self.root, image=self.bg_image)
        self.background_label.pack(fill=BOTH, expand=True)

        self.login_frame = Frame(self.root, bg="white")
        self.login_frame.place(in_=self.background_label, relx=0.5, rely=0.5, relwidth=0.3, relheight=0.55,
                               anchor=CENTER)

        self.login_title_image = PhotoImage(file="Login Title.png")
        self.login_title = Label(self.login_frame, image=self.login_title_image, bg="white", fg="black")
        # login_title.configure(font=("Montserrat Bold", 25, "bold"))
        self.login_title.place(anchor=CENTER, relx=0.5, rely=0.05)

        self.username_var = StringVar()
        self.login_username = ttk.Entry(self.login_frame, font=("arial 12", 15), textvariable=self.username_var,
                                        width=25)
        self.login_username.place(anchor=CENTER, relx=0.5, rely=0.3)
        add_placeholder_to(self.login_username, 'Enter your Employee Code...')

        self.password_var = StringVar()
        self.login_password = ttk.Entry(self.login_frame, font=("arial 12", 15), textvariable=self.password_var,
                                        width=25)
        self.login_password.place(anchor=CENTER, relx=0.5, rely=0.45)
        add_placeholder_to(self.login_password, 'Enter your Password...')

        self.login_btn = Button(self.login_frame, text="Log In", font=("times new roman", 12), bg="green")
        self.login_btn.place(anchor=CENTER, relx=0.5, rely=0.63, width=180)

        self.register_label = Label(self.login_frame, text="Don't Have An Account?Sign Up", background="white")
        self.register_label.place(anchor=CENTER, relx=0.5, rely=0.95)


root = Tk()
root.geometry('1366x768')
obj = Login(root)

root.mainloop()
