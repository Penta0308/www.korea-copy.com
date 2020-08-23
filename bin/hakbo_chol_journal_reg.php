<?php
error_reporting(E_ALL ^ E_NOTICE);

/*if (file_exists("C:/www.korea-copy.com/minju/ftpdata/Minju ".date("Y.m.d").".pdf")
 && file_exists("C:/www.korea-copy.com/minju/ftpdata/Minju ".date("Y-n-j").".zip")) {
	rename(
	  "C:/www.korea-copy.com/minju/ftpdata/Minju ".date("Y.m.d").".pdf",
	  "C:/www.korea-copy.com/minju/".date("Y")."/data/Minju ".date("Y.m.d").".pdf"
	);
	rename(
	  "C:/www.korea-copy.com/minju/ftpdata/Minju ".date("Y-n-j").".zip",
	  "C:/www.korea-copy.com/minju/Minju ".date("Y-n-j").".zip"
	);
	proc_feed("Minju ".date("Y-n-j") . ".zip");

	rename(
	  "C:/www.korea-copy.com/minju/Minju ".date("Y-n-j").".zip",
	  "C:/www.korea-copy.com/finish/Minju ".date("Y-n-j").".zip"
	);
	unlink("C:/www.korea-copy.com/minju/ftpdata/minju_complete.txt");
}*/

proc_feed("Hakbo(Chol) 2019-2.zip"); ////////////////////////////////////////////////////////////
print "done.\n";
exit;

function proc_feed($zip_fname)
{
	$serverName = "localhost\\SQLEXPRESS";
	$connectionInfo = array("UID"=>"sa",
					"PWD"=>"0ulBTrIb",
					"Database"=>"KPPress",
					"CharacterSet"=>"UTF-8");

	$msdb = sqlsrv_connect($serverName, $connectionInfo);
	if ($msdb === FALSE){
		print "failed to connect to sql server\n";
		print var_export(sqlsrv_errors(), true);
		exit;
	} 
	
	$fname = "C:/www.korea-copy.com/minju/".$zip_fname;
	print $fname."\n";

	$zip = new ZipArchive();
	$res = $zip->open($fname);
	//$ret = true;
	if ($res === true) {
		print "[ZIP OPEN OK]\n";
		
		//removeDir('C:/www.korea-copy.com/minju/hakbo_chol_zip_tmp');
		mkdir('C:/www.korea-copy.com/minju/hakbo_chol_zip_tmp');
		$zip->extractTo('C:/www.korea-copy.com/minju/hakbo_chol_zip_tmp/');
		$zip->close();

		$xmlfname = "Hakbo(Chol) 2019-2.xml"; ////////////////////////////////////////////////////////////////////

		$ww = explode(" ", $xmlfname);
		$xmldfile_exploded = explode(".", $ww[1]);
		$xmldfile_exploded2 = explode("-", $xmldfile_exploded[0]);
		$BalHengYear = $xmldfile_exploded2[0];
		$GwonHo = $xmldfile_exploded2[1];
		
		if (file_exists("C:/www.korea-copy.com/minju/hakbo_chol_zip_tmp/".$xmlfname)) {
			print "[FOUNT FILE ($xmlfname)]\n";
			
			$dom = new DOMDocument('1.0', 'UTF-8');
			$dom->load("C:/www.korea-copy.com/minju/hakbo_chol_zip_tmp/".$xmlfname);

			$root = $dom->getElementsByTagName('topics')->item(0);
			$topic = $root->getElementsByTagName('topic');
			$sqllist = array();
			foreach ($topic as $node) {
				print "[HAKBO CHOL JOURNAL ARTICLE FOUNT]\n";
				$perio = $node->getElementsByTagName('perio')->item(0)->nodeValue;
				$date = $node->getElementsByTagName('date')->item(0)->nodeValue;
				$side = $node->getElementsByTagName('side')->item(0)->nodeValue;
				//$no = $node->getElementsByTagName('no')->item(0)->nodeValue;
				$ltitle = $node->getElementsByTagName('ltitle')->item(0)->nodeValue;
				$kind = $node->getElementsByTagName('kind')->item(0)->nodeValue;
				$field = $node->getElementsByTagName('field')->item(0)->nodeValue;
				$region = $node->getElementsByTagName('region')->item(0)->nodeValue;
				$title = $node->getElementsByTagName('title')->item(0)->nodeValue;
				$stitle = $node->getElementsByTagName('stitle')->item(0)->nodeValue;
				$text = $node->getElementsByTagName('text')->item(0)->nodeValue;
				$author = $node->getElementsByTagName('author')->item(0)->nodeValue;
				$w = explode("\n", $text);

				$sn = "";
				foreach($w as $www) {
					$sn = trim($www);
					$sn = mb_substr($sn, 0, 190, 'utf-8');
					if ($sn != "") {
						if (mb_substr($sn, -1) == '.') {
							$sn = $sn . "..";
						} else {
							$sn = $sn . "...";
						}
						break;
					}
				}

				if (trim($kind) != ""){
					$title = "<".$kind."> ".$title;
				}
				if (trim($ltitle) != ""){
					$title = "<".$ltitle."> ".$title;
				}
	
				$WriterName = $author;
				$Title = __trim($title);
				$SubTitle = __trim($stitle);
				$SubNayong = $sn;
				$Nayong1 = mb_substr($text, 0, 1800, 'utf-8');
				$Nayong2 = str_replace($Nayong1, "", $text);

				$sql = "INSERT INTO [KPPress].[dbo].[JournalsArticle] ([JArticleID], [Title], [TitleEng], [Writers], [Nayong1] ,[Nayong2], [JournalID], [BalHengYear], [GwonHo], [Rugye], [Page], [JunSongCher], [JunSongDate], [FileName], [FileSize], [Status], [InputDateTime]) VALUES (?, ?, '', ?, ? ,?, ?, ?, ?, ?, '-', '', '', ?, ?, ?, Getdate())";
				
				$sqllist[] = array(
					'sql' => $sql,
					'params' => array('dummy', $title, $WriterName, $Nayong1, $Nayong2, '2027', $BalHengYear, $GwonHo, '0', '', '', '1')
				);
			}

			$journal_pdf_fname = sprintf("C:/www.korea-copy.com/minju/Hakbo(Chol) %04d.%d.pdf", $BalHengYear, $GwonHo);
			if (file_exists($journal_pdf_fname)) {
				$sql = "INSERT INTO [KPPress].[dbo].[JournalsArticle] ([JArticleID], [Title], [TitleEng], [Writers], [Nayong1] ,[Nayong2], [JournalID], [BalHengYear], [GwonHo], [Rugye], [Page], [JunSongCher], [JunSongDate], [FileName], [FileSize], [Status], [InputDateTime]) VALUES (?, ?, '', ?, ? ,?, ?, ?, ?, ?, '-', '', '', ?, ?, ?, Getdate())";

				$sqlw = "select MAX(JArticleID) AS maxid from KPPress.dbo.JournalsArticle";
				$result = sqlsrv_query($msdb, $sqlw);
				$row = sqlsrv_fetch_array($result);
				$max_articleid = $row['maxid'] + 1;
				
				$FileName = sprintf("/Uploaded/Journal/2027/KPJ_%d.pdf", $max_articleid);
				$FileSize = filesize($journal_pdf_fname);

				$title = "학보(철학) PDF ".$BalHengYear."-".$GwonHo;

				$params = array($max_articleid, $title, '', '', '', '2027', $BalHengYear, $GwonHo, '0', $FileName, $FileSize, '1');

				$ret = sqlsrv_query($msdb, $sql, $params);
				if ($ret === false) {
					//print var_export(sqlsrv_errors(), true) . "\n";
					file_put_contents('hakbo_chol_journal_err.txt', var_export(sqlsrv_errors(), true), FILE_APPEND);
					file_put_contents('hakbo_chol_journal.txt', var_export($sql['params'], true), FILE_APPEND);
				}
				file_put_contents('hakbo_chol_journal.txt', var_export($sql, true), FILE_APPEND);
				file_put_contents('hakbo_chol_journal.txt', var_export($params, true), FILE_APPEND);

				@copy($journal_pdf_fname, sprintf("C:/WebSite/KPM%s", $FileName));
			}
			sleep(1);

			//$sqllist = array_reverse($sqllist);
			foreach ($sqllist as $sql) {
				$sqlw = "select MAX(JArticleID) AS maxid from KPPress.dbo.JournalsArticle";
				$result = sqlsrv_query($msdb, $sqlw);
				$row = sqlsrv_fetch_array($result);
				$max_articleid = $row['maxid'] + 1;

				$sql['params'][0] = $max_articleid;

				file_put_contents('hakbo_chol_journal.txt', var_export($sql['sql'], true), FILE_APPEND);
				file_put_contents('hakbo_chol_journal.txt', var_export($sql['params'], true), FILE_APPEND);
				
				$ret = sqlsrv_query($msdb, $sql['sql'], $sql['params']);
				if ($ret === false) {
					//print var_export(sqlsrv_errors(), true) . "\n";
					file_put_contents('hakbo_chol_journal_err.txt', var_export(sqlsrv_errors(), true), FILE_APPEND);
					file_put_contents('hakbo_chol_journal.txt', var_export($sql['params'], true), FILE_APPEND);
				}
				sleep(1);
			}


			//_sendmail2('suyama@btl.co.jp', 'suyama@btl.co.jp', "C:/www.korea-copy.com/minju/hakbo_chol_zip_tmp/".$xmlfname);
			
		}else{
			print "[file not found]";
		}
	} else {
		print "error 1[$res]\n";
	}

	sqlsrv_free_stmt($result);
	sqlsrv_close($msdb);
}


function __trim($str)
{
	$str = trim($str);
	$str = preg_replace('/[\n\r\t]/', ' ', $str);
	$str = preg_replace('/\s(?=\s)/', ' ', $str);
	return $str;
}


function removeDir( $dir ) {

    $cnt = 0;

    $handle = opendir($dir);
    if (!$handle) {
        return ;
    }

    while (false !== ($item = readdir($handle))) {
        if ($item === "." || $item === "..") {
            continue;
        }

        $path = $dir . DIRECTORY_SEPARATOR . $item;

        if (is_dir($path)) {
            $cnt = $cnt + removeDir($path);
        }
        else {
            unlink($path);
        }
    }
    closedir($handle);

    if (!rmdir($dir)) {
        return ;
    }
}

function _sendmail2($to, $from, $file)
{
	$mailTo      = $to;
	$mailSubject = 'Hakbo Chol Journal Article '.$file;
	$mailMessage = 'Hakbo Chol Journal Article '.$file;
	 
	//$dir = 'C:/www.korea-copy.com/ftpdata/';
	$fileName    = $file;
	$file = basename($fileName);
	 
	$mailFrom    = $from;
	$returnMail  = $from;
	 
	mb_language("Ja") ;
	mb_internal_encoding("UTF-8");
	 
	$header  = "From: $mailFrom\r\n";
	$header .= "MIME-Version: 1.0\r\n";
	$header .= "Content-Type: multipart/mixed; boundary=\"__PHPRECIPE__\"\r\n";
	$header .= "\r\n";
	 
	$body  = "--__PHPRECIPE__\r\n";
	$body .= "Content-Type: text/plain; charset=\"ISO-2022-JP\"\r\n";
	$body .= "\r\n";
	$body .= $mailMessage . "\r\n";
	$body .= "--__PHPRECIPE__\r\n";
	 
	$handle = fopen($fileName, 'r');
	$attachFile = fread($handle, filesize($fileName));
	fclose($handle);
	$attachEncode = base64_encode($attachFile);
	 
	$body .= "Content-Type: image/jpeg; name=\"$file\"\r\n";
	$body .= "Content-Transfer-Encoding: base64\r\n";
	$body .= "Content-Disposition: attachment; filename=\"$file\"\r\n";
	$body .= "\r\n";
	$body .= chunk_split($attachEncode) . "\r\n";
	$body .= "--__PHPRECIPE__--\r\n";
	 
	$result = mb_send_mail($mailTo, $mailSubject, $body, $header,'-f' . $returnMail);
	 
	if($result){
		echo 'mail sent ('.$file.').'."\n";
	}else{
		echo 'failure of th send mail. '.$file."\n";
	}

	return true;
}
