# POSprint

**How to use POSprint**

In order to get POSprint to function properly, you should follow these steps:

1. Install printer driver software (right-click, run as admin)
    - on Devices and Printers, you will probably see 2 devices (1 printer, 1 unknown device when printer plugged in)
    - Printer model = 80 Series (POS88V)
2. Make sure printer is shared, make sure you remember the shared name
    - Go to Devices and Printers
    - Add a Printer
    - New -> Use existing Port (USB001)
    - Generic -> Generic / Text Only
    - Use driver already installed (from step #1)
    - Name & share the printer "SPRT POS Printer"
3. Python 2.7 is installed on your computer and can be accessed from the folder (add to PATH)
4. PHP doesn't need to be 'installed', just some files need to be configured
    - Edit the php.ini file - make sure extension_dir points to the correct directory of extensions
    - Edit the php.ini file - uncomment the line 'extension=php_mbstring.dll' so that the php script can use that extension
    - Edit the POSprint.php file - make sure line 16 has same name of printer created in step 2 (probably 'SPRT POS Printer')
5. You may have to install microsoft redistributable packages if you don't have microsoft visual studio already installed on your machine.
    - I've had trouble using the redistributable packages, so I just installed the full program.

Before printing, make sure:

1. the txt document & php document contain the data you want to print
     * the php file may contain formatting for printed text

# About

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
