<?

/*
ini_set("display_errors",1);
error_reporting(E_ALL);
*/

$lines = file("url.txt", FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
$all = count($lines);
$i=1;

foreach($lines as $line){
	
	// название файла	
    $arr = explode("/", $line);
	$zz = end($arr);
	$arr1 = explode("oformlenie-", $zz);
	$fname = end($arr1);	
	$page = file_get_contents($line);
	// ищем элемент
	$exist_container = preg_match("/<table.*?airports.*?>(.*?)<\/table>/s", $page, $table_html);
	if($exist_container){
		//чистим
		$clean = preg_replace("/<th style.*?>.*?<\/th>/s", "", $table_html[1]);
		$clean = preg_replace("/ style=\".*?\"/s", "", $clean);
		$clean = preg_replace("/<td><a class=\"tooltip2\">.*?<\/td>/s", "", $clean);		
		$clean= str_replace(array("\r\n\r\n", "\r\n", "\r", "\n"), '', $clean);
		$clean = preg_replace("/<a.*?>/s", "", $clean);
		$clean= str_replace('</a>', '', $clean);
		$clean = "<table>".$clean."</table>";
		// пишем в файл
		file_put_contents("result/".$fname.".txt", $clean);		
	}	
	
	if($exist_container) echo "Загружаю...$line ($i из $all)".PHP_EOL;
	else echo "Элемент на странице $line не найден ($i из $all)".PHP_EOL;
	sleep(1);
	$i++;
}


?>