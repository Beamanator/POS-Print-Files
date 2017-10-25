# POSprint.py
# Written by "The RIPS Guy" - <rips@stars-egypt.org>
# Compiled from many Stack Overflow questions & other online tutorials

# Popen is used for calling batch jobs from python
from subprocess import Popen

# Tkinter and tkFont are used for creating a nice GUI for the user
from Tkinter import *
import tkFont

# import random class for randomizing numbers
import random

# os is used for getting the current path (cwd)
import os

#########################################################################
#                            TODO                                       #
#########################################################################
# 1) Incremental Counter
# 2) Print / write to new incremental counter file

# =============================== Main App class for GUI ==================================
class App:
    def writeIndexToFile(self, cid):
        """ Write the given cid (client index) to a file - php will print that file. """
        with open("POSprint_ClientIndexHolder.txt", "w") as f:
            f.seek(0)
            f.write(str(cid))
            f.truncate()

    def writeProgramToFile(self):
        """ Write the current selected program to a file - php will print that file. """
        with open("POSprint_ProgramHolder.txt", "w") as f:
            f.seek(0)
            f.write(self.program.get())
            f.truncate()

    def TriggerBatchFile(self):
        """ Triggers batch file """
        # Actually print index via POS printer via batch
        mycwd = os.getcwd()
        p = Popen("POSprint.bat", cwd=r"" + mycwd)
        stdout, stderr = p.communicate()

    def POSPrint(self):
        """ Print index by calling .bat which calls php file """
        # get client index from input text box
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

        # finally, write program to file then trigger batch file
        self.writeProgramToFile()
        self.TriggerBatchFile()

    def POSPrintRand(self):
        """ Print (random) index like above - POSPrint """
        # get 'from' and 'to' values from text boxes
        rand_from = self.rand_from_val.get()
        rand_to = self.rand_to_val.get()

        # check if 
        if rand_from == '' or rand_to == '':
            print 'Must enter "from" and "to" values'
            self.UpdateRandStringText('Error - see console')
            return

        rand_from = int(rand_from)
        rand_to = int(rand_to)

        # if rand array index is -1, need to create rand array and set index to 0
        if self.rand_array_index == -1:
            # get random number array
            self.rand_array = random.sample( range(rand_from, rand_to), (rand_to - rand_from) )

            # set index to 0
            self.rand_array_index = 0

        # increment until out of bounds
        elif self.rand_array_index + 1 < len(self.rand_array):
            self.rand_array_index += 1

        else:
            self.UpdateRandStringText('Click "Reset" Button')
            return

        # update 'from' and 'to' labels
        self.UpdateRandStringIndices( self.rand_array_index + 1, len(self.rand_array) )

        next_val = self.rand_array[ self.rand_array_index ]

        # update client_previous_val to next_num [after making sure this num hasn't been printed]
        self.client_previous_val.set( str(next_val) )

        # finally, write program to file then trigger batch file
        self.writeProgramToFile()
        #self.TriggerBatchFile()

    def ResetClientIndex(self):
        """ Resets the client index in GUI - Not in txt file """
        self.client_next_val.set("00")
        self.client_previous_val.set("")

        self.rand_from_val.set("")
        self.rand_to_val.set("")

        self.rand_array = []

        self.UpdateRandStringText('')

        # Don't need to reset file since the file gets changed in other function
        #  when print button is clicked

    def UpdateRandStringIndices(self, first, second):
        """ Update the string that displays current index of printing """
        # create new string (+ is for concatenating strings)
        new_text = "Printed ["+str(first)+"] of ["+str(second)+"] #s"

        # update string in GUI
        self.random_range_label.config(text=new_text)

    def UpdateRandStringText(self, text):
        """ Update the rand string to some text """
        # create new string from new text
        if text == '':
            new_text = "Printed [0] of [0] #s"
        else:
            new_text = text

        # update string in GUI
        self.random_range_label.config(text=new_text)

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

    def getProgramFromFile(self):
        """ Get initial program name from file """
        # read data from program holder txt file
        with open("POSprint_ProgramHolder.txt", "r+") as f:
            data = f.read()
            # return data from text file
            return data
        
    def __init__(self):
        """ Main function - see comments for details """
        PROGRAMS = [
            "PS / RLAP Reception",
            "RLAP Checking"
        ]

        root=Tk()
        
        # create a custom font
        self.customFont = tkFont.Font(family="Helvetica", size=18)
        self.buttonFont = tkFont.Font(family="Helvetica", size=18)
        self.largeTextFont = tkFont.Font(family="Helvetica", size=24)
        self.mediumTextFont = tkFont.Font(family="Helvetica", size=18)
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
               ).grid(row=4,column=2)
        # Button for printing random numbers:
        Button(root, text="Print Rand", padx=0, pady=0, font=self.buttonFont,
               bg="cyan", command=self.POSPrintRand
               ).grid(row=4,column=1)

        # Add labels
        Label(root, text="Next Client # to print:",
              font=self.largeTextFont, padx=10
              ).grid(row=1,column=2)
        Label(root, text="Last # printed:",
              font=self.smallTextFont, padx=100
              ).grid(row=2,column=2,sticky=E+W)
        # Randomizer Labels
        Label(root, text="Random #s",
            font=self.largeTextFont, padx=10
            ).grid(row=1,column=0)
        Label(root, text="From:",
            font=self.smallTextFont, padx=0
            ).grid(row=2,column=0)
        Label(root, text="To:",
            font=self.smallTextFont, padx=0
            ).grid(row=2,column=1)
        # split into two lines because .grid() returns object with None type
        self.random_range_label = Label(root, text="Printed [0] of [0] #s",
            font=self.smallTextFont, padx=0
            )
        self.random_range_label.grid(row=4,column=0)

        # Add Entry box for # to print
        self.client_previous_val = StringVar()
        self.client_previous_val.set("")
        self.client_previous = Entry(root, text=self.client_previous_val,
            font=self.smallTextFont,
            width=4, state="disabled"
            ).grid(row=2,column=3,sticky=W)
        # client # to print [with validation in onValidate()]
        valcmd = (root.register(self.onValidate),
                  '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.client_next_val = StringVar()
        self.client_next_val.set("")
        self.client_next = Entry(root, text=self.client_next_val,
            font=self.largeTextFont,
            width=4, validate="key", validatecommand=valcmd
            ).grid(row=1,column=3,sticky=W)
        # Randomizer for from / to entry boxes
        self.rand_from_val = StringVar()
        self.rand_from_val.set("")
        self.rand_from = Entry(root, text=self.rand_from_val,
            font=self.mediumTextFont,
            width=4, validate="key", validatecommand=valcmd
            ).grid(row=3,column=0)
        self.rand_to_val = StringVar()
        self.rand_to_val.set("")
        self.rand_to = Entry(root, text=self.rand_to_val,
            font=self.mediumTextFont,
            width=4, validate="key", validatecommand=valcmd
            ).grid(row=3,column=1)

        # Setup default program name text for OptionMenu
        self.program = StringVar()
        # - get program from text file
        initialProgram = self.getProgramFromFile()
        # - if there is data in file & data is part of PROGRAMS array,
        # --- set data as initial program name
        if len(initialProgram) > 0 and initialProgram in PROGRAMS:
            self.program.set(initialProgram)
        # - else, default to first element in array
        else:
            self.program.set(PROGRAMS[0])
        # Create OptionMenu dropdown for program names
        option = apply(OptionMenu, (root, self.program) + tuple(PROGRAMS))
        option.pack()
        option.config(width=20, height=1, font=self.mediumTextFont)
        option["menu"].config(font=self.mediumTextFont)
        option.grid(row=0,column=2)

        # initialize rand array index
        self.rand_array_index = -1
        
        # prepare for printing!
        self.prepPrint()

        root.mainloop()

# Create the App (window) and run the program!
app = App()
