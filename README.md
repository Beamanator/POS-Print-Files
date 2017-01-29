# POSprint

**How to use POSprint**

In order to get POSprint to function properly, you need to make sure:

1. Install printer driver software
2. Make sure printer is shared, make sure you remember the shared name
3. Python 2.7 is installed on your computer and can be accessed from the folder
4. PHP is installed and make sure it can be accessed from the folder
5. Edit the php.ini file - make sure extension_dir points to the correct directory of extensions
6. Edit the php.ini file - uncomment the line 'extension=php_mbstring.dll' so that the php script can use that extension
7. You may have to install microsoft redistributable packages if you don't have microsoft visual studio already installed on your machine

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
