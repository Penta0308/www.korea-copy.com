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
function CblockBasicUser(){global $_SERVER;
return isset($_SERVER['REMOTE_USER']) && strlen($_SERVER['REMOTE_USER']) > 0
? $_SERVER['REMOTE_USER']
: (isset($_SERVER['PHP_AUTH_USER']) && strlen($_SERVER['PHP_AUTH_USER']) > 0 ? $_SERVER['PHP_AUTH_USER'] : '');}
function CblockAccLogPut($user,$page){global $LLSET_DEF_FETC;
if ($user == '') { return; }
$path = CblockAccLogPath($user);
if (!LlutlFileExist($path)) { LlutlMkDir(dirname($path)); }
$acclog = CblockAccLogGet($user);
$dt = LlutlDateTime(time());
array_unshift($acclog, array('page'			=> $page,'time'			=> sprintf('%04d-%02d-%02d %02d:%02d:%02d',$dt['year'], $dt['mon'], $dt['day'], $dt['hour'], $dt['min'], $dt['sec']),'remote_addr'	=> LlutlRemoteAddr(),'user_agent'	=> LlutlEnv('HTTP_USER_AGENT'),));
$f = LlsetGetFetc();
$log_save = LlutlGetNum0(isset($f['log_save']) ? $f['log_save'] : $LLSET_DEF_FETC['log_save']);
if ($log_save <= 0) { $log_save = $LLSET_DEF_FETC['log_save']; }
if (sizeof($acclog) > $log_save) { array_pop($acclog); }
$loc  = CblockAccLogLock($user);
file_put_contents($path, serialize($acclog));
CblockAccLogUnlock($loc);}
function CblockAccLogGet($user){$rtn  = array();
$path = CblockAccLogPath($user);
if (LlutlFileExist($path)){$loc  = CblockAccLogLock($user);
$file = file_get_contents($path);
CblockAccLogUnlock($loc);
$rtn = @unserialize($file);}
return is_array($rtn) ? $rtn : array();}
function CblockAccLogDel($user){$path = CblockAccLogPath($user);
if (LlutlFileExist($path)){$path_loc = CblockAccLogPath($user, 'loc');
unlink($path);
unlink($path_loc);}}
function CblockAccLogClear(){LlutlRmDir(LLSET_DIR_ACCLOG);}
function CblockAccLogPath($user,$ext = 'cgi'){return LLSET_DIR_ACCLOG.$user.'.'.$ext;}
function CblockAccLogLock($user){$path = CblockAccLogPath($user, 'loc');
if (!LlutlFileExist($path)){LlutlMkDir(dirname($path));
file_put_contents($path, time());}
return LlutlFileOpenLock($path, 'r+');}
function CblockAccLogUnlock(&$loc){LlutlFileCloseUnlock($loc);}
function CblockDailyExec(){$is_exec = FALSE;
$tm      = time();
if (LlidfPassTimeChk(LLSET_FILE_EXEC_DAILY, LLIDF_PASS_TP_DAY, $tm, array('hour'=>8,'min'=>0))){$nowdt = LlutlDateTime($tm);
$today = sprintf('%04d-%02d-%02d', $nowdt['year'], $nowdt['mon'], $nowdt['day']);
LlidfPassTimeSet(LLSET_FILE_EXEC_DAILY, $tm);
$is_exec = TRUE;}
return $is_exec;}
function CblockGetUsers($admin = FALSE){$tbl     = 'fsinfo';
$offset  = 0;
$nline   = 0;
$sjkns   = array();
if ($admin) { $sjkns[] = array('fid'=>'user_type', 'type'=>'text', 'val'=>LLSET_USER_TYPE_ADMIN); }
$order   = 'fid=ins_time;type=text;desc=N';
$recs    = LlsetSelectFlds($tbl, $offset, $nline, $sjkns, $order);
$rtns = array();
foreach ($recs as $rec){$user        = $rec['user'];
$rtns[$user] = $rec['user_type'];}
return $rtns;}
function CblockSetSinfoFields(&$rec,$def = array()){foreach (array_keys($rec) as $fid){if (substr($fid, -5) == '_kana')	{ $rec[$fid] = LlutlConvForKanaArea($rec[$fid]); }}}
?>