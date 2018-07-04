<?php
/**
 * This print-out will be used for St Andrews Refugee Services (StARS) in Cairo, Egypt
 *
 * Originally created by Michael Billington <michael.billington@gmail.com>
 * Edited and adapted to SPRT POS Printer by The RIPS Guy <rips@stars-egypt.org>
 *
 * Code originally from Michael's text-size.php example file
 */
require __DIR__ . './escpos-php-development/autoload.php';
use Mike42\Escpos\Printer;
use Mike42\Escpos\PrintConnectors\WindowsPrintConnector;

/*      Log initial text to make sure this file is being executed        */
$log_init_print = date("d-M-Y") . " - Print triggered";
logText($log_init_print);

/*                Connect & Print Text to POS Printer                     */
try {
	/* Set up printer */
	$connector = new WindowsPrintConnector("SPRT POS Printer");
	$printer = new Printer($connector);

	/* Initialize */
	$printer -> initialize();

	// set timezone to Egypt to get date correct
	date_default_timezone_set("Egypt");

	// center the text:
	$printer -> setJustification(Printer::JUSTIFY_CENTER);

	// title
	$printer -> setTextSize(5, 5);
	$printer -> text( "StARS\n" );

	// program name
	$printer -> setTextSize(2, 2);
	$printer -> text( getProgramName() . "\n\n" );

	// get small number - in txt file
	$printer -> setTextSize(1, 1);
	$printer -> text( getSmallNum() . "\n" );

	// get big number - in txt file
	$printer -> setTextSize(5, 5);
	$printer -> text( getBigNum() . "\n" );

	// print date
	$printer -> setTextSize(1, 1);
	$printer -> text( date("d-M-Y") . "\n" );
	
	// cut paper & close printer connection
	$printer -> cut();
	$printer -> close();
} catch(Exception $e) {
	echo "Couldn't print to this printer: " . $e -> getMessage() . "\n";
}

// get program name from txt file
function getProgramName()
{
	$filename = "POSprint_ProgramHolder.txt";
	return readMyFile($filename);
}

// get small number from txt file
function getSmallNum()
{
	$filename = "POSprint_SmallNumHolder.txt";
	return readMyFile($filename);
}

// get big number from txt file
function getBigNum()
{
	$filename = "POSprint_BigNumHolder.txt";
    return readMyFile($filename);
}

// get text from file with name $filename
function readMyFile($filename)
{
	$file = fopen($filename, "r") or die("Unable to open " . $filename . "!");
    $index = fread($file, filesize($filename));
    fclose($file);
    return $index;
}

// log text to $log_filename file
function logText($text_to_log) {
	$log_filename = "POSprint_LogHolder.txt";

	// open with 'a' mode, which is append (creates file if it doesn't exist yet)
	$log_file = fopen($log_filename, 'a') or die ("Cannot open file: " . $log_filename);

	fwrite($log_file, "\n" . $text_to_log);
	fclose($log_file);
}