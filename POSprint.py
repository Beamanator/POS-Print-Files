# POSprint.py
# Written by "The RIPS Guy" - <rips@stars-egypt.org>
# Compiled from many Stack Overflow questions & other online tutorials

# Popen is used for calling batch jobs from python
from subprocess import Popen

# Tkinter and tkFont are used for creating a nice GUI for the user
from Tkinter import *
import tkFont

# os is used for getting the current path (cwd)
import os

# =============================== Main App class for GUI ==================================
class App:
    def writeIndexToFile(self, cid):
        """ Write the given cid (client index) to a file - php will print that file. """
        with open("POSprint_ClientIndexHolder.txt", "w") as f:
            f.seek(0)
            f.write(str(cid))
            f.truncate()

    def POSPrint(self):
        """ Print index by calling .bat which calls php file """
        cid = self.client_next_val.get()
        # set last printed # to current index:
        self.client_previous_val.set(cid)

        # write client_previous_val to file [same as cid for now]
        self.writeIndexToFile(cid)

        # increment next client index by 1. if 999, reset to 0
        if (int(cid) == 999):
            cid = -1
        cid = int(cid) + 1
        if (cid < 10):
            cid = "0" + str(cid)
        self.client_next_val.set(cid)

        # Actually print index via POS printer via batch
        mycwd = os.getcwd()
        p = Popen("POSprint.bat", cwd=r"" + mycwd)
        stdout, stderr = p.communicate()

    def ResetClientIndex(self):
        """ Resets the client index in GUI - Not in txt file """
        self.client_next_val.set("00")
        self.client_previous_val.set("")
        # Don't need to reset file since the file gets changed in other function
        #  when print button is clicked

    def onValidate(self, d, i, P, s, S, v, V, W):
        """ Validate data in client index box, on key press """
        # Validate data in client index box
        # - only allow #s, and only up to 3 numbers
        # - return True to allow the change
        # - return False to reject the change
        # exact details on this validation can be found on SO here:
        # http://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter

        # if character entered is not a number, don't enter it.
        if (d == str(1) and int(i) != -1):
            char = P[int(i)]
            if (not char.isdigit()):
                return False
        # if more than 3 numbers are entered, stop allowing entry
        length = len(P)
        if (length > 3):
            return False
        # everything looks good, so return True
        return True

    def prepPrint(self):
        """ Prepare print function by setting next index to 0, prev index to # in file """
        # set next # to print as 00
        self.client_next_val.set("00")
        
        # show user the previous client_previous_val # printed
        with open("POSprint_ClientIndexHolder.txt", "r+") as f:
            data = f.read()
            try:
                x = int(data)
            except ValueError:
                # If data was a string, reset client index to 0'
                f.seek(0)
                f.write("0")
                f.truncate()
            # put data into textbox
            x = int(data)
            if (x < 10):
                data = "0" + str(x)
            self.client_previous_val.set(data)
        
    def __init__(self):
        """ Main function - see comments for details """
        root=Tk()
        # create a custom font
        self.customFont = tkFont.Font(family="Helvetica", size=18)
        self.buttonFont = tkFont.Font(family="Helvetica", size=18)
        self.largeTextFont = tkFont.Font(family="Helvetica", size=24)
        self.smallTextFont = tkFont.Font(family="Helvetica", size=12)
        
        # Set window details
        root.title("StARS SIO Label Printer")
        # Set starting window size
        # - width x height + starting x + starting y [from monitor window]
        root.geometry('700x400+200+200')

        # Make all rows (mostly) the same height:
        root.rowconfigure(0, weight=2)
        root.rowconfigure(1, weight=2)
        root.rowconfigure(2, weight=1)
        root.rowconfigure(3, weight=2)
        root.rowconfigure(4, weight=2)

        # Make 3 columns - 1 small, 1 big, 1 small
        #for c in range(3):
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=3)
        root.columnconfigure(2, weight=1)
        
        # Add reset button in top-left corner
        Button(root, text="Reset", padx=30, font=self.buttonFont,
               bg="red", command=self.ResetClientIndex
               ).grid(row=0,column=0)

        # Add Print button in middle-bottom
        Button(root, text="Print", padx=20, pady=5, font=self.buttonFont,
               bg="green", command=self.POSPrint
               ).grid(row=4,column=1)

        # Add labels
        Label(root, text="Next Client # to print:",
              font=self.largeTextFont, padx=10
              ).grid(row=1,column=1)
        Label(root, text="Last # printed:",
              font=self.smallTextFont, padx=100
              ).grid(row=2,column=1,sticky=E+W)

        # Add Entry box for # to print
        self.client_previous_val = StringVar()
        self.client_previous_val.set("")
        self.client_previous = Entry(root, text=self.client_previous_val,
                            font=self.smallTextFont,
                            width=4, state="disabled"
              ).grid(row=2,column=2,sticky=W)
        # client # to print [with validation in onValidate()]
        valcmd = (root.register(self.onValidate),
                  '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.client_next_val = StringVar()
        self.client_next_val.set("")
        self.client_next = Entry(root, text=self.client_next_val,
                            font=self.largeTextFont,
                            width=4, validate="key", validatecommand=valcmd
              ).grid(row=1,column=2,sticky=W)
        # prepare for printing!
        self.prepPrint()

        root.mainloop()

# Create the App (window) and run the program!
app = App()
