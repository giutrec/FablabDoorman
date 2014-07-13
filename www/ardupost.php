<?php
try
{
//open the database
$db = new SQLite3("/mnt/sda1/arduino/www/FablabDoorman/logger.db");

$username = $_POST["username"]; 
$cardcode = $_POST["cardcode"]; 

if ($username =='' || $cardcode == ''){
print 'tutti i campi sono obbligatori <br>';
print '<a href="javascript:history.back()"> torna indietro </a>';
}else{
//Insert record  
$cardcode = strtoupper($cardcode);
$db->exec("INSERT INTO arduinoallowedusers (username, cardcode) VALUES ('$username', '$cardcode');");
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
