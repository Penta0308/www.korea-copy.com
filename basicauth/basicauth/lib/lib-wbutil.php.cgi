<?php
///////////////////////////////////////////////////////////////////////
/// LITTLE-NET WEB TOOL : BasicAuth 1.7
/// http://l-tool.net/
/// http://little-net.jp/
/// Copyright (C) Akira Mori. All rights reserved.
/// 2008-03-15 : created
/// 2013-09-09 : modified
/// [UTF-8]
///////////////////////////////////////////////////////////////////////
if (!defined('LLUTL_REP_MARK')) { define('LLUTL_REP_MARK', '##'); }
define('LLUTL_REP_MARK1', '<!--'.LLUTL_REP_MARK);
define('LLUTL_REP_MARK2', LLUTL_REP_MARK.'-->');
define('LLUTL_ARY_TO_STR_JOI', ';');
define('LLUTL_ARY_TO_STR_JOI_MARK', '<#ARY_TO_STR_JOI#>');
define('LLUTL_SAFE_CODE', 'UTF-8');
define('LLUTL_PHP_VERSION', str_replace('.', '', PHP_VERSION));
if (!isset($_REQUEST)){$_REQUEST = array();
foreach ($HTTP_GET_VARS as $v_key => $v_val){$_REQUEST[$v_key] = $v_val;}
foreach ($HTTP_POST_VARS as $v_key => $v_val){$_REQUEST[$v_key] = $v_val;}}
if (!isset($_SERVER)){$_SERVER = array();
foreach ($HTTP_SERVER_VARS as $v_key => $v_val){$_SERVER[$v_key] = $v_val;}}
$LLUTL_REQUEST = $_REQUEST;
define('LLUTL_CONV_REQUEST', LLUTL_ENCODING != LLUTL_HTTP_ENCODING);
if (LLUTL_CONV_REQUEST){$reqs = array();
foreach ($_REQUEST as $k => $v){$k = mb_convert_encoding($k, LLUTL_ENCODING, LLUTL_HTTP_ENCODING);
if (is_array($v)){$reqs[$k] = array();
foreach ($v as $v2){if (LLUTL_STRIPSLASHES) { $v2 = stripslashes($v2); }
$reqs[$k][] = mb_convert_encoding($v2, LLUTL_ENCODING, LLUTL_HTTP_ENCODING);}}
else{if (LLUTL_STRIPSLASHES) { $v = stripslashes($v); }
$reqs[$k] = mb_convert_encoding($v, LLUTL_ENCODING, LLUTL_HTTP_ENCODING);}}
$_REQUEST = $reqs;}
define('LLUTL_CHK_STRIPSLASHES', LLUTL_CONV_REQUEST ? FALSE : LLUTL_STRIPSLASHES);
function LlutlMsgf($code,$p1 = '',$p2 = '',$p3 = '',$p4 = '',$p5 = ''){return str_replace(array('$p1','$p2','$p3','$p4','$p5'),array($p1,  $p2,  $p3,  $p4,  $p5),LlutlMsg($code));}
function LlutlMsg($code){global $LLMSG_MYSTR;
global $LLMSG_STR;
if      (defined('LLUTL_MSG_LANG') && isset($LLMSG_MYSTR[$code.'-'.LLUTL_MSG_LANG]))	{ return $LLMSG_MYSTR[$code.'-'.LLUTL_MSG_LANG]; }
else if (isset($LLMSG_MYSTR[$code]))													{ return $LLMSG_MYSTR[$code]; }
else if (defined('LLUTL_MSG_LANG') && isset($LLMSG_STR[$code.'-'.LLUTL_MSG_LANG]))		{ return $LLMSG_STR[$code.'-'.LLUTL_MSG_LANG]; }
else if (isset($LLMSG_STR[$code]))														{ return $LLMSG_STR[$code]; }
return '';}
function LlutlStripslashes($src){if (is_array($src)){$rtn = array();
foreach ($src as $s){$rtn[] = stripslashes($s);}
return $rtn;}
else{return stripslashes($src);}}
function LlutlIsPara($fld){return isset($_REQUEST[$fld]);}
function LlutlIsParaArray($fld){return isset($_REQUEST[$fld]) && is_array($_REQUEST[$fld]);}
function LlutlPara($fld,$def){global $_REQUEST;
if (isset($_REQUEST[$fld]) && $_REQUEST[$fld] != ''){$def = LLUTL_CHK_STRIPSLASHES ? LlutlStripslashes($_REQUEST[$fld]) : $_REQUEST[$fld];}
return $def;}
function LlutlParaRaw($fld,$def){global $LLUTL_REQUEST;
if (isset($LLUTL_REQUEST[$fld]) && $LLUTL_REQUEST[$fld] != ''){$def = LLUTL_CHK_STRIPSLASHES ? LlutlStripslashes($LLUTL_REQUEST[$fld]) : $LLUTL_REQUEST[$fld];}
return $def;}
function LlutlPara2($fld,$def){global $_REQUEST;
if (isset($_REQUEST[$fld])){$def = LLUTL_CHK_STRIPSLASHES ? LlutlStripslashes($_REQUEST[$fld]) : $_REQUEST[$fld];}
return $def;}
function LlutlParas($fld){global $_REQUEST;
$rtn = array();
if (isset($_REQUEST[$fld])){if (is_array($_REQUEST[$fld])){if (LLUTL_CHK_STRIPSLASHES){foreach ($_REQUEST[$fld] as $val){$val = stripslashes($val);
array_push($rtn, $val);}}
else{foreach ($_REQUEST[$fld] as $val){array_push($rtn, $val);}}}
else{$val = LLUTL_CHK_STRIPSLASHES ? stripslashes($_REQUEST[$fld]) : $_REQUEST[$fld];
array_push($rtn, $val);}}
return $rtn;}
function LlutlParaToArray($prefix){global $_REQUEST;
$lprefix = strlen($prefix);
$para = array();
if (LLUTL_CHK_STRIPSLASHES){foreach ($_REQUEST as $key => $val){if (substr($key, 0, $lprefix) == $prefix){$val = LlutlStripslashes($val);
$para[$key] = $val;}}}
else{foreach ($_REQUEST as $key => $val){if (substr($key, 0, $lprefix) == $prefix){$para[$key] = $val;}}}
return $para;}
function LlutlParaPrHtmlHidden($tstr){print LlutlParaGetHtmlHidden($tstr, '');}
function LlutlParaGetHtmlHidden($tstr,$skip){global $_REQUEST;
$para = '';
$tge  = LlutlHtmlXhtmlTag('>');
$len  = strlen($tstr);
$skip.= ',' . $skip . ',';
if (LLUTL_CHK_STRIPSLASHES){foreach ($_REQUEST as $key => $vals){if (substr($key, 0, $len) == $tstr && !strstr($skip, ','.$key.',')){if (is_array($vals)){foreach ($vals as $val){$val = stripslashes($val);
$para .= "<input type=\"hidden\" name=\"${key}[]\" value=\"${val}\"${tge}\n";}}
else{$val = stripslashes($vals);
$para .= "<input type=\"hidden\" name=\"${key}\" value=\"${val}\"${tge}\n";}}}}
else{foreach ($_REQUEST as $key => $vals){if (substr($key, 0, $len) == $tstr && !strstr($skip, ','.$key.',')){if (is_array($vals)){foreach ($vals as $val){$para .= "<input type=\"hidden\" name=\"${key}[]\" value=\"${val}\"${tge}\n";}}
else{$val = $vals;
$para .= "<input type=\"hidden\" name=\"${key}\" value=\"${val}\"${tge}\n";}}}}
return $para;}
function LlutlArrayToHtmlHidden($name,$para){$str = '';
$tge = LlutlHtmlXhtmlTag('>');
if (is_array($para)){foreach ($para as $val){$str .= "<input type=\"hidden\" name=\"${name}[]\" value=\"${val}\"${tge}\n";}}
else{$str .= "<input type=\"hidden\" name=\"${name}\" value=\"${para}\"${tge}\n";}
return $str;}
function LlutlEnv($key){global $_SERVER;
return isset($_SERVER[$key]) ? $_SERVER[$key] : '';}
$LLUTL_KTP = '';
function LlutlGetKtp(){global $LLUTL_KTP;
if ($LLUTL_KTP == ''){$ua = substr(LlutlEnv('HTTP_USER_AGENT'), 0, 4);
if     ($ua == 'DoCo') { $LLUTL_KTP = 'i'; }
elseif ($ua == 'J-PH') { $LLUTL_KTP = 'j'; }
elseif ($ua == 'Voda') { $LLUTL_KTP = 'v'; }
elseif ($ua == 'Soft') { $LLUTL_KTP = 's'; }
elseif ($ua == 'KDDI') { $LLUTL_KTP = 'k'; }
elseif ($ua == 'UP.B') { $LLUTL_KTP = 'e'; }
elseif ($ua == 'PDXG') { $LLUTL_KTP = 'h'; }
elseif ($ua == 'DDIP') { $LLUTL_KTP = 'd'; }
elseif ($ua == 'ASTE') { $LLUTL_KTP = 'a'; }
elseif ($ua == 'L-mo') { $LLUTL_KTP = 'l'; }
else { $LLUTL_KTP = 'p'; }}
return $LLUTL_KTP;}
function LlutlGetDom(){$ktp = LlutlGetKtp();
if     ($ktp == 'i') { return '@docomo.ne.jp'; }
elseif ($ktp == 'j') { return '@.vodafone.ne.jp'; }
elseif ($ktp == 'k') { return '@ezweb.ne.jp'; }
elseif ($ktp == 'e') { return '@ezweb.ne.jp'; }
elseif ($ktp == 's') { return '@softbank.ne.jp'; }
else   { return '@.ne.jp'; }}
function LlutlGetMtp($mail){if      (stristr($mail, '@docomo.ne.jp')   !== FALSE) { return 'i'; }
else if (eregi('(@jp-.\.ne\.jp)', $mail)   !== FALSE) { return 'j'; }
else if (stristr($mail, '.vodafone.ne.jp') !== FALSE) { return 'j'; }
else if (stristr($mail, '@ezweb.ne.jp')    !== FALSE) { return 'e'; }
else { return 'p'; }}
function LlutlIsKtaiIp($ip_addr = ''){global $LLUTL_KTAI_IP;
if ($ip_addr == '') { $ip_addr = LlutlRemoteAddr(); }
$ips = explode('.', $ip_addr);
$ip_chk = $ips[0].'.'.$ips[1].'.'.$ips[2];
return isset($LLUTL_KTAI_IP[$ip_chk]);}
function LlutlHtmlEscape($str,$null = ''){if ($str == '') { return $null; }
return str_replace(array('&#',            '&',     '<',    '>',    '"',      ' ',      "\n",                      '%%AMP_SHARP%%'),array('%%AMP_SHARP%%', '&amp;', '&lt;', '&gt;', '&quot;', '&nbsp;', LlutlHtmlXhtmlTag('<br>'), '&#'),$str);}
function LlutlHtmlEscape2($str,$null = ''){if ($str == '') { return $null; }
return str_replace(array('&#',            '&',     '<',    '>',    '"',      ' ',      '%%AMP_SHARP%%'),array('%%AMP_SHARP%%', '&amp;', '&lt;', '&gt;', '&quot;', '&nbsp;', '&#'),$str);}
function LlutlHtmlEscapeTag($str,$null = ''){if ($str == '') { return $null; }
return str_replace(array('<',   '>',   '&nbsp;',    '"'),array('&lt;','&gt;','&amp;nbsp;','&quot;'),$str);}
function LlutlHtmlEscapeTag2($str,$null = ''){if ($str == '') { return $null; }
return str_replace(array('<',   '>',   '&nbsp;',    '"',     "\n"),array('&lt;','&gt;','&amp;nbsp;','&quot;',LlutlHtmlXhtmlTag('<br>')),$str);}
function LlutlHtmlEscapeTagForText($str,$null = ''){if ($str == '') { return $null; }
return str_replace(array('&gt;',    '&lt;',    '<',   '>',   '&nbsp;',    '"',     "'"),array('&amp;gt;','&amp;lt;','&lt;','&gt;','&amp;nbsp;','&quot;','&#39;'),$str);}
function LlutlHtmlEscapeTagForTarea($str,$null = ''){if ($str == '') { return $null; }
return str_replace(array('&gt;',    '&lt;',    '<',   '>',   '&nbsp;',   ),array('&amp;gt;','&amp;lt;','&lt;','&gt;','&amp;nbsp;'),$str);}
function LlutlHtmlEscapeZen($str,$null = ''){if (!is_array($str) && $str == '') { return $null; }
return str_replace(array('<',  '>',  '"',  "'"),array('＜', '＞', '”', '’'),$str);}
function LlutlHtmlEscapeCRLF($str,$null = ''){if (!is_array($str) && $str == '') { return $null; }
return str_replace( array("\n", "\r"), array(LlutlHtmlXhtmlTag('<br>'), ''), $str);}
function LlutlHtmlEscapeCRLF2($str,$null = '',$nobr = '$NOBR$'){$wks = explode($nobr, $str);
$dst = '';
$cnt = 0;
foreach ($wks as $wk){$wk   = $cnt % 2 == 0 ? LlutlHtmlEscapeCRLF($wk, '') : $wk;
$dst .= $wk;
$cnt ++;}
return $dst != '' ? $dst : $null;}
function LlutlHtmlAutoLink($str,$blank = TRUE){$str = LlutlConvertEncoding($str, LLUTL_SAFE_CODE, LLUTL_ENCODING);
$target = $blank ? 'target="_blank"' : '';
$str = eregi_replace("([[:alnum:]\._-]+)@([[:alnum:]\._-]+)","<a href=\"mailto:\\1@\\2\">\\1@\\2</a>", $str);
$str = str_replace('&nbsp;', ' ', $str);
$str = ereg_replace("(https?|ftp)(://[[:alnum:]\+\$\;\?\.%,!#~*/:@&=_-]+)",

"<a href=\"\\1\\2\" $target>\\1\\2</a>", $str);
$str = LlutlConvertEncoding($str, LLUTL_ENCODING, LLUTL_SAFE_CODE);
return $str;}
function LlutlToJavaEncode($str){$str = mb_convert_encoding($str, 'UTF-8', LLUTL_ENCODING);
$str = rawurlencode($str);
return $str;}
function LlutlFromJavaDecode($str){$str = rawurldecode($str);
$str = mb_convert_encoding($str, LLUTL_ENCODING, 'UTF-8');
return $str;}
function LlutlPrJavaChkFld(){print LlutlGetJavaChkFld();}
function LlutlGetNum($str){$str = mb_convert_kana($str, "KVa", LLUTL_ENCODING);
$str_len = strlen($str);
$rtn = '';
for ($i = 0; $i < $str_len; $i ++){$c = substr($str, $i, 1);
if (strstr('0123456789.-', $c)) { $rtn .= $c; }}
return $rtn;}
function LlutlGetNum0($str){$num = LlutlGetNum($str);
if ($num == '') { $num = 0; }
return $num;}
function LlutlKanaHan($str){return mb_convert_kana($str, "ka", LLUTL_ENCODING);}
function LlutlKanaZen($str){return mb_convert_kana($str, "KV", LLUTL_ENCODING);}
function LlutlConvForKanaArea($str){return mb_convert_kana($str, "asHcV", LLUTL_ENCODING);}
function LlutlConvertEncoding($src,$to,$from){if (is_array($src)){$rtn = array();
foreach ($src as $v) { $rtn[] = mb_convert_encoding($v, $to, $from); }
return $rtn;}
else{return mb_convert_encoding($src, $to, $from);}}
function LlutlStripTags($str){$str = mb_convert_encoding($str, LLUTL_SAFE_CODE, LLUTL_ENCODING);
$str = strip_tags($str);
$str = mb_convert_encoding($str, LLUTL_ENCODING, LLUTL_SAFE_CODE);
return $str;}
function LlutlStrToUpper($str){$str = mb_convert_encoding($str, LLUTL_SAFE_CODE, LLUTL_ENCODING);
$str = str_replace(array('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'),array('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'),$str);
$str = mb_convert_encoding($str, LLUTL_ENCODING, LLUTL_SAFE_CODE);
return $str;}
function LlutlCutStr($str,$len,$add = '...'){$str  = str_replace(array("\r","\n"), array('',''), $str);
$dstr = mb_substr($str, 0, $len);
if (mb_strlen($str) > $len) { $dstr .= $add; }
return $dstr;}
function LlutlSplit($spl,$str){$spl = mb_convert_encoding($spl, LLUTL_SAFE_CODE, LLUTL_ENCODING);
$str = mb_convert_encoding($str, LLUTL_SAFE_CODE, LLUTL_ENCODING);
$wk  = explode($spl, $str);
$rtn = array();
foreach ($wk as $w){$rtn[] = mb_convert_encoding($w, LLUTL_ENCODING, LLUTL_SAFE_CODE);}
return $rtn;}
function LlutlStrReplace($rep1,$rep2,$str){$rep1 = LlutlConvertEncoding($rep1, LLUTL_SAFE_CODE, LLUTL_ENCODING);
$rep2 = LlutlConvertEncoding($rep2, LLUTL_SAFE_CODE, LLUTL_ENCODING);
$str  = LlutlConvertEncoding($str,  LLUTL_SAFE_CODE, LLUTL_ENCODING);
$str  = str_replace($rep1, $rep2, $str);
return LlutlConvertEncoding($str, LLUTL_ENCODING, LLUTL_SAFE_CODE);}
function LlutlReplaceSpStr($src,$r){$str_len = strlen($src);
$rtn = '';
for ($i = 0; $i < $str_len; $i ++){$c = substr($src, $i, 1);
if (preg_match('/[0-9A-Za-z]/', $c)){$rtn .= $c;}
else{$rtn .= $r;}}
return $rtn;}
function LlutlStrToAry($str,$joi = LLUTL_ARY_TO_STR_JOI){$rtn   = array();
$wks   = explode($joi, $str);
$nwk   = sizeof($wks);
$i     = 0;
$depth = 0;
LlutlStrToAry_child($wks, $nwk, $i, $depth, $rtn, $joi);
return $rtn;}
function LlutlStrToAry_child(&$wks,$nwk,&$i,&$depth,&$rtn,$joi){if ($i >= $nwk) { return; }
$depth ++;
$dep = $wks[$i];
while ($dep == $depth){$i ++;
$key = LlutlAryToStr_decode($wks[$i], $joi); $i ++;
$tp  = $wks[$i]; $i ++;
$val = $wks[$i]; $i ++;
if ($tp == 0){$rtn[$key] = LlutlAryToStr_decode($val, $joi);}
else{$rtn[$key] = array();
LlutlStrToAry_child($wks, $nwk, $i, $depth, $rtn[$key], $joi);}
if ($i >= $nwk) { break; }
$dep = $wks[$i];}
$depth --;}
function LlutlAryToStr(&$ary,$joi = LLUTL_ARY_TO_STR_JOI){$wks = array();
$depth = 0;
LlutlAryToStr_child($ary, $joi, $wks, $depth);
return join($joi, $wks);}
function LlutlAryToStr_child(&$ary,$joi,&$wks,&$depth){$depth ++;
foreach ($ary as $key => $val){$wks[] = $depth;
$wks[] = LlutlAryToStr_encode($key, $joi);
if (is_array($val)){$wks[] = 1;
$wks[] = '';
LlutlAryToStr_child($val, $joi, $wks, $depth);}
else{$wks[] = 0;
$wks[] = LlutlAryToStr_encode($val, $joi);}}
$depth --;}
function LlutlAryToStr_encode($str,$joi){return str_replace(	array("\r\n",          "\n",          "\r",          "\t",           $joi),array(LLTBF_MARK_CRLF, LLTBF_MARK_LF, LLTBF_MARK_CR, LLTBF_MARK_TAB, LLUTL_ARY_TO_STR_JOI_MARK),$str);}
function LlutlAryToStr_decode($str,$joi){return str_replace(	array(LLTBF_MARK_CRLF, LLTBF_MARK_LF, LLTBF_MARK_CR, LLTBF_MARK_TAB, LLUTL_ARY_TO_STR_JOI_MARK),array("\r\n",          "\n",          "\r",          "\t",           $joi),$str);}
function LlutlGetFile($path,$path2 = ''){$file = @file($path);
if (!$file && $path2 != '') { $file = @file($path2); }
if (!$file){print('file not found : '.$path);
exit;}
return implode("", $file);}
function LlutlFilePutContents($path,$str){$fp   = fopen($path, "w");	if (!$fp) { return FALSE; }
$byte = fwrite($fp, $str);	if (!$byte) { return FALSE; }
$rtn  = fclose($fp);		if (!$rtn) { return FALSE; }
@chmod($path, LLUTL_MODE_MKFIL);
return $byte;}
function LlutlReadUrlWriteHtml($path_url,$path_html,$prep = array(),$srep = array()){$html = '';
$fp = @fopen($path_url, 'r');
if (!$fp) { return "error : fopen($path_url, r)"; }
while (!feof($fp)){$html .= fgets($fp, 4096);}
fclose($fp);
if (sizeof($prep) > 0) { $html = preg_replace(array_keys($prep), array_values($prep), $html); }
if (sizeof($srep) > 0) { $html = str_replace(array_keys($srep), array_values($srep), $html); }
$fp = @fopen($path_html, 'w');
if (!$fp) { return "error : fopen($path_html, w)"; }
fputs($fp, $html);
fclose($fp);
return '';}
function LlutlMkDir($dir,$mode =  LLUTL_MODE_MKDIR){if (!LlutlDirExist($dir)){$mkdir = '';
if (substr($dir, 0, 1) == '/') { $mkdir = '/'; $dir = substr($dir, 1); }
$dirs = explode('/', $dir);
foreach ($dirs as $dname){$mkdir .= $dname . '/';
if (!LlutlDirExist($mkdir)){if (@mkdir($mkdir, $mode)) { @chmod($mkdir, $mode); }}}}}
function LlutlClearDir($dir,$tm){$handle = @opendir($dir);
if (!$handle) { return; }
while (false!==($FolderOrFile = @readdir($handle))){if ($FolderOrFile != "." && $FolderOrFile != ".."){$fname = "${dir}/${FolderOrFile}";
$stat = @stat($fname);
if ($stat['mtime'] < $tm){if (is_dir($fname)){LlutlRmDir($fname);}
else{@unlink($fname);}}}}
@closedir($handle);}
function LlutlRmDir($dir){$handle = @opendir($dir);
if (!$handle) { return FALSE; }
while (false!==($FolderOrFile = @readdir($handle))){if ($FolderOrFile != "." && $FolderOrFile != ".."){if (is_dir("$dir/$FolderOrFile")){LlutlRmDir("$dir/$FolderOrFile");}
else{@unlink("$dir/$FolderOrFile");}}}
@closedir($handle);
if (@rmdir($dir)) { return true; }
return false;}
function LlutlCopys($oldname,$newname,$dirperm = LLUTL_MODE_MKDIR,$filperm = 0,$errdie = TRUE){if (is_file($oldname)){$perms = $filperm == 0 ? fileperms($oldname) : $filperm;
return copy($oldname, $newname) && chmod($newname, $perms);}
elseif (is_dir($oldname)){LlutlCopys_MyDir($oldname, $newname, $dirperm, $filperm);}
else if ($errdie){die("Cannot copy file: $oldname (it's neither a file nor a directory)");}}
function LlutlCopys_MyDir($oldname, $newname, $dirperm, $filperm){if (!is_dir($newname)){$perms = $dirperm == 0 ? fileperms($oldname) : $dirperm;
LlutlMkDir($newname, $perms);
chmod($newname, $perms);}
$dir = opendir($oldname);
while ($file = readdir($dir)){if ($file == "." || $file == "..") { continue; }
LlutlCopys("$oldname/$file", "$newname/$file", $dirperm, $filperm);}
closedir($dir);}
function LlutlFileCreate($fpath,$mode){if (!LlutlFileExist($fpath)){$fp = fopen($fpath, "a");
if (!$fp) { LlutlPrint("ファイルを開けません : LlutlFileCreate()\n"); exit; }
fclose($fp);
chmod($fpath, $mode);}}
function LlutlFileExist($path){if (LLUTL_FEXIST_TYPE == 0){return file_exists($path);}
elseif (LLUTL_FEXIST_TYPE == 1){$fp = @fopen($path, "r");
if (!$fp) { return FALSE; }
fclose($fp);
return TRUE;}
else{print(sprintf("ERROR : %s-%d\n",__FILE__,__LINE__));
exit;}}
function LlutlDirExist($path){if (LLUTL_FEXIST_TYPE == 0){return file_exists($path);}
elseif (LLUTL_FEXIST_TYPE == 1){$dir = @opendir($path);
if (!$dir) { return FALSE; }
closedir($dir);
return TRUE;}
else{print(sprintf("ERROR : %s-%d\n",__FILE__,__LINE__));
exit;}}
function LlutlCopyAllFiles($fr_dir,$to_dir,$prefix,$suffix,$mode){if (substr($fr_dir, -1) != '/') { $fr_dir .= '/'; }
if (substr($to_dir, -1) != '/') { $to_dir .= '/'; }
if ($dir = opendir($fr_dir)){while (($file = readdir($dir)) !== false){if ($file == '.')  { continue; }
if ($file == '..') { continue; }
if ($prefix != '' && $prefix != substr($file, 0, strlen($prefix))) { continue; }
if ($suffix != '' && $suffix != substr($file, -1*strlen($suffix))) { continue; }
copy($fr_dir.$file, $to_dir.$file);
if ($mode != '') { chmod($to_dir.$file, $mode); }}
closedir($dir);}}
function LlutlGlob($sr_dir,$prefix = '',$suffix = ''){$rtn = array();
if (substr($sr_dir, -1) != '/') { $sr_dir .= '/'; }
if ($dir = @opendir($sr_dir)){while (($file = readdir($dir)) !== false){if ($file == '.')  { continue; }
if ($file == '..') { continue; }
if ($prefix != '' && $prefix != substr($file, 0, strlen($prefix))) { continue; }
if ($suffix != '' && $suffix != substr($file, -1*strlen($suffix))) { continue; }
$rtn[] = $file;}
closedir($dir);}
return $rtn;}
function LlutlUnlink($sr_dir,$prefix = '',$suffix = ''){$ps = LlutlGlob($sr_dir, $prefix, $suffix);
foreach ($ps as $p) { unlink("$sr_dir/$p"); }
return sizeof($ps);}
function LlutlDels($delname){if (is_file($delname)){return unlink($delname);}
elseif (is_dir($delname)){LlutlDels_MyDir($delname);}}
function LlutlDels_MyDir($delname){$dir = opendir($delname);
while ($file = readdir($dir)){if ($file == "." || $file == "..") { continue; }
LlutlDels("$delname/$file");}
closedir($dir);
rmdir($delname);}
function LlutlImgGetType($tag_name){global $_FILES;
$mtyp = strtolower($_FILES[$tag_name]['type']);
if     (stristr($mtyp, 'gif'))  { return 'gif'; }
elseif (stristr($mtyp, 'png'))  { return 'png'; }
elseif (stristr($mtyp, 'jpg'))  { return 'jpg'; }
elseif (stristr($mtyp, 'jpeg')) { return 'jpg'; }
elseif (stristr($mtyp, 'bmp'))  { return 'bmp'; }
else                            { return $mtyp; }
return '';}
function LlutlImgGetType2($tag_name){global $_FILES;
return LlutlImgGetType2Base($_FILES[$tag_name]['name']);}
function LlutlImgGetType2Base($path){global $_FILES;
$nms = explode('.', strtolower($path));
$sz  = sizeof($nms);
if ($sz < 2) { return ''; }
$rtn = $nms[$sz - 1];
if ($rtn == 'jpeg') { $rtn = 'jpg'; }
return $rtn;}
function LlutlImgSearchPath($base_path,$add = '-'){$dname = dirname($base_path);
$bname = basename($base_path);
if ($add != '' && substr($bname, -1) != $add) { $bname .= $add; }
$ps = LlutlGlob($dname, $bname);
return sizeof($ps) <= 0 ? '' : $dname.'/'.$ps[0];}
$LLUTL_IMG_NEW_PATH_TNO = 0;
function LlutlImgNewPath($img_base,$fext){global $LLUTL_IMG_NEW_PATH_TNO;
$tno   = $LLUTL_IMG_NEW_PATH_TNO <= 0 ? sprintf('%03d', time() % 1000)
: $LLUTL_IMG_NEW_PATH_TNO;
return $img_base . '-' . $tno . '.' . $fext;}
function LlutlImgPathTnoFix($tno){global $LLUTL_IMG_NEW_PATH_TNO;
$LLUTL_IMG_NEW_PATH_TNO = $tno;;}
$LLUTL_IMG_UPLOAD_INFO = array();
function LlutlImgUpload($tag_name,$del_flg,$exttypes,$maxsize,$img_base,&$emsg){global $_FILES;
global $LLUTL_IMG_UPLOAD_INFO;
$dname = dirname($img_base);
$bname = basename($img_base);
$LLUTL_IMG_UPLOAD_INFO = array('up'=>FALSE, 'del'=>FALSE);
if (isset($_FILES[$tag_name]['name']) &&
strlen($_FILES[$tag_name]['name']) > 0){$fext = LlutlImgGetType2($tag_name);
if ($fext == '' || ($exttypes != '' && !stristr($exttypes, $fext))){$emsg = LlutlMsgf('imgupload01');
return FALSE;}
if ($_FILES[$tag_name]['size'] > $maxsize){$emsg = LlutlMsgf('imgupload02', (int)($maxsize / 1024));
return FALSE;}
LlutlMkDir($dname, LLUTL_MODE_MKIMD);
LlutlImgUnlink($dname, $bname);
$rfile = $_FILES[$tag_name]['tmp_name'];
$ofile = LlutlImgNewPath($img_base, $fext);
if (is_uploaded_file($rfile)){move_uploaded_file($rfile, $ofile);
chmod($ofile, LLUTL_MODE_MKIMG);
$LLUTL_IMG_UPLOAD_INFO = $_FILES[$tag_name];
$LLUTL_IMG_UPLOAD_INFO['fpath'] = LlutlPara('fpath'.substr($tag_name,1), '');
$LLUTL_IMG_UPLOAD_INFO['fext']  = $fext;
$LLUTL_IMG_UPLOAD_INFO['ofile'] = $ofile;
$LLUTL_IMG_UPLOAD_INFO['up']    = TRUE;}
else{$emsg = LlutlMsgf('imgupload03');
return FALSE;}}
else if ($del_flg){LlutlImgUnlink($dname, $bname);
$LLUTL_IMG_UPLOAD_INFO['del'] = TRUE;}
return TRUE;}
function LlutlImgUnlink($dname,$bname){if (substr($bname, -1) != '-') { $bname .= '-'; }
LlutlUnlink($dname, $bname);}
function LlutlImgCopy($img_base_from,$img_base_to){$rfile = LlutlImgSearchPath($img_base_from);
if ($rfile == '') { return FALSE; }
$wks   = explode('.', $rfile);
$fext  = array_pop($wks);
$ofile = LlutlImgNewPath($img_base_to, $fext);
$dname = dirname($img_base_to);
$bname = basename($img_base_to);
LlutlMkDir($dname, LLUTL_MODE_MKIMD);
LlutlImgUnlink($dname, $bname);
copy($rfile, $ofile);
chmod($ofile, LLUTL_MODE_MKIMG);
return TRUE;}
function LlutlImageGDEnable(){return function_exists('imagecreatefromjpeg');}
function LlutlImageGDCopyFile($fr_path,&$to_path,$to_w,$to_h,$trim = FALSE){$pathes = explode('.', $fr_path);
$fext   = array_pop($pathes);
LlutlMkDir(dirname($to_path), LLUTL_MODE_MKIMD);
$fr_img = '';
if      ($fext == 'jpg'  && function_exists('imagecreatefromjpeg')) { $fr_img = imagecreatefromjpeg($fr_path); }
else if ($fext == 'jpeg' && function_exists('imagecreatefromjpeg')) { $fr_img = imagecreatefromjpeg($fr_path); }
else if ($fext == 'gif'  && function_exists('imagecreatefromgif'))  { $fr_img = imagecreatefromgif($fr_path); }
else if ($fext == 'png'  && function_exists('imagecreatefrompng'))  { $fr_img = imagecreatefrompng($fr_path); }
else if ($fext == 'bmp'  && function_exists('imagecreatefrombmp'))  { $fr_img = imagecreatefrombmp($fr_path); }
if ($fr_img == ''){if (strcmp($fr_path, $to_path) != 0){copy($fr_path, $to_path);
chmod($to_path, LLUTL_MODE_MKIMG);}
return TRUE;}
$fr_w   = imagesx($fr_img);
$fr_h   = imagesy($fr_img);
$ap   = array();
if ($trim){$asize = LlutlImageGDAdjustSizeTrim($fr_w, $fr_h, $to_w, $to_h);
$ap['src_x'] = $asize['rsrc_x'];
$ap['src_y'] = $asize['rsrc_y'];
$ap['src_w'] = $asize['rsrc_w'];
$ap['src_h'] = $asize['rsrc_h'];
$ap['dst_x'] = 0;
$ap['dst_y'] = 0;
$ap['dst_w'] = $asize['width'];
$ap['dst_h'] = $asize['height'];
$ap['per']   = $asize['per'];}
else{$asize = LlutlImageGDAdjustSize($fr_w, $fr_h, $to_w, $to_h);
$ap['src_x'] = 0;
$ap['src_y'] = 0;
$ap['src_w'] = $fr_w;
$ap['src_h'] = $fr_h;
$ap['dst_x'] = 0;
$ap['dst_y'] = 0;
$ap['dst_w'] = $asize['width'];
$ap['dst_h'] = $asize['height'];
$ap['per']   = $asize['per'];}
if ($ap['per'] == 1 && strcmp($fr_path, $to_path) == 0) { return TRUE; }
$to_img = function_exists('imagecreatetruecolor') ? imagecreatetruecolor($ap['dst_w'], $ap['dst_h'])
: imagecreate($ap['dst_w'], $ap['dst_h']);
imagefill($to_img, 0, 0, 0xFFFFFF);
if (function_exists('imagecopyresampled')){imagecopyresampled($to_img, $fr_img,$ap['dst_x'], $ap['dst_y'], $ap['src_x'], $ap['src_y'],$ap['dst_w'], $ap['dst_h'], $ap['src_w'], $ap['src_h']);}
else{imagecopyresized($to_img, $fr_img,$ap['dst_x'], $ap['dst_y'], $ap['src_x'], $ap['src_y'],$ap['dst_w'], $ap['dst_h'], $ap['src_w'], $ap['src_h']);}
if      ($fext == 'jpg')  { imagejpeg($to_img, $to_path); }
else if ($fext == 'jpeg') { imagejpeg($to_img, $to_path); }
else if ($fext == 'png')  { imagepng($to_img, $to_path); }
else if ($fext == 'gif'){if (function_exists('imagegif')){imagegif($to_img, $to_path);}
else{$to_path = substr($to_path, 0, -4).'.png';
imagepng($to_img, $to_path);}}
else if ($fext == 'bmp'){$to_path = substr($to_path, 0, -4).'.png';
imagepng($to_img, $to_path);}
chmod($to_path, LLUTL_MODE_MKIMG);
return TRUE;}
function imagecreatefrombmp($filename){$tmp_name1 = tempnam("/tmp", "GD");
$tmp_name2 = tempnam("/tmp", "GD");
file_put_contents($tmp_name1, file_get_contents($filename));
if(ConvertBMP2GD($tmp_name1, $tmp_name2)){$img = imagecreatefromgd($tmp_name2);
unlink($tmp_name1);
unlink($tmp_name2);
return $img;}
return false;}
function ConvertBMP2GD($src, $dest = false){if(!($src_f = fopen($src, "rb"))) { return false; }
if(!($dest_f = fopen($dest, "wb"))) { return false; }
$header = unpack("vtype/Vsize/v2reserved/Voffset", fread($src_f, 14));
$info = unpack("Vsize/Vwidth/Vheight/vplanes/vbits/Vcompression/Vimagesize/Vxres/Vyres/Vncolor/Vimportant", fread($src_f, 40));
extract($info);
extract($header);
if($type != 0x4D42) { return false; }
$palette_size = $offset - 54;
$ncolor = $palette_size / 4;
$gd_header = "";
$gd_header .= ($palette_size == 0) ? "\xFF\xFE" : "\xFF\xFF";
$gd_header .= pack("n2", $width, $height);
$gd_header .= ($palette_size == 0) ? "\x01" : "\x00";
if($palette_size) { $gd_header .= pack("n", $ncolor); }
$gd_header .= "\xFF\xFF\xFF\xFF";
fwrite($dest_f, $gd_header);
if($palette_size){$palette = fread($src_f, $palette_size);
$gd_palette = "";
$j = 0;
while($j < $palette_size){$b = $palette{$j++};
$g = $palette{$j++};
$r = $palette{$j++};
$a = $palette{$j++};
$gd_palette .= "$r$g$b$a";}
$gd_palette .= str_repeat("\x00\x00\x00\x00", 256 - $ncolor);
fwrite($dest_f, $gd_palette);}
$scan_line_size = (($bits * $width) + 7) >> 3;
$scan_line_align = ($scan_line_size & 0x03) ? 4 - ($scan_line_size & 0x03) : 0;
for($i = 0, $l = $height - 1; $i < $height; $i++, $l--){fseek($src_f, $offset + (($scan_line_size + $scan_line_align) * $l));
$scan_line = fread($src_f, $scan_line_size);
if($bits == 24){$gd_scan_line = "";
$j = 0;
while($j < $scan_line_size){$b = $scan_line{$j++};
$g = $scan_line{$j++};
$r = $scan_line{$j++};
$gd_scan_line .= "\x00$r$g$b";}}
else if($bits == 8){$gd_scan_line = $scan_line;}
else if($bits == 4){$gd_scan_line = "";
$j = 0;
while($j < $scan_line_size){$byte = ord($scan_line{$j++});
$p1 = chr($byte >> 4);
$p2 = chr($byte & 0x0F);
$gd_scan_line .= "$p1$p2";}
$gd_scan_line = substr($gd_scan_line, 0, $width);}
else if($bits == 1){$gd_scan_line = "";
$j = 0;
while($j < $scan_line_size){$byte = ord($scan_line{$j++});
$p1 = chr((int) (($byte & 0x80) != 0));
$p2 = chr((int) (($byte & 0x40) != 0));
$p3 = chr((int) (($byte & 0x20) != 0));
$p4 = chr((int) (($byte & 0x10) != 0));
$p5 = chr((int) (($byte & 0x08) != 0));
$p6 = chr((int) (($byte & 0x04) != 0));
$p7 = chr((int) (($byte & 0x02) != 0));
$p8 = chr((int) (($byte & 0x01) != 0));
$gd_scan_line .= "$p1$p2$p3$p4$p5$p6$p7$p8";}
$gd_scan_line = substr($gd_scan_line, 0, $width);}
fwrite($dest_f, $gd_scan_line);}
fclose($src_f);
fclose($dest_f);
return true;}
function LlutlImageGDAdjustSizeFromPath($path,$max_w,$max_h){$info = LlutlImageGDGetInfo($path);
return LlutlImageGDAdjustSize($info['width'], $info['height'], $max_w, $max_h);}
function LlutlImageGDAdjustSize($src_w,$src_h,$max_w,$max_h){$per_w  = $src_w > 0 ? $max_w / $src_w : 0;
$per_h  = $src_h > 0 ? $max_h / $src_h : 0;
$per    = $per_w < $per_h ? $per_w : $per_h;
if ($per > 1.0) { $per = 1; }
return array('width'  => (int)($src_w * $per),'height' => (int)($src_h * $per),'per'    => $per,);}
function LlutlImageGDAdjustSizeTrim($src_w,$src_h,$max_w,$max_h){$per_w  = $max_w / $src_w;
$per_h  = $max_h / $src_h;
$per    = $per_w > $per_h ? $per_w : $per_h;
if ($per > 1.0) { $per = 1; }
$new_w = (int)($src_w * $per);
$new_h = (int)($src_h * $per);
$width  = $new_w > $max_w ? $max_w : $new_w;
$height = $new_h > $max_h ? $max_h : $new_h;
$trim_w = (int)(($new_w - $width) / $per);	if ($trim_w < 0) { $trim_w = 0; }
$trim_h = (int)(($new_h - $height) / $per);	if ($trim_h < 0) { $trim_h = 0; }
return array('rsrc_x' => (int)($trim_w / 2),'rsrc_y' => (int)($trim_h / 2),'rsrc_w' => (int)($width / $per),'rsrc_h' => (int)($height / $per),'width'  => $width,'height' => $height,'per'    => $per,);}
function LlutlImageGDGetInfo($path){$rtn = array('path'   => $path,'result' => FALSE,'width'  => 0,'height' => 0,);
$imsz = @getimagesize($path);
if ($imsz){$rtn['result'] = TRUE;
$rtn['width']  = $imsz[0];
$rtn['height'] = $imsz[1];}
return $rtn;}
function LlutlFileOpenLock($fname,$open_mode){if (LLUTL_LOCK_TYPE == 0){return LlutlFileOpenLockFlock($fname, $open_mode, LOCK_EX);}
else{return LlutlFileOpenLockMkdir($fname, $open_mode);}}
function LlutlFileOpenLockFlock($fname,$open_mode,$lock_mode){$loc = array('type'   => LLUTL_LOCK_TYPE,'file'   => $fname,'dir'    => '','fp'     => 0,);
$loc['fp'] = fopen($fname, $open_mode);
if (!$loc['fp']) { print(sprintf("ERROR : %s-%d\n",__FILE__,__LINE__)); exit; }
flock($loc['fp'], $lock_mode);
return $loc;}
function LlutlFileOpenLockMkdir($fname,$open_mode){$loc = array('type'   => LLUTL_LOCK_TYPE,'file'   => $fname,'dir'    => $fname . '_lockd','fp'     => 0,);
$loc['fp'] = fopen($fname, $open_mode);
if (!$loc['fp']) { print(sprintf("ERROR : %s-%d\n",__FILE__,__LINE__)); exit; }
$retry = LLUTL_LOCK_TYPE;
while (!@mkdir($loc['dir'], LLUTL_MODE_MKDIR)){$retry --;
if ($retry <= 0) { print("LOCK BUSY\n"); exit; }
sleep(1);}
return $loc;}
function LlutlFileCloseUnlock(&$loc){if ($loc['type'] == 0){flock($loc['fp'], LOCK_UN);}
else{rmdir($loc['dir']);}
fclose($loc['fp']);}
function LlutlSendMail($to_addr,$to_name,$fr_addr,$fr_name,$subj,$body,$attached_files = array()){$mime_code = 'iso-2022-jp';
$mime_bit  = '7bit';
$mail = new PHPMailer();
$mail->CharSet  = $mime_code;
$mail->Encoding = $mime_bit;
$to_name		= LlutlSendMail_encode_mimeheader(LlutlKanaZen($to_name), $mime_code);
$mail->AddAddress($to_addr, LlutlKanaZen($to_name));
$mail->From		= $fr_addr;
$mail->FromName	= LlutlSendMail_encode_mimeheader(LlutlKanaZen($fr_name), $mime_code);
$mail->Subject	= LlutlSendMail_encode_mimeheader(LlutlKanaZen($subj), $mime_code);
$mail->Body		= mb_convert_encoding(LlutlKanaZen($body), $mime_code, LLUTL_ENCODING);
if (sizeof($attached_files) > 0){foreach ($attached_files as $at_path => $at_name){$mail->AddAttachment($at_path, $at_name);}}
if (!$mail->Send()){LlutlLog(__FILE__, __LINE__, $mail->ErrorInfo);
return FALSE;}
$mail->ClearAddresses();
$mail->ClearAttachments();
return TRUE;}
function LlutlSendMail_encode_mimeheader($src,$mime_code){$chk_code  = strtoupper(substr(LLUTL_ENCODING, 0, 4)) != 'SJIS' ? "SJIS-win" : LLUTL_ENCODING;
if (LLUTL_ENCODING != $chk_code) { $src = mb_convert_encoding($src, $chk_code, LLUTL_ENCODING); }
$wstrs = array();
if (TRUE){$cs   = unpack('C*', $src);
$tp   = 0;
$tpc  = -1;
$idx  = 0;
$idxs = array();
foreach ($cs as $c){if ($tp == 1)														{ $tp = 2; }
else if ((0x81 <= $c && $c <= 0x9F) || (0xE0 <= $c && $c <= 0xFC))	{ $tp = 1; }
else																{ $tp = 0; }
if (($tp == 1 && $tpc == 0) || ($tp == 0 && $tpc > 0)) { $idxs[] = $idx; }
$tpc = $tp;
$idx ++;}
$idxs[] = $idx;
$i = 0;
foreach ($idxs as $idx){$len = $idx - $i;
$wstrs[] = substr($src, $i, $len);
$i = $idx;}}
$dest = '';
foreach ($wstrs as $wstr){$lines = array();
$pos   = 0;
$split = 36;
$line = substr($wstr, $pos, $split);
while ($line != null && $line != ''){$lines[] = $line;
$pos += $split;
$line = substr($wstr, $pos, $split);}
foreach ($lines as $line){$line  = mb_convert_encoding($line, $mime_code, $chk_code);
$dest .= mb_encode_mimeheader($line, $mime_code, "B");}}
return $dest;}
function LlutlSendMail_encode_mimeheader_old($src,$mime_code){$chk_code  = strtoupper(substr(LLUTL_ENCODING, 0, 4)) != 'SJIS' ? "SJIS-win" : LLUTL_ENCODING;
if (LLUTL_ENCODING != $chk_code) { $src = mb_convert_encoding($src, $chk_code, LLUTL_ENCODING); }
if (!LlutlSendMail_chk_sjis_eng_only($src) && strlen($src) > 24) { $src = mb_convert_kana($src, "ASKV", $chk_code); }
$lines = array();
$pos = 0;
$split = 36;
$line = substr($src, $pos, $split);
while ($line != null && $line != ''){$lines[] = $line;
$pos += $split;
$line = substr($src, $pos, $split);}
$dest = '';
foreach ($lines as $line){$line  = mb_convert_encoding($line, $mime_code, $chk_code);
$dest .= mb_encode_mimeheader($line, $mime_code, "B");}
return $dest;}
function LlutlSendMail_chk_sjis_eng_only($str){$cs = unpack('C*', $str);
$tp = 0;
foreach ($cs as $c){if ($tp == 1){$tp = 2;
return FALSE;}
else if ((0x81 <= $c && $c <= 0x9F) || (0xE0 <= $c && $c <= 0xFC)){$tp = 1;
return FALSE;}
else{$tp = 0;}}
return TRUE;}
function LlutlSendMail_old($to_addr,$to_name,$fr_addr,$fr_name,$subj,$body,$attached_files = array()){$mime_code = 'ISO-2022-JP';
$mail = new PHPMailer();
$mail->CharSet  = $mime_code;
$mail->Encoding = "7bit";
$to_name = mb_encode_mimeheader(mb_convert_encoding($to_name, $mime_code, LLUTL_ENCODING));
$mail->AddAddress($to_addr, $to_name);
$mail->From		= $fr_addr;
$mail->FromName	= mb_encode_mimeheader(mb_convert_encoding($fr_name, $mime_code, LLUTL_ENCODING));
$mail->Subject	= mb_encode_mimeheader(mb_convert_encoding($subj, $mime_code, LLUTL_ENCODING));
$mail->Body		= mb_convert_encoding($body, $mime_code, LLUTL_ENCODING);
if (sizeof($attached_files) > 0){foreach ($attached_files as $at_path => $at_name){$mail->AddAttachment($at_path, $at_name);}}
if (!$mail->Send()){LlutlLog(__FILE__, __LINE__, $mail->ErrorInfo);
return FALSE;}
$mail->ClearAddresses();
$mail->ClearAttachments();
return TRUE;}
function LlutlPriceStr($price){$fu = FALSE;
if ($price < 0){$price = -1 * $price;
$fu = TRUE;}
$ary = array();
$cnt = 0;
for ($i = strlen($price) - 1; $i >= 0; $i --){$c = substr($price, $i, 1);
if ($cnt > 0 && ($cnt % 3) == 0 && preg_match('/[0-9]/', $c)) { $ary[] = ','; }
$ary[] = $c;
$cnt ++;}
$rtn = '';
foreach ($ary as $c){$rtn = $c . $rtn;}
return $fu ? '-'.$rtn : $rtn;}
function LlutlMonthLastDay($year,$mon){if ($mon == 2){$uruu = FALSE;
if     ($year % 400 == 0) { $uruu = TRUE; }
elseif ($year % 100 == 0) { $uruu = FALSE; }
elseif ($year %   4 == 0) { $uruu = TRUE; }
return $uruu ? 29 : 28;}
elseif ($mon == 4 || $mon == 6 || $mon == 9 || $mon == 11){return 30;}
else{return 31;}}
function LlutlDateAddYear($date,$add_year){$ymd = preg_split('/(-| |:)/', $date);
if (!isset($ymd[1])) { return ''; }
$end_year = $ymd[0] + 1;
$end_mon  = $ymd[1];
$last_day = LlutlMonthLastDay($end_year, $end_mon);
$end_day  = $ymd[2] >= $last_day ? $ymd[2] : $last_day;
return sprintf("%04d-%02d-%02d", $end_year, $end_mon, $end_day);}
function LlutlDateAddDay($date,$add_day){$ymd = preg_split('/(-| |:)/', $date);
if (!isset($ymd[1])) { return ''; }
$tm = LlutlUnixTime($ymd[0], $ymd[1], $ymd[2], 0, 0, 0);
$dt = LlutlDateTime($tm + ($add_day * 86400));
return sprintf("%04d-%02d-%02d", $dt['year'], $dt['mon'], $dt['day']);}
function LlutlDateStrToAry($str){$ary = preg_split('/(-| |:)/', $str);
$rtn = array();
foreach ($ary as $d) { $rtn[] = sprintf('%d', $d); }
return $rtn;}
function LlutlPTopDir(){$pd = dirname($_SERVER['SCRIPT_NAME']);
if (TOP_DIR == '../') { $pd = dirname($pd); }
return $pd.'/';}
function LlutlPSize($id,$sv,$pd){$sv = str_replace('www.', '', $sv);
return	substr(crypt($id, $id), 2, 2).
substr(crypt($sv, $sv), 2, 2).
substr(crypt($pd, $pd), 2, 2);}
function LlutlCrypt($str){if (strlen($str) < 2) { $str .= 'ab'; }
$salt = substr($str, -2);
return	crypt($str, $salt);}
function LlutlCryptOneTimePwd($tm,$salt,$len = 6){$str = crypt(strrev($tm), $salt);
$str = preg_replace('/([^0-9A-Za-z])/', '', $str);
return substr($str, 2, $len);}
function LlutlCryptOneTimePwd2($tm,$len = 6){$salt = substr(strrev(sprintf('%d', (int)($tm / 86400))), 0, 2);
return LlutlCryptOneTimePwd($tm, $salt, $len);}
function crypt_apr1_md5($plainpasswd) {
    $salt = substr(str_shuffle("abcdefghijklmnopqrstuvwxyz0123456789"), 0, 8);
    $len = strlen($plainpasswd);
    $text = $plainpasswd.'$apr1$'.$salt;
    $bin = pack("H32", md5($plainpasswd.$salt.$plainpasswd));
    for($i = $len; $i > 0; $i -= 16) { $text .= substr($bin, 0, min(16, $i)); }
    for($i = $len; $i > 0; $i >>= 1) { $text .= ($i & 1) ? chr(0) : $plainpasswd{0}; }
    $bin = pack("H32", md5($text));
    for($i = 0; $i < 1000; $i++) {
        $new = ($i & 1) ? $plainpasswd : $bin;
        if ($i % 3) $new .= $salt;
        if ($i % 7) $new .= $plainpasswd;
        $new .= ($i & 1) ? $bin : $plainpasswd;
        $bin = pack("H32", md5($new));
    }
    for ($i = 0; $i < 5; $i++) {
        $k = $i + 6;
        $j = $i + 12;
        if ($j == 16) $j = 5;
        $tmp = $bin[$i].$bin[$k].$bin[$j].$tmp;
    }
    $tmp = chr(0).chr(0).$bin[11].$tmp;
    $tmp = strtr(strrev(substr(base64_encode($tmp), 2)),
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",
    "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz");
    return "$"."apr1"."$".$salt."$".$tmp;
}
function LlutlCryptBasic($id,$pwd){return crypt_apr1_md5($pwd); /*crypt($pwd, substr($id, 0, 2));*/ }
$LLUTL_LOG_PATH = '';
function LlutlLogSetPath($path){global $LLUTL_LOG_PATH;
$LLUTL_LOG_PATH = $path;}
function LlutlLog($file,$line,$msg){global $LLUTL_LOG_PATH;
$logpath = $LLUTL_LOG_PATH != '' ? $LLUTL_LOG_PATH : LLUTL_LOG_PATH;
$dt      = LlutlDateTime(time());
$tstamp  = sprintf("## %04d-%02d-%02d %02d:%02d:%02d ##",$dt['year'], $dt['mon'], $dt['day'], $dt['hour'], $dt['min'], $dt['sec']);
$log_no  = $dt['yday'] % 3;
$nxt_no  = $log_no + 1; if ($nxt_no >= 3) { $nxt_no = 0; }
$logfile = sprintf("%s-%d.cgi", $logpath, $log_no);
$nxtfile = sprintf("%s-%d.cgi", $logpath, $nxt_no);
$fd = @fopen($logfile, "a");
if (!$fd){LlutlMkDir(dirname($logfile));
$fd = fopen($logfile, "a");
if (!$fd){LlutlPrint('ログファイルオープンエラー');
exit;}}
fputs($fd, "$tstamp\n$file - $line\n$msg\n");
fclose($fd);
if (defined('LLUTL_MODE_MKLOG')){@chmod(dirname($logfile), LLUTL_MODE_MKLGD);
@chmod($logfile, LLUTL_MODE_MKLOG);}
else{chmod($logfile, LLUTL_MODE_MKFIL);}
@unlink($nxtfile);}
function LlutlPrint($msg){print(mb_convert_encoding($msg, LLUTL_HTTP_ENCODING, LLUTL_ENCODING));}
function LlutlTimeCheck($ctrl,$path,$sec = 0){$fname = $path.'.cgi';
$stat = @stat($fname);
if (!LlutlFileExist($fname)){$fp = fopen($fname, "a");
if (!$fp) { print(sprintf("ERROR : %s-%d\n",__FILE__,__LINE__)); exit; }
fputs($fp, sprintf("%d\n", -1));
fclose($fp);
chmod($fname, LLUTL_MODE_MKFIL);}
if ($ctrl == 'check'){if (!$stat) { return TRUE; }
$sa = time() - $stat['mtime'];
return $sa >= $sec ? TRUE : FALSE;}
else if ($ctrl == 'set'){@unlink($fname);
$fp = @fopen($fname, "w");
if (!$fp) { return FALSE; }
fputs($fp, time());
fclose($fp);
chmod($fname, LLUTL_MODE_MKFIL);
return TRUE;}
$estr = sprintf('ERROR : LlutlTimeCheck(%s) ctrl failed.', $ctrl);
LlutlLog(__FILE__, __LINE__, $estr);
print($estr);
exit;}
function LlutlDateTime($time){$wdays = array('日', '月', '火', '水', '木', '金', '土', '日');
$adays = array('SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN');
$lt  = localtime($time, 0);
$rtn = array('yday' => $lt[7],'wday' => $wdays[$lt[6]],'year' => $lt[5] + 1900,'mon'  => $lt[4] + 1,'day'  => $lt[3],'hour' => $lt[2],'min'  => $lt[1],'sec'  => $lt[0],'aday' => $adays[$lt[6]],);
return $rtn;}
function LlutlDateTimeFromDb($dbstr){$dd = preg_split('/(-| |:)/', $dbstr);
return LlutlDateTime(LlutlUnixTime($dd[0], $dd[1], $dd[2], $dd[3], $dd[4], $dd[5]));}
function LlutlUnixTime($year,$mon,$day,$hour,$min,$sec){return mktime($hour, $min, $sec, $mon, $day, $year);}
function LlutlGetSaDay($y1,$m1,$d1,$y2,$m2,$d2){$dtm1 = mktime(0, 0, 0, $m1, $d1, $y1);
$dtm2 = mktime(0, 0, 0, $m2, $d2, $y2);
return (int)(($dtm1 - $dtm2) / 86400);}
function LlutlDateCheck($yy,$mm,$dd){if ($yy < 1900 || $yy > 2100) { return FALSE; }
if ($mm < 1 || $mm > 12) { return FALSE; }
if ($dd < 1 || $dd > 31) { return FALSE; }
if ($mm == 2){$uruu = LlutlDateIsUruu($yy);
if ($uruu == TRUE  && $dd > 29) { return FALSE; }
if ($uruu == FALSE && $dd > 28) { return FALSE; }}
elseif ($mm == 4 || $mm == 6 || $mm == 9 || $mm == 11){if ($dd > 30) { return FALSE; }}
return TRUE;}
function LlutlDateIsUruu($year){$uruu = FALSE;
if     ($year % 400 == 0) { $uruu = TRUE; }
elseif ($year % 100 == 0) { $uruu = FALSE; }
elseif ($year %   4 == 0) { $uruu = TRUE; }
return $uruu;}
function LlutlDateGetMonLastDay($year,$mon){$day = 31;
if ($mon == 2){$day = LlutlDateIsUruu($year) ? 29 : 28;}
elseif ($mon==4 || $mon==6 || $mon==9 || $mon==11){$day = 30;}
return $day;}
function LlutlCutLastStr($str){if (LLUTL_ENCODING == 'SJIS' || LLUTL_ENCODING == 'SJIS-win'){$cs = unpack('C*', $str);
$tp = 0;
foreach ($cs as $c){if ($tp == 1){$tp = 2;}
else if ((0x81 <= $c && $c <= 0x9F) || (0xE0 <= $c && $c <= 0xFC)){$tp = 1;}
else{$tp = 0;}}
return $tp == 1 ? substr($str, 0, -1) : $str;}
else if (LLUTL_ENCODING == 'UTF-8'){$cs = unpack('C*', $str);
$tp = 0;
foreach ($cs as $c){if ($tp == 21 || $tp == 31 || $tp == 32 || $tp == 41 || $tp == 42 || $tp == 43){$tp ++;}
else if (0x00 <= $c && $c <= 0x7F){$tp = 11;}
else if (0xC0 <= $c && $c <= 0xDF){$tp = 21;}
else if (0xE0 <= $c && $c <= 0xEF){$tp = 31;}
else if (0xF0 <= $c && $c <= 0xF7){$tp = 41;}
else{$tp = 0;}}
if ($tp == 11 || $tp == 22 || $tp == 33 || $tp == 44)	{ return $str; }
else if ($tp == 21 || $tp == 32 || $tp == 43)			{ return substr($str, 0, -1); }
else if ($tp == 31 || $tp == 42)						{ return substr($str, 0, -2); }
else if ($tp == 43)										{ return substr($str, 0, -3); }
return $str;}}
function LlutlAddslashesSjis($str){$dst = '';
$cs = unpack('C*', $str);
$cc = '';
$tp = 0;
foreach ($cs as $c){if ($tp == 1){$tp = 2;
$c2 = chr($cc).chr($c);
$dst .= $c2;}
else if ((0x81 <= $c && $c <= 0x9F) || (0xE0 <= $c && $c <= 0xFC)){$tp = 1;}
else{$tp = 0;
$dst .= addslashes(chr($c));}
$cc = $c;}
return $dst;}
function LlutlChkEnglishOnly($str){if (LLUTL_ENCODING == 'SJIS' || LLUTL_ENCODING == LLUTL_SJIS){$str = mb_convert_kana($str, "a", LLUTL_SJIS);
$cs = unpack('C*', $str);
$tp = 0;
foreach ($cs as $c){if ($tp == 1){$tp = 2;
return FALSE;}
else if ((0x81 <= $c && $c <= 0x9F) || (0xE0 <= $c && $c <= 0xFC)){$tp = 1;
return FALSE;}
else{$tp = 0;}}
return TRUE;}
else if (LLUTL_ENCODING == 'UTF-8'){$str = mb_convert_kana($str, "a", "UTF-8");
$cs = unpack('C*', $str);
$tp = 0;
foreach ($cs as $c){if ($tp == 21 || $tp == 31 || $tp == 32 || $tp == 41 || $tp == 42 || $tp == 43){$tp ++;
return FALSE;}
else if (0x00 <= $c && $c <= 0x7F){$tp = 11;}
else if (0xC0 <= $c && $c <= 0xDF){$tp = 21;
return FALSE;}
else if (0xE0 <= $c && $c <= 0xEF){$tp = 31;
return FALSE;}
else if (0xF0 <= $c && $c <= 0xF7){$tp = 41;
return FALSE;}
else{$tp = 0;}}
return TRUE;}}
function LlutlStrCutTopCRLF($str){if (substr($str, 0, 2) == "\r\n") { return substr($str, 2); }
if (substr($str, 0, 1) == "\n")   { return substr($str, 1); }
if (substr($str, 0, 1) == "\r")   { return substr($str, 1); }
return $str;}
function LlutlStrCutBottomCRLF($str){if (substr($str, -2) == "\r\n") { return substr($str, 0, -2); }
if (substr($str, -1) == "\n")   { return substr($str, 0, -1); }
if (substr($str, -1) == "\r")   { return substr($str, 0, -1); }
return $str;}
function LlutlReplaceIf($if,$case,$html,$mpre = LLUTL_REP_MARK1,$msuf = LLUTL_REP_MARK2){$if_not = str_replace('IF_', 'IF_NOT_', $if);
$html   = LlutlReplaceIfBase($if, $case, $html, $mpre, $msuf);
$html   = LlutlReplaceIfBase($if_not, !$case, $html, $mpre, $msuf);
return $html;}
function LlutlReplaceCase($case_label,$case_key,$html,$mpre = LLUTL_REP_MARK1,$msuf = LLUTL_REP_MARK2){$htmls = explode($mpre.$case_label.$msuf, $html);
if (!isset($htmls[1])) { return $html; }
$wk    = explode($mpre.'CASE'.$msuf, ' '.LlutlStrCutTopCRLF($htmls[1]));
$html1 = substr(array_shift($wk), 1);
$nwk   = sizeof($wk);
for ($i = 0; $i < $nwk; $i += 2){$kstr = $wk[$i];
$val  = $wk[$i+1];
$case = FALSE;
$set  = TRUE;
if (substr($kstr, 0, 1) == '^'){$kstr = substr($kstr, 1);
$case = TRUE;
$set  = FALSE;}
foreach (explode(',', $kstr) as $key){if ($case_key == $key){$case = $set;
break;}}
if ($case) { $html1 .= LlutlStrCutTopCRLF($val); }}
return $htmls[0].$html1.LlutlStrCutTopCRLF($htmls[2]);}
function LlutlReplaceIfBase($if,$case,$html,$mpre = LLUTL_REP_MARK1,$msuf = LLUTL_REP_MARK2){$rhtml = '';
$cnt   = 0;
$htmls = explode($mpre.$if.$msuf, $html);
foreach ($htmls as $chtml){$chtmls = explode($mpre.'/'.$if.$msuf, $chtml);
foreach ($chtmls as $dhtml){if ($cnt % 2 == 0 || $case) { $rhtml .= LlutlStrCutTopCRLF($dhtml); }
$cnt ++;}}
return $rhtml;}
function LlutlChkHtmlIfStat($html,$mpre = LLUTL_REP_MARK1,$msuf = LLUTL_REP_MARK2){$ifs = array(0 => array(), 1 => array());
foreach (array(0 => $mpre.'IF_', 1 => $mpre.'/IF_') as $idx => $chk){$wk1 = explode($chk,  $html);
array_shift($wk1);
foreach ($wk1 as $str){$wk2 = explode($msuf, $str);
$if  = $wk2[0];
if (!isset($ifs[$idx][$if])) { $ifs[$idx][$if] = 0; }
$ifs[$idx][$if] ++;}}
foreach ($ifs[0] as $str => $cnt){if (!isset($ifs[1][$str]) || $cnt != $ifs[1][$str]){return $mpre.'IF_'.$str.$msuf.' ～ '.$mpre.'/IF_'.$str.$msuf.' が正しく指定されていません。';}}
foreach ($ifs[1] as $str => $cnt){if (!isset($ifs[0][$str]) || $cnt != $ifs[0][$str]){return $mpre.'IF_'.$str.$msuf.' ～ '.$mpre.'/IF_'.$str.$msuf.' が正しく指定されていません。';}}
return '';}
function LlutlReplaceCase2($case_label,$case_key,$html,$mpre = LLUTL_REP_MARK1,$msuf = LLUTL_REP_MARK2){$htmls = explode($mpre.$case_label.$msuf, $html);
if (!isset($htmls[1])) { return $html; }
$html = '';
$cnt  = 0;
foreach ($htmls as $wkhtml){if ($cnt % 2 == 1){$html .= LlutlReplaceCase2Base($case_key, $wkhtml, $mpre, $msuf);}
else{$html .= $wkhtml;}
$cnt ++;}
return $html;}
function LlutlReplaceCase2Base($case_key,$html,$mpre = LLUTL_REP_MARK1,$msuf = LLUTL_REP_MARK2){$wk    = explode($mpre.'CASE'.$msuf, ' '.$html);
$html1 = substr(array_shift($wk), 1);
$nwk   = sizeof($wk);
for ($i = 0; $i < $nwk; $i += 2){$kstr = $wk[$i];
$val  = $wk[$i+1];
$case = FALSE;
$set  = TRUE;
if (substr($kstr, 0, 1) == '^'){$kstr = substr($kstr, 1);
$case = TRUE;
$set  = FALSE;}
foreach (explode(',', $kstr) as $key){if ($case_key == $key){$case = $set;
break;}}
if ($case) { $html1 .= $val; }}
return LlutlStrCutTopCRLF($html1);}
function LlutlReplaceKtai($html){$prep = array();
$ktp  = LlutlGetKtp();
if ($ktp == 'i'){$prep['/\.png/'] = '.gif';}
elseif ($ktp == 'j'){$prep['/\.gif/'] = '.png';
if (stristr(LlutlEnv('HTTP_USER_AGENT'), 'J-PHONE/2.0')){$prep['/method=post/i'] = 'method=get';}}
elseif ($ktp == 'p'){$prep['/<body([^>]*)>/i'] = '<body$1><table align=center border=1 cellpadding=10 width=150><tr><td><tt>';
$prep['/<\/body>/i'] = '</tt></td></tr></table></body>';}
if ($ktp != 'j' && $ktp != 'p'){$prep['/enctype=([^ ]*)/i'] = '';}
return preg_replace(array_keys($prep), array_values($prep), $html);}
$LLUTL_GET_TMP_DIR = './';
function LlutlGetTmpDir($dir){global $LLUTL_GET_TMP_DIR;
$rtn = $LLUTL_GET_TMP_DIR;
$LLUTL_GET_TMP_DIR = $dir;
return $rtn;}
function LlutlHtmlXhtmlTag($type){if      ($type == '>')        { return LlutlIsXhtml() ? ' />'    : '>'; }
else if ($type == '<br>')     { return LlutlIsXhtml() ? '<br />' : '<br>'; }
else if ($type == 'checked')  { return LlutlIsXhtml() ? ' checked="checked"'    : ' checked'; }
else if ($type == 'selected') { return LlutlIsXhtml() ? ' selected="selected" ' : ' selected'; }
return '';}
$LLUTL_CHK_XHTML = FALSE;
function LlutlChkXhtml(&$html){global $LLUTL_CHK_XHTML;
$LLUTL_CHK_XHTML = preg_match('/<html([^>]*)xhtml/i', $html);}
function LlutlIsXhtml(){global $LLUTL_CHK_XHTML;
return $LLUTL_CHK_XHTML;}
function LlutlGetTmp($pid){$stac = 0;
$html = LlutlGetTmpHtml($pid, $stac);
if (defined('LLUTL_TMP_ENCODING') && strcmp(LLUTL_ENCODING, LLUTL_TMP_ENCODING) != 0){$html = mb_convert_encoding($html, LLUTL_ENCODING, LLUTL_TMP_ENCODING);}
LlutlChkXhtml($html);
return $html;}
function LlutlIncludeHtml(&$html,$label,$file){$data = LlutlGetFile($file);
$html = str_replace($label, $data, $html);}
function LlutlGetTmpHtml($pid,&$stac){global $LLUTL_GET_TMP_DIR;
$stac ++;
if ($stac > 5){LlutlPrint('入れ子のページが多すぎます');
exit;}
$pid = str_replace("\0", '', basename(trim($pid)));
$html = LlutlGetFile($LLUTL_GET_TMP_DIR."tmp-$pid.html", $LLUTL_GET_TMP_DIR."tmp-$pid.htm");
$htmls = explode(LLUTL_REP_MARK1.'TMP_HTML'.LLUTL_REP_MARK2, $html);
if (sizeof($htmls) > 1){$html = '';
$cnt  = 0;
foreach ($htmls as $hstr){if ($cnt % 2 == 0){$html .= $hstr;}
else{$pid   = $hstr;
$html .= LlutlGetTmpHtml($pid, $stac);}
$cnt ++;}}
$stac --;
return $html;}
function LlutlMailSenderInfo(){$ip_addr = LlutlRemoteAddr();
$info  = '';
$info .= 'USER AGENT: '.LlutlEnv('HTTP_USER_AGENT')."\n";
$info .= 'IP ADDRESS: '.$ip_addr;
return $info;}
function LlutlGetSelOpt(&$list,$val){$opt = '';
foreach ($list as $lval => $lstr){$sel = strcmp($lval, $val) == 0 ? LlutlHtmlXhtmlTag('selected') : '';
$opt.= "<option value=\"${lval}\" ${sel}>${lstr}</option>\n";}
return $opt;}
function LlutlGetCheckBox($fname,$fval,$val){$chk = $fval == $val ? LlutlHtmlXhtmlTag('checked') : '';
$tge = LlutlHtmlXhtmlTag('>');
return "<input type=\"checkbox\" name=\"${fname}\" value=\"${fval}\" ${chk}${tge}";}
function LlutlGetRadio($fname,&$list,$val,$fsep){$opt = '';
$joi = '';
$tge = LlutlHtmlXhtmlTag('>');
foreach ($list as $lval => $lstr){$sel = strcmp($lval, $val) == 0 ? LlutlHtmlXhtmlTag('checked') : '';
$opt.= "$joi<input type=\"radio\" name=\"${fname}\" value=\"${lval}\" ${sel}${tge}${lstr}\n";
$joi = $fsep;}
return $opt;}
function LlutlInchkExist(&$ips,$fid){if (!isset($ips[$fid])) { return FALSE; }
if (is_array($ips[$fid])){if (sizeof($ips[$fid]) <= 0)   { return FALSE; }}
else{if ($ips[$fid] == '')   { return FALSE; }}
return TRUE;}
function LlutlInchkHankaku($str,$chk = '0-9A-Za-z'){$str_len = strlen($str);
for ($i = 0; $i < $str_len; $i ++){$c = substr($str, $i, 1);
if (!preg_match('/['.$chk.']/', $c)) { return FALSE; }}
return TRUE;}
function LlutlInchkRange($str,$min,$max){if ($str == '') { return TRUE; }
$num = LlutlGetNum($str);
if ($num == '') { return FALSE; }
if ($num < $min || $max < $num) { return FALSE; }
return TRUE;}
function LlutlRemoteAddr(){$addr = LlutlEnv('HTTP_X_FORWARDED_FOR');
return $addr != '' ? $addr : LlutlEnv('REMOTE_ADDR');}
function LlutlUserAgentCutQuot($ua = ''){if ($ua == '') { $ua = LlutlEnv('HTTP_USER_AGENT'); }
return str_replace(array('"',"'"), array('',''), $ua);}
$LLUTL_SESSION3_START = FALSE;
function LlutlSession3_start($sid = ''){global $LLUTL_SESSION3_START;
if (!$LLUTL_SESSION3_START){if (defined('LLUTL_SESSION_DIR')){LlutlMkDir(LLUTL_SESSION_DIR);
session_save_path(LLUTL_SESSION_DIR);}
if ($sid != '') { @session_id($sid); }
@session_start();
$LLUTL_SESSION3_START = TRUE;}}
function LlutlSession3Set($key,$val,$sid = ''){LlutlSession3_start($sid);
$_SESSION[$key] = $val;}
function LlutlSession3Get($key,$sid = ''){LlutlSession3_start($sid);
if (!isset($_SESSION[$key])) { return ''; }
return $_SESSION[$key];}
function LlutlSession3Defined($key,$sid = ''){LlutlSession3_start($sid);
return isset($_SESSION[$key]);}
function LlutlSession3Clear($sid = ''){global $LLUTL_SESSION3_START;
LlutlSession3_start($sid);
if ($LLUTL_SESSION3_START){if (is_array($_SESSION)){foreach ($_SESSION as $key => $val){session_unregister($key);
unset($_SESSION[$key]);}}
if (isset($_COOKIE[session_name()])){setcookie(session_name(), '', time()-42000, '/');}
session_destroy();
$LLUTL_SESSION3_START = FALSE;}}
function LlutlSession3Id(){global $LLUTL_SESSION3_START;
if ($LLUTL_SESSION3_START){$sids = explode('=', strip_tags(SID));
return isset($sids[1]) ? $sids[1] : '';}
return '';}
define('LLUTL_SESSION_TYPE_PARA', 'GP'.LLUTL_SITE_ID);
function LlutlGPSet($group,$pfid,$val){global $GLOBAL_PARA;
if (!isset($GLOBAL_PARA[$group])  || !isset($GLOBAL_PARA[$group][$pfid]))
{ print("global parameter error : $group - $pfid"); exit; }
$key = LLUTL_SESSION_TYPE_PARA.'_'.$group.'_'.$pfid;
LlutlSession3Set($key, $val);
return $val;}
function LlutlGPGet($group,$pfid,$def = ''){global $GLOBAL_PARA;
if (!isset($GLOBAL_PARA[$group])  || !isset($GLOBAL_PARA[$group][$pfid]))
{ print("global parameter error : $group - $pfid"); exit; }
$key = LLUTL_SESSION_TYPE_PARA.'_'.$group.'_'.$pfid;
return LlutlSession3Defined($key) ? LlutlSession3Get($key) : $def;}
function LlutlGPIsSet($group,$pfid){global $GLOBAL_PARA;
if (!isset($GLOBAL_PARA[$group])  || !isset($GLOBAL_PARA[$group][$pfid]))
{ print("global parameter error : $group - $pfid"); exit; }
$key = LLUTL_SESSION_TYPE_PARA.'_'.$group.'_'.$pfid;
return LlutlSession3Defined($key);}
function LlutlGPClear($group = '',$pfid = ''){global $GLOBAL_PARA;
$prekey = LLUTL_SESSION_TYPE_PARA.'_';
if ($group != '') $prekey .= $group.'_';
if ($pfid  != '') $prekey .= $pfid;
$lprekey = strlen($prekey);
LlutlSession3_start();
$keys = array();
foreach ($_SESSION as $key => $val){if (strncmp($key, $prekey, $lprekey) == 0) { $keys[] = $key; }}
foreach ($keys as $key){session_unregister($key);
unset($_SESSION[$key]);}}
function LlutlIsSSL(){$env = LlutlEnv('SSL_PROTOCOL');
if ($env == '') { return FALSE; }
return TRUE;}
function LlutlStrToHex($src){return join('',unpack('H*',$src));}
function LlutlHexToStr($src){return pack('H*', $src);}
function LlutlStrToAngo($seed,$str,&$ivh){if ($str == '') { return ''; }
$td  = mcrypt_module_open('rijndael-256', '', 'ofb', '');
$iv  = mcrypt_create_iv(mcrypt_enc_get_iv_size($td), MCRYPT_DEV_RANDOM);
$ivh = join('',unpack('H*',$iv));
$ks  = mcrypt_enc_get_key_size($td);
$key = substr(md5($seed), 0, $ks);
mcrypt_generic_init($td, $key, $iv);
$ango = mcrypt_generic($td, $str);
mcrypt_generic_deinit($td);
mcrypt_module_close($td);
return join('',unpack('H*',$ango));}
function LlutlAngoToStr($seed,$ango,$ivh){if ($ango == '') { return ''; }
$td = mcrypt_module_open('rijndael-256', '', 'ofb', '');
$iv = pack('H*', $ivh);
$ks = mcrypt_enc_get_key_size($td);
$key = substr(md5($seed), 0, $ks);
mcrypt_generic_init($td, $key, $iv);
$str = mdecrypt_generic($td, pack('H*', $ango));
mcrypt_generic_deinit($td);
mcrypt_module_close($td);
return $str;}
function LlutlGetWebPage($url,&$cookies,$method = "GET",$post = array(),$headers = '',$localhost = FALSE){$port_http  = 80;
$port_https = 443;
$urls       = parse_url($url);
$url_scheme = $urls['scheme'];
$url_host   = $urls['host'];
$url_path   = $urls['path'];
$url_query  = isset($urls['query']) ? '?'.$urls['query'] : '';
$def_port   = $url_scheme == 'https' ? $port_https : $port_http;
$url_port   = isset($urls['port'])  ? $urls['port'] : $def_port;
$url_user   = isset($urls['user'])  ? $urls['user'] : '';
$url_pass   = isset($urls['pass'])  ? $urls['pass'] : '';
$request = '';
$request .= "$method $url_path$url_query HTTP/1.0\r\n";
$request .= "Host: $url_host\r\n";
$request .= "User-Agent: PHP/".phpversion()."\r\n";
if ($url_user != '' && $url_pass != ''){$request .= "Authorization: Basic ".base64_encode("$url_user:$url_pass")."\r\n";}
if (sizeof($cookies) > 0){$chead = '';
$cjoi  = 'Cookie: ';
foreach ($cookies as $fid => $fval){$chead .= $cjoi . $fid . '=' . $fval;
$cjoi   = '; ';}
$request .= $chead."\r\n";}
$request .= $headers;
if (strtoupper($method) == "POST"){$postwk = array();
while (list($name, $value) = each($post)){$postwk[] = $name."=".urlencode($value);}
$postdata = implode("&", $postwk);
$request .= "Content-Type: application/x-www-form-urlencoded\r\n";
$request .= "Content-Length: ".strlen($postdata)."\r\n";
$request .= "\r\n";
$request .= $postdata;}
else{$request .= "\r\n";}
$errno    = '';
$errstr   = '';
$soc_host = $localhost ? 'localhost' : $url_host;
if ($url_scheme == 'https') { $soc_host = 'ssl://'.$soc_host; }

$fp = fsockopen($soc_host, $url_port, $errno, $errstr, 60);
if (!$fp){print(sprintf("fsockopen(%s) fail. %s (%s)\n", $soc_host, $errstr, $errno));
return "$errstr ($errno)".LlutlHtmlXhtmlTag('<br>')."\n";}
fputs($fp, $request);
$response = "";
while (!feof($fp)){$response .= fgets($fp, 4096);}
fclose($fp);
$DATA = explode("\r\n\r\n", $response, 2);
$res_head = $DATA[0];
$res_data = $DATA[1];
$wks = explode("\r\n", $res_head);
foreach ($wks as $line){$lwks = preg_split('/(:|=|;)/', trim($line));
if ($lwks[0] == 'Set-Cookie'){$cname = trim($lwks[1]);
$cval  = trim($lwks[2]);
$cookies[$cname] = $cval;}}
return $res_data;}
function LlutlRtrim($str,$code){if (LLUTL_PHP_VERSION >= 410) { return rtrim($str, $code); }
$len = strlen($str);
for ($i = $len ; $i > 0; $i --){$c = substr($str, $i-1, 1);
if (!strstr($code, $c)) { break; }}
return $i <= 0 ? '' : substr($str, 0, $i);}
define('LLIDF_PASS_TP_DAY',   'D');
define('LLIDF_PASS_TP_MONTH', 'M');
function LlidfGetCounter($path,$chkstr){$referer = LlutlEnv('HTTP_REFERER');
foreach (explode(',', $chkstr) as $str){if (strstr($referer, $str)) { return LlidfGetCurrent($path); }}
return LlidfGetNext($path);}
function LlidfPassTimeChk($path,$pass_tp,$now_tm,$chk_dhm){$now_lt = localtime($now_tm, 0);
$lid = LlidfOpen($path);
$set_tm = LlidfGet($lid);
LlidfClose($lid);
if ($set_tm <= 0) { return TRUE; }
$set_lt = localtime($set_tm, 0);
if ($pass_tp == LLIDF_PASS_TP_DAY){$pass_day = LlutlGetSaDay($now_lt[5]+1900, $now_lt[4]+1, $now_lt[3],$set_lt[5]+1900, $set_lt[4]+1, $set_lt[3]);
if ($pass_day <= 0) { return FALSE; }
if ($pass_day >= 2) { return TRUE; }
$now_min = ($now_lt[2] * 60) + $now_lt[1];
$chk_min = ($chk_dhm['hour'] * 60) + $chk_dhm['min'];
if ($now_min >= $chk_min) { return TRUE; }
return FALSE;}
elseif ($pass_tp == LLIDF_PASS_TP_MONTH){$now_mon = ($now_lt[5] * 12) + $now_lt[4];
$set_mon = ($set_lt[5] * 12) + $set_lt[4];
$pass_mon = $now_mon - $set_mon;
if ($pass_mon <= 0) { return FALSE; }
if ($pass_mon >= 2) { return TRUE; }
$now_min = ($now_lt[3] * 1440) + ($now_lt[2] * 60) + $now_lt[1];
$chk_min = ($chk_dhm['day'] * 1440) + ($chk_dhm['hour'] * 60) + $chk_dhm['min'];
if ($now_min >= $chk_min) { return TRUE; }
return FALSE;}
return FALSE;}
function LlidfPassTimeSet($path,$now_tm){$lid = LlidfOpen($path);
LlidfSet($lid, $now_tm);
LlidfClose($lid);}
function LlidfGetNext($path,$minval = 0,$maxval = 0){$lid = LlidfOpen($path);
$id = LlidfGet($lid);
$id ++;
if     ($id < $minval) { $id = $minval; }
elseif ($maxval > $minval && $id > $maxval) { $id = $minval; }
LlidfSet($lid, $id);
LlidfClose($lid);
return $id;}
function LlidfGetCurrent($path){$lid = LlidfOpen($path);
$id = LlidfGet($lid);
LlidfClose($lid);
return $id;}
function LlidfGetNextTime($path){$tm = time();
$lid = LlidfOpen($path);
$id = LlidfGet($lid);
if ($tm <= $id) { $tm = $id + 1; }
LlidfSet($lid, $tm);
LlidfClose($lid);
return $tm;}
function LlidfRealFileName($path){return $path.'.cgi';}
function LlidfFileExist($path){return LlutlFileExist(LlidfRealFileName($path));}
function LlidfOpen($path){$fname = $path.'.cgi';
if (!LlutlFileExist($fname)){LlutlMkDir(dirname($fname));
$fp = fopen($fname, "a");
if (!$fp) { print(sprintf("ERROR : %s-%d\n",__FILE__,__LINE__)); exit; }
fputs($fp, sprintf("%d\n", -1));
fclose($fp);
chmod($fname, LLUTL_MODE_MKFIL);}
$lid = LlutlFileOpenLock($fname, 'r+');
return $lid;}
function LlidfClose($lid){LlutlFileCloseUnlock($lid);}
function LlidfGet($lid){fseek($lid['fp'], 0, 0);
$id = LlutlRtrim(fgets($lid['fp'], 256), "\r\n");
return $id;}
function LlidfSet($lid,$id){fseek($lid['fp'], 0, 0);
if (fputs($lid['fp'], sprintf("%d\n", $id)) <= 0){LlutlPrint("ファイルに書き込めません\n");
exit;}
fflush($lid['fp']);}
define('LLTBF_POS_BOT', -1);
define('LLTBF_WILD_CARD', '*');
define('LLTBF_REC_MAX_SIZE', 81920);
define('LLTBF_MARK_CRLF', '<#CRLF#>');
define('LLTBF_MARK_CR',   '<#CR#>');
define('LLTBF_MARK_LF',   '<#LF#>');
define('LLTBF_MARK_TAB',  '<#TAB#>');
$LLTBF_AUTO_LOCK = TRUE;
function LltbfInsert($path,$fld,$pos){if ($pos == LLTBF_POS_BOT){return LltbfInsertBot($path, $fld);}
elseif ($pos <= 1){return LltbfInsertTop($path, $fld);}
$fname = Lltbf_Initilize($path);
$loc = Lltbf_Lock($fname);
$fp_dat = fopen($fname['DAT'], "r");
if (!$fp_dat) { print(sprintf("ERROR : %s-%d\n",__FILE__,__LINE__)); exit; }
$fp_tmp = fopen($fname['TMP'], "w");
if (!$fp_tmp) { print(sprintf("ERROR : %s-%d\n",__FILE__,__LINE__)); exit; }
$ins = 0;
$cnt = 1;
while (!feof($fp_dat)){if ($cnt == $pos){Lltbf_Fputs($fp_tmp, LltbfFieldToLine($fld) . "\n");
$ins ++;}
Lltbf_Fputs($fp_tmp, fgets($fp_dat, LLTBF_REC_MAX_SIZE));
$cnt ++;}
if ($ins == 0){Lltbf_Fputs($fp_tmp, LltbfFieldToLine($fld) . "\n");}
if (!fclose($fp_tmp)){LlutlPrint("ファイルに書き込めません\n");
exit;}
fclose($fp_dat);
LltbfRenameTmpToDat($path);
Lltbf_Unlock($loc);
return sizeof($fld);}
function LltbfInsertTop($path,$fld){$fname = Lltbf_Initilize($path);
$loc = Lltbf_Lock($fname);
$fp_dat = fopen($fname['DAT'], "r");
if (!$fp_dat) { print(sprintf("ERROR : %s-%d\n",__FILE__,__LINE__)); exit; }
$fp_tmp = fopen($fname['TMP'], "w");
if (!$fp_tmp) { print(sprintf("ERROR : %s-%d\n",__FILE__,__LINE__)); exit; }
Lltbf_Fputs($fp_tmp, LltbfFieldToLine($fld) . "\n");
$cnt = 0;
while (!feof($fp_dat)){Lltbf_Fputs($fp_tmp, fgets($fp_dat, LLTBF_REC_MAX_SIZE));}
if (!fclose($fp_tmp)){LlutlPrint("ファイルに書き込めません\n");
exit;}
fclose($fp_dat);
LltbfRenameTmpToDat($path);
Lltbf_Unlock($loc);
return sizeof($fld);}
function LltbfInsertBot($path,$fld){$fname = Lltbf_Initilize($path);
$loc = Lltbf_Lock($fname);
$fp_dat = fopen($fname['DAT'], "a");
if (!$fp_dat) { print(sprintf("ERROR : %s-%d\n",__FILE__,__LINE__)); exit; }
Lltbf_Fputs($fp_dat, LltbfFieldToLine($fld) . "\n");
if (!fclose($fp_dat)){LlutlPrint("ファイルに書き込めません\n");
exit;}
Lltbf_Unlock($loc);
return sizeof($fld);}
function LltbfSelect($path,$key_idx,$key_val,&$fld){$keys = array($key_idx => "$key_val");
return LltbfSelect2($path, $keys, $fld);}
function LltbfSelect2($path,$keys,&$fld){$fname = Lltbf_Initilize($path);
$loc = Lltbf_Lock($fname);
$fp_dat = fopen($fname['DAT'], "r");
if (!$fp_dat) { print(sprintf("ERROR : %s-%d\n",__FILE__,__LINE__)); exit; }
while (!feof($fp_dat)){$fld = LltbfGetField($fp_dat);
$same_rec = TRUE;
foreach($keys as $idx => $val){if (!isset($fld[$idx]) || !Lltbf_IsMatch($fld[$idx], $val)) { $same_rec = FALSE; break; }}
if ($same_rec){fclose($fp_dat);
Lltbf_Unlock($loc);
return sizeof($fld);}}
fclose($fp_dat);
Lltbf_Unlock($loc);
return -1;}
function LltbfDelete($path,$key_idx,$key_val){$keys = array($key_idx => "$key_val");
return LltbfDelete2($path, $keys);}
function LltbfDelete2($path,$keys){$fname = Lltbf_Initilize($path);
$loc = Lltbf_Lock($fname);
$fp_dat = fopen($fname['DAT'], "r");
if (!$fp_dat) { print(sprintf("ERROR : %s-%d\n",__FILE__,__LINE__)); exit; }
$fp_tmp = fopen($fname['TMP'], "w");
if (!$fp_tmp) { print(sprintf("ERROR : %s-%d\n",__FILE__,__LINE__)); exit; }
$cnt = 0;
while (!feof($fp_dat)){$line = fgets($fp_dat, LLTBF_REC_MAX_SIZE);
if ($line == '') { continue; }
$fld = LltbfLineToField($line);
$same_rec = TRUE;
foreach($keys as $idx => $val){if (!isset($fld[$idx]) || !Lltbf_IsMatch($fld[$idx], $val)) { $same_rec = FALSE; break; }}
if ($same_rec){$cnt ++;}
else{Lltbf_Fputs($fp_tmp, $line);}}
if (!fclose($fp_tmp)){LlutlPrint("ファイルに書き込めません\n");
exit;}
fclose($fp_dat);
LltbfRenameTmpToDat($path);
Lltbf_Unlock($loc);
return $cnt;}
function LltbfDeleteRec($path,$num1,$num2){$fname = Lltbf_Initilize($path);
$loc = Lltbf_Lock($fname);
$fp_dat = fopen($fname['DAT'], "r");
if (!$fp_dat) { print(sprintf("ERROR : %s-%d\n",__FILE__,__LINE__)); exit; }
$fp_tmp = fopen($fname['TMP'], "w");
if (!$fp_tmp) { print(sprintf("ERROR : %s-%d\n",__FILE__,__LINE__)); exit; }
$cnt = 0;
$del = 0;
while (!feof($fp_dat)){$line = fgets($fp_dat, LLTBF_REC_MAX_SIZE);
if ($line == '') { continue; }
$cnt ++;
if ( $num1 <= $cnt && ($cnt <= $num2 || $num2 <= 0) ){$del ++;}
else{Lltbf_Fputs($fp_tmp, $line);}}
if (!fclose($fp_tmp)){LlutlPrint("ファイルに書き込めません\n");
exit;}
fclose($fp_dat);
LltbfRenameTmpToDat($path);
Lltbf_Unlock($loc);
return $del;}
function LltbfUpdate($path,$key_idx,$key_val,$fld){$keys = array($key_idx => "$key_val");
return LltbfUpdate2($path, $keys, $fld);}
function LltbfUpdate2($path,$keys,$fld){$fname = Lltbf_Initilize($path);
$loc = Lltbf_Lock($fname);
$fp_dat = fopen($fname['DAT'], "r");
if (!$fp_dat) { print(sprintf("ERROR : %s-%d\n",__FILE__,__LINE__)); exit; }
$fp_tmp = fopen($fname['TMP'], "w");
if (!$fp_tmp) { print(sprintf("ERROR : %s-%d\n",__FILE__,__LINE__)); exit; }
$up_line = LltbfFieldToLine($fld). "\n";
$cnt = 0;
while (!feof($fp_dat)){$line = fgets($fp_dat, LLTBF_REC_MAX_SIZE);
if ($line == '') { continue; }
$fld = LltbfLineToField($line);
$same_rec = TRUE;
foreach($keys as $idx => $val){if (!isset($fld[$idx]) || !Lltbf_IsMatch($fld[$idx], $val)) { $same_rec = FALSE; break; }}
if ($same_rec){Lltbf_Fputs($fp_tmp, $up_line);
$cnt ++;}
else{Lltbf_Fputs($fp_tmp, $line);}}
if (!fclose($fp_tmp)){LlutlPrint("ファイルに書き込めません\n");
exit;}
fclose($fp_dat);
LltbfRenameTmpToDat($path);
Lltbf_Unlock($loc);
return $cnt;}
function LltbfRecCount($path){$fname = Lltbf_Initilize($path);
$fp_dat = fopen($fname['DAT'], "r");
if (!$fp_dat) { print(sprintf("ERROR : %s-%d\n",__FILE__,__LINE__)); exit; }
$cnt = 0;
while (!feof($fp_dat)){$line = fgets($fp_dat, LLTBF_REC_MAX_SIZE);
if ($line == '') { continue; }
$cnt ++;}
fclose($fp_dat);
return $cnt;}
function LltbfGetField($fp_dat){return LltbfLineToField(fgets($fp_dat, LLTBF_REC_MAX_SIZE));}
function LltbfGetFname($path){return Lltbf_Initilize($path);}
function LltbfRenameTmpToDat($path){$fname = Lltbf_Initilize($path);
$old_path = $fname['DAT'] . '.old';
if (LlutlFileExist($old_path)){print("rename error!");
return;}
rename($fname['DAT'], $old_path);
rename($fname['TMP'], $fname['DAT']);
unlink($old_path);
chmod($fname['DAT'], LLUTL_MODE_MKFIL);}
function LltbfLineToField($line){$line = LlutlRtrim($line, "\r\n");
$fld  = explode("\t", $line);
return str_replace(array(LLTBF_MARK_CRLF, LLTBF_MARK_LF, LLTBF_MARK_CR, LLTBF_MARK_TAB),array("\r\n",          "\n",          "\r",          "\t"),$fld);}
function LltbfFieldToLine($fld){$fld2 = str_replace(array("\r\n",          "\n",          "\r",          "\t"),array(LLTBF_MARK_CRLF, LLTBF_MARK_LF, LLTBF_MARK_CR, LLTBF_MARK_TAB),$fld);
return join("\t", $fld2);}
function LltbfIndexToKey($ifld,$keys){$kfld = array();
$nfld = count($ifld);
$idx  = 0;
foreach ( $keys as $key ){if ($idx < $nfld){$kfld[$key] = $ifld[$idx];}
else{$kfld[$key] = '';}
$idx ++;}
return $kfld;}
function LltbfKeyToIndex($kfld,$keys){$ifld = array();
$idx  = 0;
foreach ( $keys as $key ){$ifld[$idx] = $kfld[$key];
$idx ++;}
return $ifld;}
function LltbfFileToArray($path){$rtn = array();
$fname = LltbfGetFname($path);
$loc = Lltbf_Lock($fname);
$fp_dat = fopen($fname['DAT'], "r");
$idx = 0;
while ($fp_dat && !feof($fp_dat)){$line = fgets($fp_dat, LLTBF_REC_MAX_SIZE);
if ($line == '') { continue; }
$rtn[$idx] = LltbfLineToField($line);
$idx ++;}
fclose($fp_dat);
Lltbf_Unlock($loc);
return $rtn;}
function LltbfFileToKeyVal($path,$idx_key,$idx_val){$rtn = array();
$fname = LltbfGetFname($path);
$loc = Lltbf_Lock($fname);
$fp_dat = fopen($fname['DAT'], "r");
$idx = 0;
while ($fp_dat && !feof($fp_dat)){$line = fgets($fp_dat, LLTBF_REC_MAX_SIZE);
if ($line == '') { continue; }
$ifld = LltbfLineToField($line);
$key  = $ifld[$idx_key];
$val  = $ifld[$idx_val];
$rtn[$key] = $val;}
fclose($fp_dat);
Lltbf_Unlock($loc);
return $rtn;}
function LltbfArrayToFile($path,&$data){$fname = LltbfGetFname($path);
$loc = Lltbf_Lock($fname);
$fp_dat = fopen($fname['DAT'], "w");
foreach ($data as $ifld){Lltbf_Fputs($fp_dat, LltbfFieldToLine($ifld) . "\n");}
if (!fclose($fp_dat)){LlutlPrint("ファイルに書き込めません\n");
exit;}
Lltbf_Unlock($loc);}
function LltbfArrayToStr($data,$fjoi,$rjoi){$rtn = '';
$joi = '';
foreach ($data as $fld){foreach ($fld as $val){$val = str_replace($rjoi[0], $rjoi[1], $val);
$val = str_replace($fjoi[0], $fjoi[1], $val);
$rtn .= $joi . $val;
$joi = $fjoi[0];}
$joi = $rjoi[0];}
return $rtn;}
function LltbfStrToArray($str,$fjoi,$rjoi){$str = str_replace($rjoi, "\t", $str);
$lines = explode("\t", $str);
$rtn = array();
$idx = 0;
foreach ($lines as $line){$line = str_replace($fjoi, "\t", $line);
$ifld = explode("\t", $line);
$rtn[$idx] = $ifld;
$idx ++;}
return $rtn;}
function LltbfUnlink($path){$fname = LltbfGetFname($path);
@unlink($fname['DAT']);
@unlink($fname['LOC']);
@unlink($fname['TMP']);}
function LltbfNewField($fmt){$fld = array();
foreach ($fmt as $val){$fld[$val] = '';}
return $fld;}
function LltbfExist($path){$fname = Lltbf_GetFname($path);
return LlutlFileExist($fname['DAT']);}
function LltbfAutoLock($flag){global $LLTBF_AUTO_LOCK;
$rtn = $LLTBF_AUTO_LOCK;
$LLTBF_AUTO_LOCK = $flag;
return $rtn;}
function LltbfLock($fname){return LlutlFileOpenLock($fname['LOC'], 'r+');}
function LltbfUnlock(&$loc){LlutlFileCloseUnlock($loc);}
function LltbfRename($fr_path,$to_path){$fr_fname = Lltbf_GetFname($fr_path);
$to_fname = Lltbf_GetFname($to_path);
@rename($fr_fname['DAT'], $to_fname['DAT']);
@rename($fr_fname['LOC'], $to_fname['LOC']);}
function Lltbf_Initilize($path){$fname = Lltbf_GetFname($path);
if (!LlutlFileExist($fname['DAT'])){LlutlMkDir(dirname($fname['DAT']));
$fp_dat = fopen($fname['DAT'], "a");
if (!$fp_dat){print(sprintf("ERROR : %s-%d : fopen(%s) failed\n",__FILE__,__LINE__,$fname['DAT']));
exit;}
fclose($fp_dat);
chmod($fname['DAT'], LLUTL_MODE_MKFIL);}
if (!LlutlFileExist($fname['LOC'])){$fp_loc = fopen($fname['LOC'], "a");
if (!$fp_loc){print(sprintf("ERROR : %s-%d : fopen(%s) failed\n",__FILE__,__LINE__,$fname['LOC']));
exit;}
fclose($fp_loc);
chmod($fname['LOC'], LLUTL_MODE_MKFIL);}
return $fname;}
function Lltbf_GetFname($path){return array('DAT' => $path.'.cgi','TMP' => $path.'.tmp','LOC' => $path.'.loc');}
function Lltbf_Fputs($fp,$data){if (strlen($data) > 0){if (fputs($fp, $data) <= 0){LlutlPrint("ファイルに書き込めません\n");
exit;}}}
function Lltbf_IsMatch($str1,$str2){$str1 = str_replace("\r", '', $str1);
$str2 = str_replace("\r", '', $str2);
$len = strlen($str2);
if ($len == 0){return strlen($str1) == 0 ? TRUE : FALSE;}
elseif (substr($str2, -1) == LLTBF_WILD_CARD){return strncmp($str1, $str2, $len-1) == 0 ? TRUE : FALSE;}
else{return strcmp($str1, $str2) == 0 ? TRUE : FALSE;}}
function Lltbf_Lock(&$fname){global $LLTBF_AUTO_LOCK;
return $LLTBF_AUTO_LOCK ? LltbfLock($fname) : '';}
function Lltbf_Unlock(&$loc){global $LLTBF_AUTO_LOCK;
if ($LLTBF_AUTO_LOCK) { LltbfUnlock($loc); }}
?>
