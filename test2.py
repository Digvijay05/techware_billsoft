import time
import tkinter
import datetime
import pyautogui

"""
Example tkinter Clock widget, counting seconds and minutes in realtime.
Functions just like a Label widget.
The Clock class has three functions:
__init__ creates the clock widget, which is just an ordinary label.
The tick() function rewrites the label every 200 milliseconds (5 times 
  each minute) to the current time. This updates the seconds.
The blink_colon() function rewrites the label every second, making the
  colon appear to blink every second.
The secret sauce is tkinter's .after command. When a function completes,
the .after command triggers another (or the same) function to run after
a specified delay. __init__ triggers tick(), then tick() keeps triggering
itself until stopped.
All that complexity is hidden from you. Simply treat the clock as another
label widget with a funny name. *It should automatically work.*
How to add the clock widget:
    tkinter.Label(parent, text="Foo").pack()      # A widget
    Clock(parent).widget.pack()                   # Just another widget 
    tkinter.Label(parent, text="Bar").pack()      # Yet another widget
How to start/stop the clock widget:
    You don't.
    If you create a Clock().widget, the clock will start.
    If you destroy the widget, the clock will also be destroyed.
    To hide/restore the clock, use .pack_forget() and re-.pack().
    The clock will keep running while hidden.
"""


class Clock(tkinter.Label):
    """ Class that contains the clock widget and clock refresh """

    def __init__(self, parent=None, seconds=True, colon=False):
        """
        Create and place the clock widget into the parent element
        It's an ordinary Label element with two additional features.
        """
        tkinter.Label.__init__(self, parent)

        self.display_seconds = seconds
        if self.display_seconds:
            self.time = time.strftime('%H:%M:%S %TM')
        else:
            self.time = time.strftime('%I:%M %p').lstrip('0')
        self.display_time = self.time
        self.configure(text=self.display_time)

        if colon:
            self.blink_colon()

        self.after(1, self.tick)

    def tick(self):
        """ Updates the display clock every 200 milliseconds """
        if self.display_seconds:
            new_time = time.strftime('%H:%M:%S')
        else:
            new_time = time.strftime('%I:%M %p').lstrip('0')
        if new_time != self.time:
            self.time = new_time
            self.display_time = self.time
            self.config(text=self.display_time)
        self.after(1, self.tick)

    def blink_colon(self):
        """ Blink the colon every second """
        if ':' in self.display_time:
            self.display_time = self.display_time.replace(':', ' ')
        else:
            self.display_time = self.display_time.replace(' ', ':', 1)
        self.config(text=self.display_time)
        self.after(1000, self.blink_colon)


from tkinter import *


class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        """Display text in tooltip window"""
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        position = pyautogui.position()
        tw.wm_geometry("+%d+%d" % (position.x, position.y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))

        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


if __name__ == "__main__":
    """
    Create a tkinter window and populate it with elements
    One of those elements merely happens to include the clocks.
    The clock widget can be configure()d like any other Label widget.
    Nothing special needs to be added to main(). The Clock class
      updates the widget automatically when you create the widget.
    """

    # Create window and frame

    window = tkinter.Tk()
    frame = tkinter.Frame(window, width=400, height=400)
    frame.pack()

    # Add the frame elements, including the clock like any other element

    tkinter.Label(frame, text="Clock with seconds:").pack()

    clock1 = Clock(frame)
    CreateToolTip(clock1, "This is A Tooltip")
    clock1.pack()
    clock1.configure(bg='green', fg='yellow', font=("helvetica", 35))

    tkinter.Label(frame, text=" ").pack()

    tkinter.Label(frame, text="Clock with blinking colon:").pack()

    clock2 = Clock(frame, seconds=False, colon=True)
    clock2.pack()
    clock2.configure(bg='red', fg='white', font=("arial", 20))

    tkinter.Label(frame, text=" ").pack()

    tkinter.Label(frame, text="Have a nice day.").pack()

    window.mainloop()
