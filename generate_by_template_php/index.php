<?
ini_set("display_errors",1);
error_reporting(E_ALL);

require_once 'SimpleXLSX.php';


if ( $xlsx = SimpleXLSX::parse('data.xlsx')) {			
	foreach ( $xlsx->rows() as $r => $row ) {		
		if($r===0) continue;
		
		$from = "from/".$row[0].".txt";
		$to = "to/".$row[0]."-new.txt";
		
		$page = file_get_contents($from);	
		
		$new = str_replace("#gde#", $row[11], $page);
		$new = str_replace("#regiongde#", $row[14], $new);
		$new = str_replace("#chego#", $row[12], $new);
		$new = str_replace("#regiochego#", $row[15], $new);
		$new = str_replace("#tam#", $row[1], $new);
		$new = str_replace("#tamchego#", $row[3], $new);
		$new = str_replace("#tam#", $row[1], $new);
		$new = str_replace("#tamchego#", $row[3], $new);			
		$new = str_replace("#cod#", $row[6], $new);
		$new = str_replace("#adr#", $row[7], $new);
		$new = str_replace("#phone#", "+".$row[8], $new);
		$new = str_replace("#map#", $row[10], $new);
		$new = str_replace("#tamtable#", $row[19], $new);
		$new = str_replace("#svhtable#", $row[20], $new);			  
		$new = str_replace('"fontSize":"medium"', '{"fontSize":"medium"}', $new);
		$new = str_replace('"className":"service-block"', '{"className":"service-block"}', $new);
		$new = str_replace('"height":30', '{"height":30}', $new);
		$new = str_replace('"level":3', '{"level":3}', $new);		
		$new = str_replace('"className":"st"', '{"className":"st"}', $new);
		$new = str_replace("  ", " ", $new);
		
		$result = file_put_contents($to, $new);
		if($result) echo "Создан файл: ".$row[1].PHP_EOL;
	}
} else {
	echo SimpleXLSX::parseError();
}

?>