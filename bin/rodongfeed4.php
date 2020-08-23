<?php
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
	
	$fname = "C:/www.korea-copy.com/ftpdata/".$zip_fname;

	$zip = new ZipArchive();
	$res = $zip->open($fname);
	if ($res === true) {
		removeDir('C:/www.korea-copy.com/ftpdata/zip');
		mkdir('C:/www.korea-copy.com/ftpdata/zip');
		$zip->extractTo('C:/www.korea-copy.com/ftpdata/zip/');
		$zip->close();
		sleep(10);

		$xmlfname = "2017-11-29.xml";
		if (file_exists("C:/www.korea-copy.com/ftpdata/zip/".$xmlfname)) {
			$dom = new DOMDocument('1.0', 'UTF-8');
			$dom->load("C:/www.korea-copy.com/ftpdata/zip/".$xmlfname);

			$root = $dom->getElementsByTagName('topics')->item(0);
			$topic = $root->getElementsByTagName('topic');
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
				if (mb_strlen($author) > 45) {
					$author = "";
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

				$sql = "INSERT INTO [KPPress].[dbo].[Articles] ([ArticleID], [WriterName], [Email], [Title], [SubTitle], [LanguageID], [SectionID], [MediaID], [LocalID], [SubNayong], [SubNayongChk], [Nayong1] ,[Nayong2] ,[AuthID] ,[InputDateTime], [JunsongDateTime], [LastLoginUserID], [Importance], [LinkArticles], [chkPhoto]) VALUES (?, ?, ? ,?, ?, '101', '0', '1001', '0', ?, NULL, ?, ?, ?, dateadd(day, -1,Getdate()), dateadd(day, -1,Getdate()), '', '1', '', ?)";
				$ret = sqlsrv_query($msdb, $sql, array($max_articleid, $WriterName, $Email, $Title, $SubTitle, $SubNayong, $Nayong1, $Nayong2, $AuthID, $chkPhoto));
				if ($ret === false) {
					//print var_export(sqlsrv_errors(), true) . "\n";
					file_put_contents('rodong_err.txt', var_export(sqlsrv_errors(), true), FILE_APPEND);
					file_put_contents('rodong_err.txt', var_export(array($max_articleid, $WriterName, $Email, $Title, $SubTitle, $SubNayong, $Nayong1, $Nayong2, $AuthID, $chkPhoto), true), FILE_APPEND);
				}

				file_put_contents('test_0.sql', var_export(array($max_articleid, $WriterName, $Email, $Title, $SubTitle, $SubNayong, $Nayong1, $Nayong2, $AuthID, $chkPhoto), true), FILE_APPEND);
			}


			// ftp to dow jones
			$djfname = "Rodong 2017-11-29.xml";
			copy("C:/www.korea-copy.com/ftpdata/zip/".$xmlfname, "C:/www.korea-copy.com/ftpdata/zip/".$djfname);

			$ftp = ftp_connect("provider.dowjones.com");
			if ($ftp === FALSE) {
				print "failure of the connect to ftp server (provider.dowjones.com).\n";

			} else {
				$res = ftp_login($ftp, "CPPKORME3", "Tu8e6h6Cupr8wafuHEwr");
				if ($res === FALSE) {
					print "failure of the login to ftp server (provider.dowjones.com).\n";
					ftp_close($ftp);
					
				} else {
					$res = ftp_pasv($ftp, true);
					if ($res === FALSE) {
						print "failure of the change pasv mode.\n";
						ftp_close($ftp);
						
					} else {
						$res = ftp_put($ftp, $djfname, "C:/www.korea-copy.com/ftpdata/zip/".$djfname, FTP_BINARY);
						if ($res === FALSE) {
							print "failure of the put file ($djfname).\n";
						} else {
							_sendmail2('suyama@btl.co.jp', 'suyama@btl.co.jp', "C:/www.korea-copy.com/ftpdata/zip/".$djfname);
						}
							
						ftp_close($ftp);
					}
				}
			}


		}else{
			$logstr = sprintf("%s [FILE NOT FOUND $xmlfname].\n", date("Y/m/d H:i:s"));
			file_put_contents('test_0.sql', $logstr, FILE_APPEND);
			print "[file not found]";
		}
	} else {
		$logstr = sprintf("%s [ZIP FILE OPEN ERROR $fname].\n", date("Y/m/d H:i:s"));
		file_put_contents('test_0.sql', $logstr, FILE_APPEND);
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

//function proc_ftp($pdf_fname, $zip_fname, $zip_fname2)
function proc_ftp($pdf_fname, $zip_fname, $pic_fname)
{
	$ftp = ftp_connect("210.113.28.219");
	if ($ftp === FALSE) {
		print "failure of the connect to ftp server (210.113.28.219).\n";
		return false;
	}

	$res = ftp_login($ftp, "Rodong", "Rod!#ong!yna");
	if ($res === FALSE) {
		print "failure of the login to ftp server (210.113.28.219).\n";
		ftp_close($ftp);
		return false;
	}

	$res = ftp_pasv($ftp, true);
	if ($res === FALSE) {
		print "failure of the change pasv mode.\n";
		ftp_close($ftp);
		return false;
	}

	$res = ftp_chdir($ftp, "Rodong_Article");
	if ($res === FALSE) {
		print "failure of the change directory (Rodong_Article).\n";
		ftp_close($ftp);
		return false;
	}

	print "connected.\n";

	$res = ftp_put($ftp, $pdf_fname, "C:/www.korea-copy.com/ftpdata/".$pdf_fname, FTP_BINARY);
	if ($res === FALSE) {
		print "failure of the put file ($pdf_fname).\n";
		ftp_close($ftp);
		return false;
	}

	print "success of put the file $pdf_fname\n";

	/*$res = ftp_put($ftp, $zip_fname, "C:/www.korea-copy.com/ftpdata/".$zip_fname, FTP_BINARY);
	if ($res === FALSE) {
		print "failure of the put file ($zip_fname).\n";
		ftp_close($ftp);
		return false;
	}*/

	//print "success of put the file $zip_fname\n";

	//$res = ftp_put($ftp, $zip_fname, "C:/www.korea-copy.com/ftpdata/".$zip_fname2, FTP_BINARY);
	//if ($res === FALSE) {
	//	print "failure of the put file ($zip_fname2).\n";
	//	ftp_close($ftp);
	//	return false;
	//}
	//
	//print "success of put the file $zip_fname2\n";


	ftp_close($ftp);
	

	/*$ftp = ftp_connect("210.113.28.219");
	if ($ftp === FALSE) {
		print "failure of the connect to ftp server (210.113.28.219).\n";
		return false;
	}

	$res = ftp_login($ftp, "Rodong", "Rod!#ong!yna");
	if ($res === FALSE) {
		print "failure of the login to ftp server (210.113.28.219).\n";
		ftp_close($ftp);
		return false;
	}

	$res = ftp_pasv($ftp, true);
	if ($res === FALSE) {
		print "failure of the change pasv mode.\n";
		ftp_close($ftp);
		return false;
	}

	$res = ftp_chdir($ftp, "Rodong_Photo");
	if ($res === FALSE) {
		print "failure of the change directory (Rodong_Photo).\n";
		ftp_close($ftp);
		return false;
	}

	print "connected.\n";

	$res = ftp_put($ftp, $pic_fname, "C:/www.korea-copy.com/ftpdata/".$pic_fname, FTP_BINARY);
	if ($res === FALSE) {
		print "failure of the put file ($pic_fname).\n";
		ftp_close($ftp);
		return false;
	}

	print "success of put the file $pic_fname\n";

	ftp_close($ftp);*/
	
	return true;
}

function proc_ftp_for_newrodong($pdf_fname, $zip_fname, $pic_fname)
{
	$ftp = ftp_connect("www.dprkmedia.net");
	if ($ftp === FALSE) {
		print "failure of the connect to ftp server (www.dprkmedia.net).\n";
		return false;
	}

	$res = ftp_login($ftp, "devuser", "negoro##00");
	if ($res === FALSE) {
		print "failure of the login to ftp server (www.dprkmedia.net).\n";
		ftp_close($ftp);
		return false;
	}

	$res = ftp_pasv($ftp, true);
	if ($res === FALSE) {
		print "failure of the change pasv mode.\n";
		ftp_close($ftp);
		return false;
	}

	print "connected.\n";

	$year = date('Y');
	$res = ftp_chdir($ftp, "/data/rodong/pdf/$year/");
	if ($res === FALSE) {
		print "failure of the change directory (1).\n";
		ftp_close($ftp);
		return false;
	}

	$res = ftp_put($ftp, $pdf_fname, "C:/www.korea-copy.com/ftpdata/".$pdf_fname, FTP_BINARY);
	if ($res === FALSE) {
		print "failure of the put file ($pdf_fname).\n";
		ftp_close($ftp);
		return false;
	}

	print "success of put the file $pdf_fname\n";

	$res = ftp_chdir($ftp, "/data/rodong/photo/$year/zip/");
	if ($res === FALSE) {
		print "failure of the change directory (2).\n";
		ftp_close($ftp);
		return false;
	}

	$res = ftp_put($ftp, $pic_fname, "C:/www.korea-copy.com/ftpdata/".$pic_fname, FTP_BINARY);
	if ($res === FALSE) {
		print "failure of the put file ($pic_fname).\n";
		ftp_close($ftp);
		return false;
	}

	print "success of put the file $pic_fname\n";

	$res = ftp_chdir($ftp, "/data/rodong/text/$year/");
	if ($res === FALSE) {
		print "failure of the change directory (3).\n";
		ftp_close($ftp);
		return false;
	}

	$res = ftp_put($ftp, $zip_fname, "C:/www.korea-copy.com/ftpdata/".$zip_fname, FTP_BINARY);
	if ($res === FALSE) {
		print "failure of the put file ($zip_fname).\n";
		ftp_close($ftp);
		return false;
	}

	print "success of put the file $zip_fname\n";

	ftp_close($ftp);

	return true;
}

function proc_ftp_transdata($csv_fname)
{
	$ftp = ftp_connect("www.dprkmedia.net");
	if ($ftp === FALSE) {
		print "failure of the connect to ftp server (www.dprkmedia.net).\n";
		return false;
	}

	$res = ftp_login($ftp, "devuser", "negoro##00");
	if ($res === FALSE) {
		print "failure of the login to ftp server (www.dprkmedia.net).\n";
		ftp_close($ftp);
		return false;
	}

	$res = ftp_pasv($ftp, true);
	if ($res === FALSE) {
		print "failure of the change pasv mode.\n";
		ftp_close($ftp);
		return false;
	}

	print "connected.\n";

	$year = date('Y');
	$res = ftp_chdir($ftp, "/data/rodong/text/$year/");
	if ($res === FALSE) {
		print "failure of the change directory (3).\n";
		ftp_close($ftp);
		return false;
	}

	$res = ftp_put($ftp, $csv_fname, "C:/www.korea-copy.com/ftpdata/".$csv_fname, FTP_BINARY);
	if ($res === FALSE) {
		print "failure of the put file ($csv_fname).\n";
		ftp_close($ftp);
		return false;
	}

	print "success of put the file $csv_fname\n";

	ftp_close($ftp);

	return true;
}

//function proc_mail($pdf_fname, $zip_fname, $zip_fname2)
function proc_mail($pdf_fname, $zip_fname, $pic_fname)
{
	_sendmail('rodong1@yna.co.kr', 'sangho@qa2.so-net.ne.jp', $pdf_fname);
//	_sendmail('rodong1@yna.co.kr', 'sangho@qa2.so-net.ne.jp', $zip_fname);
//	_sendmail('rodong1@yna.co.kr', 'sangho@qa2.so-net.ne.jp', $pic_fname);
	//_sendmail('rodong1@yna.co.kr', 'sangho@qa2.so-net.ne.jp', $zip_fname2);
}

function _sendmail($to, $from, $file)
{
	$mailTo      = $to;
	$mailSubject = 'Rodong Article '.$file;
	$mailMessage = 'Rodong Article '.$file;
	 
	$dir = 'C:/www.korea-copy.com/ftpdata/';
	$fileName    = $dir.$file;
	 
	$mailFrom    = $from;
	$returnMail  = $from;
	 
	mb_language("Ja") ;
	mb_internal_encoding("UTF-8");
	 
	$header  = "From: $mailFrom\r\n";
	$header .= "MIME-Version: 1.0\r\n";
	$header .= "Content-Type: multipart/mixed; boundary=\"__PHPRECIPE__\"\r\n";
	//$header .= "Bcc: suyama@btl.co.jp, sangho@qa2.so-net.ne.jp\r\n";
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
//	 $attachEncode="hhh";
	 
	$body .= "Content-Type: image/jpeg; name=\"$file\"\r\n";
	$body .= "Content-Transfer-Encoding: base64\r\n";
	$body .= "Content-Disposition: attachment; filename=\"$file\"\r\n";
	$body .= "\r\n";
	$body .= chunk_split($attachEncode) . "\r\n";
	$body .= "--__PHPRECIPE__--\r\n";
	 
	//$result = mb_send_mail($mailTo, $mailSubject, $body, $header,'-f' . $returnMail);
	$result = mb_send_mail("suyama@btl.co.jp", $mailSubject, $body, $header,'-f' . $returnMail);
	 
	if($result){
		echo 'mail sent ('.$file.').'."\n";
	}else{
		echo 'failure of th send mail. '.$file."\n";
	}

	return true;
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

function main()
{
	$pdf_fname = date("Y.m.d") . ".pdf";
	//$zip_fname = date("Y-m-d") . "(1).zip";
	//$zip_fname2 = date("Y-m-d") . "(2).zip";
	$zip_fname = date("Y-m-d") . ".zip";
	$pic_fname = date("Y-m-d") . "(photo).zip";

	$pdf_fname = "2017.12.09.pdf";
	$zip_fname = "2017-11-29.zip";
	$pic_fname = "2017-11-29(photo).zip";

	$hh = date("H");
	$mm = date("i");

	//if (file_exists("C:/www.korea-copy.com/ftpdata/".$pdf_fname) && file_exists("C:/www.korea-copy.com/ftpdata/".$zip_fname)&& file_exists("C:/www.korea-copy.com/ftpdata/".$zip_fname2)) {
//	if (file_exists("C:/www.korea-copy.com/ftpdata/".$pdf_fname) && file_exists("C:/www.korea-copy.com/ftpdata/".$zip_fname) && file_exists("C:/www.korea-copy.com/ftpdata/".$pic_fname)) {
//	if (file_exists("C:/www.korea-copy.com/ftpdata/".$pdf_fname) && file_exists("C:/www.korea-copy.com/ftpdata/".$zip_fname)) {

		if (!file_exists("C:/www.korea-copy.com/ftpdata/filesent")) {
			//proc_ftp($pdf_fname, $zip_fname, $zip_fname2);
			//proc_mail($pdf_fname, $zip_fname, $zip_fname2);
//			proc_ftp($pdf_fname, $zip_fname, $pic_fname);
			proc_mail($pdf_fname, $zip_fname, $pic_fname);

			//proc_ftp_for_newrodong($pdf_fname, $zip_fname, $pic_fname);
			
			//touch("C:/www.korea-copy.com/ftpdata/filesent");

			$logstr = sprintf("%s PDF,ZIP sent.\n", date("Y/m/d H:i:s"));
			file_put_contents('test_0.sql', $logstr, FILE_APPEND);
		}

//		if (!file_exists("C:/www.korea-copy.com/ftpdata/feedcomplete") /*&& $hh >= 8 && $mm >= 15*/) {
//			proc_feed($zip_fname);
//			touch("C:/www.korea-copy.com/ftpdata/feedcomplete");
//
//			$logstr = sprintf("%s XML feeded (0815).\n", date("Y/m/d H:i:s"));
//			file_put_contents('test_0.sql', $logstr, FILE_APPEND);
//		}

//		if (file_exists("C:/www.korea-copy.com/ftpdata/filesent") /*&& $hh >= 8 && $mm >= 30*/) {
//
//			$yyyy = date("Y");
//			$ret = copy("C:/www.korea-copy.com/ftpdata/".$pdf_fname, "C:/www.korea-copy.com/rodong/".$yyyy."/data/".$pdf_fname);
//
//			rename("C:/www.korea-copy.com/ftpdata/".$pdf_fname, "C:/www.korea-copy.com/finish/".$pdf_fname);
//			rename("C:/www.korea-copy.com/ftpdata/".$zip_fname, "C:/www.korea-copy.com/finish/".$zip_fname);
//			rename("C:/www.korea-copy.com/ftpdata/".$pic_fname, "C:/www.korea-copy.com/finish/".$pic_fname);
//			//rename("C:/www.korea-copy.com/ftpdata/".$zip_fname2, "C:/www.korea-copy.com/finish/".$zip_fname2);
//
//			$logstr = sprintf("%s korea-copy copied.\n", date("Y/m/d H:i:s"));
//			file_put_contents('test_0.sql', $logstr, FILE_APPEND);
//
//			unlink("C:/www.korea-copy.com/ftpdata/filesent");
//			unlink("C:/www.korea-copy.com/ftpdata/feedcomplete");
//
//			$logstr = sprintf("%s unlink files.\n", date("Y/m/d H:i:s"));
//			file_put_contents('test_0.sql', $logstr, FILE_APPEND);
//		}
//	}

	/*$trans_csv_fname = date("Ymd") . ".csv";
	if (file_exists("C:/www.korea-copy.com/ftpdata/".$trans_csv_fname)) {
		proc_ftp_transdata($trans_csv_fname);
		_sendmail2('suyama@btl.co.jp', 'suyama@btl.co.jp', "C:/www.korea-copy.com/ftpdata/".$trans_csv_fname);
		rename("C:/www.korea-copy.com/ftpdata/".$trans_csv_fname, "C:/www.korea-copy.com/finish/".$trans_csv_fname);
	}*/

	return true;
}

main();
exit;
?>
