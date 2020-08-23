<?php
$yearlist = array();
$handle = opendir('.');
while($year = readdir($handle)){
	if ($year == "." || $year == "..") {
		continue;
	}
	if (is_dir("./".$year)) {
		$fff = false;
		$kk = opendir("./".$year."/data");
		while($kkk = readdir($kk)) {
			if ($kkk == "." || $kkk == "..") {
				continue;
			}
			$fff = true;
			break;
		}
		closedir($kk);
		if ($fff) {
			$yearlist[] = $year;
		}
	}
}
closedir($handle);
rsort($yearlist, SORT_NUMERIC);
//var_dump($yearlist);
$maxyear = $yearlist[0];

$pdflist = array();
$handle = opendir('./'.$maxyear.'/data/');
while($pdf = readdir($handle)){
	if ($year == "." || $year == "..") {
		continue;
	}
	if (is_file("./".$maxyear.'/data/'.$pdf)) {
		$pdflist[] = $pdf;
	} 
}
closedir($handle);
rsort($pdflist, SORT_STRING);
//var_dump($pdflist);

$maxdate = "";
$maxY = "";
$maxM = "";
$maxD = "";
$maxNum = "";
foreach($pdflist as $idx => $val){
	preg_match('/^rodong(([0-9]{4})([0-9]{2})([0-9]{2}))-([0-9]{1,2}).pdf$/', $val, $matches);
	if ($maxdate === "" || $maxdate === $matches[1]) {
		$maxdate = $matches[1];
		$maxY = $matches[2];
		$maxM = $matches[3];
		$maxD = $matches[4];
		if ($maxNum < $matches[5]) {
			$maxNum = $matches[5];
		}
	} else if ($maxdate !== $matches[1]) {
		break;
	}
}
$lastestdate = sprintf("%d年%d月%d日号", $maxY, $maxM, $maxD);
//var_dump($lastestdate);
//var_dump($maxNum);
?>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">

<html lang="ja">

<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<title>労働新聞PDFデータサービス【トライアル】 -会員ページ-</title>
	<meta name="keywords" content="">
	<meta name="description" content="">
	<meta http-equiv="Content-Style-Type" content="text/css">
	<link href="../text.css" rel="stylesheet" type="text/css">

<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-33156338-3']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

    </script>

</head>

<body>
<!-- #page ページの整形：中央寄せ等 -->
<div id="page">

<!-- #header 画面上部のヘッド部分 -->
<div id="head">
	<img src="../img/rodong-title2012.png" alt="rodong-title" width="750" height="125">
</div>

<!-- #mainmenu メニュー部分 --> 
<div id="menu">
	<ul>
	<li><a href="../index.html">ＨＯＭＥ</a></li>
	<li><a href="../rules.html">利用規定</a></li>
	</ul>
</div>

<h1>ようこそ会員ページへ</h1>

<!-- #submenu 左側スペース -->
<div id="submenu">
	<p>メニュー</p>
	<p><ul>
	<li><a href="../index.html">ＨＯＭＥ</a></li>
	<li><a href="../rules.html">利用規定</a></li>
	</ul></p>
	<p>リンク</p>
	<p><ul>
	<li><a href="http://www.korea-m.com/" target="_blank">会社情報</a></li>
	<li><a href="http://dprkmedia.com/" target="_blank">ＫＰＭデータベース</a></li>
	</ul></p>
</div>

<!-- #main 本文スペース -->
<div id="main">

	<h2>最新号</h2>
	<p><font size="3"><?php print $lastestdate; ?><br>
	<?php
	for ($i=1 ; $i <= $maxNum ; $i++){
		print '<a href="http://www.korea-copy.com/rodong/'.$maxyear.'/data/rodong'.$maxdate.'-'.$i.'.pdf">'.$i.'面</a> ';
	}
	?>
    <br>

    <h2>過去号</h2>
	<dl>
	<?php
	foreach ($yearlist as $idx => $val){
		print '<img src="../img/folder.gif" alt="folder" width="25" height="25">';
		print '<a href="http://www.korea-copy.com/rodong/'.$val.'/index.php"><font size="4">'.$val.'</font></a><br>';
		if ($idx == 0) {
			print '<br>';
		}
	}
	?>
	</dl>
</div>

<!-- #foot 画面一番下 -->
<div id="foot">
	<p>Copyright(C) KOREA MEDIA. All rights reserved.<br>
	このホームページに掲載されている記事・写真の無断転載を禁じます。</p>
</div>

</div>

</body>
</html>
