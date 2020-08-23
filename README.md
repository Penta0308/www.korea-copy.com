# www.korea-copy.com
This Source was gained by hacking North Korea's Web Server for agitation.

You can find many information in this source code


#### Source
```PHP
<?php
require_once("Net/POP3.php");             // PEAR Net_POP3
require_once("Mail/mimeDecode.php");      // PEAR MimeDecode

error_reporting(E_ALL ^ E_NOTICE);

$pop3 = new Net_POP3();

// 接続
$res = $pop3->connect ("59.106.182.68", 110);

// ログイン ( APOP )
$res = $pop3->login("dprk-feed-minju.btl", "negoro##00", true);

// 受信メールの更新件数取得
$numMsg = $pop3->numMsg();
print "$numMsg";

for ($i=1 ; $i<=$numMsg ; $i++) {

	$tempfname = "";
	//メールをパースする
	$decoder = new Mail_mimeDecode($pop3->getMsg($i));

	$params['include_bodies'] = true; //ボディを解析する
	$params['decode_bodies'] = true; //ボディをコード変換する
	$params['decode_headers'] = true; //ヘッダをコード変換する
	$structure = $decoder->decode($params);

	//送信者のメールアドレスを抽出
	$mailaddress = $structure->headers['from'];
	$mailsubject = $structure->headers['subject'];
	$date = $structure->headers['date'];

	$timeStamp = strtotime($date);
	$timeDiff = $timeNow-$timeStamp;
	$date = date('Y-m-d H:i:s', $timeStamp);

	if (strstr($mailaddress, "kpeic@star-co.net.kp") !== FALSE) {
		// kpeic からのメール

        $body = "";
        switch(strtolower($structure->ctype_primary)){
            // シングルパート(テキストのみ)
            // -----------------------------------------------------
            case "text":
                $body = $structure->body;
                break;

            // マルチパート(画像付き)
            // -----------------------------------------------------
            case "multipart":
                foreach($structure->parts as $part){

                    switch(strtolower($part->ctype_primary)){
                        // テキスト
                        case "text":
                            $body = $part->body;
                            break;

                        // zip
                        case "application":
                            //拡張子を取得する(小文字に変換
                            $type = strtolower($part->ctype_secondary);

                            if($type != "octet-stream"){
                                continue;
                            }

							$part->ctype_parameters['name'] = str_replace("minju", "Minju", $part->ctype_parameters['name']);
							$part->ctype_parameters['name'] = str_replace("munhak", "Munhak", $part->ctype_parameters['name']);
							file_put_contents("C:/www.korea-copy.com/minju/".$part->ctype_parameters['name'], $part->body);

							$ss = "Minju " . date("Y-m-d") . ".zip";
							$ss2 = "Minju " . date("Y-n-j") . ".zip";
							if ($part->ctype_parameters['name'] == $ss || $part->ctype_parameters['name'] == $ss2) {
								if (file_exists("C:/www.korea-copy.com/minju/".$part->ctype_parameters['name'])) {
									proc_feed($part->ctype_parameters['name']);
									unlink("C:/www.korea-copy.com/minju/".$part->ctype_parameters['name']);
								}
							} else {
								$ss = "Munhak " . date("Y-m-d", strtotime("-1 day")) . ".zip";
								$ss2 = "Munhak " . date("Y-n-j", strtotime("-1 day")) . ".zip";
								if ($part->ctype_parameters['name'] == $ss || $part->ctype_parameters['name'] == $ss2) {
									if (file_exists("C:/www.korea-copy.com/minju/".$part->ctype_parameters['name'])) {
										proc_feed2($part->ctype_parameters['name']);
										unlink("C:/www.korea-copy.com/minju/".$part->ctype_parameters['name']);
									}
								}
							}
                            
                            break;
                    }
                }
                break;
            default:
                $body = ""; 
        }
			
		
	} else {
		// 上記以外
	}

	// データを取得したら削除マーク(実際の削除は　$pop3->disconnect(); 時)
	$pop3->deleteMsg($i);
}





// 接続解除
$pop3->disconnect();
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

	if (file_exists($fname)) {
		$logstr = sprintf("%s [FILE FOUND (feed1) $fname].\n", date("Y/m/d H:i:s"));
		file_put_contents('test_2.sql', $logstr, FILE_APPEND);
	} else {
		$logstr = sprintf("%s [FILE NOT FOUND (feed1) $fname].\n", date("Y/m/d H:i:s"));
		file_put_contents('test_2.sql', $logstr, FILE_APPEND);
	}

	$zip = new ZipArchive();
	$res = $zip->open($fname);
	if ($res === true) {
		removeDir('C:/www.korea-copy.com/minju/zip_tmp');
		$qq = mkdir('C:/www.korea-copy.com/minju/zip_tmp');

		if ($qq == true) {
			$logstr = sprintf("%s [mkdir (feed1) success].\n", date("Y/m/d H:i:s"));
			file_put_contents('test_2.sql', $logstr, FILE_APPEND);
		} else {
			$logstr = sprintf("%s [mkdir (feed1) fail].\n", date("Y/m/d H:i:s"));
			file_put_contents('test_2.sql', $logstr, FILE_APPEND);
		}
		
		
		$zip->extractTo('C:/www.korea-copy.com/minju/zip_tmp/');
		$zip->close();
		sleep(10);

		$xmlfname = date("Y-m-d") . ".xml";
		$xmlfname2 = date("Y-n-j") . ".xml";
		if (file_exists("C:/www.korea-copy.com/minju/zip_tmp/".$xmlfname)) {
			// NOOP
		} else if(file_exists("C:/www.korea-copy.com/minju/zip_tmp/".$xmlfname2)) {
			$xmlfname = $xmlfname2;
		}
		$xmlfname = date("Y-n-j") . ".xml";
		
		if (file_exists("C:/www.korea-copy.com/minju/zip_tmp/".$xmlfname)) {
			$dom = new DOMDocument('1.0', 'UTF-8');
			$dom->load("C:/www.korea-copy.com/minju/zip_tmp/".$xmlfname);

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

				switch ($field) {
					case '정치':
						$field = '101';
						break;
					case '외교':
						$field = '102';
						break;
					case '경제':
						$field = '103';
						break;
					case '사회':
						$field = '104';
						break;
					case '문호':
						$field = '105';
						break;
					case '정보과학':
						$field = '106';
						break;
					case '체육':
						$field = '107';
						break;
					case '사설':
					case '론평':
						$field = '108';
						break;
					default:
						$field = '0';
						break;
				}

				switch ($region) {
					case '평양시':
						$region = '101';
						break;
					case '개성시':
						$region = '102';
						break;
					case '남포시':
						$region = '103';
						break;
					case '라선시':
						$region = '104';
						break;
					case '평안북도':
					case '평안남도':
						$region = '105';
						break;
					case '자강도':
						$region = '106';
						break;
					case '량강도':
						$region = '107';
						break;
					case '함경북도':
					case '함경남도':
						$region = '108';
						break;
					case '황해북도':
					case '황해남도':
						$region = '109';
						break;
					case '강원도':
						$region = '110';
						break;
					default:
						$region = '0';
						break;
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

				$sql = "INSERT INTO [KPPress].[dbo].[Articles] ([ArticleID], [WriterName], [Email], [Title], [SubTitle], [LanguageID], [SectionID], [MediaID], [LocalID], [SubNayong], [SubNayongChk], [Nayong1] ,[Nayong2] ,[AuthID] ,[InputDateTime], [JunsongDateTime], [LastLoginUserID], [Importance], [LinkArticles], [chkPhoto]) VALUES (?, ?, ? ,?, ?, '101', ?, '1002', ?, ?, NULL, ?, ?, ?, Getdate(), GetDate(), '', '1', '', ?)";
				$sqllist[] = array(
					'sql' => $sql,
					'params' => array($max_articleid, $WriterName, $Email, $Title, $SubTitle, $field, $region, $SubNayong, $Nayong1, $Nayong2, $AuthID, $chkPhoto)
				);
				/*$ret = sqlsrv_query($msdb, $sql, array($max_articleid, $WriterName, $Email, $Title, $SubTitle, $field, $region, $SubNayong, $Nayong1, $Nayong2, $AuthID, $chkPhoto));
				if ($ret === false) {
					//print var_export(sqlsrv_errors(), true) . "\n";
					file_put_contents('minju_err.txt', var_export(sqlsrv_errors(), true), FILE_APPEND);
					file_put_contents('minju_err.txt', var_export(array($max_articleid, $WriterName, $Email, $Title, $SubTitle, $field, $region, $SubNayong, $Nayong1, $Nayong2, $AuthID, $chkPhoto), true), FILE_APPEND);
				}
				file_put_contents('test_1.sql', var_export(array($max_articleid, $WriterName, $Email, $Title, $SubTitle, $field, $region, $SubNayong, $Nayong1, $Nayong2, $AuthID, $chkPhoto), true), FILE_APPEND);*/
				
			}

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
					file_put_contents('minju_err.txt', var_export(sqlsrv_errors(), true), FILE_APPEND);
					file_put_contents('minju_err.txt', var_export($sql['params'], true), FILE_APPEND);
				}
				file_put_contents('test_1.sql', var_export($sql['params'], true), FILE_APPEND);
				sleep(1);
			}

			// ftp to dow jones
			$djfname = "Minju " . date("Y-m-d") . ".xml";
			copy("C:/www.korea-copy.com/minju/zip_tmp/".$xmlfname, "C:/www.korea-copy.com/minju/zip_tmp/".$djfname);

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
						$res = ftp_put($ftp, $djfname, "C:/www.korea-copy.com/minju/zip_tmp/".$djfname, FTP_BINARY);
						if ($res === FALSE) {
							print "failure of the put file ($djfname).\n";
						} else {
							_sendmail2('suyama@btl.co.jp', 'suyama@btl.co.jp', "C:/www.korea-copy.com/minju/zip_tmp/".$djfname);
						}
							
						ftp_close($ftp);
					}
				}
			}

		}else{
			$logstr = sprintf("%s [FILE NOT FOUND (feed1) $xmlfname].\n", date("Y/m/d H:i:s"));
			file_put_contents('test_2.sql', $logstr, FILE_APPEND);
			print "[file not found]";
		}
	}else{
		$logstr = sprintf("%s [ZIP FILE OPEN ERROR (feed1) $fname].\n", date("Y/m/d H:i:s"));
		file_put_contents('test_2.sql', $logstr, FILE_APPEND);
	}

	sqlsrv_free_stmt($result);
	sqlsrv_close($msdb);
}

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
		removeDir('C:/www.korea-copy.com/minju/zip_tmp');
		mkdir('C:/www.korea-copy.com/minju/zip_tmp');
		$zip->extractTo('C:/www.korea-copy.com/minju/zip_tmp/');
		$zip->close();

		$xmlfname = date("Y-m-d", strtotime("-1 day")) . ".xml";
		$xmlfname2 = date("Y-n-j", strtotime("-1 day")) . ".xml";
		if (file_exists("C:/www.korea-copy.com/minju/zip_tmp/".$xmlfname)) {
			// NOOP
		} else if(file_exists("C:/www.korea-copy.com/minju/zip_tmp/".$xmlfname2)) {
			$xmlfname = $xmlfname2;
		}

		if (file_exists("C:/www.korea-copy.com/minju/zip_tmp/".$xmlfname)) {
			$dom = new DOMDocument('1.0', 'UTF-8');
			$dom->load("C:/www.korea-copy.com/minju/zip_tmp/".$xmlfname);

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
				$sqllist[] = array(
					'sql' => $sql,
					'params' => array($max_articleid, $WriterName, $Email, $Title, $SubTitle, $SubNayong, $Nayong1, $Nayong2, $AuthID, $chkPhoto)
				);
				/*$ret = sqlsrv_query($msdb, $sql, array($max_articleid, $WriterName, $Email, $Title, $SubTitle, $SubNayong, $Nayong1, $Nayong2, $AuthID, $chkPhoto));
				if ($ret === false) {
					//print var_export(sqlsrv_errors(), true) . "\n";
					file_put_contents('munhak_err.txt', var_export(sqlsrv_errors(), true), FILE_APPEND);
					file_put_contents('munhak_err.txt', var_export(array($max_articleid, $WriterName, $Email, $Title, $SubTitle, $SubNayong, $Nayong1, $Nayong2, $AuthID, $chkPhoto), true), FILE_APPEND);
				}
				file_put_contents('test_2.sql', var_export(array($max_articleid, $WriterName, $Email, $Title, $SubTitle, $SubNayong, $Nayong1, $Nayong2, $AuthID, $chkPhoto), true), FILE_APPEND);*/
				
			}

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
					file_put_contents('test_2.sql', var_export($sql['params'], true), FILE_APPEND);
					sleep(1);
				}
		}else{
			$logstr = sprintf("%s [FILE NOT FOUND (feed2) $xmlfname].\n", date("Y/m/d H:i:s"));
			file_put_contents('test_2.sql', $logstr, FILE_APPEND);
			print "[file not found]";
		}
	}else{
		$logstr = sprintf("%s [ZIP FILE OPEN ERROR (feed2) $fname].\n", date("Y/m/d H:i:s"));
		file_put_contents('test_2.sql', $logstr, FILE_APPEND);
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
```
Fucking useless developer that has no mother hardcoding Sensitive information  LOL.

### LICENSE

They don't have any conception about copyright. 

Depending on their motherfucking communism. (they shared fucking North Korea's supreme leader kim jung woon's mother Go Young hee and
north korea's citizen share kim's mother and gangbanging her)

So i share this repository with mit license
