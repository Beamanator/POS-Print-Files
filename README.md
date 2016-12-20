# POSprint

**How to use POSprint**

In order to get POSprint to function properly, you need to make sure:
1) Python can be accessed from the folder
2) PHP can be accessed from the folder
  * A quick test to make sure your folder has php access is to run "php testphp.php" via the command line in Windows
  
Before printing, make sure:
1) the txt document & php document contain the data you want to print
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
