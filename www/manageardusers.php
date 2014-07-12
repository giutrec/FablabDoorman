<?php
$db = new SQLite3('./logger.db');

echo '<table>';
echo '<tr><td>utente</td><td>Cardcode</td><td><td></tr>';

$results = $db->query('SELECT * FROM arduinoallowedusers');
while ($row = $results->fetchArray()) {
echo '<tr><td>';
echo $row['username'];
echo '</td><td>';
echo $row['cardcode'];
echo '</td><td>';
//echo '<form action="modfabuser.php" method="POST"><fieldset> <select name="timeAccessProfile" ><option value="direttivo"'; if ($row['timeAccessProfile'] == "direttivo"){ echo 'selected="selected"'; } echo '>Direttivo</option> <option value="Host">Host</option><option value="ordinario">ordinario</option></select></fieldset><input type="submit" value="modifica"></form>';
echo '<form action="delarduser.php" method="POST"><input type="hidden" name="id" value=';
echo $row['id'];
echo '><input type="submit" value="Cancella"></form>';
echo '</td></tr>';
}
echo '</table>';
?>
