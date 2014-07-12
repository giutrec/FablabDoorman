<?php
try
{
//open the database
$db = new SQLite3("/mnt/sda1/arduino/www/FablabDoorman/logger.db");

$id = $_POST["id"]; 

if ($id == ''){
print '<a href="javascript:history.back()"> torna indietro </a>';
}else{
//Insert record  
$db->exec("DELETE from fablaballowedusers where id= '$id';");
print 'utente cancallato!';
print '<a href="javascript:history.back()">torna indietro</a>';
}
$db = NULL;
}
catch(PDOException $e)
{
print 'Exception : ' .$e->getMessage();
}

?>
