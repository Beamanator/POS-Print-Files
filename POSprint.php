<?php
/**
 * This print-out will be used for St Andrews Refugee Services (StARS) in Cairo, Egypt
 *
 * Originally created by Michael Billington <michael.billington@gmail.com>
 * Edited and adapted to SPRT POS Printer by The RIPS Guy <rips@stars-egypt.org>
 *
 * Code originally from Michael's text-size.php example file
 */
require __DIR__ . '..\..\escpos-php-development\escpos-php-development/autoload.php';
use Mike42\Escpos\Printer;
use Mike42\Escpos\PrintConnectors\WindowsPrintConnector;

try {
	/* Set up printer */
	$connector = new WindowsPrintConnector("SPRT POS Printer");
	$printer = new Printer($connector);

	/* Initialize */
	$printer -> initialize();

	// set timezone to Egypt to get date correct
	date_default_timezone_set("Egypt");

	// title
	$printer -> setTextSize(5, 5);
	$printer -> text("  StARS\n");
	$printer -> setTextSize(2, 2);
	$printer -> text("  PS / RLAP Reception" . "\n\n");

	// client index - in txt file
	$printer -> setTextSize(5, 5);
	$printer -> text("   " . readIndex() . "\n");

	// print date
	$printer -> setTextSize(1, 1);
	$printer -> text("               " . date("d-M-Y") . "\n");
	
	// cut paper & close printer connection
	$printer -> cut();
	$printer -> close();
} catch(Exception $e) {
	echo "Couldn't print to this printer: " . $e -> getMessage() . "\n";
}

function readIndex()
{
    $file = fopen("POSprint_ClientIndexHolder.txt", "r") or die("Unable to open file!");
    $index = fread($file, filesize("POSprint_ClientIndexHolder.txt"));
    fclose($file);
    return $index;
}
