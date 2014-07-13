<?php
$db = new SQLite3('./logger.db');

echo '<table>';
echo '<tr><td>utente</td><td>Cardcode</td><td><td></tr>';

$results = $db->query('SELECT * FROM visitorsallowedusers');
while ($row = $results->fetchArray()) {
echo '<tr><td>';
echo $row['username'];
echo '</td><td>';
echo $row['cardcode'];
echo '</td><td>';
echo '<form action="delvisituser.php" method="POST"><input type="hidden" name="id" value=';
echo $row['id'];
echo '><input type="submit" value="Cancella"></form>';
echo '</td></tr>';
}
echo '</table>';
?>
