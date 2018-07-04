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

# time is used for pausing - for rand printing and error troubleshooting
import time

#########################################################################
#                            TODO                                       #
#########################################################################
# 1) Incremental Counter
# 2) Print / write to new incremental counter file

# =============================== Main App class for GUI ==================================
class App:
    def writeNumToFile(self, num, size):
        """ Write the given 'num' to a file depending on size - php will print that file. """
        file = ""
        if size == "small":
            file = "POSprint_SmallNumHolder.txt"
        elif size == "big":
            file = "POSprint_BigNumHolder.txt"
        else:
            print("Size not recognized - error")
            return
        
        with open(file, "w") as f:
            f.seek(0)
            f.write(str(num))
            f.truncate()

    def writeProgramToFile(self):
        """ Write the current selected program to a file - php will print that file. """
        with open("POSprint_ProgramHolder.txt", "w") as f:
            f.seek(0)
            f.write(self.program.get())
            f.truncate()

    def getLeadingZeroString(self, num):
        """ Function returns a string with leading zeroes if needed """
        if (num < 10):
            num = "0" + str(num)
        else:
            return str(num)

        return num

    def POSPrint(self):
        """ Print index by calling .bat which calls php file """
        # get client index from input text box
        cid = self.client_next_val.get()
        
        # set last printed # to current index:
        self.client_previous_val.set(cid)

        # increment next client index by 1. if 999, reset to 0
        nextid = cid
        if (int(nextid) == 999):
            nextid = -1
        nextid = int(nextid) + 1

        # format number, then set variables
        nextid = self.getLeadingZeroString( nextid )
        self.client_next_val.set(nextid)

        # set big and small nums to print
        big_num = cid
        small_num = cid

        # finally, write program & nums to file then trigger batch file
        print('Printing nums: big (' + str(big_num) + '); small (' + str(small_num) + ')')
        self.writeNumToFile(small_num, 'small')
        self.writeNumToFile(big_num, 'big')
        self.writeProgramToFile()
        self.TriggerBatchFile()

    def ResetClientIndex(self):
        """ Resets the client index in GUI - Not in txt file """
        self.client_next_val.set("00")
        self.client_previous_val.set("")

        # Don't need to reset file since the file gets changed in other function
        #  when print button is clicked

    def POSPrintRand(self):
        """ Print (random) index like above - POSPrint """
        
        # create local vars from object properties
        r_from = self.rand_from
        r_to = self.rand_to

        # if range hasn't been set, get new range
        if self.rand_from == -1 or self.rand_to == -1:
            r_from = self.rand_from_val.get()
            r_to = self.rand_to_val.get()

            # if either of new values aren't populated, error and quit
            if r_from == '' or r_to == '':
                print 'Must enter "from" and "to" values in GUI'
                self.UpdateRandStringText('Error - see console')
                return

            # else, set up new range & disable entries
            else:
                self.rand_from = r_from
                self.rand_to = r_to

                self.rand_from_entry.config(state="disabled")
                self.rand_to_entry.config(state="disabled")
                print('New range: ' + r_from + '-' + r_to)

        # convert string variables to integers. don't need validation
        r_from = int(r_from)
        r_to = int(r_to)

        # if rand array index is -1, need to create rand array and set index to 0
        if self.rand_array_index == -1:
            # get random number array -> once :)
            # https://docs.python.org/2/library/random.html
            self.rand_array = random.sample( range(r_from, r_to + 1),
                (r_to - r_from + 1) )

            # set index to 0 to start looping
            self.rand_array_index = 0

        # increment until index out of bounds
        elif self.rand_array_index + 1 < len(self.rand_array):
            self.rand_array_index += 1

        # index out of bounds, so show error
        else:
            print('Please clear data in order to print new random range')
            self.UpdateRandStringText('Finished Printing Range')
            return

        # update 'from' and 'to' labels
        self.UpdateRandStringIndices( self.rand_array_index + 1, len(self.rand_array) )

        # get next value to print
        next_val = self.rand_array[ self.rand_array_index ]

        # set big and small nums to print
        big_num = self.getLeadingZeroString( next_val )
        small_num = self.getLeadingZeroString( self.rand_array_index + r_from )

        # update client_previous_val to next_num
        self.client_previous_val.set( big_num )

        # finally, write program & nums to file then trigger batch file
        print('Printing nums: big (' + big_num + '); small (' + small_num + ')')
        self.writeNumToFile( big_num, 'big' )
        self.writeNumToFile( small_num, 'small' )
        self.writeProgramToFile()
        self.TriggerBatchFile()

    def ClearRandData(self):
        """ Clear Data for Randomization """
        # enable entries
        print('<-- Resetting entry box states !-->')
        self.rand_from_entry.config(state="normal")
        self.rand_to_entry.config(state="normal")
        # reset random variables
        print('<-- Resetting rand values !-->')
        self.rand_from_val.set("")
        self.rand_to_val.set("")
        # reset range
        print('<-- Resetting rand variables !-->')
        self.rand_from = -1
        self.rand_to = -1
        # reset array
        print('<-- Resetting rand array and index !-->')
        self.rand_array_index = -1
        self.rand_array = []
        # reset bottom-left random string
        print('<-- Resetting rand string !-->')
        self.UpdateRandStringText('')

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

    def prepPrint(self):
        """ Prepare print function by setting next index to 0, prev index to # in file """
        # set next # to print as 00
        self.client_next_val.set("00")
        
        # show user the previous big # printed
        with open("POSprint_BigNumHolder.txt", "r+") as f:
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
        # possible program titles to go in dropdown and be printed
        PROGRAMS = [
            "PS / RLAP Reception",
            "RLAP Checking"
        ]

        self.root=Tk()
        
        # create a custom font
        self.customFont = tkFont.Font(family="Helvetica", size=18)
        self.buttonFont = tkFont.Font(family="Helvetica", size=18)
        self.largeTextFont = tkFont.Font(family="Helvetica", size=24)
        self.mediumTextFont = tkFont.Font(family="Helvetica", size=18)
        self.smallTextFont = tkFont.Font(family="Helvetica", size=12)
        
        # Set window details
        self.root.title("StARS SIO Label Printer")
        # Set starting window size
        # - width x height + starting x + starting y [from monitor window]
        self.root.geometry('800x400+100+200')

        # Make all rows (mostly) the same height:
        self.root.rowconfigure(0, weight=2)
        self.root.rowconfigure(1, weight=2)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=2)
        self.root.rowconfigure(4, weight=2)

        # Make 3 columns - 1 small, 1 big, 1 small
        #for c in range(3):
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)
        self.root.columnconfigure(2, weight=1)
        
        # Add reset button in top-left corner
        Button(self.root, text="Reset", padx=30, font=self.buttonFont,
               bg="red", command=self.ResetClientIndex
               ).grid(row=0,column=2)
        # Add Print button in middle-bottom
        Button(self.root, text="Print", padx=20, pady=5, font=self.buttonFont,
               bg="green", command=self.POSPrint
               ).grid(row=4,column=2)
        # Button for printing random numbers:
        Button(self.root, text="Print Rand", padx=0, pady=0, font=self.buttonFont,
               bg="cyan", command=self.POSPrintRand
               ).grid(row=4,column=1)
        # Button for resetting randomizer data
        Button(self.root, text="Clear", padx=0, pady=0, font=self.buttonFont,
                bg="yellow", command=self.ClearRandData
                ).grid(row=1,column=1)
 
        # Add labels
        Label(self.root, text="Next Client # to print:",
              font=self.largeTextFont, padx=10
              ).grid(row=1,column=2)
        Label(self.root, text="Last # printed:",
              font=self.smallTextFont, padx=100
              ).grid(row=2,column=2,sticky=E+W)
        # Randomizer Labels
        Label(self.root, text="Random #s",
            font=self.largeTextFont, padx=10
            ).grid(row=1,column=0)
        Label(self.root, text="From:",
            font=self.smallTextFont, padx=0
            ).grid(row=2,column=0)
        Label(self.root, text="To:",
            font=self.smallTextFont, padx=0
            ).grid(row=2,column=1)
        # split into two lines because .grid() returns object with None type
        self.random_range_label = Label(self.root, text="Printed [0] of [0] #s",
            font=self.smallTextFont, padx=0
            )
        self.random_range_label.grid(row=4,column=0)

        # Add Entry box for # to print
        self.client_previous_val = StringVar()
        self.client_previous_val.set("")
        self.client_previous = Entry(self.root, text=self.client_previous_val,
            font=self.smallTextFont,
            width=4, state="disabled"
            ).grid(row=2,column=3,sticky=W)
        # client # to print [with validation in onValidate()]
        valcmd = (self.root.register(self.onValidate),
                  '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.client_next_val = StringVar()
        self.client_next_val.set("")
        self.client_next = Entry(self.root, text=self.client_next_val,
            font=self.largeTextFont,
            width=4, validate="key", validatecommand=valcmd
            ).grid(row=1,column=3,sticky=W)
        # Randomizer for from / to entry boxes
        self.rand_from_val = StringVar()
        self.rand_from_val.set("")
        self.rand_from_entry = Entry(self.root, text=self.rand_from_val,
            font=self.mediumTextFont,
            width=4, validate="key", validatecommand=valcmd
            )
        self.rand_from_entry.grid(row=3,column=0)
        self.rand_to_val = StringVar()
        self.rand_to_val.set("")
        self.rand_to_entry = Entry(self.root, text=self.rand_to_val,
            font=self.mediumTextFont,
            width=4, validate="key", validatecommand=valcmd
            )
        self.rand_to_entry.grid(row=3,column=1)

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
        option = apply(OptionMenu, (self.root, self.program) + tuple(PROGRAMS))
        option.pack()
        option.config(width=18, height=1, font=self.mediumTextFont)
        option["menu"].config(font=self.mediumTextFont)
        option.grid(row=0,column=0)

        # initialize rand array index -> -1 means array needs
        # to be created still
        self.rand_array_index = -1
        # initialize vars as -1 to show range not set yet
        self.rand_from = -1
        self.rand_to = -1
        
        # prepare for printing!
        self.prepPrint()
        self.root.mainloop()

    def TriggerBatchFile(self):
        """ Triggers batch file """
        # Actually print index via POS printer via batch
        mycwd = os.getcwd()
        p = Popen("POSprint.bat", cwd=r"" + mycwd)
        stdout, stderr = p.communicate()

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

# Create the App (window) and run the program!
app = App()