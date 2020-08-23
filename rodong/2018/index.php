<?php
$monthname = array(null, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec');

$w = explode("\\", dirname(__FILE__));
$curyear = end($w);
//var_dump($year);

$pdflist = array();
$handle = opendir('./data/');
while($pdf = readdir($handle)){
	if ($pdf == "." || $pdf == "..") {
		continue;
	}
	if (is_file('./data/'.$pdf)) {
		$pdflist[] = $pdf;
	} 
}
closedir($handle);
rsort($pdflist, SORT_STRING);
//var_dump($pdflist);

$monthlist = array();
$daypdfnum = array();
foreach($pdflist as $idx => $val){
	preg_match('/^(([0-9]{4})\.([0-9]{2})\.([0-9]{2})).pdf$/', $val, $matches);
	if (!in_array($matches[2], $monthlist)){
		$monthlist[] = (int)$matches[3];
	}

//if ((int)$matches[2] == 12 && (int)$matches[3] == 18){
//var_dump($matches[4]);
//}
	//if (!isset($daypdfnum[(int)$matches[2]][(int)$matches[3]])){
		//if ((int)$daypdfnum[(int)$matches[3]][(int)$matches[4]] < (int)$matches[4]) {
			$daypdfnum[(int)$matches[3]][(int)$matches[4]] = 1;
		//}
	//}
}


sort($monthlist, SORT_NUMERIC);
//krsort($daypdfnum, SORT_NUMERIC);
//var_dump($monthlist);
//var_dump($daypdfnum);
?>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<html>

<head>
<meta name="robots" content="noindex">
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title><?php print $curyear; ?></title>
</head>

<body>

<table border="1" cellspacing="0">
<tr>
<?php
foreach($monthname as $idx => $val){
	if (is_null($val)) continue;
	if (in_array($idx, $monthlist)){
		print '<th><a href="#'.$val.'">'.$val.'.</a></th>';
	}else{
		print '<th>'.$val.'.</th>';
	}
}
?>
<tr>
</table>

<?php
foreach($daypdfnum as $month => $monthlist){
	if ($month == 0 ) continue;
	$strmonth = $monthname[$month];
	print '<h3 id="'.$strmonth.'">'.$strmonth.'</h3><a name="'.$strmonth.'"></a>';

	foreach($monthlist as $day => $daylist){
		print $strmonth . '. ' . $day . ' ';
		$yyyymmdd = sprintf("%04d%02d%02d", $curyear, $month, $day);
		$mmdd = sprintf("%02d%02d", $month, $day);
		for ($i=1 ; $i<=$daylist ; $i++){
			$fname = sprintf("%04d.%02d.%02d", $curyear, $month, $day);
			//print '<a href="http://www.korea-copy.com/rodong/'.$curyear.'/data/rodong'.$yyyymmdd.'-'.$i.'.pdf">'.$mmdd.'-'.$i.'</a> ';
			print '<a href="http://www.korea-copy.com/rodong/'.$curyear.'/data/'.$fname.'.pdf">PDF</a> ';
		}
		print '<br>';
	}

}
?>

</body>
</html>