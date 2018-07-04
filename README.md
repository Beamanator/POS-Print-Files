# POSprint

## How to use POSprint

**Follow these steps** in order to get POSprint set up properly:

1. Download the entire project directory from the [POS-Print-Files](https://github.com/Beamanator/POS-Print-Files) repo.
1. Install printer driver software from `SPRT DriverV2.0` directory
    - First, Un-zip the folder
    - Navigate to `/English` -> `/Printer Driver`
    - Install the executable **(right-click, then select run as admin)** that should be used for your computer, depending on your Windows operating system.
    - On Devices and Printers, you will probably see 2 devices (1 printer, 1 unknown device when printer plugged in)
    - In order to see the new printer under the "Printer" category, you may have to wait a while, or restart your computer.
    - Printer model = 80 Series (POS88V)
1. Make sure printer is shared - **remember the shared name**
    - Go to Devices and Printers again
    - Add a Printer
    - New -> Use existing Port (USB001)
    - Generic -> Generic / Text Only
    - Use driver already installed (from step #1)
    - Name & share the printer something like `SPRT POS Printer`
1. Install **[Python 2.7.12](https://www.python.org/downloads/release/python-2712/)** on your computer and can be accessed from the folder (add to PATH)
    - Note: Make sure you're installing the correct version of Python! This has only been tested with [v2.7.12](https://www.python.org/downloads/release/python-2712/)
1. PHP doesn't need to be 'installed', just some files need to be configured
    - Edit the php.ini file - make sure extension_dir points to the correct directory of extensions
    - Edit the php.ini file - uncomment the line 'extension=php_mbstring.dll' so that the php script can use that extension
    - Edit the POSprint.php file - make sure line 16 has same name of printer created in step 2 (probably 'SPRT POS Printer')
1. You may have to install [microsoft redistributable packages](https://www.microsoft.com/en-eg/download/details.aspx?id=48145) if you don't have microsoft visual studio already installed on your machine.
    - I've had some trouble and some success using the redistributable packages, so I often just installed the [full program](https://msdn.microsoft.com/en-us/library/e2h7fzkw.aspx).
1. **Important Step**: Copy all of the files starting with `POSprint` into the folder called `CODE_GOES_HERE`.
    - You should only need to download the printer driver and all of the python / php installers one time. However, if some code updates come out for the POSprint files, the updated files always need to be place inside the `POSprint` directory.
    - After you move all of the POSprint... files into `/CODE_GOES_HERE`, you may want to make sure they don't also exist anywhere else, just to avoid confusion later.

**Now you're ready to go? This is how you should run the program:**
1. Navigate into your `/CODE_GOES_HERE` directory and double-click the `POSprint.py` file (the python executable).
    - You should see a GUI pop up, with a black box logging window behind it.

That's it! Before you try printing for the first time, I would recommend you make sure:

1. The txt document & php document contain the data you want to print
    - Note: the php file may contain formatting for printed text
    
## Possible Issues / Errors

**Here are some common errors I've run into and how to solve (most of) them:**

1. PHP Warning: (.../autoload.php): failed to open stream: No such file or directory in ...
    - Make sure line 10 of POSprint.php is looking at the correct directory for escpos-php-development/autoload.php
1. Error with function readFile()
    - readFile exists in some other libraries used in this repo, so can't make a new function named readFile
1. Everything looks good, but printer is not printing (related to #2).
    - No solution yet :(

## About

**What is POSprint?**

POSprint is a project that was built under very specific specifications. It may not be useful for others to see, but I hope it will bring a bit more light to the POS printing world.

The main flow of POSprint is:
- POSprint.py creates a GUI using Tkinter, and writes a number to the file POSprint_ClientIndexHolder.txt
- Once the "Print" button is clicked, python runs POSprint.bat
- POSprint.bat calls POSprint.php, as if it were from the Windows cmd
- POSprint.php calls some libraries built by Mike42 (Blog post link [here](https://mike42.me/blog/2015-04-getting-a-usb-receipt-printer-working-on-windows)) to send POS commands to the POS printer so some nice text is printed.

POSprint uses the following languages:
- Python 2.7
- Windows batch file commands
- PHP

## Explanation of Files:
1. Code files
    1. `POSprint.bat`
        - Called by .py, triggers the .php file
    1. `POSprint.php`
        - Called by .bat file, connects to printer and reads data from .txt file(s)
    1. `POSprint.py`
        - Triggered by user, writes data to files and triggers .bat file
1. Text files
    1. `POSprint_BigNumHolder.txt`
        - Holds the number to be printed in *large* text
    1. `POSprint_ClientIndexHolder.txt`
        - Holds the index of the current client for in-order printing
    1. `POSprint_LogHolder.txt`
        - Holds logged text (isn't printed, just logged)
    1. `POSprint_ProgramHolder.txt`
        - Holds program text to be printed
    1. `POSprint_SmallNumHolder.txt`
        - Holds the number to be printed in *small* text