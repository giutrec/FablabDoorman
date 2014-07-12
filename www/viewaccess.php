<?php
$db = new SQLite3('./logger.db');

echo '<table>';
echo '<tr><td>carcode</td><td>datetime</td></tr>';

$results = $db->query('SELECT * FROM intothedoor');
while ($row = $results->fetchArray()) {
echo '<tr><td>';
echo $row['cardcode'];
echo '</td><td>';
echo $row['datetime'];
echo '</td>';
echo '</tr>';
}
echo '</table>';
?>
