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
define('WBADMIN', TRUE);
define('LLUTL_ENCODING',		'UTF-8');
define('LLUTL_HTTP_ENCODING',	'UTF-8');
define('LLUTL_SJIS',			'SJIS-win');
error_reporting(E_ALL);
ini_set('display_errors', TRUE);
mb_language("Japanese");
mb_internal_encoding(LLUTL_ENCODING);
mb_http_output(LLUTL_HTTP_ENCODING);
@putenv("TZ=Asia/Tokyo");
include_once(MYDIR."/../lib/set-site.php.cgi");
include_once(MYDIR."/../lib/set-wbmsg.php.cgi");
include_once(MYDIR."/set-wbmsg.php.cgi");
include_once(MYDIR."/../lib/set-wbutil.php.cgi");
include_once(MYDIR."/../lib/lib-wbutil.php.cgi");
include_once(MYDIR."/../lib/set-wbset.php.cgi");
include_once(MYDIR."/set-wbset.php.cgi");
include_once(MYDIR."/../lib/lib-wbset.php.cgi");
include_once(MYDIR."/com-block.php.cgi");
$SES_ADMIN = FALSE;
$BODY_ONLOAD = '';
$HEAD_MENU   = TRUE;
$INCHK_MSG = '';
$GLOBAL_PARA = array('sinfo_list'	=> array('page'				=> '','order'				=> '','jkn_user'			=> '','jkn_cmt'			=> '','jkn_user_type'		=> '',),);
$BASIC_USER = '';
function main(){global $INCHK_MSG;
global $SES_ADMIN;
global $BODY_ONLOAD;
global $HEAD_MENU;
global $BASIC_USER;
global $_SERVER;
$p_act = LlutlPara('p_act', 'sinfo_list');
$p_tmp = LlutlPara('p_tmp', '');
LlsetSetPathPrefix(LLSET_DIR_SET);
if (!LLUTL_SUEXEC){print str_replace('##MSG##', LlutlMsgf('basicauth01'), LlsetReadTemp('stop', ''));
exit;}
$BASIC_USER = CblockBasicUser();
$admin_users = CblockGetUsers(TRUE);
if (htpasswd_valid() && sizeof($admin_users) > 0 && !isset($admin_users[$BASIC_USER])){$p_act = 'user_err';}
CblockDailyExec();
$rep = array();
switch ($p_act){case 'sinfo_ins01':		inchk_sinfo_ins01($p_act, $p_tmp, $html, $rep); break;
case 'sinfo_ins02':		inchk_sinfo_ins02($p_act, $p_tmp, $html, $rep); break;
case 'sinfo_upd02':		inchk_sinfo_upd02($p_act, $p_tmp, $html, $rep); break;
case 'sinfo_down':		inchk_sinfo_down($p_act, $p_tmp, $html, $rep); break;
case 'sinfo_up02':		inchk_sinfo_up02($p_act, $p_tmp, $html, $rep); break;
case 'etc_set02':		inchk_etc_set02($p_act, $p_tmp, $html, $rep); break;}
$html = LlsetReadTemp($p_act, $p_tmp);
switch ($p_act){case 'sinfo_list':		form_sinfo_list($html, $rep); break;
case 'sinfo_ins01':		form_sinfo_ins01($html, $rep); break;
case 'sinfo_ins02':		form_sinfo_ins02($html, $rep); break;
case 'sinfo_upd01':		form_sinfo_upd01($html, $rep); break;
case 'sinfo_upd02':		form_sinfo_upd02($html, $rep); break;
case 'sinfo_del':		form_sinfo_del($html, $rep); break;
case 'sinfo_log01':		form_sinfo_log01($html, $rep); break;
case 'sinfo_log02':		form_sinfo_log02($html, $rep); break;
case 'sinfo_logclear':	form_sinfo_logclear($html, $rep); break;
case 'sinfo_clear':		form_sinfo_clear($html, $rep); break;
case 'sinfo_down':		form_sinfo_down($html, $rep); break;
case 'sinfo_up01':		form_sinfo_up01($html, $rep); break;
case 'sinfo_up02':		form_sinfo_up02($html, $rep); break;
case 'etc_set01':		form_etc_set01($html, $rep); break;
case 'etc_set02':		form_etc_set02($html, $rep); break;}
$rep['##BASIC_USER##'] = $BASIC_USER;
$html = LlutlReplaceIf('IF_BASIC_USER', $BASIC_USER != '', $html);
LlsetReplaceCommon($html, $rep);
print $html;}
function inchk_sinfo_ins01(&$p_act,&$p_tmp,&$html,&$rep){global $INCHK_MSG;
global $LLSET_ALL;
$ips  = LlutlParaToArray('i_');
$tbl  = 'fsinfo';
$flds = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
$emsg = '';
if ($emsg == ''){}
if ($emsg != ''){$p_act = 'sinfo_list';
$p_tmp = '';
$INCHK_MSG = $emsg;
return;}}
function inchk_sinfo_ins02(&$p_act,&$p_tmp,&$html,&$rep){global $INCHK_MSG;
global $LLSET_ALL;
$ips  = LlutlParaToArray('i_');
$tbl  = 'fsinfo';
$flds = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
$emsg = '';
if ($emsg == ''){$chks = array('user'		=> '','pwd'		=> '','user_type'	=> '',);
$emsg = LlsetChk2Exist($tbl, $ips, $chks);}
if ($emsg == ''){$chks = array('user'		=> 'alpha','pwd'		=> 'alpha',);
$emsg = LlsetChk2Roma($flds, $ips, $chks);}
if ($emsg == ''){$admin_users = CblockGetUsers(TRUE);
if (sizeof($admin_users) <= 0 && $ips['i_user_type'] != LLSET_USER_TYPE_ADMIN){$emsg = LlutlMsgf('sinfoinsinchk01');}}
if ($emsg == ''){$all_users = CblockGetUsers();
if (isset($all_users[$ips['i_user']])){$emsg = LlutlMsgf('sinfoinsinchk02');}}
if ($emsg != ''){$p_act = 'sinfo_ins01';
$p_tmp = 'sinfo_set01';
$INCHK_MSG = $emsg;
return;}}
function inchk_sinfo_upd02(&$p_act,&$p_tmp,&$html,&$rep){global $INCHK_MSG;
global $LLSET_ALL;
$ips  = LlutlParaToArray('i_');
$tbl  = 'fsinfo';
$flds = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
$emsg = '';
if ($emsg == ''){$chks = array('user_type'	=> '',);
$emsg = LlsetChk2Exist($tbl, $ips, $chks);}
if ($emsg == ''){$chks = array('pwd'		=> 'alpha',);
$emsg = LlsetChk2Roma($flds, $ips, $chks);}
if ($emsg != ''){$p_act = 'sinfo_upd01';
$p_tmp = 'sinfo_set01';
$INCHK_MSG = $emsg;
return;}}
function inchk_sinfo_down(&$p_act,&$p_tmp,&$html,&$rep){global $INCHK_MSG;
global $LLSET_ALL;
$ips  = LlutlParaToArray('i_');
$tbl  = 'fsinfo';
$flds = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
$emsg = '';
if ($emsg == ''){}
if ($emsg != ''){$p_act = 'sinfo_list';
$p_tmp = '';
$INCHK_MSG = $emsg;
return;}}
function inchk_sinfo_up02(&$p_act,&$p_tmp,&$html,&$rep){global $INCHK_MSG;
global $LLSET_ALL;
$ips  = LlutlParaToArray('i_');
$tbl  = 'fsinfo';
$flds = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
$emsg = '';
if ($emsg == ''){}
if ($emsg != ''){$p_act = 'sinfo_list';
$p_tmp = '';
$INCHK_MSG = $emsg;
return;}}
function inchk_etc_set02(&$p_act,&$p_tmp,&$html,&$rep){global $INCHK_MSG;
global $LLSET_ALL;
$ips  = LlutlParaToArray('i_');
$tbl  = 'fetc';
$flds = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
$emsg = '';
if ($emsg == ''){$chks = array('auth_name'		=> '','auth_name_enc'	=> '','log_save'		=> '',);
$emsg = LlsetChk2Exist($tbl, $ips, $chks);}
if ($emsg == ''){$chks = array('log_save'		=> 'num,1,1000',);
$emsg = LlsetChk2Roma($flds, $ips, $chks);}
if ($emsg != ''){$p_act = 'etc_set01';
$p_tmp = '';
$INCHK_MSG = $emsg;
return;}}
function form_sinfo_list(&$html,&$rep){global $GLOBAL_PARA;
global $LLSET_ALL;
global $LLSET_LIST;
global $LLSET_SELECT_FLDS_COUNT;
global $BASIC_USER;
$pname = 'sinfo';
$pgrp  = $pname.'_list';
if (LlutlPara('p_init', '') == '1') { LlsetParaClear($pgrp); }
$tbl    = 'f'.$pname;
$tblfld = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
$list_order = LlsetGetOrder('admin_'.$pname.'_list');
$w_ary_keys = array_keys($list_order);
$def_ord    = array_shift($w_ary_keys);
$p_page     = LlsetParaGet($pgrp, 'p_', 'page', '1');
$p_order    = LlsetParaGet($pgrp, 'p_', 'order', $def_ord);
$jkns = array();
foreach ($GLOBAL_PARA[$pgrp] as $gfid => $gval){$ugfid = strtoupper($gfid);
if (substr($gfid, 0, 4) != 'jkn_') { continue; }
$fid   = substr($gfid, 4);
$jval  = LlsetParaGet($pgrp, 'p_', $gfid, '');
$ftype = isset($tblfld[$fid]) ? $tblfld[$fid][LLSET_FI_TYPE] : '';
$jkns['p_'.$gfid] = $jval;
if ($ftype == 'sel' || $ftype == 'radio'){$list = LlsetGetList($tbl, $fid);
$rep['##OPT_'.$ugfid.'##'] = LlsetGetSelOpt($list, $jval);}
else{$rep['##I_'.$ugfid.'##'] = $jval;}}
$sjkns = array();
foreach ($jkns as $jfid => $jval){if ($jval == '') { continue; }
$fid   = substr($jfid, 6);
$ftype = isset($tblfld[$fid]) ? $tblfld[$fid][LLSET_FI_TYPE] : '';
if ($ftype == 'text' || $ftype == 'tarea'){$sjkns[] = array('fid'=>$fid, 'type'=>'*text*', 'val'=>$jval);}
else if ($ftype == 'int'){$sjkns[] = array('fid'=>$fid, 'type'=>'int', 'val'=>$jval);}
else{$sjkns[] = array('fid'=>$fid, 'type'=>'text', 'val'=>$jval);}}
$nline  = LlsetGetNline('admin_'.$pname.'_list');
$offset = ($p_page - 1) * $nline;
$recs   = LlsetSelectFlds($tbl, $offset, $nline, $sjkns, $p_order);
$nrec   = $LLSET_SELECT_FLDS_COUNT;
$npage  = (int)(($nrec - 1) / $nline) + 1; if ($npage <= 0) { $npage = 1; }
if ($p_page > $npage) { $p_page = $npage; }
$htmls = explode('<!--##LIST##-->', $html);
$html1 = '';
$cnt   = 0;
foreach ($recs as $key => $rec){$line = $htmls[1];
$lrep = array();
$lrep['##LIST_KEY##'] = $key;
$lrep['##LIST_CNT##'] = $cnt + $offset + 1;
foreach ($rec as $fid => $val){$ufid  = strtoupper($fid);
$ftype = isset($tblfld[$fid]) ? $tblfld[$fid][LLSET_FI_TYPE] : '';
if ($ftype == 'sel' || $ftype == 'radio'){$list = LlsetGetList($tbl, $fid);
$str  = isset($list[$val]) ? $list[$val] : $val;
$lrep['##LIST_'.$ufid.'##']     = $val != '' ? $val : '　';
$lrep['##LIST_'.$ufid.'_STR##'] = $str != '' ? $str : '　';}
else if (substr($fid,-5) == '_time'){$lrep['##LIST_'.$ufid.'##'] = substr($val, 0, 10);}
else{$lrep['##LIST_'.$ufid.'##'] = LlsetCutStr($val, 100);}}
if ($cnt % 2 == 1){$lrep['"d1"'] = '"d2"';}
$acclog = array_shift(CblockAccLogGet($rec['user']));
$lrep['##LIST_ACC_TIME##'] = isset($acclog['time']) ? substr($acclog['time'], 0, 10) : '（なし）';
$line = LlutlReplaceIf('IF_LIST_BASIC_USER', strcmp($rec['user'], $BASIC_USER) == 0, $line);
$html1 .= str_replace(array_keys($lrep), array_values($lrep), $line);
$cnt ++;}
$html = $htmls[0] . $html1 . $htmls[2];
LlsetReplacePageList($html,$rep,$offset,$nline,$nrec,$npage,$p_page,$cnt);
$rep['##OPT_ORDER##']  = LlsetGetSelOpt($list_order, $p_order);
$rep['##PAGE##']       = $p_page;
$users = CblockGetUsers();
$html = LlutlReplaceIf('IF_USER_EXIST', sizeof($users) > 0, $html);}
function form_sinfo_ins01(&$html,&$rep){global $LLSET_ALL;
global $LLSET_LIST;
$pname  = 'sinfo';
$tbl    = 'f'.$pname;
$tblfld = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
$def = array();
if (LlutlPara('p_case', '') == 'ins'){$admin_users = CblockGetUsers(TRUE);
$def['user_type'] = sizeof($admin_users) > 0 ? LLSET_USER_TYPE_NORMAL : LLSET_USER_TYPE_ADMIN;}
else if (LlutlPara('p_case', '') == 'cpy'){$p_key = LlutlPara('p_key', '');
$def   = LlsetSelect1($tbl, '', $p_key);}
$max_file_size = 1024;
foreach ($tblfld as $fid => $finfo){$ufid = strtoupper($fid);
$ival = LlutlIsParaArray('i_'.$fid) ? LlutlParas('i_'.$fid)
: LlutlPara2('i_'.$fid, isset($def[$fid]) ? $def[$fid] : '');
if ($finfo[LLSET_FI_TYPE] == 'radio'){$list = LlsetGetList($tbl, $fid);
LlsetReplaceSlist($html, $fid, $ival, $list, TRUE);
$html = LlutlReplaceIf('IF_'.$ufid, sizeof($list) > 0, $html);}
else if ($finfo[LLSET_FI_TYPE] == 'sel'){$list = LlsetGetList($tbl, $fid);
$rep['##OPT_'.$ufid.'##'] = LlsetGetSelOpt($list, $ival);
$html = LlutlReplaceIf('IF_'.$ufid, sizeof($list) > 0, $html);}
else if ($finfo[LLSET_FI_TYPE] == 'check'){$list = LlsetGetList($tbl, $fid);
$ival = is_array($ival) ? $ival : LlsetMfldStrToAry($ival);
LlsetReplaceSlist($html, $fid, $ival, $list, TRUE);
$html = LlutlReplaceIf('IF_'.$ufid, sizeof($list) > 0, $html);}
else if ($finfo[LLSET_FI_TYPE] == 'img'){$resize_wh = isset($finfo[LLSET_FI_RESIZE_WH]) ? $finfo[LLSET_FI_RESIZE_WH] : '';
$rep['##SIZE_'.$ufid.'##']      = $finfo[LLSET_FI_ISIZE];
$rep['##TYPE_'.$ufid.'##']      = $finfo[LLSET_FI_ITYPE];
$rep['##RESIZE_WH_'.$ufid.'##'] = $resize_wh;
$rep['##'.$ufid.'##']           = $ival;
$html = LlutlReplaceIf('IF_RESIZE_WH_'.$ufid, $resize_wh != '', $html);
$max_file_size += LlutlGetNum0($finfo[LLSET_FI_ISIZE]) * 1024;
$rep['##I_'.$ufid.'##'] = LlsetEscapeTagForIn($ival, 'text');}
else{$rep['##I_'.$ufid.'##'] = LlsetEscapeTagForIn($ival, $finfo[LLSET_FI_TYPE]);}}
$rep['##MAX_FILE_SIZE##'] = $max_file_size;
$rep['##P_KEY##']  = LlutlPara('p_key', '');
$rep['##P_CASE##'] = LlutlPara('p_case', '');
$rep['##STR1##']   = 'ins';
$rep['##KSTR1##']  = '登録';
$rep['##KSTR2##']  = '登　録';
$rep['##PAGE##']   = LlutlPara('p_page',  1);
$rep['<!--##HIDDEN_PARA##-->'] = '';
$html = LlutlReplaceIf('IF_INS', TRUE, $html);
$html = LlutlReplaceIf('IF_CPY', LlutlPara('p_case', '') == 'cpy', $html);
$html = LlutlReplaceIf('IF_BASIC_USER', FALSE, $html);}
function form_sinfo_ins02(&$html,&$rep){global $LLSET_ALL;
$pname  = 'sinfo';
$tbl    = 'f'.$pname;
$tblfld = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
$ips     = LlutlParaToArray('i_');
$cpy_key = LlutlPara('p_key', '');
$cpy_hdn = array();
if ($cpy_key != ''){$cpy_hdn['p_key']  = $cpy_key;
$cpy_hdn['p_case'] = 'cpy';}
$m_msg = LlutlMsgf($pname.'ins01');
$m_err = FALSE;
$m_hdn = array('p_act' => $pname.'_list');
if (!LlsetIsUpdateMode($html, $rep, $m_msg, $m_err, $m_hdn)) { return; }
$insfld = array();
if (!$m_err){foreach ($tblfld as $fid => $finfo){$ival = isset($ips['i_'.$fid]) ? $ips['i_'.$fid] : '';
if ($fid == 'remote_addr'){$ival = LlutlRemoteAddr();}
else if ($fid == 'user_agent'){$ival = LlutlEnv('HTTP_USER_AGENT');}
else if ($finfo[LLSET_FI_TYPE] == 'int' && $ival == ''){$ival = 0;}
else if ($finfo[LLSET_FI_TYPE] == 'datetime' && $ival == ''){$ival = LlsetFieldDateTime();}
$insfld[$fid] = is_array($ival) ? LlsetMfldAryToStr($ival) : $ival;}
CblockSetSinfoFields($insfld);}
if (!$m_err){$insfld['pwd'] = LlutlCryptBasic($insfld['user'], $insfld['pwd']);
if (LlsetInsert1($tbl, '', $insfld, 1) < 1){$m_msg = LlutlMsgf($pname.'ins02');
$m_err = TRUE;
$m_hdn = array('p_act'=>$pname.'_ins01','p_tmp'=>$pname.'_set01') + $cpy_hdn + $ips;}
else{global $LLSET_NEW_KEY;
$my_key = $LLSET_NEW_KEY;
if (!LlsetImageUpload($tbl, $my_key, $m_msg, $cpy_key)){$m_err  = TRUE;}}}
if (!$m_err){$rtn_msg = update_basic_files();
if ($rtn_msg != ''){$m_msg = $rtn_msg;
$m_err = TRUE;}}
LlsetReplaceFormMsg($html, $rep, $m_msg, $m_err, $m_hdn);}
function form_sinfo_upd01(&$html,&$rep){global $LLSET_ALL;
global $BASIC_USER;
$pname  = 'sinfo';
$tbl    = 'f'.$pname;
$tblfld = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
$kfid   = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_KEY_FID];
$p_key = LlutlPara('p_key', '');
$def = LlsetSelect1($tbl, '', $p_key);
$def['pwd'] = '';
$user = $def['user'];
$max_file_size = 1024;
foreach ($tblfld as $fid => $finfo){$ufid = strtoupper($fid);
$ival = LlutlPara2('i_'.$fid, isset($def[$fid]) ? $def[$fid] : '');
if ($finfo[LLSET_FI_TYPE] == 'radio'){$list = LlsetGetList($tbl, $fid);
LlsetReplaceSlist($html, $fid, $ival, $list, TRUE);
$html = LlutlReplaceIf('IF_'.$ufid, sizeof($list) > 0, $html);
$rep['##I_'.$ufid.'##'] = LlsetEscapeTagForIn($ival, 'text');}
else if ($finfo[LLSET_FI_TYPE] == 'sel'){$list = LlsetGetList($tbl, $fid);
$rep['##OPT_'.$ufid.'##'] = LlsetGetSelOpt($list, $ival);
$html = LlutlReplaceIf('IF_'.$ufid, sizeof($list) > 0, $html);
$rep['##I_'.$ufid.'##'] = LlsetEscapeTagForIn($ival, 'text');}
else if ($finfo[LLSET_FI_TYPE] == 'check'){$list = LlsetGetList($tbl, $fid);
$ival = is_array($ival) ? $ival : LlsetMfldStrToAry($ival);
LlsetReplaceSlist($html, $fid, $ival, $list, TRUE);
$html = LlutlReplaceIf('IF_'.$ufid, sizeof($list) > 0, $html);}
else if ($finfo[LLSET_FI_TYPE] == 'img'){$is_img  = TRUE;
$img_tag = LlsetGetImgTag($tbl, $p_key, $fid, LLSET_ADMIN_IMG_MAX_W, LLSET_ADMIN_IMG_MAX_H, $ival);
if ($img_tag == '') { $is_img = FALSE; $img_tag = LlutlMsgf('imgupload04'); }
$resize_wh = isset($finfo[LLSET_FI_RESIZE_WH]) ? $finfo[LLSET_FI_RESIZE_WH] : '';
$rep['##IMG_'.$ufid.'##']       = $img_tag;
$rep['##SIZE_'.$ufid.'##']      = $finfo[LLSET_FI_ISIZE];
$rep['##TYPE_'.$ufid.'##']      = $finfo[LLSET_FI_ITYPE];
$rep['##RESIZE_WH_'.$ufid.'##'] = $resize_wh;
$rep['##'.$ufid.'##']           = $ival;
$html = LlutlReplaceIf('IF_'.$ufid, $is_img, $html);
$html = LlutlReplaceIf('IF_RESIZE_WH_'.$ufid, $resize_wh != '', $html);
$max_file_size += LlutlGetNum0($finfo[LLSET_FI_ISIZE]) * 1024;
$rep['##I_'.$ufid.'##'] = LlsetEscapeTagForIn($ival, 'text');}
else{$rep['##I_'.$ufid.'##'] = LlsetEscapeTagForIn($ival, $finfo[LLSET_FI_TYPE]);
$rep['##'.$ufid.'##']   = LlutlHtmlEscapeTag2($ival);}}
$rep['##MAX_FILE_SIZE##'] = $max_file_size;
$rep['##P_KEY##']  = $p_key;
$rep['##P_CASE##'] = LlutlPara('p_case', '');
$rep['##STR1##']   = 'upd';
$rep['##KSTR1##']  = '更新';
$rep['##KSTR2##']  = '更　新';
$rep['##PAGE##']   = LlutlPara('p_page',  1);
$rep['<!--##HIDDEN_PARA##-->'] = '';
$html = LlutlReplaceIf('IF_INS', FALSE, $html);
$html = LlutlReplaceIf('IF_CPY', FALSE, $html);
$html = LlutlReplaceIf('IF_BASIC_USER', strcmp($BASIC_USER, $user) == 0, $html);}
function form_sinfo_upd02(&$html,&$rep){global $LLSET_ALL;
$pname  = 'sinfo';
$tbl    = 'f'.$pname;
$tblfld = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
$ips   = LlutlParaToArray('i_');
$p_key = LlutlPara('p_key', '');
$upd_hdn = array('p_key'  => $p_key,);
$def = LlsetSelect1($tbl, '', $p_key);
$old_rec = $def;
$m_msg = LlutlMsgf($pname.'upd01');
$m_err = FALSE;
$m_hdn = array('p_act' => $pname.'_list');
if (!LlsetIsUpdateMode($html, $rep, $m_msg, $m_err, $m_hdn)) { return; }
$updfld = array();
if (!$m_err){foreach ($ips as $ifid => $ival){$fid   = substr($ifid, 2);
$finfo = $tblfld[$fid];
if ($finfo[LLSET_FI_TYPE] == 'id' && $ival == ''){$ival = LlsetNewId($tbl, $fid);}
else if ($finfo[LLSET_FI_TYPE] == 'onum' && $ival == ''){$grpfid = isset($finfo[LLSET_FI_ONUMGRP]) ? $finfo[LLSET_FI_ONUMGRP] : '';
$grpval = $grpfid != '' ? $ips['i_'.$grpfid] : '';
$ival = LlsetNewOnum($tbl, $fid, $grpfid, $grpval);}
else if ($finfo[LLSET_FI_TYPE] == 'int' && $ival == ''){$ival = 0;}
else if ($finfo[LLSET_FI_TYPE] == 'datetime' && $ival == ''){$ival = LlsetFieldDateTime();}
$updfld[$fid] = is_array($ival) ? LlsetMfldAryToStr($ival) : $ival;}
$fid = 'upd_time';		if (isset($def[$fid])) { $updfld[$fid] = LlsetFieldDateTime(); }
$fid = 'remote_addr';	if (isset($def[$fid])) { $updfld[$fid] = LlutlRemoteAddr(); }
$fid = 'user_agent';	if (isset($def[$fid])) { $updfld[$fid] = LlutlEnv('HTTP_USER_AGENT'); }
CblockSetSinfoFields($updfld, $old_rec);}
if (!$m_err){$updfld['pwd'] = $updfld['pwd'] == '' ? $old_rec['pwd'] : LlutlCryptBasic($old_rec['user'], $updfld['pwd']);
if (LlsetUpdate1($tbl, '', $p_key, $updfld) < 1){$m_msg  = LlutlMsgf($pname.'upd02');
$m_err  = TRUE;
$m_hdn  = array('p_act' => $pname.'_upd01','p_tmp'=> $pname.'_set01') + $ips;}
else{$my_key = $p_key;
if (!LlsetImageUpload($tbl, $my_key, $m_msg)){$m_err  = TRUE;}}}
if (!$m_err){$rtn_msg = update_basic_files();
if ($rtn_msg != ''){$m_msg = $rtn_msg;
$m_err = TRUE;}}
LlsetReplaceFormMsg($html, $rep, $m_msg, $m_err, $m_hdn);}
function form_sinfo_log01(&$html,&$rep){$user    = LlutlPara('p_user', '');
$acclogs = CblockAccLogGet($user);
$rep['##USER##'] = $user;
$logs = "";
foreach ($acclogs as $log){$vals = array();
foreach (array('time','page','remote_addr','user_agent') as $fid){$vals[] = isset($log[$fid]) ? $log[$fid] : '';}
$logs .= join(", ", $vals)."\n";}
$rep['##ACCLOGS##'] = $logs;
$wks = explode('.', MYACT);
$rep['##MYEXT##'] = $wks[1];}
function form_sinfo_log02(&$html,&$rep){global $LLSET_ALL;
$pname  = 'sinfo';
$m_msg = LlutlMsgf($pname.'logdel01');
$m_err = FALSE;
$m_hdn = array('p_act' => $pname.'_list');
if (!LlsetIsUpdateMode($html, $rep, $m_msg, $m_err, $m_hdn)) { return; }
$user = LlutlPara('p_user', '');
CblockAccLogDel($user);
LlsetReplaceFormMsg($html, $rep, $m_msg, $m_err, $m_hdn);}
function form_sinfo_del(&$html,&$rep){global $LLSET_ALL;
$pname  = 'sinfo';
$tbl    = 'f'.$pname;
$tblfld = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
$p_keys = LlutlParas('p_keys');
$m_msg = LlutlMsgf($pname.'del01');
$m_err = FALSE;
$m_hdn = array('p_act' => $pname.'_list');
if (!LlsetIsUpdateMode($html, $rep, $m_msg, $m_err, $m_hdn)) { return; }
foreach ($p_keys as $p_key){$rec = LlsetSelect1($tbl, '', $p_key);
CblockAccLogDel($rec['user']);
LlsetDelete1($tbl, '', $p_key);}
if (!$m_err){$rtn_msg = update_basic_files();
if ($rtn_msg != ''){$m_msg = $rtn_msg;
$m_err = TRUE;}}
LlsetReplaceFormMsg($html, $rep, $m_msg, $m_err, $m_hdn);}
function form_sinfo_logclear(&$html,&$rep){global $LLSET_ALL;
$pname  = 'sinfo';
$m_msg = LlutlMsgf($pname.'logclear01');
$m_err = FALSE;
$m_hdn = array('p_act' => $pname.'_list');
if (!LlsetIsUpdateMode($html, $rep, $m_msg, $m_err, $m_hdn)) { return; }
CblockAccLogClear();
LlsetReplaceFormMsg($html, $rep, $m_msg, $m_err, $m_hdn);}
function form_sinfo_clear(&$html,&$rep){global $LLSET_ALL;
$pname  = 'sinfo';
$tbl    = 'f'.$pname;
$tblfld = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
$p_keys = LlutlParas('p_keys');
$m_msg = LlutlMsgf($pname.'clear01');
$m_err = FALSE;
$m_hdn = array('p_act' => $pname.'_list');
if (!LlsetIsUpdateMode($html, $rep, $m_msg, $m_err, $m_hdn)) { return; }
CblockAccLogClear();
LlsetDeleteTable($tbl, '');
if (!$m_err){$rtn_msg = update_basic_files();
if ($rtn_msg != ''){$m_msg = $rtn_msg;
$m_err = TRUE;}}
LlsetReplaceFormMsg($html, $rep, $m_msg, $m_err, $m_hdn);}
function form_sinfo_down(&$html,&$rep){global $LLSET_DEF_FFIELD;
$tbl          = 'fsinfo';
$is_multi     = TRUE;
$def          = array();
$limit_check  = FALSE;
$fname_prefix = 'basicauth-user';
LlsetSettingDownload($tbl, $is_multi, $def, $limit_check, $fname_prefix);}
function form_sinfo_up01(&$html,&$rep){}
function form_sinfo_up02(&$html,&$rep){$m_msg       = LlutlMsgf('setupload01');
$m_err       = FALSE;
$m_hdn       = array('p_act' => 'sinfo_list');
$tbl         = 'fsinfo';
$is_multi    = TRUE;
$limit_check = FALSE;
$file_fid    = 'i_up_file';
LlsetSettingUpload($html, $rep, $m_msg, $m_err, $m_hdn, $tbl, $is_multi, $limit_check, $file_fid);
if (!$m_err){$rtn_msg = update_basic_files();
if ($rtn_msg != ''){$m_msg = $rtn_msg;
$m_err = TRUE;}}}
function form_etc_set01(&$html,&$rep){global $LLSET_DEF_FETC;
LlsetFormEtcSet01($html, $rep, $LLSET_DEF_FETC);}
function form_etc_set02(&$html,&$rep){$m_msg  = '';
$m_err  = FALSE;
$m_hdn  = array();
if (!LlsetFormEtcSet022($html, $rep, 'sinfo_list', $m_msg, $m_err, $m_hdn)) { return; }
if (!$m_err){$rtn_msg = update_auth_name();
if ($rtn_msg != ''){$m_msg = $rtn_msg;
$m_err = TRUE;}}
LlsetReplaceFormMsg($html, $rep, $m_msg, $m_err, $m_hdn);}
function htpasswd_valid(){if (!file_exists(LLSET_PATH_HTACCESS)) { return FALSE; }
$ilines = @file(LLSET_PATH_HTACCESS); if (!$ilines) { return FALSE; }
$label  = strtoupper('AuthUserFile');
$l      = strlen($label);
foreach ($ilines as $line){if (strncmp($label, strtoupper($line), $l) == 0) { return TRUE; }}
return FALSE;}
function update_htaccess(&$olines){$fp = @fopen(LLSET_PATH_HTACCESS, "w"); if (!$fp) { return LlutlMsgf('basicfile02', '.htaccess'); }
foreach ($olines as $line) { fputs($fp, $line); }
if (!@fclose($fp)) { return LlutlMsgf('basicfile02', '.htaccess'); }
return '';}
function update_basic_files(){$tbl    = 'fsinfo';
$offset = 0;
$nline  = 0;
$sjkns  = array();
$order  = 'fid=ins_time;type=text;desc=N';
$recs   = LlsetSelectFlds($tbl, $offset, $nline, $sjkns, $order);
if (!file_exists(LLSET_PATH_HTPASSWD)) { return LlutlMsgf('basicfile01', '.htpasswd'); }
$fp = @fopen(LLSET_PATH_HTPASSWD, "w"); if (!$fp) { return LlutlMsgf('basicfile02', '.htpasswd'); }
$user_cnt = 0;
foreach ($recs as $rec){if ($rec['user_type'] == LLSET_USER_TYPE_STOP) { continue; }
$line = $rec['user'].':'.$rec['pwd']."\n";
fputs($fp, $line);
$user_cnt ++;}
if (!@fclose($fp)) { return LlutlMsgf('basicfile02', '.htpasswd'); }
$htpasswd_path = dirname(dirname(dirname(__FILE__))).'/'.basename(LLSET_PATH_HTPASSWD);
if (!file_exists(LLSET_PATH_HTACCESS)) { return LlutlMsgf('basicfile01', '.htaccess'); }
$ilines    = @file(LLSET_PATH_HTACCESS); if (!$ilines) { return LlutlMsgf('basicfile02', '.htaccess'); }
$is_upd    = FALSE;
$olines    = array();
$label_s   = '#BasicAuth';	$l_s = strlen($label_s);
$label_e   = '#/BasicAuth';	$l_e = strlen($label_e);
$is_target = FALSE;
foreach ($ilines as $line){$oline = $line;
if (strncmp($oline, $label_s, $l_s) == 0){$is_target = TRUE;}
else if (strncmp($oline, $label_e, $l_e) == 0){$is_target = FALSE;}
else if ($is_target){if ($user_cnt > 0){foreach (array('#AuthType', '#AuthName', '#AuthUserFile', '#AuthGroupFile', '#require') as $label){$l = strlen($label);
if (strncmp($oline, $label, $l) == 0){$oline  = $label == '#AuthUserFile'
? substr($label, 1)." ${htpasswd_path}\n"
: substr($line, 1);
$is_upd = TRUE;
break;}}}
else{foreach (array('AuthType', 'AuthName', 'AuthUserFile', 'AuthGroupFile', 'require') as $label){$l = strlen($label);
if (strncmp($oline, $label, $l) == 0){$oline  = $label == 'AuthUserFile'
? "#${label}\n"
: "#${line}";
$is_upd = TRUE;
break;}}}}
$olines[] = $oline;}
if ($is_upd){$emsg = update_htaccess($olines);
if ($emsg != '') { return $emsg; }}
return '';}
function update_auth_name(){$f = LlsetGetFetc();
$auth_name_enc = $f['auth_name_enc'];
$auth_name     = $f['auth_name']; if ($auth_name == '') { return ''; }
$auth_name     = LlutlStrReplace('"', "", $auth_name);
$e_auth_name   = mb_convert_encoding($auth_name, $auth_name_enc, LLUTL_ENCODING);
if (!file_exists(LLSET_PATH_HTACCESS)) { return LlutlMsgf('basicfile01', '.htaccess'); }
$ilines    = @file(LLSET_PATH_HTACCESS); if (!$ilines) { return LlutlMsgf('basicfile02', '.htaccess'); }
$is_upd    = FALSE;
$olines    = array();
$label_s   = '#BasicAuth';	$l_s = strlen($label_s);
$label_e   = '#/BasicAuth';	$l_e = strlen($label_e);
$is_target = FALSE;
foreach ($ilines as $line){$oline = $line;
if (strncmp($oline, $label_s, $l_s) == 0){$is_target = TRUE;}
else if (strncmp($oline, $label_e, $l_e) == 0){$is_target = FALSE;}
else if ($is_target){foreach (array('#AuthName', 'AuthName') as $label){$l = strlen($label);
if (strncmp($oline, $label, $l) == 0){$oline  = sprintf('%s "%s"', $label, $e_auth_name)."\n";
$is_upd = TRUE;
break;}}}
$olines[] = $oline;}
if ($is_upd){$emsg = update_htaccess($olines);
if ($emsg != '') { return $emsg; }}
return '';}
main();
?>