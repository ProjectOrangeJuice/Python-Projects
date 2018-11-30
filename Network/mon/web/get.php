<?php
	
	$db = new SQLite3('store.db');
	
    $tablesquery = $db->query("SELECT * FROM 'store'");
    echo "<table style='width:100%'>  <tr>    <td>ID</td>  <td>Address</td>    <td>App</td>      <td>Username</td>       <td>Secure</td>  </tr>";
        
        

    while ($table = $tablesquery->fetchArray(SQLITE3_ASSOC)) {
        
        
        echo "<tr>";
		echo "<td>" . $table['ids']  . "</td>";
	//	echo "<td>" . $table['connection']  . "</td>";
		echo "<td>" . $table['address']  . "</td>";
		echo "<td>" . $table['app']  . "</td>";
		echo "<td>" . $table['username']  . "</td>";
		echo "<td>" . $table['secure']  . "</td>";
		echo "</tr>";
    }
	
	
	?>
