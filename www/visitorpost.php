<?php
try
{
//set the timezone
date_default_timezone_set("Europe/Rome");
//date_default_timezone_set("UTC");

//open the database
$db = new SQLite3("/mnt/sda1/arduino/www/FablabDoorman/logger.db");

$username = $_POST["username"]; 
$cardcode = $_POST["cardcode"]; 
$sday = $_POST["sday"]; 
$smonth = $_POST["smonth"]; 
$syear = $_POST["syear"]; 
$eday = $_POST["eday"]; 
$emonth = $_POST["emonth"]; 
$eyear = $_POST["eyear"];
$shour = $_POST["shour"];
$ehour = $_POST["ehour"];

if ($username == '' || $cardcode == '' || $sday == '' || $smonth == '' || $syear == '' || $eday == '' || $emonth == '' || $eyear == '' || $shour == '' || $ehour == '') {
print 'tutti i campi sono obbligatori <br>';
print '<a href="javascript:history.back()"> torna indietro </a>';
}else{
$startdate = mktime($shour, 0, 0, $smonth, $sday, $syear);
$expiredate = mktime($ehour, 0, 0, $emonth, $eday, $eyear);
//Insert record  
$db->exec("INSERT INTO visitorsallowedusers (username, cardcode, start_time, end_time, expiredate, startdate) VALUES ('$username', '$cardcode', '$shour', '$ehour', '$expiredate', '$startdate' );");
print 'aggiunto correttamente!<br>';
print '<a href="javascript:history.back()"> aggiungi un alto utente </a>';
}
$db = NULL;
}
catch(PDOException $e)
{
print 'Exception : ' .$e->getMessage();
}

?>
