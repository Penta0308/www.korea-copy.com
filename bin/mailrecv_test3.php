<?php
error_reporting(E_ALL ^ E_NOTICE);

proc_feed2("Munhak 2020-2-8.zip");
print "done.\n";
exit;

function proc_feed2($zip_fname)
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

	$zip = new ZipArchive();
	$res = $zip->open($fname);
	if ($res === true) {
		removeDir('C:/www.korea-copy.com/minju/zip');
		mkdir('C:/www.korea-copy.com/minju/zip');
		$zip->extractTo('C:/www.korea-copy.com/minju/zip/');
		$zip->close();

		$xmlfname = date("Y-m-d", strtotime("-1 day")) . ".xml";
		$xmlfname2 = date("Y-n-j", strtotime("-1 day")) . ".xml";
		if (file_exists("C:/www.korea-copy.com/minju/zip/".$xmlfname)) {
			// NOOP
		} else if(file_exists("C:/www.korea-copy.com/minju/zip/".$xmlfname2)) {
			$xmlfname = $xmlfname2;
		}
		$xmlfname = "2020-2-8.xml";

		if (file_exists("C:/www.korea-copy.com/minju/zip/".$xmlfname)) {
			$dom = new DOMDocument('1.0', 'UTF-8');
			$dom->load("C:/www.korea-copy.com/minju/zip/".$xmlfname);

			$root = $dom->getElementsByTagName('topics')->item(0);
			$topic = $root->getElementsByTagName('topic');
			$sqllist = array();
			
			foreach ($topic as $node) {
				$perio = $node->getElementsByTagName('perio')->item(0)->nodeValue;
				$date = $node->getElementsByTagName('date')->item(0)->nodeValue;
				$side = $node->getElementsByTagName('side')->item(0)->nodeValue;
				$no = $node->getElementsByTagName('no')->item(0)->nodeValue;
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

				/*if (mb_strstr($author, '조선중앙통신', false, 'utf-8') !== false) {
					$Email = '조선중앙통신'; 
				} else {
					$Email = ""; 
				}
				if (mb_strstr($author, '조선중앙통신', false, 'utf-8') !== false) {
					$author = '';
				}
				if ($author == '본사기자') {
					$author = '본사';
				} else {
					$author = str_replace("본사기자", "", $author);
					$author = explode(" ", trim($author));
					$author = implode(",", $author);
				}*/

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

				$chkPhoto = '0';
				$AuthID = '303';
				if (trim($Nayong1) == '' && trim($Nayong2) == ""){
					$Nayong1 = " ";
					$chkPhoto = '1';
					$AuthID = '301';
					//continue;
				}

				$sql = "select MAX(articleid) AS maxid from KPPress.dbo.Articles";
				$result = sqlsrv_query($msdb, $sql);
				$row = sqlsrv_fetch_array($result);
				$max_articleid = $row['maxid'] + 1;

				$sql = "INSERT INTO [KPPress].[dbo].[Articles] ([ArticleID], [WriterName], [Email], [Title], [SubTitle], [LanguageID], [SectionID], [MediaID], [LocalID], [SubNayong], [SubNayongChk], [Nayong1] ,[Nayong2] ,[AuthID] ,[InputDateTime], [JunsongDateTime], [LastLoginUserID], [Importance], [LinkArticles], [chkPhoto]) VALUES (?, ?, ? ,?, ?, '101', '0', '1005', '0', ?, NULL, ?, ?, ?, Getdate(), GetDate(), '', '1', '', ?)";
				//$sql = "INSERT INTO [KPPress].[dbo].[Articles] ([ArticleID], [WriterName], [Email], [Title], [SubTitle], [LanguageID], [SectionID], [MediaID], [LocalID], [SubNayong], [SubNayongChk], [Nayong1] ,[Nayong2] ,[AuthID] ,[InputDateTime], [JunsongDateTime], [LastLoginUserID], [Importance], [LinkArticles], [chkPhoto]) VALUES (?, ?, ? ,?, ?, '101', '0', '1005', '0', ?, NULL, ?, ?, ?, dateadd(day, -2,Getdate()), dateadd(day, -2,Getdate()), '', '1', '', ?)";
				$sqllist[] = array(
					'sql' => $sql,
					'params' => array($max_articleid, $WriterName, $Email, $Title, $SubTitle, $SubNayong, $Nayong1, $Nayong2, $AuthID, $chkPhoto)
				);
/*				$ret = sqlsrv_query($msdb, $sql, array($max_articleid, $WriterName, $Email, $Title, $SubTitle, $SubNayong, $Nayong1, $Nayong2, $AuthID, $chkPhoto));
				if ($ret === false) {
					//print var_export(sqlsrv_errors(), true) . "\n";
					file_put_contents('munhak_err.txt', var_export(sqlsrv_errors(), true), FILE_APPEND);
					file_put_contents('munhak_err.txt', var_export(array($max_articleid, $WriterName, $Email, $Title, $SubTitle, $SubNayong, $Nayong1, $Nayong2, $AuthID, $chkPhoto), true), FILE_APPEND);
				}
*/				//file_put_contents('test.sql', var_export(array($max_articleid, $WriterName, $Email, $Title, $SubTitle, $SubNayong, $Nayong1, $Nayong2, $AuthID, $chkPhoto), true), FILE_APPEND);
			}
//var_dump($sqllist);
			$sqllist = array_reverse($sqllist);
			foreach ($sqllist as $sql) {
				$sqlw = "select MAX(articleid) AS maxid from KPPress.dbo.Articles";
				$result = sqlsrv_query($msdb, $sqlw);
				$row = sqlsrv_fetch_array($result);
				$max_articleid = $row['maxid'] + 1;
				
				$sql['params'][0] = $max_articleid;
				
				$ret = sqlsrv_query($msdb, $sql['sql'], $sql['params']);
				if ($ret === false) {
					//print var_export(sqlsrv_errors(), true) . "\n";
					file_put_contents('munhak_err.txt', var_export(sqlsrv_errors(), true), FILE_APPEND);
					file_put_contents('munhak_err.txt', var_export($sql['params'], true), FILE_APPEND);
				}
				sleep(1);
			}
			
		}else{
			print "[file not found]";
		}
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
	$mailSubject = 'Rodong Article '.$file;
	$mailMessage = 'Rodong Article '.$file;
	 
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
