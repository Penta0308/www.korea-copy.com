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
define('MYDIR',   dirname(__FILE__));
define('MYDIRNM', basename(MYDIR));
define('LLUTL_ENCODING',		'UTF-8');
define('LLUTL_HTTP_ENCODING',	'UTF-8');
define('LLUTL_SJIS',			'SJIS-win');
error_reporting(E_ALL);
ini_set('display_errors', TRUE);
mb_language("Japanese");
mb_internal_encoding(LLUTL_ENCODING);
mb_http_output(LLUTL_HTTP_ENCODING);
@putenv("TZ=Asia/Tokyo");
ini_set('session.name',				'pses');
ini_set('session.cache_limiter',	'none');
ini_set('session.gc_maxlifetime',	'3600');
ini_set('session.use_cookies',		'1');
ini_set('session.use_only_cookies',	'1');
ini_set('session.use_trans_sid',	'0');
include_once(MYDIR."/../lib/set-wbmsg.php.cgi");
include_once(MYDIR."/set-wbmsg.php.cgi");
include_once(MYDIR."/../lib/set-wbutil.php.cgi");
include_once(MYDIR."/../lib/lib-wbutil.php.cgi");
include_once(MYDIR."/../lib/set-wbset.php.cgi");
include_once(MYDIR."/set-wbset.php.cgi");
include_once(MYDIR."/../lib/lib-wbset.php.cgi");
include_once(MYDIR."/com-block.php.cgi");
$INCHK_MSG = '';
$GLOBAL_PARA = array();
function main(){global $INCHK_MSG;
$p_act = LlutlPara('p_act', 'jump');
$p_tmp = LlutlPara('p_tmp', '');
LlsetSetPathPrefix(LLSET_DIR_SET);
CblockDailyExec();
$rep = array();
if (strncmp(MYACT, 'basicauth-log', 13) == 0){exec_log(); exit;}
switch ($p_act){case 'jump':				jump(); exit;
case 'version':				LlsetPrintVersion(); exit;}
$html = LlsetReadTemp($p_act, $p_tmp);
switch ($p_act){}
LlsetReplaceCommon($html, $rep);
print $html;}
function exec_log(){$user = CblockBasicUser();
if ($user != ''){$page = LlutlPara('page', '');
CblockAccLogPut($user, $page);}
header('Content-type: image/gif');
readfile(LLSET_PATH_ACCLOG_IMG);
exit;}
function jump(){$wks  = explode('.', MYACT);
$fext = $wks[1];
header('Location: ./'.LLUTL_DIRNM_WB.'/'.MYDIRNM.'/index.'.$fext);
exit;}
main();
?>