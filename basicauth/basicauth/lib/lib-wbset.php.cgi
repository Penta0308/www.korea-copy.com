<?php
///////////////////////////////////////////////////////////////////////
/// WebBlock 1.4 : lib
/// 2008-03-29 : Akira Mori
/// 2013-09-09 : Akira Mori
/// Copyright (C) Akira Mori. All rights reserved.
/// http://l-tool.net/
///////////////////////////////////////////////////////////////////////
$LLSET_NEW_KEY = '';
$LLSET_GET_LTSET = FALSE;
function LlsetGetLtset(){global $LLSET_GET_LTSET;
if ($LLSET_GET_LTSET === FALSE){$LLSET_GET_LTSET = array();
$path = '.ltset';
if (file_exists($path)){$lines = @file($path);
foreach ($lines as $line){$line = trim($line);
if (strncmp($line, '//', 2) == 0) { continue; }

$wk = explode('//', $line); if (isset($wk[1])) { $line = trim($wk[0]); }

if ($line == '') { continue; }
$dd = preg_split('/(=|;)/', $line);
if (isset($dd[1])){$LLSET_GET_LTSET[trim($dd[0])] = trim($dd[1]);}}}}
return $LLSET_GET_LTSET;}
$LLSET_PATH_PREFIX = '';
function LlsetSetPathPrefix($prefix){global $LLSET_PATH_PREFIX;
$rtn = $LLSET_PATH_PREFIX;
$LLSET_PATH_PREFIX = $prefix;
return $rtn;}
$LLSET_PATH_PREFIX2 = '';
$LLSET_PATH_PREFIX2_TIDS = array();
function LlsetSetPathPrefix2($prefix,$tids){global $LLSET_PATH_PREFIX2;
global $LLSET_PATH_PREFIX2_TIDS;
$rtn = $LLSET_PATH_PREFIX2;
$LLSET_PATH_PREFIX2 = $prefix;
$LLSET_PATH_PREFIX2_TIDS = $tids;
return $rtn;}
function LlsetGetPath($tid,$pkey){global $LLSET_ALL;
global $LLSET_PATH_PREFIX;
global $LLSET_PATH_PREFIX2;
global $LLSET_PATH_PREFIX2_TIDS;
$path = in_array($tid, $LLSET_PATH_PREFIX2_TIDS)
? $LLSET_PATH_PREFIX2.$LLSET_ALL[$tid][LLSET_AI_TBL][LLSET_TI_PATH]
: $LLSET_PATH_PREFIX.$LLSET_ALL[$tid][LLSET_AI_TBL][LLSET_TI_PATH];
if (strlen($pkey) <= 0){return $path;}
else{if (strcmp(substr($path,-1), '/') == 0){return $path . substr($pkey, 1);}
else{return $path . $pkey;}}}
function LlsetFormat($tid){global $LLSET_ALL;
$fmt = array(LLSET_KEY_FID);
$tbl = $LLSET_ALL[$tid][LLSET_AI_TBL];
if (isset($tbl[LLSET_TI_FMT]) && $tbl[LLSET_TI_FMT] != NULL){foreach($tbl[LLSET_TI_FMT] as $fid){$fmt[] = $fid;}}
else{foreach($tbl[LLSET_TI_FLD] as $fid => $sfld){if (strncmp($sfld[LLSET_FI_TYPE], 'cmt', 3) != 0){$fmt[] = $fid;}}}
return $fmt;}
function LlsetFormatIdx($tid){$idxs = array();
$idx  = 0;
$fmt  = LlsetFormat($tid);
foreach ($fmt as $fid){$idxs[$fid] = $idx;
$idx ++;}
return $idxs;}
function LlsetNewField($tid){$kfld = array();
$fmt  = LlsetFormat($tid);
foreach($fmt as $fid) { $kfld[$fid] = ''; }
return $kfld;}
function LlsetAddPKey($pkey){return '-'.$pkey;}
function LlsetGetSelIdxKey($fmt,$keys){$ikeys = array(0 => LLTBF_WILD_CARD);
if ($keys != NULL){$ikeys = array();
$idx = 0;
foreach($fmt as $fmval){if (isset($keys[$fmval])) { $ikeys[$idx] = $keys[$fmval]; }
$idx ++;}}
return $ikeys;}
define('LLSET_DB_SCNDS_EQ',			0);
define('LLSET_DB_SCNDS_LIKE',		1);
define('LLSET_DB_SCNDS_LIKE_PRE',	2);
function LlsetFdbSelect($tid,$pkey,$sfids,$scnds){global $LLSET_ALL;
$path = LlsetGetPath($tid, $pkey);
$fmt  = LlsetFormat($tid);
$sfid_ref = array();
foreach ($sfids as $fid){$sfid_ref[$fid] = $fid;}
$ftp_idx = array();
$cnd_idx = array();
$cnd_len = array();
$sel_idx = array();
if (TRUE){$idx = 0;
$sel_idx[$idx] = LLSET_KEY_FID;
$idx ++;
foreach($LLSET_ALL[$tid][LLSET_AI_TBL] as $fid => $finfo){$fmt[$fid]     = $idx;
$ftp_idx[$idx] = $finfo[LLSET_FI_TYPE];
if (isset($scnds[$fid])){$cnd_idx[$idx] = $scnds[$fid];
$cnd_len[$idx] = array();
$idx2 = 0;
foreach ($scnds[$fid][1] as $v){$cnd_len[$idx][$idx2] = strlen($v);
$idx2 ++;}}
if (isset($sfid_ref[$fid])){$sel_idx[$idx] = $fid;}
if (isset($order[$fid])){$ord_idx[$idx] = $order[$fid];}
$idx ++;}}
$fname = Lltbf_initialize($path);
$loc = Lltbf_lock($fname);
$fp_dat = fopen($fname['DAT'], "r");
if (!$fp_dat) { LlutlLog(__FILE__, __LINE__, sprintf("LlsetSelectDb(%s,...) open failed.", $tid)); exit; }
$recs = array();
while (!feof($fp_dat)){$fld = LltbfGetField($fp_dat);
$is_sel = TRUE;
foreach ($cnd_idx as $idx => $info){if (!isset($fld[$idx])) { $is_sel = FALSE; break; }
$fval   = $fld[$idx];
$iscnds = $info[0];
$ivals  = $info[1];
if ($iscnds == LLSET_DB_SCNDS_EQ){if ($ftp_idx[$idx] == 'int'){$is_sel2 = FALSE;
foreach ($ivals as $iv){if ($fval == $iv) { $is_sel2 = TRUE; break; }}
if (!$is_sel2) { $is_sel = FALSE; break; }}
else{$is_sel2 = FALSE;
foreach ($ivals as $iv){if (strcmp($fval, $iv) == 0) { $is_sel2 = TRUE; break; }}
if (!$is_sel2) { $is_sel = FALSE; break; }}}
else if ($iscnds == LLSET_DB_SCNDS_LIKE){$is_sel2 = FALSE;
foreach ($ivals as $iv){if (mb_strpos($fval, $iv) !== FALSE) { $is_sel2 = TRUE; break; }}
if (!$is_sel2) { $is_sel = FALSE; break; }}
else if ($iscnds == LLSET_DB_SCNDS_LIKE_PRE){$is_sel2 = FALSE;
$idx2 = 0;
foreach ($ivals as $iv){if (strncmp($fval, $iv, $scnd_len[$idx][$idx2]) == 0) { $is_sel2 = TRUE; break; }
$idx2 ++;}
if (!$is_sel2) { $is_sel = FALSE; break; }}}
if (!$is_sel) { continue; }
$wrec = array();
foreach ($sel_idx as $idx => $fid){$wrec[$fid] = $fld[$idx];}
$recs[] = $wrec;}
fclose($fp_dat);
Lltbf_unlock($loc);
return $recs;}
define('LLSET_DB_ORDER_NUM',		1);
define('LLSET_DB_ORDER_TEXT',		2);
define('LLSET_DB_ORDER_NUM_DESC',	-1);
define('LLSET_DB_ORDER_TEXT_DESC',	-2);
$LLSET_FDB_SORT_ORDER = array();
function LlsetFdbSort(&$recs,$order){global $LLSET_FDB_SORT_ORDER;
$LLSET_FDB_SORT_ORDER = $order;
usort($recs, 'LlsetFldSort_cmp');}
function LlsetFldSort_cmp($a, $b){global $LLSET_FDB_SORT_ORDER;
foreach ($LLSET_FDB_SORT_ORDER as $fid => $order_type){if ($order_type == LLSET_DB_ORDER_NUM){if      ($a[$fid] < $b[$fid]) { return -1; }
else if ($a[$fid] > $b[$fid]) { return 1; }}
else if ($order_type == LLSET_DB_ORDER_NUM_DESC){if      ($b[$fid] < $a[$fid]) { return -1; }
else if ($b[$fid] > $a[$fid]) { return 1; }}
else if ($order_type == LLSET_DB_ORDER_TEXT){$r = strcmp($a[$fid], $b[$fid]);
if ($r != 0) { return $r; }}
else if ($order_type == LLSET_DB_ORDER_TEXT_DESC){$r = strcmp($b[$fid], $a[$fid]);
if ($r != 0) { return $r; }}}
return 0;}
function LlsetFieldDateTime($tm = 0){$dt = LlutlDateTime($tm <= 0 ? time() : $tm);
return sprintf('%04d-%02d-%02d %02d:%02d:%02d', $dt['year'], $dt['mon'], $dt['day'], $dt['hour'], $dt['min'], $dt['sec']);}
function LlsetAddSqlFromSelectJkns(&$sql,&$joi,&$jkns){foreach ($jkns as $jkn){$jfid  = $jkn['fid'];
$jtype = str_replace('int', 'num', $jkn['type']);
$jval  = str_replace("'", '', $jkn['val']);
$len   = is_array($jval) ? sizeof($jval) : strlen($jval);
if      ($jtype == 'num'  ) { $sql .= " ${joi} ${jfid} =  '${jval}'"; }
else if ($jtype == '^num' ) { $sql .= " ${joi} ${jfid} <> '${jval}'"; }
else if ($jtype == 'num>=') { $sql .= " ${joi} ${jfid} >= '${jval}'"; }
else if ($jtype == 'num>' ) { $sql .= " ${joi} ${jfid} >  '${jval}'"; }
else if ($jtype == 'num<=') { $sql .= " ${joi} ${jfid} <= '${jval}'"; }
else if ($jtype == 'num<' ) { $sql .= " ${joi} ${jfid} <  '${jval}'"; }
else if ($jtype == 'num()'){$jvals = is_array($jval) ? $jval : array($jval);
$jstr  = "'".join("','", $jvals)."'";
$sql  .= " ${joi} ${jfid} in (${jstr})";}
else if ($jtype == 'text'   ) { $sql .= " ${joi} ${jfid} = '${jval}'"; }
else if ($jtype == 'text*'  ) { $sql .= " ${joi} ${jfid} like '${jval}%'"; }
else if ($jtype == '*text'  ) { $sql .= " ${joi} ${jfid} like '%${jval}'"; }
else if ($jtype == '*text*' ) { $sql .= " ${joi} ${jfid} like '%${jval}%'"; }
else if ($jtype == '^text'  ) { $sql .= " ${joi} ${jfid} <> '${jval}'"; }
else if ($jtype == '^text*' ) { $sql .= " ${joi} ${jfid} not like '${jval}%'"; }
else if ($jtype == '^*text' ) { $sql .= " ${joi} ${jfid} not like '%${jval}'"; }
else if ($jtype == '^*text*') { $sql .= " ${joi} ${jfid} not like '%${jval}%'"; }
else if ($jtype == 'text>=' ) { $sql .= " ${joi} strcmp(${jfid}, '${jval}') >= 0"; }
else if ($jtype == 'text>'  ) { $sql .= " ${joi} strcmp(${jfid}, '${jval}') >  0"; }
else if ($jtype == 'text<=' ) { $sql .= " ${joi} strcmp(${jfid}, '${jval}') <= 0"; }
else if ($jtype == 'text<'  ) { $sql .= " ${joi} strcmp(${jfid}, '${jval}') <  0"; }
else if ($jtype == 'text()' ){$jvals = is_array($jval) ? $jval : array($jval);
$jstr  = "'".join("','", $jvals)."'";
$sql  .= " ${joi} ${jfid} in (${jstr})";}
else if ($jtype == 'text[]' ){$jvals = is_array($jval) ? $jval : array($jval);
$wsql  = array();
foreach ($jvals as $v) { $wsql[] = "${jfid} like '%${v}%'"; }
if (sizeof($wsql) <= 0) { continue; }
$sql  .= " ${joi} (".join(' and ', $wsql).")";}
$joi = 'and';}}
$LLSET_SELECT_FLDS_CMP = array();
$LLSET_SELECT_FLDS_COUNT = 0;
function LlsetSelectFlds($tbl,$offset = 0,$nline = 0,$jkns = array(),$order = ''){global $LLSET_ALL;
global $LLSET_SELECT_FLDS_CMP;
global $LLSET_SELECT_FLDS_COUNT;
$tblfld = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
$recs = array();
if (TRUE){$path  = LlsetGetPath($tbl, '');
$fmt   = LlsetFormat($tbl);
$dats  = LltbfFileToArray($path);
foreach ($dats as $dat){$flds = LltbfIndexToKey($dat, $fmt);
$is_set = TRUE;
foreach ($jkns as $jkn){$jfid  = $jkn['fid'];
$jtype = str_replace('int','num',$jkn['type']);
$jval  = $jkn['val'];
$len   = is_array($jval) ? sizeof($jval) : strlen($jval);
if      ($jtype == 'num'     && $flds[$jfid] != $jval)								{ $is_set = FALSE; break; }
else if ($jtype == '^num'    && $flds[$jfid] == $jval)								{ $is_set = FALSE; break; }
else if ($jtype == 'num>='   && $flds[$jfid] <  $jval)								{ $is_set = FALSE; break; }
else if ($jtype == 'num>'    && $flds[$jfid] <= $jval)								{ $is_set = FALSE; break; }
else if ($jtype == 'num<='   && $flds[$jfid] >  $jval)								{ $is_set = FALSE; break; }
else if ($jtype == 'num<'    && $flds[$jfid] >= $jval)								{ $is_set = FALSE; break; }
else if ($jtype == 'num()'   && !in_array($flds[$jfid], $jval))						{ $is_set = FALSE; break; }
else if ($jtype == 'text'    && strcmp($flds[$jfid], $jval) != 0)					{ $is_set = FALSE; break; }
else if ($jtype == 'text*'   && strncmp($flds[$jfid], $jval, $len) != 0)			{ $is_set = FALSE; break; }
else if ($jtype == '*text'   && strcmp(substr($flds[$jfid], -1*$len), $jval) != 0)	{ $is_set = FALSE; break; }
else if ($jtype == '*text*'  && strpos($flds[$jfid], $jval) === FALSE)				{ $is_set = FALSE; break; }
else if ($jtype == '^text'   && strcmp($flds[$jfid], $jval) == 0)					{ $is_set = FALSE; break; }
else if ($jtype == '^text*'  && strncmp($flds[$jfid], $jval, $len) == 0)			{ $is_set = FALSE; break; }
else if ($jtype == '^*text'  && strcmp(substr($flds[$jfid], -1*$len), $jval) == 0)	{ $is_set = FALSE; break; }
else if ($jtype == '^*text*' && strpos($flds[$jfid], $jval) !== FALSE)				{ $is_set = FALSE; break; }
else if ($jtype == 'text>='  && strcmp($flds[$jfid], $jval) < 0)					{ $is_set = FALSE; break; }
else if ($jtype == 'text>'   && strcmp($flds[$jfid], $jval) <= 0)					{ $is_set = FALSE; break; }
else if ($jtype == 'text<='  && strcmp($flds[$jfid], $jval) > 0)					{ $is_set = FALSE; break; }
else if ($jtype == 'text<'   && strcmp($flds[$jfid], $jval) >= 0)					{ $is_set = FALSE; break; }
else if ($jtype == 'text()'  && !in_array($flds[$jfid], $jval))						{ $is_set = FALSE; break; }
else if ($jtype == 'text[]'){foreach ($jval as $v){if (strpos($flds[$jfid], $v) === FALSE){$is_set = FALSE;
break 2;}}}}
if (!$is_set) { continue; }
$recs[] = $flds;}}
$LLSET_SELECT_FLDS_COUNT = sizeof($recs);
if ($order != ''){$LLSET_SELECT_FLDS_CMP = array();
foreach (explode(',', $order) as $w1){$wcmp = array();
foreach (explode(';', $w1) as $w2){$w3 = explode('=', $w2);
$wk = trim($w3[0]);
$wv = trim($w3[1]);
if ($wk == 'desc'){$wcmp[$wk] = strtoupper(substr($wv, 0, 1)) == 'Y';}
else{$wcmp[$wk] = $wv;}}
$LLSET_SELECT_FLDS_CMP[] = $wcmp;}
usort($recs, 'LlsetSelectFlds_cmp');}
$rtns  = array();
$cnt   = 0;
$nset  = 0;
foreach ($recs as $rec){if ($cnt >= $offset){$key = $rec[LLSET_KEY_FID];
$rtns[$key] = $rec;
$nset ++;}
if ($nline > 0 && $nset >= $nline) { break; }
$cnt ++;}
return $rtns;}
function LlsetSelectFlds_cmp($a, $b){global $LLSET_SELECT_FLDS_CMP;
$orders = $LLSET_SELECT_FLDS_CMP;
$ord = array_shift($orders);
while ($ord != NULL){$fid  = $ord['fid'];
$type = $ord['type'];
$desc = $ord['desc'];
if ($type == 'int' || $type == 'num'){if ($desc){if      ($a[$fid] < $b[$fid]) { return 1; }
else if ($a[$fid] > $b[$fid]) { return -1; }}
else{if      ($a[$fid] > $b[$fid]) { return 1; }
else if ($a[$fid] < $b[$fid]) { return -1; }}}
else if ($type == 'text'){$p = strcmp($a[$fid], $b[$fid]);
if ($desc){if      ($p < 0) { return 1; }
else if ($p > 0) { return -1; }}
else{if      ($p > 0) { return 1; }
else if ($p < 0) { return -1; }}}
else{LlutlDebugWrite('ERROR : '.__FILE__.' Line.'.__LINE__);
exit;}
$ord = array_shift($orders);}
return 0;}
function LlsetSelect($tid,$pkey,$keys){$fmt   = LlsetFormat($tid);
$ikeys = LlsetGetSelIdxKey($fmt, $keys);
$kfld = array();
LlsetSelect2(LlsetGetPath($tid, $pkey), $fmt, $ikeys, $kfld);
return $kfld;}
function LlsetSelect1($tid,$pkey,$key){$kfld = array();
LlsetSelect2(LlsetGetPath($tid, $pkey), LlsetFormat($tid), array(0 => $key), $kfld);
return $kfld;}
function LlsetSelect2($path,$fmt,$keys,&$kfld){$ifld = array();
$srtn = LltbfSelect2($path, $keys, $ifld);
if ($srtn <= 0) { return $srtn; }
$kfld = LltbfIndexToKey($ifld, $fmt);
return $srtn;}
function LlsetSelResult(&$fld){if (sizeof($fld) <= 0 || $fld[LLSET_KEY_FID] == '') { return FALSE; }
return TRUE;}
function LlsetGetKeyVal($tid,$pkey,$key_fld,$val_fld){$fmt   = LlsetFormat($tid);
$keys  = array($key_fld => 0, $val_fld => 1);
$ikeys = LlsetGetSelIdxKey($fmt, $keys);
$idxs  = array(0 => 0, 1 => 0);
foreach ($ikeys as $idx => $val) { $idxs[$val] = $idx; }
return LltbfFileToKeyVal(LlsetGetPath($tid, $pkey), $idxs[0], $idxs[1]);}
$LLSET_UPD_INS1_KEY = '';
function LlsetUpdIns1($tid,$pkey,$key,&$kfld,$pos){global $LLSET_UPD_INS1_KEY;
global $LLSET_NEW_KEY;
$sfld = LlsetSelect1($tid, $pkey, $key);
if (sizeof($sfld) > 0 && $sfld[LLSET_KEY_FID] != ''){foreach($kfld as $fid => $fval){$sfld[$fid] = $fval;}
if (LlsetUpdate1($tid, $pkey, $key, $sfld, TRUE) <= 0) { return FALSE; }
$LLSET_UPD_INS1_KEY = $sfld[LLSET_KEY_FID];}
else{$sfld = array();
$fmt  = LlsetFormat($tid);
foreach($fmt as $fid){$sfld[$fid] = isset($kfld[$fid]) ? $kfld[$fid] : '';}
if (LlsetInsert1($tid, $pkey, $sfld, $pos) <= 0) { return FALSE; }
$LLSET_UPD_INS1_KEY = $LLSET_NEW_KEY;}
return TRUE;}
function LlsetInsert1($tid,$pkey,&$kfld,$pos){return LlsetInsert2(LlsetGetPath($tid, $pkey), LlsetFormat($tid), $kfld, $pos);}
function LlsetInsert2($path,$fmt,&$kfld,$pos){global $LLSET_NEW_KEY;
LltbfAutoLock(FALSE);
$fname = LltbfGetFname($path);
$loc   = LltbfLock($fname);
rewind($loc['fp']);
$val = fgets($loc['fp'], 256);
if (!$val || !isset($val) || strlen($val) <= 0){$maxkey = -1;
$kv = LltbfFileToKeyVal($path, 0, 0);
foreach ($kv as $kv1 => $kv2){if ($maxkey < $kv1) { $maxkey = $kv1; }}
$key = $maxkey < 0 ? LLSET_KEY_INIT_VAL : $maxkey + 1;}
else{$key = LlutlRtrim($val, "\r\n") + 1;}
rewind($loc['fp']);
fputs($loc['fp'], "$key\n");
$kfld[LLSET_KEY_FID] = $key;
$ifld = LltbfKeyToIndex($kfld, $fmt);
$irtn = LltbfInsert($path, $ifld, $pos);
LltbfUnlock($loc);
LltbfAutoLock(TRUE);
$LLSET_NEW_KEY = $key;
return $irtn;}
function LlsetUpdate1($tid,$pkey,$key,&$kfld,$all_fld = FALSE){$l_path = LlsetGetPath($tid, $pkey);
$l_fmt  = LlsetFormat($tid);
$l_key  = array(0 => $key);
if ($all_fld){return LlsetUpdate2($l_path, $l_fmt, $l_key, $kfld);}
else{$ufld = array();
LlsetSelect2($l_path, $l_fmt, $l_key, $ufld);
foreach ($kfld as $fid => $fval) { $ufld[$fid] = $fval; }
return LlsetUpdate2($l_path, $l_fmt, $l_key, $ufld);}}
function LlsetUpdate2($path,$fmt,$keys,&$kfld){$ifld = LltbfKeyToIndex($kfld, $fmt);
return LltbfUpdate2($path, $keys, $ifld);}
function LlsetUpdate3($tbl,$jkns,$updfld){global $LLSET_ALL;
$tflds = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
$idxs  = LlsetFormatIdx($tbl);
$path  = LlsetGetPath($tbl, '');
$dats  = LltbfFileToArray($path);
$ndats = sizeof($dats);
$cnt   = 0;
for ($i = 0; $i < $ndats; $i ++){foreach ($jkns as $fid => $v){$idx   = $idxs[$fid];
$ftype = isset($tflds[$fid]) ? $tflds[$fid][LLSET_FI_TYPE] : '';
$ftp3  = substr($ftype, 0, 3);
if ($ftp3 == 'int' || $ftp3 == 'num' || $ftp3 == 'flo')	{ if ($dats[$i][$idx] != $v) { continue 2; } }
else													{ if (strcmp($dats[$i][$idx], $v) != 0) { continue 2; } }}
foreach ($updfld as $fid => $v){$idx = $idxs[$fid];
$dats[$i][$idx] = $v;}
$cnt ++;}
LltbfArrayToFile($path, $dats);
return $cnt;}
function LlsetDelete1($tid,$pkey,$key){LlsetDeleteRecImages($tid, $pkey, $key);
return LltbfDelete2(LlsetGetPath($tid, $pkey), array(0 => $key));}
function LlsetDeleteRecCTables($tid,$pkey,$key){global $LLSET_ALL;
$slsts = $LLSET_ALL[$tid][LLSET_AI_TBL][LLSET_TI_LST];
if (!is_array($slsts)) { return; }
foreach ($slsts as $fid => $slst){$type = $slst[LLSET_LI_TYPE];
if (strcmp($type, 'child') == 0){$ctid  = $slst[LLSET_LI_CTID];
$cpkey = $pkey . '-' . $key;
LlsetDeleteTable($ctid, $cpkey);}}}
function LlsetDeleteTable($tid,$pkey){$path  = LlsetGetPath($tid, $pkey);
$fmt   = LlsetFormat($tid);
$fname = LltbfGetFname($path);
$loc = LltbfLock($fname);
$fp  = fopen($fname['DAT'], "r");
while ($fp && !feof($fp)){$kfld = LltbfIndexToKey(LltbfGetField($fp), $fmt);
if (strlen($kfld[LLSET_KEY_FID]) <= 0) { continue; }
LlsetDeleteRecCTables($tid, $pkey, $kfld[LLSET_KEY_FID]);
LlsetDeleteRecImages($tid, $pkey, $kfld[LLSET_KEY_FID]);}
fclose($fp);
LltbfUnlock($loc);
LltbfUnlink($path);}
function LlsetDeleteRecImages($tid,$pkey,$key){LlsetDelImg($tid, $key);}
function LlsetDeleteImage($tid,$fid,$pkey,$key){LlsetDelImgFile($tid, $key, $fid);}
function LlsetMove1($tid,$pkey,$key,$pos){return LlsetMove2(LlsetGetPath($tid, $pkey), array(0 => $key), $pos);}
function LlsetMove2($path,$keys,$pos){LltbfAutoLock(FALSE);
$fname = LltbfGetFname($path);
$loc   = LltbfLock($fname);
$ifld = array();
if (LltbfSelect2($path, $keys, $ifld) <= 0){LltbfUnlock($loc);
LltbfAutoLock(TRUE);
return -1;}
LltbfDelete2($path, $keys);
$irtn = LltbfInsert($path, $ifld, $pos);
LltbfUnlock($loc);
LltbfAutoLock(TRUE);
return $irtn;}
function LlsetCrypt($str){return substr(crypt($str, 'LS'), 2);}
function LlsetImgGetBasePath($tid,$fid,$pkey,$key){global $LLSET_ALL;
$sfld = $LLSET_ALL[$tid][LLSET_AI_TBL][LLSET_TI_FLD][$fid];
$path = $sfld[LLSET_FI_IPATH];
$pkey.= '-' . $key;
if (strcmp(substr($path,-1), '/') == 0){return $path . substr($pkey, 1);}
else{return $path . $pkey;}}
function LlsetImgSearchPathFromId($tid,$fid,$pkey,$key){return LlsetImgSearchPath(LlsetImgGetBasePath($tid, $fid, $pkey, $key));}
function LlsetImgSearchPath($base){return LlutlImgSearchPath($base);}
function LlsetImgSetTag($img_path,$img_info_str,$add_param){if ($img_path == '') { return ''; }
$tag_add = '';
$img_info = LlsetImgGetInfo($img_info_str);
if ($img_info['width'] != '')  { $tag_add .= ' width="'.$img_info[width].'"'; }
if ($img_info['height'] != '') { $tag_add .= ' height="'.$img_info[height].'"'; }
$tge = LlutlHtmlXhtmlTag('>');
return "<img src=\"${img_path}\" border=\"0\" ${tag_add} ${add_param}${tge}";}
function LlsetImgGetInfo($img_info_str){$img_info = array( 'width' => '', 'height' => '');
if (strlen($img_info_str) > 0){$p = explode(',', $img_info_str);
$np = count($p);
if ($np > 0) { $img_info['width']  = $p[0]; }
if ($np > 1) { $img_info['height'] = $p[1]; }}
return $img_info;}
function LlsetImgGetTag($tbl,$fid,$pkey,$key,$img_info,$def){$img_path = LlsetImgSearchPathFromId($tbl, $fid, $pkey, $key);
return LlsetImgSetTag($img_path, $img_info, $def);}
function LlsetGetImageType($tag_name){return LlutlImgGetType($tag_name);}
function LlsetGetSelOpt(&$list,$val,$lary = TRUE){$opt = '';
foreach ($list as $lval => $lstr){if (!$lary) { $lval = $lstr; }
$sel = '';
if (is_array($val)){if (in_array($lval, $val)) { $sel = LlutlHtmlXhtmlTag('selected'); }}
else{if (strcmp($lval, $val) == 0) { $sel = LlutlHtmlXhtmlTag('selected'); }}
$opt.= "<option value=\"${lval}\" ${sel}>${lstr}</option>\n";}
return $opt;}
function LlsetGetSelOpt2(&$list,$val){$opt    = '';
$selset = FALSE;
foreach ($list as $vals){$lval = $vals[0];
$lstr = $vals[1];
$sel  = '';
if (!$selset && strcmp($lval, $val) == 0){$sel = LlutlHtmlXhtmlTag('selected');
$selset = TRUE;}
$opt.= "<option value=\"${lval}\" ${sel}>${lstr}</option>\n";}
return $opt;}
function LlsetGetSelOptPage($npage,$nline,$page){$opt_page = '';
for ($i = 1; $i <= $npage; $i ++){$l1  = ($i - 1) * $nline + 1;
$l2  = $l1 + $nline - 1;
$sel = $i == $page ? LlutlHtmlXhtmlTag('selected') : '';
$opt_page .= "<option value=\"${i}\" ${sel}>&nbsp;${i}&nbsp;PAGE&nbsp;(${l1}".'～'."${l2})&nbsp;</option>\n";}
return $opt_page;}
function LlsetGetNumList($num1,$num2,$str){$list = array();
for ($i = $num1; $i <= $num2; $i ++){$list[$i] = $i.$str;}
return $list;}
function LlsetGetCheckBox($fname,$fval,$val){$chk = $fval == $val ? LlutlHtmlXhtmlTag('checked') : '';
$tge = LlutlHtmlXhtmlTag('>');
return "<input type=\"checkbox\" name=\"${fname}\" value=\"${fval}\" ${chk}${tge}";}
function LlsetGetCheckBoxes($fname,&$list,$lvals,$fsep){$vals = array();
foreach ($lvals as $lval) { $vals[$lval] = $lval; }
$opt = '';
$joi = '';
$tge = LlutlHtmlXhtmlTag('>');
foreach ($list as $lval => $lstr){$chk = isset($vals[$lval]) ? LlutlHtmlXhtmlTag('checked') : '';
$opt.= "${joi}<input type=\"checkbox\" name=\"${fname}\" value=\"${lval}\" ${chk}${tge}${lstr}\n";
$joi = $fsep;}
return $opt;}
function LlsetGetRadio($fname,&$list,$val,$fsep){$opt = '';
$joi = '';
$tge = LlutlHtmlXhtmlTag('>');
foreach ($list as $lval => $lstr){$chk = strcmp($lval, $val) == 0 ? LlutlHtmlXhtmlTag('checked') : '';
$opt.= "${joi}<input type=\"radio\" name=\"${fname}\" value=\"${lval}\" ${chk}${tge}${lstr}\n";
$joi = $fsep;}
return $opt;}
function LlsetIsExist(&$fld,$fid){return isset($fld[$fid]) && $fld[$fid] != '';}
function LlsetIsDb($tid){global $LLSET_ALL;
return $LLSET_ALL[$tid][LLSET_AI_TBL][LLSET_TI_PATH] == '#' ? TRUE : FALSE;}
function LlsetDbFormat($tid){global $LLSET_ALL;
$fmt   = array();
$sflds = $LLSET_ALL[$tid][LLSET_AI_TBL][LLSET_TI_FLD];
foreach($sflds as $fid => $sfld){if (strncmp($sfld[LLSET_FI_TYPE], 'cmt', 3) != 0){$fmt[] = $fid;}}
return $fmt;}
function LlsetDbCreateTable($db,$tid,$exit = FALSE){global $KUSET_ALL;
$sflds = $KUSET_ALL[$tid][KUSET_AI_TBL][KUSET_TI_FLD];
$key   = $KUSET_ALL[$tid][KUSET_AI_TBL][KUSET_TI_DB_KEY];
if (LldbTableExist($db, $tid)) { return; }
$sql = 'create table '.$tid;
$joi = '(';
foreach($sflds as $fid => $sfld){$type = $sfld[KUSET_FI_TYPE];
$sql .= "$joi $fid $type";
$joi  = ',';}
if ($key != '') { $sql .= "$joi primary key ($key)"; }
$sql .= ')';
LldbExec($db, LldbCodePhpToDb($sql), FALSE);}
function LlsetDbDropTable($db,$tid,$exit = FALSE){$sql = 'drop table '.$tid.';';
LldbExec($db, LldbCodePhpToDb($sql), $exit);}
function LlsetIsUnique($tbl,$fid,$fval,$pkey = '',$key = ''){$chks = LlsetGetKeyVal($tbl, $pkey, $fid, LLSET_KEY_FID);
if ($key == ''){return isset($chks[$fval]) ? FALSE : TRUE;}
else{return isset($chks[$fval]) && $chks[$fval] != $key ? FALSE : TRUE;}}
function LlsetReplaceSlist(&$html,$label,&$val,&$list,$lary = FALSE,$add_label = ''){$ulab = $add_label.strtoupper($label);
$llab = strtolower($label);
$vals = is_array($val) ? $val : array($val);
$chk  = LlutlHtmlXhtmlTag('checked');
$sel  = LlutlHtmlXhtmlTag('selected');
$para = array();
$str1 = explode('<!--'.LLUTL_REP_MARK.'SLIST_'.$ulab.'_PARA'.LLUTL_REP_MARK, $html);
if (isset($str1[1])){$str2 = explode(LLUTL_REP_MARK.'-->', $str1[1]);
foreach (explode(',', $str2[0]) as $str3){$str4 = explode('=', $str3);
$para[$str4[0]] = $str4[1];}
$html = $str1[0].substr(strstr($str1[1], LLUTL_REP_MARK.'-->'), 5);}
$col = LlutlGetNum0(isset($para['col']) ? $para['col'] : '');
$htmls = explode('<!--'.LLUTL_REP_MARK.'SLIST_'.$ulab.LLUTL_REP_MARK.'-->', $html);
if (isset($htmls[1])){$html1 = '';
$cnt   = 0;
foreach ($list as $lval => $lstr){if (!$lary) { $lval = $lstr; }
$line = $htmls[1];
$lrep = array();
$lrep[LLUTL_REP_MARK.'SLIST_'.$ulab.'_VAL'.LLUTL_REP_MARK] = $lval;
$lrep[LLUTL_REP_MARK.'SLIST_'.$ulab.'_STR'.LLUTL_REP_MARK] = $lstr;
$lrep[LLUTL_REP_MARK.'SLIST_'.$ulab.'_CNT'.LLUTL_REP_MARK] = $cnt + 1;
$lrep[LLUTL_REP_MARK.'SLIST_'.$ulab.'_CHK'.LLUTL_REP_MARK] = in_array($lval, $vals) ? $chk : '';
$lrep[LLUTL_REP_MARK.'SLIST_'.$ulab.'_SEL'.LLUTL_REP_MARK] = in_array($lval, $vals) ? $sel : '';
if ($col > 0){$line = LlutlReplaceIf('IF_SLIST_'.$ulab.'_LEFT',  $cnt % $col == 0,        $line);
$line = LlutlReplaceIf('IF_SLIST_'.$ulab.'_RIGHT', $cnt % $col == $col - 1, $line);
$line = LlutlReplaceIf('IF_SLIST_'.$ulab.'_EXIST', TRUE, $line);}
$line = LlutlReplaceCase('CASE_SLIST_'.$ulab, $lval, $line);
$html1 .= str_replace(array_keys($lrep), array_values($lrep), $line);
$cnt ++;}
if ($col > 0 && ($cnt % $col) > 0){$nzan = $col - ($cnt % $col);
for ($i = 1; $i <= $nzan; $i ++){$line = $htmls[1];
$line = LlutlReplaceIf('IF_SLIST_'.$ulab.'_LEFT',  FALSE, $line);
$line = LlutlReplaceIf('IF_SLIST_'.$ulab.'_RIGHT', $i == $nzan, $line);
$line = LlutlReplaceIf('IF_SLIST_'.$ulab.'_EXIST', FALSE, $line);
$html1 .= str_replace(array_keys($lrep), array_values($lrep), $line);}}
$html = $htmls[0] . $html1 . $htmls[2];}}
function LlsetReplaceList(&$html,$label,$fid,$val,$list){$ulab = 'LIST_'.strtoupper($label.'_'.$fid);
$vals  = is_array($val) ? $val : array($val);
$htmls = explode('<!--'.LLUTL_REP_MARK.$ulab.LLUTL_REP_MARK.'-->', $html);
if (isset($htmls[1])){$html1 = '';
foreach ($vals as $k){$nm = isset($list[$k]) ? $list[$k] : $k;
$line = $htmls[1];
$lrep = array();
$lrep[LLUTL_REP_MARK.$ulab.'_STR'.LLUTL_REP_MARK] = $nm;
$html1 .= str_replace(array_keys($lrep), array_values($lrep), $line);}
$html = $htmls[0] . $html1 . $htmls[2];}}
function LlsetWorkInfoPut($group,&$winfo,$lock = TRUE){$dat_path = LlsetWorkInfoPath($group);
$lh = $lock ? LlsetWorkInfoLock($group) : FALSE;
file_put_contents($dat_path, serialize($winfo));
if ($lock) { LlsetWorkInfoUnlock($lh); }}
function LlsetWorkInfoGet($group,$lock = TRUE){$dat_path = LlsetWorkInfoPath($group);
if (file_exists($dat_path)){$lh = $lock ? LlsetWorkInfoLock($group) : FALSE;
$dstr = file_get_contents($dat_path);
if ($lock) { LlsetWorkInfoUnlock($lh); }
return unserialize($dstr);}
else{return array();}}
function LlsetWorkInfoUpd($group,$key,$val){$lh = LlsetWorkInfoLock($group);
$winfo = LlsetWorkInfoGet($group, FALSE);
$winfo[$key] = $val;
LlsetWorkInfoPut($group, $winfo, FALSE);
LlsetWorkInfoUnlock($lh);}
function LlsetWorkInfoPath($group,$ext = 'cgi'){return substr(LLSET_DIR_WORK_INFO, -1) == '/' ? LLSET_DIR_WORK_INFO.$group.'.'.$ext : LLSET_DIR_WORK_INFO.'/'.$group.'.'.$ext;}
function LlsetWorkInfoLock($group){LlutlMkDir(LLSET_DIR_WORK_INFO);
$loc_path = LlsetWorkInfoPath($group, 'loc');
return LlutlFileOpenLock($loc_path, 'a+');}
function LlsetWorkInfoUnlock(&$lh){LlutlFileCloseUnlock($lh);}
function LlsetSetHiddenPara($jkns = array()){$hidden_para = '';
$tail = LlutlHtmlXhtmlTag('>')."\n";
foreach ($jkns as $fid => $fval){if (is_array($fval)){foreach ($fval as $fval2){$fval2 = LlutlHtmlEscapeTagForText($fval2);
$hidden_para.= "<input type=\"hidden\" name=\"${fid}[]\" value=\"${fval2}\"${tail}";}}
else{$fval = LlutlHtmlEscapeTagForText($fval);
$hidden_para.= "<input type=\"hidden\" name=\"${fid}\" value=\"${fval}\"${tail}";}}
return $hidden_para;}
function LlsetPara($fid,$is_array,$def){if ($is_array){if (LlutlIsPara($fid)){if (LlutlIsParaArray($fid)){return LlutlParas($fid);}
else{return LlsetMfldStrToAry(LlutlPara2($fid, ''));}}
else{return LlutlIsPara(LLSET_NODEF_PREFIX.$fid) ? array() : $def;}}
else{return LlutlPara2($fid, $def);}}
function LlsetGetFF($tid,$fid,$reload = FALSE){$f = LlsetGetF($tid, $reload);
return $f[$fid];}
$LLSET_GET_F = array();
function LlsetGetF($tid,$reload = FALSE){global $LLSET_GET_F;
if ($reload || !isset($LLSET_GET_F[$tid]) || sizeof($LLSET_GET_F[$tid]) <= 0){$tids = explode(':', $tid);
if (sizeof($tids) >= 2){$info = LlsetReadFileList(LlsetPathFileListTable($tids[1], $tids[0]));
$LLSET_GET_F[$tid] = isset($info['data'][0]) ? $info['data'][0] : array();}
else{$LLSET_GET_F[$tid] = LlsetSelect($tid, '', NULL);}}
return $LLSET_GET_F[$tid];}
function LlsetClearGetF(){global $LLSET_GET_F;
$LLSET_GET_F = array();}
function LlsetExistGetF($tid){$tids = explode(':', $tid);
if (sizeof($tids) >= 2){$f = LlsetGetF($tid);
return sizeof($f) > 0;}
else{$f = LlsetGetF($tid);
return isset($f[LLSET_KEY_FID]) && $f[LLSET_KEY_FID] != '';}}
function LlsetGetBaseFetc(){return LlsetIsExistBase() ? LlsetGetF(LLUTL_DIRNM_BASE.':fetc') : array();}
function LlsetGetFetc($fid = ''){$f = LlsetGetF('fetc');
return $fid == '' ? $f : $f[$fid];}
function LlsetGetFidp($fid = ''){$f = LlsetGetF('fidp');
return $fid == '' ? $f : $f[$fid];}
function LlsetSiteTitle(){$site_title = LlsetGetFetc('site_title');
return $site_title != '' ? $site_title : LlsetSiteTitleDef();}
function LlsetSiteTitleDef(){return LLSET_PRODUCT_NAME.' ver.'.LLSET_PRODUCT_VER;}
function LlsetAdminAddLinks($label){$text = LlsetGetFetc($label);
if (trim($text) == '') { return array(); }
return explode("\n", str_replace(array("\r\n", "\n\r", "\r"), array("\n", "\n", "\n"), $text));}
function LlsetMfldToDispStr($mfld,$null = '',$joi  = LLSET_MFLD_SEP_DISP){if (is_array($mfld)){if (sizeof($mfld) <= 0) { return $null; }
return join($joi, $mfld);}
else{if (trim($mfld) == '') { return $null; }
return join($joi, LlsetMfldStrToAry($mfld));}}
function LlsetMfldStrToAry($str){$rtn = array();
foreach (explode(LLSET_MFLD_SEP, $str) as $fld){if ($fld != '') { $rtn[] = $fld; }}
return $rtn;}
function LlsetMfldAryToStr(&$ary){$wk = array();
foreach ($ary as $fld){if ($fld != '') { $wk[] = $fld; }}
return LLSET_MFLD_SEP.implode(LLSET_MFLD_SEP, $wk).LLSET_MFLD_SEP;}
function LlsetMfldStrToDispStr($str,&$list){$disp = array();
$ary  = is_array($str) ? $str : LlsetMfldStrToAry($str);
foreach ($ary as $cd){if ($cd != ''){$disp[] = isset($list[$cd]) ? $list[$cd] : $cd;}}
return join(LLSET_MFLD_SEP_DISP, $disp);}
function LlsetIsUpdateMode(&$html,&$rep,$msg,$err = FALSE,$hdn = array(),$btn = '　戻　る　'){if (LlsetIsUpdateModeFlag()) { return TRUE; }
if (LlsetSiteUpdateMode() == 'SAMPLE'){$msg = LlutlMsgf('updatemode01');
$err = TRUE;}
else{$msg = LlutlMsgf('formset02');
$err = TRUE;}
LlsetReplaceFormMsg($html, $rep, $msg, $err, $hdn, $btn);
return FALSE;}
function LlsetIsUpdateModeFlag(){return LlsetSiteUpdateMode() == '' ? TRUE : FALSE;}
function LlsetSiteUpdateMode(){return defined('SET_SITE_UPDATE_MODE') ? SET_SITE_UPDATE_MODE : '';}
$LLSET_REPLACE_FORM_MSG_SKIP = FALSE;
function LlsetReplaceFormMsg(&$html,&$rep,$msg,$err = FALSE,$hdn = array(),$btn = '　戻　る　'){global $LLSET_REPLACE_FORM_MSG_SKIP;
if ($LLSET_REPLACE_FORM_MSG_SKIP) { return; }
$rep['##MSG##']     = $msg;
$rep['##MSG_BTN##'] = $btn;
$rep['<!--##MSG_HIDDEN_PARA##-->'] = LlsetSetHiddenPara($hdn);
$html = LlutlReplaceIf('IF_MSG_ERR',         $err, $html);
$html = LlutlReplaceIf('IF_MSG_HIDDEN_PARA', sizeof($hdn) > 0, $html);}
function LlsetReplaceFormMsg2(&$html,&$rep,$msg,$act  = '',$tmp  = '',$hidden_para = '',$btn  = '　戻　る　',$act2 = '',$tmp2 = '',$hidden_para2 = '',$btn2 = '　追　加　',$auto_submit = FALSE){$rep['##MSG##']                 = $msg;
$rep['##P_ACT##']               = $act;
$rep['##P_TMP##']               = $tmp;
$rep['<!--##HIDDEN_PARA##-->']  = $hidden_para;
$rep['##BTN##']                 = $btn;
$rep['##P_ACT2##']              = $act2;
$rep['##P_TMP2##']              = $tmp2;
$rep['<!--##HIDDEN_PARA2##-->'] = $hidden_para2;
$rep['##BTN2##']                = $btn2;
$html = LlutlReplaceIf('IF_AUTO_SUBMIT', $auto_submit, $html);
$html = LlutlReplaceIf('IF_BTN2', TRUE, $html);}
function LlsetReplaceFormByList(&$html,$label,$lname){global $LLSET_LIST;
$htmls  = explode('<!--\('.$label.$lname.'\)-->', $html);
$html1  = '';
$cnt    = 1;
foreach ($LLSET_LIST[$lname] as $k => $v){$line = $htmls[1];
$lrep = array('('.$label.$lname.'_CNT)'	=> $cnt,'('.$label.$lname.'_KEY)'	=> $k,'('.$label.$lname.'_KEY_L)'	=> strtolower($k),'('.$label.$lname.'_KEY_U)'	=> strtoupper($k),'('.$label.$lname.'_VAL)'	=> $v,);
$html1 .= str_replace(array_keys($lrep), array_values($lrep), $line);
$cnt ++;}
$html = $htmls[0] . $html1 . $htmls[2];}
function LlsetReplaceFormByNum(&$html,$label,$num){$htmls  = explode('<!--##'.$label.'##-->', $html);
$html1  = '';
for ($cnt = 1; $cnt <= $num; $cnt ++){$line = $htmls[1];
$html1 .= str_replace(	array('(1)', '(01)'),array($cnt,   sprintf('%02d', $cnt)),$line);}
$html = $htmls[0] . $html1 . $htmls[2];}
function LlsetReplaceFormList(&$html,$tbl,$prefix,$suffix,$type,$label,$lrep = array()){global $LLSET_ALL;
$repstr = sizeof($lrep) > 0 ? $lrep[0] : '';
$lpre   = strlen($prefix);
$lsuf   = strlen($suffix);
$htmls  = explode('<!--##'.$label.'##-->', $html);
$html1  = '';
$tblfld = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
$idx    = 1;
foreach ($tblfld as $fid => $finfo){if ($lpre > 0 && strcmp(substr($fid, 0, $lpre), $prefix) != 0) { continue; }
if ($lsuf > 0 && strcmp(substr($fid, -1*$lsuf), $suffix) != 0) { continue; }
if ($finfo[LLSET_FI_TYPE] != $type) { continue; }
$line   = $htmls[1];
if ($repstr != '') { $line = str_replace($repstr, array_shift($lrep), $line); }
$html1 .= str_replace(	array('(%d)', '01'),array($idx,   sprintf('%02d', $idx)),$line);
$idx ++;}
$html = $htmls[0] . $html1 . $htmls[2];}
function LlsetReplaceGmapRecs(&$html,&$rep,&$recs,$label){global $LLSET_LIST_GMAP_JPN;
global $LLSET_LIST_GMAP_KEN;
$cnt      = 0;
$min_plat = 999;
$min_plng = 999;
$max_plat = -999;
$max_plng = -999;
$pzoom    = LLSET_GMAP_MAX_ZOOM_DEF;
$pken     = '';
$htmls    = explode('<!--##'.$label.'##-->', $html);
if (isset($htmls[1])){$html1 = '';
$num   = 0;
foreach ($recs as $rec){$num   ++;
$plat  = $rec['sel_gmap_plat'];
$plng  = $rec['sel_gmap_plng'];
$pzoom = $rec['sel_gmap_zoom'];
$pken  = $rec['ken'];
if ($plat <  -90 ||  90 < $plat) { continue; }
if ($plng < -180 || 180 < $plng) { continue; }
if ($min_plat > $plat) { $min_plat = $plat; }
if ($min_plng > $plng) { $min_plng = $plng; }
if ($max_plat < $plat) { $max_plat = $plat; }
if ($max_plng < $plng) { $max_plng = $plng; }
$line = LlutlStrCutTopCRLF($htmls[1]);
$lrep = array();
$lrep['##'.$label.'_GMAP_MARKER_LAT##']   = $plat;
$lrep['##'.$label.'_GMAP_MARKER_LNG##']   = $plng;
$lrep['##'.$label.'_GMAP_MARKER_TITLE##'] = isset($rec['gmap_marker_title']) ? $rec['gmap_marker_title'] : '';
$lrep['##'.$label.'_GMAP_MARKER_TYPE##']  = isset($rec['gmap_marker_type'])  ? $rec['gmap_marker_type']  : '';
$html1 .= str_replace(array_keys($lrep), array_values($lrep), $line);
$cnt ++;}
$html = $htmls[0] . $html1 . LlutlStrCutTopCRLF($htmls[2]);}
if ($cnt >= 2){$ksu = 8;
$ad_lat = abs(($max_plat - $min_plat) / $ksu);
$ad_lng = abs(($max_plng - $min_plng) / $ksu);
$min_plat = $min_plat - $ad_lat;
$max_plat = $max_plat + $ad_lat;
$min_plng = $min_plng - $ad_lng;
$max_plng = $max_plng + $ad_lng;}
$rep['##'.$label.'_GMAP_MARKER_CNT##']     = $cnt;
$rep['##'.$label.'_GMAP_MARKER_LAT_MIN##'] = $min_plat;
$rep['##'.$label.'_GMAP_MARKER_LNG_MIN##'] = $min_plng;
$rep['##'.$label.'_GMAP_MARKER_LAT_MAX##'] = $max_plat;
$rep['##'.$label.'_GMAP_MARKER_LNG_MAX##'] = $max_plng;
$rep['##'.$label.'_GMAP_MARKER_ZOOM##']    = $pzoom;
$rep['##GMAP_MAX_ZOOM##'] = LLSET_GMAP_MAX_ZOOM_DEF;
$rep['##GMAP_MIN_LAT##']  = isset($LLSET_LIST_GMAP_KEN[$pken]) ? $LLSET_LIST_GMAP_KEN[$pken][0] : $LLSET_LIST_GMAP_JPN[0];
$rep['##GMAP_MIN_LNG##']  = isset($LLSET_LIST_GMAP_KEN[$pken]) ? $LLSET_LIST_GMAP_KEN[$pken][1] : $LLSET_LIST_GMAP_JPN[1];
$rep['##GMAP_MAX_LAT##']  = isset($LLSET_LIST_GMAP_KEN[$pken]) ? $LLSET_LIST_GMAP_KEN[$pken][2] : $LLSET_LIST_GMAP_JPN[2];
$rep['##GMAP_MAX_LNG##']  = isset($LLSET_LIST_GMAP_KEN[$pken]) ? $LLSET_LIST_GMAP_KEN[$pken][3] : $LLSET_LIST_GMAP_JPN[3];
return $cnt;}
function LlsetAryToStr(&$ary,$list = array(),$joi = LLSET_MFLD_SEP_DISP){$str = array();
foreach ($ary as $key){$str[] = isset($list[$key]) ? $list[$key] : $key;}
return join($joi, $str);}
function LlsetCutStr($str,$lens,$add  = '..',$ladd = '',$strip_tags = TRUE){if ($strip_tags) { $str = strip_tags($str); }
$str = str_replace(array("\r","\n"), array('',''), $str);
if (is_array($lens)){$pos = 0;
$lines = array();
foreach ($lens as $len){$dstr = mb_substr($str, $pos, $len);
if ($dstr == null || $dstr == '') { break; }
$pos += mb_strlen($dstr);
$lines[] = $dstr;}
if ($ladd != ''){$nlens  = sizeof($lens);
$nlines = sizeof($lines);
for ($i = 0; $i < $nlens - $nlines; $i ++) { $lines[] = $ladd; }}
$rtn = LlutlHtmlEscapeTag2(join("\n", $lines));
return mb_strlen($str) > $pos ? $rtn.$add : $rtn;}
else{$len  = $lens;
$str  = str_replace(array("\r","\n"), array('',''), $str);
$dstr = mb_substr($str, 0, $len);
if (mb_strlen($str) > $len) { $dstr .= $add; }
return LlutlHtmlEscapeTag($dstr);}}
function LlsetCutStrAddWbr($str,$len,$int = 10,$add = '..',$strip_tags = TRUE){if ($strip_tags) { $str = strip_tags($str); }
$str = str_replace(array("\r","\n"), array('',''), $str);
$wstr = mb_substr($str, 0, $len);
$pos = 0;
$lines = array();
while (TRUE){$dstr = mb_substr($wstr, $pos, $int);
if ($dstr == null || $dstr == '') { break; }
$pos += mb_strlen($dstr);
$lines[] = LlutlHtmlEscapeTag2($dstr);}
$rtn = join(LlutlHtmlXhtmlTag('<wbr>'), $lines);
return mb_strlen($str) > $pos ? $rtn.$add : $rtn;}
function LlsetWorkNumber($reset = FALSE){$cookie_name = 'LLSET_WORK_NUMBER_'.fileinode(__FILE__);
$num = isset($_COOKIE[$cookie_name]) ? LlutlGetNum0($_COOKIE[$cookie_name]) : 0;
if ($num == 0 || $reset){$num = LlsetNewId('', 'work_number', time());
@setcookie($cookie_name, $num, 0);}
return $num;}
function LlsetIsRepeat($label,$reset = FALSE){$cookie_name = 'LLSET_IS_REPEAT_'.fileinode(__FILE__).'_'.$label;
if ($reset){@setcookie($cookie_name, 0, 0);
return FALSE;}
else{$is_exec = isset($_COOKIE[$cookie_name]) ? LlutlGetNum0($_COOKIE[$cookie_name]) : 0;
if ($is_exec == 0){@setcookie($cookie_name, 1, 0);
return FALSE;}
else{return TRUE;}}}
function LlsetSettingDownload($tbl,$is_multi,$def = array(),$limit_check = TRUE,$fname_prefix = ''){if ($fname_prefix == '') { $fname_prefix = MYDIRNM.'-'.$tbl; }
$dt    = LlutlDateTime(time());
$fname = sprintf('%s-%02d%02d%02d.txt', $fname_prefix, $dt['year']%100, $dt['mon'], $dt['day']);
if ($limit_check && LlsetIsLimit()) { exit; }
$flds   = array(LLSET_WB_VER,$tbl,);
$odata = join("\t", $flds)."\r\n";
$data = array();
if ($is_multi) { $data = LlsetSelectFlds($tbl); }
else           { $data = LlsetExistGetF($tbl) ? LlsetGetF($tbl) : $def; }
$odata .= LlutlAryToStr($data);
$len = strlen($odata);
header("Content-Disposition: attachment;filename=$fname\n\n");
header("Content-Length: ${len}");
header("Content-Type: application/octet-stream");
print($odata);
exit;}
function LlsetSettingUpload(&$html,&$rep,&$m_msg,&$m_err,&$m_hdn,$tbl,$is_multi,$limit_check = TRUE,$file_fid = 'i_up_file'){global $_FILES;
if (!LlsetIsUpdateMode($html, $rep, $m_msg, $m_err, $m_hdn)) { return; }
if ($limit_check && LlsetIsLimit()) { $m_msg = LlutlMsgf('limit01'); $m_err = TRUE; }
$file = array();
if (!$m_err){if (isset($_FILES[$file_fid]['name']) && strlen($_FILES[$file_fid]['name']) > 0){$file = file($_FILES[$file_fid]['tmp_name']);}
else{$m_msg = LlutlMsgf('setupload02');
$m_err = TRUE;}}
if (!$m_err){$header     = isset($file[0]) ? trim($file[0]) : '';
$whead1     = explode("\t", $header);
$whead2     = explode(' ', $whead1[0]);
$h_ver_name = isset($whead2[0]) ? trim($whead2[0]) : '';
$h_ver_num  = isset($whead2[1]) ?  LlutlGetNum0($whead2[1]) : 0;
$h_tbl      = isset($whead1[1]) ? trim($whead1[1]) : '';
if (strcmp(LLSET_WB_VER_NAME, $h_ver_name) != 0){$m_msg = LlutlMsgf('setupload03');
$m_err = TRUE;}
else if ($h_ver_num <= 0){$m_msg = LlutlMsgf('setupload03');
$m_err = TRUE;}
else if (LLSET_WB_VER_NUM < $h_ver_num){$m_msg = LlutlMsgf('setupload04');
$m_err = TRUE;}
else if (strcmp($tbl, $h_tbl) != 0){if ($h_ver_name == 'Inquiry' && $h_ver_num == 2.2 && $h_tbl == ''){;}
else{$m_msg = LlutlMsgf('setupload03');
$m_err = TRUE;}}}
if (!$m_err){$data = isset($file[1]) ? trim($file[1]) : '';
if ($is_multi){$c_data = LlsetSelectFlds($tbl);
if (sizeof($c_data) > 0){$m_msg = LlutlMsgf('setupload06');
$m_err = TRUE;}
else{$recs = LlutlStrToAry($data);
foreach ($recs as $rec){if (LlsetInsert1($tbl, '', $rec, LLTBF_POS_BOT) <= 0){$m_msg = LlutlMsgf('setupload05');
$m_err = TRUE;
break;}}}}
else{$setfld = LlutlStrToAry($data);
if (!LlsetUpdIns1($tbl, '', LLTBF_WILD_CARD, $setfld, 1)){$m_msg = LlutlMsgf('setupload05');
$m_err = TRUE;}}}
LlsetReplaceFormMsg($html, $rep, $m_msg, $m_err, $m_hdn);}
function LlsetImageUpload($tbl,$key,&$msg,$skey = '',$work = FALSE){global $LLSET_ALL;
$rtn = TRUE;
$tblfld = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
foreach ($tblfld as $fid => $finfo){$imgcopy  = isset($finfo[LLSET_FI_IMGCOPY]) ? $finfo[LLSET_FI_IMGCOPY] : '';
$img_wks  = explode(',', $imgcopy);
$fr_fid   = trim(array_shift($img_wks));
$img_trim = in_array('trim', $img_wks);
if ($finfo[LLSET_FI_TYPE] == 'img' && $fr_fid == ''){global $LLUTL_IMG_UPLOAD_INFO;
$img_del       = LlutlPara('d_'.$fid, '') == 1 ? TRUE : FALSE;
$img_cpy       = LlutlPara('c_'.$fid, '') == 1 ? TRUE : FALSE;
$img_type      = $finfo[LLSET_FI_ITYPE];
$img_size      = $finfo[LLSET_FI_ISIZE] * 1024;
$img_resize_wh = isset($finfo[LLSET_FI_RESIZE_WH]) ? $finfo[LLSET_FI_RESIZE_WH] : '';
$img_base      = LlsetGetImgBasePath($tbl, $key, $fid, $work);
$emsg          = '';
if ($img_cpy && $skey != ''){$img_src = LlsetGetImgBasePath($tbl, $skey, $fid);
LlutlImgCopy($img_src, $img_base);}
if (!LlutlImgUpload('f_'.$fid, $img_del, $img_type, $img_size, $img_base, $emsg)){$msg .= '<span style="color:#FF0000;">'.$emsg.'</span>'.LlutlHtmlXhtmlTag('<br>');
$rtn = FALSE;}
if ($LLUTL_IMG_UPLOAD_INFO['up'] && $img_resize_wh != '' && LlutlImageGDEnable()){$whs     = explode('x', $img_resize_wh);
$to_w    = $whs[0];
$to_h    = $whs[1];
$fr_path = $LLUTL_IMG_UPLOAD_INFO['ofile'];
$to_path = $fr_path;
LlutlImageGDCopyFile($fr_path, $to_path, $to_w, $to_h, $img_trim);}}}
foreach ($tblfld as $to_fid => $finfo){$imgcopy  = isset($finfo[LLSET_FI_IMGCOPY]) ? $finfo[LLSET_FI_IMGCOPY] : '';
$img_wks  = explode(',', $imgcopy);
$fr_fid   = trim(array_shift($img_wks));
$img_trim = in_array('trim', $img_wks);
if ($finfo[LLSET_FI_TYPE] == 'img' && $fr_fid != ''){$fr_path = LlsetGetImgPath($tbl, $key, $fr_fid);
LlsetDelImgFile($tbl, $key, $to_fid);
if ($fr_path != ''){$to_path = str_replace($fr_fid, $to_fid, $fr_path);
$whs     = explode('x', $finfo[LLSET_FI_RESIZE_WH]);
$to_w    = $whs[0];
$to_h    = $whs[1];
LlutlImageGDCopyFile($fr_path, $to_path, $to_w, $to_h, $img_trim);}}}
return $rtn;}
function LlsetGetImgPath($tbl,$key,$fld,$work = FALSE){$img_base = LlsetGetImgBasePath($tbl, $key, $fld, $work);
return LlutlImgSearchPath($img_base);}
function LlsetGetImgBasePath($tbl,$key,$fld,$work = FALSE){return LlsetGetImgBaseDir($tbl, $key, $work)."/$fld";}
$LLSET_SET_IMG_BASE_DIR = '';
function LlsetSetImgBaseDir($dir = ''){global $LLSET_SET_IMG_BASE_DIR;
$LLSET_SET_IMG_BASE_DIR = $dir;}
function LlsetGetImgBaseDir($tbl,$key,$work = FALSE){global $LLSET_SET_IMG_BASE_DIR;
if      ($work)							{ return LLUTL_DIR_WIMG."$tbl/$key"; }
else if ($LLSET_SET_IMG_BASE_DIR != '') { return $LLSET_SET_IMG_BASE_DIR."$tbl/$key"; }
else									{ return LLUTL_DIR_DIMG."$tbl/$key"; }}
function LlsetGetImgTag($tbl,$key,$fid,$max_w,$max_h,$alt,$add_opt = ''){$img_path = LlsetGetImgPath($tbl, $key, $fid);
return LlsetGetImgTagFromPath($img_path, $max_w, $max_h, $alt, $add_opt);}
$LLSET_GET_IMG_TAG_FROM_PATH = array();
function LlsetGetImgTagFromPath($img_path,$max_w,$max_h,$alt,$add_opt = '',$min_w = 0,$min_h = 0){global $LLSET_GET_IMG_TAG_FROM_PATH;
$LLSET_GET_IMG_TAG_FROM_PATH = array('path'   => $img_path,'width'  => 0,'height' => 0,);
if ($img_path == '') { return ''; }
$rtn  = '';
$fext = array_pop(explode('.', $img_path));
$tge  = LlutlHtmlXhtmlTag('>');
if (in_array($fext, array('jpg','gif','png'))){$sz_w = '';
$sz_h = '';
$info = LlutlImageGDGetInfo($img_path);
if ($max_w > 0 && $max_h > 0){$sz   = LlutlImageGDAdjustSize($info['width'], $info['height'], $max_w, $max_h);
$sz_w = $sz['width'];	if ($sz_w < $min_w) { $sz_w = $min_w; }
$sz_h = $sz['height'];	if ($sz_h < $min_h) { $sz_h = $min_h; }}
else{$sz_w = $info['width'];
$sz_h = $info['height'];}
$LLSET_GET_IMG_TAG_FROM_PATH['width']  = $sz_w;
$LLSET_GET_IMG_TAG_FROM_PATH['height'] = $sz_h;
$rtn = sprintf('<img src="%s" border="0" width="%s" height="%s" alt="%s" %s%s',$img_path, $sz_w, $sz_h,LlsetEscapeTagForIn($alt, 'text'),$add_opt, $tge);}
else{$link_str = LlsetGetFileLinkStrFromPath($img_path, $alt);
$rtn      = sprintf('<a href="%s" target="_blank">%s</a>', $img_path, $link_str);}
return $rtn;}
function LlsetGetFileLinkStrFromPath($img_path,$alt){global $LLSET_UPLOAD_IMG_FILE_LINK_STR;
if ($img_path == '') { return ''; }
$fext = array_pop(explode('.', $img_path));
return str_replace(array('#ALT#', '#FEXT#'),array($alt, strtoupper($fext)),isset($LLSET_UPLOAD_IMG_FILE_LINK_STR[$fext]) ? $LLSET_UPLOAD_IMG_FILE_LINK_STR[$fext] : $fext);}
function LlsetDelImg($tbl,$key,$work = FALSE){global $LLSET_ALL;
$dir = LlsetGetImgBaseDir($tbl, $key, $work);
LlutlRmDir($dir);}
function LlsetDelImgFile($tbl,$key,$fid,$work = FALSE){$img_base = LlsetGetImgBasePath($tbl, $key, $fid, $work);
$dname    = dirname($img_base);
$bname    = basename($img_base);
LlutlImgUnlink($dname, $bname);}
function LlsetImgPathAdjustFormTop($spath){$ltopdir = strlen(TOP_DIR);
if (strncmp(TOP_DIR, $spath, $ltopdir) == 0){return substr($spath, $ltopdir);}
return $spath;}
function LlsetAdjustOnum($tbl,$kval,$myrec = array()){global $LLSET_ALL;
$tblfld = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
$kfid   = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_KEY_FID];
$db     = LlsetDbConnect();
$rtbl   = LlsetDbTbl($tbl);
foreach ($tblfld as $fid => $finfo){if ($finfo[LLSET_FI_TYPE] == 'onum'){if (sizeof($myrec) == 0){$myrec = LldbSelect($db, $rtbl, "where ${kfid} = '${kval}'");}
$myonum = $myrec[$fid];
$grpfid = isset($finfo[LLSET_FI_ONUMGRP]) ? $finfo[LLSET_FI_ONUMGRP] : '';
$grpval = $grpfid != '' ? $myrec[$grpfid] : '';
$sql  = "where ${kfid} <> '${kval}' and ${fid} = '${myonum}'";
if ($grpfid != '') { $sql .= " and ${grpfid} = '${grpval}'"; }
$rec = LldbSelect($db, $rtbl, $sql);
if (isset($rec[$kfid])){$sql = "update ${rtbl} set ${fid} = ${fid} + 1 where ${kfid} <> '${kval}' and ${fid} >= '${myonum}'";
if ($grpfid != '') { $sql .= " and ${grpfid} = '${grpval}'"; }
LldbExec($db, LldbCodePhpToDb($sql), FALSE);}}}}
function LlsetNewOnum($dbtbl,$dbfid,$grpfid = '',$grpval = '',$minval = 1){$sql  = $grpfid != '' ? "where ${grpfid} = '${grpval}'" : '';
$onum = LlsetDbGetMax($dbtbl, $dbfid, $sql) + 1;
return $onum >= $minval ? $onum : $minval;}
function LlsetNewIdPath($fid){return LLSET_DIR_SDAT.'newid_'.$fid;}
function LlsetNewId($tbl,$fid,$minval = 1000){$path = LlsetNewIdPath($fid);
$lid = LlidfOpen($path);
$id  = LlidfGet($lid);
$id ++;
if ($id < $minval) { $id = $minval; }
$tbl1 = substr($tbl, 0, 1);
if ($tbl1 == 't'){$dat_max = LlsetDbGetMax($tbl, $fid);
if ($id <= $dat_max) { $id = $dat_max + 1; }}
else if ($tbl1 == 'f'){$dat_max = LlsetFileGetMax($tbl, $fid);
if ($id <= $dat_max) { $id = $dat_max + 1; }}
LlidfSet($lid, $id);
LlidfClose($lid);
return $id;}
$LLSET_DB_GET_REC = array();
function LlsetDbGetRec($tbl,$kfid,$key,$reset = FALSE){global $LLSET_DB_GET_REC;
if (!isset($LLSET_DB_GET_REC[$tbl]))        { $LLSET_DB_GET_REC[$tbl] = array(); }
if (!isset($LLSET_DB_GET_REC[$tbl][$kfid])) { $LLSET_DB_GET_REC[$tbl][$kfid] = array(); }
if ($reset || !isset($LLSET_DB_GET_REC[$tbl][$kfid][$key])){$db = LlsetDbConnect();
$LLSET_DB_GET_REC[$tbl][$kfid][$key] = LldbSelect($db, LlsetDbTbl($tbl), "where ${kfid} = '${key}'");}
return $LLSET_DB_GET_REC[$tbl][$kfid][$key];}
function LlsetDbDelRec($tbl,$kfid,$key){LlsetDelImg($tbl, $key);
$db = LlsetDbConnect();
LldbDelete($db, LlsetDbTbl($tbl), "where ${kfid} = '${key}'");}
function LlsetDbSetFld($tbl,$kfid,$kval,$sfid,$sval){$updfld = array();
if (TRUE){$sfids = is_array($sfid) ? $sfid : array($sfid);
$svals = is_array($sval) ? $sval : array($sval);
foreach ($sfids as $id){$updfld[$id] = array_shift($svals);}}
$db = LlsetDbConnect();
return LldbUpdate($db, LlsetDbTbl($tbl), "where ${kfid} = '${kval}'", $updfld);}
function LlsetDbGetMax($tbl,$fid,$sql = ''){$db   = LlsetDbConnect();
$flds = array("max($fid + 0) as max_id");
$recs = LldbSelectFlds($db, $flds, LlsetDbTbl($tbl), $sql, 0, 1);
return isset($recs[0]) && isset($recs[0]['max_id']) ? LlutlGetNum0($recs[0]['max_id']) : 0;}
function LlsetDbGetMin($tbl,$fid,$sql = ''){$db   = LlsetDbConnect();
$flds = array("min($fid + 0) as min_id");
$recs = LldbSelectFlds($db, $flds, LlsetDbTbl($tbl), $sql, 0, 1);
return isset($recs[0]) && isset($recs[0]['min_id']) ? LlutlGetNum0($recs[0]['min_id']) : 0;}
function LlsetFileGetMax($tbl,$fid,$sjkns = array()){$order = "fid=${fid};type=num;desc=Y";
$srecs = LlsetSelectFlds($tbl, 0, 1, $sjkns, $order);
$srec  = array_shift($srecs);
return isset($srec[$fid]) ? $srec[$fid] : 0;}
function LlsetFileGetMin($tbl,$fid,$sjkns = array()){$order = "fid=${fid};type=num;desc=N";
$srecs = LlsetSelectFlds($tbl, 0, 1, $sjkns, $order);
$srec  = array_shift($srecs);
return isset($srec[$fid]) ? $srec[$fid] : 0;}
$LLSET_DB = FALSE;
function LlsetDbConnect(){global $LLSET_DB;
if (!$LLSET_DB){$LLSET_DB = LldbConnect(LLUTL_DB_CONNECT_STR);}
return $LLSET_DB;}
$LLSET_DB = FALSE;
function LlsetDbClose(){global $LLSET_DB;
if ($LLSET_DB) { LldbClose($LLSET_DB); }
$LLSET_DB = FALSE;}
function LlsetDbTbl($tbl){return defined('SET_SITE_TBL') ? SET_SITE_TBL.$tbl : $tbl;}
function LlsetSessionSet($key,$val){LlutlSession3Set(LLUTL_SITE_ID.'_'.$key, $val);}
function LlsetSessionGet($key){return LlutlSession3Get(LLUTL_SITE_ID.'_'.$key);}
function LlsetParaGet($pgrp,$prefix,$fid,$def){if (LlutlIsPara($prefix.$fid)){if (LlutlIsParaArray($prefix.$fid)){return LlutlGPSet($pgrp, $fid, LlsetMfldAryToStr(LlutlParas($prefix.$fid)));}
else{return LlutlGPSet($pgrp, $fid, LlutlPara2($prefix.$fid, $def));}}
else{return LlutlGPGet($pgrp, $fid, $def);}}
function LlsetParaClear($pgrp,$fid = ''){LlutlGPClear($pgrp, $fid);}
function LlsetPwdToAngo($id,$pwd){return LlutlCryptBasic($id, $pwd);}
function LlsetNewPassword(){$tm  = time();
$wk  = LlutlCryptBasic(substr($tm, -2), $tm);
$cs  = unpack('C*', $wk);
$pwd = '';
$cnt = 0;
foreach ($cs as $cc){$c = chr($cc);
if (preg_match('/[0-9A-Za-z]/', $c)){$pwd .= $c;
$cnt ++;
if ($cnt >= 6) { break; }}}
return $pwd;}
function LlsetReadTemp($p_act,$p_tmp,$pre_rep = array()){$html = $p_tmp != '' ? LlutlGetTmp($p_tmp) : LlutlGetTmp($p_act);
if (defined('LLUTL_CHK_HTML_IF') && LLUTL_CHK_HTML_IF){$chkmsg = LlutlChkHtmlIfStat($html);
if ($chkmsg != '') { LlutlDebugWrite(LlutlHtmlEscapeTag($chkmsg).LlutlHtmlXhtmlTag('<br>')); }}
if (sizeof($pre_rep) > 0){$html = str_replace(array_keys($pre_rep), array_values($pre_rep), $html);}
LlsetRepeatFeild($html);
return $html;}
function LlsetReadTempExt(){global $LLUTL_GET_FILE_PATH;
return array_pop(explode('.', $LLUTL_GET_FILE_PATH));}
function LlsetRepeatFeild(&$html,$mpre = LLUTL_REP_MARK1,$msuf = LLUTL_REP_MARK2){global $LLSET_ALL;
$label = 'REPEAT_FIELD';
$wk1s  = explode($mpre.$label.$msuf, $html);
if (sizeof($wk1s) < 3) { return; }
$html = '';
$cnt  = 0;
foreach ($wk1s as $wk){$whtml = LlutlStrCutTopCRLF($wk);
if ($cnt % 2 == 0){$html .= $whtml;}
else{$para = LlsetGetParaFromHtml($whtml, $label.'_PARA');
$tbl  = $para['table'];
$fpre = isset($para['prefix']) ? $para['prefix'] : '';
$fsuf = isset($para['suffix']) ? $para['suffix'] : '';
$ftyp = isset($para['type'])   ? $para['type']   : '';
$max  = isset($para['max'])    ? $para['max']    : 0;
$html1  = '';
$tblfld = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
$lpre   = strlen($fpre);
$lsuf   = -1*strlen($fsuf);
$idx    = 1;
foreach ($tblfld as $fid => $finfo){if ($fpre != '' && strncmp($fid, $fpre, $lpre) != 0) { continue; }
if ($fsuf != '' && strcmp(substr($fid, $lsuf), $fsuf) != 0) { continue; }
if ($ftyp != '' && $finfo[LLSET_FI_TYPE] != $ftyp) { continue; }
$line = $whtml;
$html1 .= str_replace(array('{1}','{01}','{001}'), array($idx,sprintf('%02d',$idx),sprintf('%03d',$idx)), $line);
if ($max > 0 && $idx >= $max) { break; }
$idx ++;}
$html .= $html1;}
$cnt ++;}
return $html;}
function LlsetGetParaFromHtml(&$html,$label,$mpre = LLUTL_REP_MARK1,$msuf = LLUTL_REP_MARK2){$rtn = array();
$wk1s = explode($mpre.$label.$msuf, ' '.$html.' ');
if (sizeof($wk1s) != 3){LlutlDebugWrite("html parameter error : ${mpre}${label}${msuf}\n");
return $rtn;}
foreach (LlutlSplit(',', $wk1s[1]) as $pstr){$wk2s = LlutlSplit('=', $pstr);
$k = trim($wk2s[0]);
$v = isset($wk2s[1]) ? trim($wk2s[1]) : '';
$rtn[$k] = $v;}
$html = LlutlStrCutTopCRLF(substr($wk1s[0], 1).substr($wk1s[2], 0, -1));
return $rtn;}
function LlsetGetLabelParaFromHtml(&$html,$label,$mpre = LLUTL_REP_MARK1,$msuf = LLUTL_REP_MARK2){$new_html = '';
$paras    = array();
$cnt      = 0;
foreach (explode($mpre.$label.$msuf, $html) as $whtml){if ($cnt % 2 == 0){$new_html .= LlutlStrCutTopCRLF($whtml);}
else{$paras[] = $whtml;}
$cnt ++;}
$html = $new_html;
$rtn = array();
foreach ($paras as $para){$pary = array();
$lstr = '';
foreach (LlutlSplit(',', $para) as $pstr){$wk2s = LlutlSplit('=', $pstr);
$k = trim($wk2s[0]);
$v = isset($wk2s[1]) ? trim($wk2s[1]) : '';
if ($k == 'label'){$lstr = $v;}
else{$pary[$k] = $v;}}
$rtn[$lstr] = $pary;}
return $rtn;}
function LlsetIsExistBase(){return file_exists(LLUTL_DIR_BASE.'set-wbset.php.cgi');}
function LlsetReplaceCommon(&$html,&$rep,$global_para_link = array(),$chk_link = TRUE){global $INCHK_MSG;
global $SES_ADMIN;
global $BODY_ONLOAD;
global $HEAD_MENU;
$dt = LlutlDateTime(time());
$header_add = '';
$admin_url  = LLUTL_URL_ADMIN;
if (LLSET_LOGOUT_SEC > 0 && LlsetIsExistBase()){$sec = LLSET_LOGOUT_SEC;
$tge = LlutlHtmlXhtmlTag('>');
$header_add .= "<meta http-equiv=\"refresh\" content=\"${sec};url=${admin_url}?p_act=login\"${tge}";}
LlsetReplaceFileField($html, $rep, $global_para_link);
LlsetReplaceFileList($html);
$s0 = LlsetToS('6c2d746f6f6c2e6e6574');
if ($chk_link){$is_chk_rep = FALSE;
if (LlsetIsExistBase()){if (!LlsetIsSameCode('ll'.'ut'.'l_s'.'ite'.'_ti'.'tle', 'se'.'t_s'.'it'.'e_p'.'ay_c'.'ode') ||
!LlsetIsSameCode('se'.'t_s'.'ite'.'_u'.'se'.'r_n'.'ame', 'se'.'t_s'.'ite'.'_u'.'se'.'r_c'.'ode')){if (strpos(strip_tags($html), $s0) === FALSE) { $is_chk_rep = TRUE; }}}
else{if (strpos(strip_tags($html), $s0) === FALSE) { $is_chk_rep = TRUE; }}
if ($is_chk_rep){$s1 = LlsetToS('3c2f626f64793e');
$s2 = LlsetToS(	'3c646976207374796c653d22746578742d616c69'.
'676e3a63656e7465723b666f6e742d73697a653a'.
'313170783b6d617267696e2d626f74746f6d3a35'.
'70783b223e3c6120687265663d22687474703a2f'.
'2f6c2d746f6f6c2e6e65742f2220746172676574'.
'3d225f626c616e6b22207374796c653d22746578'.
'742d6465636f726174696f6e3a6e6f6e653b636f'.
'6c6f723a677261793b223e6c2d746f6f6c2e6e65'.
'743c2f613e3c2f6469763e');
$rep[$s1] = $s2."\n".$s1;}}
$rep['##INCHK_MSG##']     = $INCHK_MSG;
$rep['##URL_PTOP##']      = LLUTL_URL_PTOP;
$rep['##URL_PTOP2##']     = LLUTL_URL_PTOP2;
$rep['##URL_ADMIN##']     = $admin_url;
$rep['##MYACT##']         = isset($rep['##MYACT##'])   ? $rep['##MYACT##']   : MYACT;
$rep['##MYADMIN##']       = isset($rep['##MYADMIN##']) ? $rep['##MYADMIN##'] : LLUTL_MYADMIN;
$rep['##MYDIRNM##']       = MYDIRNM;
$rep['##USER_MYACT##']    = MYDIRNM.'.'.LLUTL_MYACT_EXT;
$rep['##HEAD_TODAY##']    = sprintf('%d/%d(%s)', $dt['mon'], $dt['day'], $dt['aday']);
$rep['##TODAY_YEAR##']    = $dt['year'];
$rep['##SITE_TITLE##']    = defined('LLUTL_SITE_TITLE') ? LLUTL_SITE_TITLE : '';
$rep['##TOOL_TITLE##']    = defined('LLSET_TOOL_TITLE') ? LLSET_TOOL_TITLE : '';
$rep['##BODY_ONLOAD##']   = $BODY_ONLOAD;
$rep['##REMOTE_ADDR##']   = LlutlRemoteAddr();
$rep['##WB_VER##']        = LLSET_WB_VER;
$rep['##HEADER_ADD##']    = $header_add;
$html = str_replace(array_keys($rep), array_values($rep), $html);
$html = LlutlReplaceIf('IF_PHP',        TRUE, $html);
$html = LlutlReplaceIf('IF_ADMIN',      $SES_ADMIN, $html);
$html = LlutlReplaceIf('IF_HEAD_MENU',  $HEAD_MENU, $html);
$html = LlutlReplaceIf('IF_INCHK_MSG',  $INCHK_MSG != '', $html);
$html = LlutlReplaceIf('IF_EXIST_BASE', LlsetIsExistBase(), $html);
if (defined('LLUTL_CHK_HTML_IF') && LLUTL_CHK_HTML_IF){$htmls = explode('##', $html);
if (sizeof($htmls) > 1){$cnt = 0;
LlutlDebugWrite(LlutlHtmlXhtmlTag('<br>'));
foreach ($htmls as $str){if ($cnt % 2 != 0) { LlutlDebugWrite("##$str##".LlutlHtmlXhtmlTag('<br>')); }
$cnt ++;}}}
if (LLUTL_HTTP_ENCODING != LLUTL_ENCODING){$charset = 'charset=';
if (LLUTL_HTTP_ENCODING == 'UTF-8') { $charset = 'charset=utf-8'; }
$html = preg_replace('/charset=shift_jis/i', $charset, $html);
$html = mb_convert_encoding($html, LLUTL_HTTP_ENCODING, LLUTL_ENCODING);}}
function LlsetIsSameCode($str,$code){$rcn = array('0','1','2','3','4','5','6','7','8','9');
$rca = array('g','h','i','j','k','l','m','n','o','p');
$w = @constant(strtoupper($str));
$wstr  = $w === NULL ? '' : $w;
$w = @constant(strtoupper($code));
$wcode = $w === NULL ? '' : pack('H*',str_replace($rca,$rcn,strrev($w)));
return strcmp($wstr, $wcode) == 0;}
$LLSET_SET_KEY_CODE = '';
function LlsetSetKeyCode(){}
function LlsetCodeFromUrl($url){if (substr($url, -1) == '/') { $url = substr($url, 0, -1); }
$wks  = explode('://', $url);

$wks  = explode('/', $wks[1]);
$pwd1 = array_shift($wks);
$pwd2 = array_pop($wks);
$salt = $pwd1;
return LlutlCryptOneTimePwd($pwd1, $salt).LlutlCryptOneTimePwd($pwd2, $salt);}
//   <!--##FILE_PARA##-->label=PAGE01,path=wbsys/page01/page.txt<!--##FILE_PARA##-->
//   <!--##FILE_PARA##-->label=PAGE01,path=wbsys/page01/page.txt,type=input<!--##FILE_PARA##-->
function LlsetReplaceFileField(&$html,&$rep,$global_para_link = array(),$mpre = LLUTL_REP_MARK1,$msuf = LLUTL_REP_MARK2){global $LLSET_ALL;
$label = 'FILE';
$paras = LlsetGetLabelParaFromHtml($html, $label.'_PARA');
foreach ($paras as $plab => $para){$flist     = LlsetReadFileList($para['path']);
$para_if   = isset($para['if'])   ? LlutlSplit(';', $para['if'])   : array();
$para_case = isset($para['case']) ? LlutlSplit(';', $para['case']) : array();
$para_type = isset($para['type']) ? $para['type'] : '';
$addlab    = "${label}_${plab}_";
if (isset($flist['recs'])){$rec  = $flist['recs'][0];
$hdns = array();
foreach ($flist['flds'] as $fid => $finfo){$ufid   = strtoupper($fid);
$replab = $addlab.$ufid;
$ftype  = isset($finfo[LLSET_FI_TYPE]) ? $finfo[LLSET_FI_TYPE] : '';
$list   = $ftype == 'sel' || $ftype == 'radio' || $ftype== 'check' ? $finfo[LLSET_FI_OPTS] : array();
$val    = isset($rec[$fid]) ? $rec[$fid] : '';
if ($ftype == 'sel' || $ftype == 'radio'){$str  = isset($list[$val]) ? $list[$val] : $val;
$rep['##'.$replab.'##']     = $val != '' ? $val : '　';
$rep['##'.$replab.'_STR##'] = $str != '' ? $str : '　';}
else if ($ftype == 'check'){$val = is_array($val) ? $val : LlsetMfldStrToAry($val);
$str = LlsetAryToStr($val, $list);
$rep['##'.$replab.'##']     = $str != '' ? $str : '　';
$rep['##'.$replab.'_STR##'] = $str != '' ? $str : '　';}
else if ($ftype == 'tarea'){$rep['##'.$replab.'##'] = LlutlHtmlEscapeCRLF2($val, '', LLSET_CMT_NOBR);}
else if ($ftype == 'datetime'){$rep['##'.$replab.'##'] = substr($val, 0, 10);
$idt = LlutlDateStrToAry($val);
$rep['##'.$replab.'_YEAR##'] = isset($idt[0]) ? sprintf('%d', $idt[0]) : '----';
$rep['##'.$replab.'_MON##']  = isset($idt[1]) ? sprintf('%d', $idt[1]) : '-';
$rep['##'.$replab.'_DAY##']  = isset($idt[2]) ? sprintf('%d', $idt[2]) : '-';
$rep['##'.$replab.'_MON2##'] = isset($idt[1]) ? sprintf('%02d', $idt[1]) : '--';
$rep['##'.$replab.'_DAY2##'] = isset($idt[2]) ? sprintf('%02d', $idt[2]) : '--';}
else if ($ftype == 'int' || $ftype == 'img' || $ftype == 'html'){$rep['##'.$replab.'##'] = $val;}
else if ($ftype == ''){$rep['##'.$replab.'##'] = $val;}
else{$rep['##'.$replab.'##'] = LlutlHtmlEscapeTag2($val);}
if (in_array($fid, $para_if)){$html = LlutlReplaceIf('IF_'.$replab, $val != '', $html);}
if (in_array($fid, $para_case)){$html = LlutlReplaceCase2('CASE_'.$replab, $val, $html);}
if ($para_type == 'input'){$def  = isset($rec[$fid]) ? $rec[$fid] : '';
$ival = isset($global_para_link[$plab])
? LlsetParaGet($global_para_link[$plab], 'i_', $fid, $def)
: LlutlPara2('i_'.$fid, $def);
$hdns['i_'.$fid] = $ival;
if ($ftype == 'radio'){LlsetReplaceSlist($html, $fid, $ival, $list, TRUE, $addlab);
$html = LlutlReplaceIf('IF_'.$replab, sizeof($list) > 0, $html);
$rep['##I_'.$replab.'##'] = LlsetEscapeTagForIn($ival, 'text');}
else if ($ftype == 'sel'){$rep['##OPT_'.$replab.'##'] = LlsetGetSelOpt($list, $ival);
$html = LlutlReplaceIf('IF_'.$replab, sizeof($list) > 0, $html);
$rep['##I_'.$replab.'##'] = LlsetEscapeTagForIn($ival, 'text');}
else if ($ftype == 'check'){$ival = is_array($ival) ? $ival : LlsetMfldStrToAry($ival);
LlsetReplaceSlist($html, $fid, $ival, $list, TRUE, $addlab);
$html = LlutlReplaceIf('IF_'.$replab, sizeof($list) > 0, $html);}
else if ($ftype == 'img'){;}
else{$rep['##I_'.$replab.'##'] = LlsetEscapeTagForIn($ival, $finfo[LLSET_FI_TYPE]);}}}
$rep['<!--##'.$addlab.'HIDDEN_PARA##-->'] = LlsetSetHiddenPara($hdns);}
else{foreach ($flist['data'][0] as $fid => $val){$ufid   = strtoupper($fid);
$replab = "${label}_${plab}_${ufid}";
$ftype  = isset($flist['ftype'][$fid]) ? $flist['ftype'][$fid] : '';
if ($ftype == 'sel' || $ftype == 'radio'){$list = $flist['list'][$fid];
$str  = isset($list[$val]) ? $list[$val] : $val;
$rep['##'.$replab.'##']     = $val != '' ? $val : '　';
$rep['##'.$replab.'_STR##'] = $str != '' ? $str : '　';}
else if ($ftype == 'img'){$rep['##'.$replab.'##']        = $val != '' ? $val : '　';
$rep['##'.$replab.'_PATH##']   = isset($flist['data'][0]["${fid}_path"])   ? $flist['data'][0]["${fid}_path"]   : '';
$rep['##'.$replab.'_WIDTH##']  = isset($flist['data'][0]["${fid}_width"])  ? $flist['data'][0]["${fid}_width"]  : '';
$rep['##'.$replab.'_HEIGHT##'] = isset($flist['data'][0]["${fid}_height"]) ? $flist['data'][0]["${fid}_height"] : '';}
else if ($ftype == 'tarea'){$rep['##'.$replab.'##'] = LlutlHtmlEscapeCRLF2($val, '', LLSET_CMT_NOBR);}
else if ($ftype == ''){;}
else if (substr($fid,-5) == '_time'){$rep['##'.$replab.'##'] = substr($val, 0, 10);
$idt = LlutlDateStrToAry($val);
$rep['##'.$replab.'_YEAR##'] = isset($idt[0]) ? sprintf('%d', $idt[0]) : '----';
$rep['##'.$replab.'_MON##']  = isset($idt[1]) ? sprintf('%d', $idt[1]) : '-';
$rep['##'.$replab.'_DAY##']  = isset($idt[2]) ? sprintf('%d', $idt[2]) : '-';
$rep['##'.$replab.'_MON2##'] = isset($idt[1]) ? sprintf('%02d', $idt[1]) : '--';
$rep['##'.$replab.'_DAY2##'] = isset($idt[2]) ? sprintf('%02d', $idt[2]) : '--';}
else{$rep['##'.$replab.'##'] = LlutlHtmlEscapeTag2($val);}
if (in_array($fid, $para_if)){$html = LlutlReplaceIf('IF_'.$replab, $val != '', $html);}
if (in_array($fid, $para_case)){$html = LlutlReplaceCase2('CASE_'.$replab, $val, $html);}}}}}
//   <!--##FLIST##-->
//   <!--##FLIST_PARA##-->path=wbsys/flist/info01.txt,if=x;x;..,case=x;x;..,if_new=x;x;...<!--##FLIST_PARA##-->
//   <!--##FLIST##-->
//   <!--##FLIST##-->
//   <!--##FLIST_PARA##-->path=wbsys/flist/info01.txt,type=input<!--##FLIST_PARA##-->
//   <!--##FLIST##-->
function LlsetReplaceFileList(&$html,$mpre = LLUTL_REP_MARK1,$msuf = LLUTL_REP_MARK2){global $LLSET_ALL;
$label = 'FLIST';
$wk1s  = explode($mpre.$label.$msuf, $html);
if (sizeof($wk1s) < 3) { return; }
$paths = array();
$html = '';
$cnt  = 0;
foreach ($wk1s as $wk){$whtml = LlutlStrCutTopCRLF($wk);
if ($cnt % 2 == 0){$html .= $whtml;}
else{$para          = LlsetGetParaFromHtml($whtml, $label.'_PARA');
$flist         = LlsetReadFileList($para['path']);
$para_if       = isset($para['if'])     ? LlutlSplit(';', $para['if'])     : array();
$para_case     = isset($para['case'])   ? LlutlSplit(';', $para['case'])   : array();
$para_if_new   = isset($para['if_new']) ? LlutlSplit(';', $para['if_new']) : array();
$para_type     = isset($para['type'])   ? $para['type'] : '';
$img_path_base = dirname($para['path']).'/'.LLUTL_DIRNM_DIMG.'/';
if (isset($flist['recs'])){$html1 = '';
$lcnt  = 0;
foreach ($flist['recs'] as $rec){$line = $whtml;
$lrep = array();
$lrep[LLUTL_REP_MARK.$label.'_CNT'.LLUTL_REP_MARK] = $lcnt + 1;
foreach ($flist['flds'] as $fid => $finfo){$ufid     = strtoupper($fid);
$replab   = $label.'_'.$ufid;
$ftype    = isset($finfo[LLSET_FI_TYPE]) ? $finfo[LLSET_FI_TYPE] : '';
$list     = $ftype == 'sel' || $ftype == 'radio' || $ftype== 'check' ? $finfo[LLSET_FI_OPTS] : array();
$val      = isset($rec[$fid]) ? $rec[$fid] : '';
$img_path = '';
if ($ftype == 'sel' || $ftype == 'radio'){$str = isset($list[$val]) ? $list[$val] : $val;
$lrep['##'.$replab.'##']     = $val != '' ? $val : '　';
$lrep['##'.$replab.'_STR##'] = $str != '' ? $str : '　';}
else if ($ftype == 'check'){$val = is_array($val) ? $val : LlsetMfldStrToAry($val);
$str = LlsetAryToStr($val, $list);
$lrep['##'.$replab.'##']     = $str != '' ? $str : '　';
$lrep['##'.$replab.'_STR##'] = $str != '' ? $str : '　';}
else if ($ftype == 'tarea'){$lrep['##'.$replab.'##'] = LlutlHtmlEscapeCRLF2($val, '', LLSET_CMT_NOBR);}
else if ($ftype == 'datetime'){$lrep['##'.$replab.'##'] = substr($val, 0, 10);
$idt = LlutlDateStrToAry($val);
$lrep['##'.$replab.'_YEAR##'] = isset($idt[0]) ? sprintf('%d', $idt[0]) : '----';
$lrep['##'.$replab.'_MON##']  = isset($idt[1]) ? sprintf('%d', $idt[1]) : '-';
$lrep['##'.$replab.'_DAY##']  = isset($idt[2]) ? sprintf('%d', $idt[2]) : '-';
$lrep['##'.$replab.'_MON2##'] = isset($idt[1]) ? sprintf('%02d', $idt[1]) : '--';
$lrep['##'.$replab.'_DAY2##'] = isset($idt[2]) ? sprintf('%02d', $idt[2]) : '--';}
else if ($ftype == 'img'){$lrep['##'.$replab.'##'] = $val;
$img_path = isset($rec["${fid}_path"]) ? $rec["${fid}_path"] : '';
$lrep['##'.$replab.'_PATH##']     = $img_path;
$lrep['##'.$replab.'_TYPE##']     = isset($rec["${fid}_type"])   ? $rec["${fid}_type"]   : '';
$lrep['##'.$replab.'_WIDTH##']    = isset($rec["${fid}_width"])  ? $rec["${fid}_width"]  : '';
$lrep['##'.$replab.'_HEIGHT##']   = isset($rec["${fid}_height"]) ? $rec["${fid}_height"] : '';
$lrep['##'.$replab.'_LINK_STR##'] = LlsetGetFileLinkStrFromPath($img_path, $val);}
else if ($ftype == 'int' || $ftype == 'html'){$lrep['##'.$replab.'##'] = $val;}
else if ($ftype == ''){$lrep['##'.$replab.'##'] = $val;}
else{$lrep['##'.$replab.'##'] = LlutlHtmlEscapeTag2($val);}
if (in_array($fid, $para_if)){$is_val = $ftype == 'img' ? $img_path != '' : $val != '';
$line = LlutlReplaceIf('IF_'.$replab, $is_val, $line);}
if (in_array($fid, $para_case)){$line = LlutlReplaceCase2('CASE_'.$replab, $val, $line);}
if (isset($para_if_new[1]) &&
$fid == $para_if_new[0]){$line = LlutlReplaceIf('IF_NEW_'.$label, LlsetIsNew($val, $para_if_new[1]), $line);}
if ($para_type == 'input'){$ival = LlutlIsParaArray('i_'.$fid) ? LlutlParas('i_'.$fid)
: LlutlPara2('i_'.$fid, isset($rec[$fid]) ? $rec[$fid] : '');
if ($ftype == 'radio'){LlsetReplaceSlist($line, $fid, $ival, $list, TRUE);
$line = LlutlReplaceIf('IF_'.$replab, sizeof($list) > 0, $line);
$lrep['##I_'.$ufid.'##'] = LlsetEscapeTagForIn($ival, 'text');}
else if ($ftype == 'sel'){$lrep['##OPT_'.$ufid.'##'] = LlsetGetSelOpt($list, $ival);
$line = LlutlReplaceIf('IF_'.$replab, sizeof($list) > 0, $line);
$lrep['##I_'.$ufid.'##'] = LlsetEscapeTagForIn($ival, 'text');}
else if ($ftype == 'check'){$ival = is_array($ival) ? $ival : LlsetMfldStrToAry($ival);
LlsetReplaceSlist($line, $fid, $ival, $list, TRUE);
$line = LlutlReplaceIf('IF_'.$replab, sizeof($list) > 0, $line);}
else if ($ftype == 'img'){;}
else{$lrep['##I_'.$ufid.'##'] = LlsetEscapeTagForIn($ival, $finfo[LLSET_FI_TYPE]);}}}
$html1 .= str_replace(array_keys($lrep), array_values($lrep), $line);
$lcnt ++;}
$html .= $html1;
$paths[$para['path']] = $lcnt;}
else{$html1 = '';
$lcnt  = 0;
foreach ($flist['data'] as $flds){$line = $whtml;
$lrep = array();
$lrep[LLUTL_REP_MARK.$label.'_CNT'.LLUTL_REP_MARK] = $lcnt + 1;
foreach ($flds as $fid => $val){$ufid   = strtoupper($fid);
$replab = $label.'_'.$ufid;
$ftype  = isset($flist['ftype'][$fid]) ? $flist['ftype'][$fid] : '';
if ($ftype == 'sel' || $ftype == 'radio'){$list = $flist['list'][$fid];
$str  = isset($list[$val]) ? $list[$val] : $val;
$lrep['##'.$replab.'##']     = $val != '' ? $val : '　';
$lrep['##'.$replab.'_STR##'] = $str != '' ? $str : '　';}
else if ($ftype == 'img'){$lrep['##'.$replab.'##']        = $val != '' ? $val : '　';
$lrep['##'.$replab.'_PATH##']   = isset($flds["${fid}_path"])   ? $flds["${fid}_path"]   : '';
$lrep['##'.$replab.'_WIDTH##']  = isset($flds["${fid}_width"])  ? $flds["${fid}_width"]  : '';
$lrep['##'.$replab.'_HEIGHT##'] = isset($flds["${fid}_height"]) ? $flds["${fid}_height"] : '';}
else if ($ftype == 'tarea'){$lrep['##'.$replab.'##'] = LlutlHtmlEscapeCRLF2($val, '', LLSET_CMT_NOBR);}
else if ($ftype == ''){;}
else if (substr($fid,-5) == '_time'){$lrep['##'.$replab.'##'] = substr($val, 0, 10);
$idt = LlutlDateStrToAry($val);
$lrep['##'.$replab.'_YEAR##'] = isset($idt[0]) ? sprintf('%d', $idt[0]) : '----';
$lrep['##'.$replab.'_MON##']  = isset($idt[1]) ? sprintf('%d', $idt[1]) : '-';
$lrep['##'.$replab.'_DAY##']  = isset($idt[2]) ? sprintf('%d', $idt[2]) : '-';
$lrep['##'.$replab.'_MON2##'] = isset($idt[1]) ? sprintf('%02d', $idt[1]) : '--';
$lrep['##'.$replab.'_DAY2##'] = isset($idt[2]) ? sprintf('%02d', $idt[2]) : '--';}
else{$lrep['##'.$replab.'##'] = LlutlHtmlEscapeTag2($val);}
if (in_array($fid, $para_if)){$line = LlutlReplaceIf('IF_'.$replab, $val != '', $line);}
if (in_array($fid, $para_case)){$line = LlutlReplaceCase2('CASE_'.$replab, $val, $line);}
if (isset($para_if_new[1]) && $fid == $para_if_new[0]){$line = LlutlReplaceIf('IF_NEW_'.$label, LlsetIsNew($val, $para_if_new[1]), $line);}}
$html1 .= str_replace(array_keys($lrep), array_values($lrep), $line);
$lcnt ++;}
$html .= $html1;}}
$cnt ++;}
foreach ($paths as $path => $lcnt){$html = LlutlReplaceIf("IF_FLIST_NOREC:${path}", $lcnt <= 0, $html);}}
function LlsetExecRemoteCall($dir,$fnc,$p1 = '',$p2 = '',$p3 = ''){$cdir = LLUTL_DIR_WB.$dir;
if (!is_dir($cdir)){print("Tool directory not found : ${cdir}");
exit;}
$url = LlutlPara('p_url', '');
if ($url == ''){print("Set 'p_url' parameter in the previous html");
exit;}
$wurls = explode('/', array_shift(explode('?', $url)));
$nsz   = sizeof($wurls);
$wurls[$nsz - 2] = $dir;
$wurl = join('/', $wurls);
$pp1  = $p1 != '' ? '&p1='.rawurlencode($p1) : '';
$pp2  = $p2 != '' ? '&p2='.rawurlencode($p2) : '';
$pp3  = $p3 != '' ? '&p3='.rawurlencode($p3) : '';
$exec_url = "${wurl}?p_act=${fnc}${pp1}${pp2}${pp3}";
$rtn = join('', file($exec_url));
if (substr($rtn, 0, 2) == 'OK') { return TRUE; }
print("Remote call error : ${dir} : ${fnc} : ${rtn}\n");
return FALSE;}
$LLSET_IS_NEW_TM = 0;
function LlsetIsNew($date_str,$new_days){global $LLSET_IS_NEW_TM;
if ($LLSET_IS_NEW_TM <= 0){$dt = LlutlDateTime(time());
$LLSET_IS_NEW_TM = LlutlUnixTime($dt['year'], $dt['mon'], $dt['day'], 0, 0, 0);}
$new_day_sec = LlutlGetNum0($new_days) * 86400;
$ymd = preg_split('/(-| |:)/', $date_str);
if (!isset($ymd[2])) { return FALSE; }
$tm = LlutlUnixTime($ymd[0], $ymd[1], $ymd[2], 0, 0, 0);
return $tm >= $LLSET_IS_NEW_TM - $new_day_sec;}
function LlsetAddImageFieldsForWriteFile(&$vals,$img_path,$fid){$img_exts   = array('jpg','jpeg','gif','png');
$img_ext    = '';
$img_width  = '';
$img_height = '';
if ($img_path != ''){$img_ext = LlutlImgGetType2Base($img_path);
if (in_array($img_ext, $img_exts)){$img_info   = LlutlImageGDGetInfo($img_path);
$img_width  = $img_info['width'];
$img_height = $img_info['height'];}}
$vals[$fid.'_path']   = LlsetImgPathAdjustFormTop($img_path);
$vals[$fid.'_ext']    = $img_ext;
$vals[$fid.'_width']  = $img_width;
$vals[$fid.'_height'] = $img_height;}
function LlsetPathFileListTable($tbl,$dirnm = MYDIRNM){$path = LLUTL_DIR_FLIST."${dirnm}-${tbl}.cgi";
LlutlMkDir(dirname($path));
return $path;}
function LlsetWriteFileListTable($tbl,$addnm = ''){global $LLSET_ALL;
$path = LlsetPathFileListTable($addnm == '' ? $tbl : $tbl.'-'.$addnm);
$tblfld = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
$kfid   = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_KEY_FID];
$f      = LlsetGetF($tbl, TRUE);
$key    = $f[LLSET_KEY_FID];
$info = array('ftype'	=> array(),'data'	=> array(),'list'	=> array(),);
$vals = array();
foreach ($tblfld as $fid => $finfo){$ftype = isset($tblfld[$fid]) ? $tblfld[$fid][LLSET_FI_TYPE] : '';
$info['ftype'][$fid] = $ftype;
if ($ftype == 'sel' || $ftype == 'radio' || $ftype == 'check'){$info['list'][$fid] = $list = LlsetGetList($tbl, $fid);}
$vals[$fid] = $f[$fid];
if ($ftype == 'img'){$img_path = LlsetGetImgPath($tbl, $key, $fid);
LlsetAddImageFieldsForWriteFile($vals, $img_path, $fid);}}
$info['data'][] = $vals;
LlsetWriteFileList($path, $info);}
function LlsetWriteFileListTableRecs($tbl,$offset = 0,$nline = 0,$jkns = array(),$order = array(),$addnm = ''){global $LLSET_ALL;
$path = LlsetPathFileListTable($addnm == '' ? $tbl : $tbl.'-'.$addnm);
$tblfld = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
$info = array('ftype'	=> array(),'data'	=> array(),'list'	=> array(),);
foreach ($tblfld as $fid => $finfo){$ftype = isset($tblfld[$fid]) ? $tblfld[$fid][LLSET_FI_TYPE] : '';
$info['ftype'][$fid] = $ftype;
if ($ftype == 'sel' || $ftype == 'radio' || $ftype == 'check'){$info['list'][$fid] = $list = LlsetGetList($tbl, $fid);}}
$recs = LlsetSelectFlds($tbl, $offset, $nline, $jkns, $order);
$cnt  = 0;
foreach ($recs as $key => $rec){$vals = array();
foreach ($rec as $fid => $val){$ftype = isset($tblfld[$fid]) ? $tblfld[$fid][LLSET_FI_TYPE] : '';
$vals[$fid] = $val;
if ($ftype == 'img'){$img_path = LlsetGetImgPath($tbl, $key, $fid);
LlsetAddImageFieldsForWriteFile($vals, $img_path, $fid);}}
$info['data'][] = $vals;
$cnt ++;}
LlsetWriteFileList($path, $info);}
function LlsetWriteFileListTableDbRecs($tbl,$sql,$offset = 0,$nline = 0,$addnm = ''){global $LLSET_ALL;
$path = LlsetPathFileListTable($addnm == '' ? $tbl : $tbl.'-'.$addnm);
$tblfld = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
$kfid   = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_KEY_FID];
$info = array('ftype'	=> array(),'data'	=> array(),'list'	=> array(),);
foreach ($tblfld as $fid => $finfo){$ftype = isset($tblfld[$fid]) ? $tblfld[$fid][LLSET_FI_TYPE] : '';
$info['ftype'][$fid] = $ftype;
if ($ftype == 'sel' || $ftype == 'radio' || $ftype == 'check'){$info['list'][$fid] = $list = LlsetGetList($tbl, $fid);}}
$db    = LlsetDbConnect();
$sflds = array_keys($tblfld);
$recs  = LldbSelectFlds($db, $sflds, LlsetDbTbl($tbl), $sql, $offset, $nline);
$cnt  = 0;
foreach ($recs as $rec){$key = $rec[$kfid];
$vals = array();
foreach ($sflds as $fid){$ftype = isset($tblfld[$fid]) ? $tblfld[$fid][LLSET_FI_TYPE] : '';
$vals[$fid] = $rec[$fid];
if ($ftype == 'img'){$img_path = LlsetGetImgPath($tbl, $key, $fid);
LlsetAddImageFieldsForWriteFile($vals, $img_path, $fid);}}
$info['data'][] = $vals;
$cnt ++;}
LlsetWriteFileList($path, $info);}
function LlsetPutFileList($tid,$tflds,&$recs,$rtn_data = FALSE){$tids  = explode(':', $tid);
$dirnm = $tids[0];
$tblnm = $tids[1];
$tbls  = explode('-', $tblnm);
$tbl   = $tbls[0];
$addnm = isset($tbls[1]) ? $tbls[1] : '';
$path = LlsetPathFileListTable($tblnm, $dirnm);
$flist = array('flds'	=> $tflds,'list'	=> array(),'recs'	=> $recs,);
foreach ($tflds as $fid => $finfo){if (in_array($finfo[LLSET_FI_TYPE], array('sel','radio','check'))){$list = LlsetGetList($tbl, $fid, FALSE, $finfo);
$flist['flds'][$fid][LLSET_FI_OPTS] = $list;}}
if ($rtn_data){return $flist;}
else{$str = serialize($flist);
return file_put_contents($path, $str);}}
function LlsetWriteFileList($path,$info){$str = serialize($info);
file_put_contents($path, $str);}
function LlsetWriteFileList2($flist,$recs){$wlist = $flist;
foreach ($flist['flds'] as $fid => $finfo){if (in_array($finfo[LLSET_FI_TYPE], array('sel','radio','check'))){$tbl = basename($flist['path']);
$list = LlsetGetList($tbl, $fid, FALSE, $finfo);
$wlist['flds'][$fid][LLSET_FI_OPTS] = $list;}}
$wlist['recs'] = $recs;
$str = serialize($wlist);
file_put_contents($flist['path'], $str);}
function LlsetAddImagePathToRecs(&$recs,$tbl,$kfid,$img_fids){global $LLSET_IMG_FILE_TYPE;
$wrecs = array();
$len_top_dir = strlen(TOP_DIR);
foreach ($recs as $rec){$key = $rec[$kfid];
foreach ($img_fids as $fid => $is_img){$path = LlsetGetImgPath($tbl, $key, $fid);
if ($path != ''){$fext = array_pop(explode('.', $path));
$rec["${fid}_path"] = substr($path, $len_top_dir);
$rec["${fid}_type"] = isset($LLSET_IMG_FILE_TYPE[$fext]) ? $LLSET_IMG_FILE_TYPE[$fext] : strtoupper($fext);
if ($is_img){$img_info = LlutlImageGDGetInfo($path);
$rec["${fid}_width"]  = $img_info['width'];
$rec["${fid}_height"] = $img_info['height'];}}}
$wrecs[] = $rec;}
return $wrecs;}
function LlsetGetImgPathForFileList2($tbl,$key,$fid){$img_path = LlsetGetImgPath($tbl, $key, 'imgl01');
if ($img_path != ''){$ws = explode('/'.LLUTL_DIRNM_DIMG.'/', $img_path);
$img_path = isset($ws[1]) ? LLUTL_DIRNM_DIMG.'/'.$ws[1] : '';}
return $img_path;}
function LlsetGetFileList($tid){$tids = explode(':', $tid);
return LlsetReadFileList(LlsetPathFileListTable($tids[1], $tids[0]));}
function LlsetReadFileList($path){$rtn = array();
if (LlutlFileExist($path)){$str = file_get_contents($path);
$rtn = unserialize($str);}
else if (LlutlFileExist(TOP_DIR.$path)){$str = file_get_contents(TOP_DIR.$path);
$rtn = unserialize($str);}
else{if (LlsetIsExistBase()){LlutlLog(__FILE__, __LINE__, sprintf("LlsetReadFileList(%s) open failed.", $path));}}
return $rtn;}
function LlsetGetOrder($label){global $LLSET_ORDER_DEF;
return $LLSET_ORDER_DEF[$label];}
function LlsetGetNline($label){global $LLSET_NLINE_DEF;
return $LLSET_NLINE_DEF[$label];}
$LLSET_GET_LIST_VALS = array();
function LlsetGetList($tbl,$fid,$check_disp = FALSE,$finfo = array()){global $LLSET_ALL;
global $LLSET_GET_LIST_VALS;
$key = "${tbl}:${fid}:${check_disp}";
if (isset($LLSET_GET_LIST_VALS[$key])) { return $LLSET_GET_LIST_VALS[$key]; }
if (sizeof($finfo) <= 0) { $finfo = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD][$fid]; }
$list = $finfo[LLSET_FI_OPTS];
if (is_array($list)) { return $list; }
$list_label = $list;
$list = array();
$wks  = explode(':', $list_label);
if (isset($wks[1])){$tbl  = $wks[0];
$fid  = $wks[1];
$list = LlsetGetListFromTblFld($tbl, $fid, $check_disp);}
$LLSET_GET_LIST_VALS[$key] = $list;
return $LLSET_GET_LIST_VALS[$key];}
function LlsetHierarchyListCnvForRegist($wlist,$lcut = 8,$joint = ' - '){$list = array();
ksort($wlist);
$stac = 0;
$l_cp = 0;
$vs   = array();
$ls   = array();
foreach ($wlist as $k => $v){$l = strlen($k);
if ($l_cp > 0){if      ($l_cp <  $l) { $stac ++; }
else if ($l_cp == $l) { ; }
else{for ($i = 0; $i <= $stac; $i ++){if ($ls[$i] >= $l){$stac = $i;
break;}}}}
$vs[$stac] = $v;
$ls[$stac] = $l;
$vstr = '';
for ($i = 0; $i < $stac; $i ++){$wv = LlsetCutStr($vs[$i], $lcut);
$vstr .= $wv . $joint;}
$vstr .= $v;
$list[$k] = $vstr;
$l_cp = $l;}
return $list;}
function LlsetGetListFromTblFld($tbl,$fid,$check_disp = FALSE){$list = array();
foreach (LlsetGetListArrayFromTable($tbl, $fid) as $fld){$nfld = sizeof($fld);
$code = $fld[0];
$name = $fld[1];
$disp = isset($fld[2]) ? $fld[2] : LLSET_DISP_ON;
if ($check_disp && $disp == LLSET_DISP_OFF) { continue; }
$list[$code] = $name;}
return $list;}
function LlsetGetListArrayFromTable($tbl,$fid){$list = array();
$f    = LlsetGetF($tbl);
if (isset($f[$fid])){$val  = $f[$fid];
foreach (LlutlSplit("\n", $val) as $line){$line = trim($line);
if ($line == '' || substr($line, 0, 1) == '#') { continue; }
$flds = array();
foreach (LlutlSplit(',', $line) as $fld){$flds[] = trim($fld);}
$list[] = $flds;}}
return $list;}
function LlsetLoginSessionSet($val,$ses_label = LLSET_LOGIN_SESSION_ADMIN){LlutlSession3Set($ses_label, $val);}
function LlsetLoginSessionGet($ses_label = LLSET_LOGIN_SESSION_ADMIN){return LlutlSession3Get($ses_label);}
function LlsetLoginCheckJump($base){if (!LlsetIsExistBase()) { return ''; }
if (LlsetIsLogin()) { return ''; }
$jump_url = LLUTL_URL_ADMIN;
if (!$base){header("Location: ${jump_url}");
exit;}
$f = LlsetGetFetc();	$is_fetc = isset($f['admin_mail']) && $f['admin_mail'] != '';
$f = LlsetGetFidp();	$is_fidp = isset($f['id'])         && $f['id']         != '';
if      (!$is_fetc && !$is_fidp) { return LlutlMsgf('init0001'); }
else if (!$is_fetc)				 { return LlutlMsgf('init0002'); }
else if (!$is_fidp)				 { return LlutlMsgf('init0003'); }
if (LlutlPara('p_from_login', '') == '1'){LlsetLogout();
$i_id    = LlutlPara('p_login_id', '');
$i_pwd   = LlutlPara('p_login_pwd', '');
$i_pwd_a = $i_pwd != '' ? LlsetPwdToAngo($i_id, $i_pwd) : '';
$f       = LlsetGetFidp();
$f_id    = isset($f['id'])  ? $f['id']  : '';
$f_pwd_a = isset($f['pwd']) ? $f['pwd'] : '';
if ($i_id == '' || $i_pwd_a == ''){header("Location: ${jump_url}?p_act=login&p_msg=login0001");
exit;}
else if (strcmp($i_id, $f_id) != 0 || strcmp($i_pwd_a, $f_pwd_a) != 0){header("Location: ${jump_url}?p_act=login&p_msg=login0002");
exit;}
else{LlsetLogin($i_id, $i_pwd_a);}}
if (!LlsetIsLogin()){header("Location: ${jump_url}?p_act=login&p_msg=login0001");
exit;}}
$LLSET_IS_LOGIN = FALSE;
function LlsetIsLogin(){global $LLSET_IS_LOGIN;
if ($LLSET_IS_LOGIN) { return TRUE; }
$wks = explode("\t", LlsetLoginSessionGet());
$ses_id       = isset($wks[0]) ? $wks[0] : '';
$ses_pwd_ango = isset($wks[1]) ? $wks[1] : '';
$LLSET_IS_LOGIN = strlen($ses_id) > 0 && strlen($ses_pwd_ango) > 0;
return $LLSET_IS_LOGIN;}
function LlsetLogin($id,$pwd_crypt){global $LLSET_IS_LOGIN;
LlsetLoginSessionSet($id."\t".$pwd_crypt);
$LLSET_IS_LOGIN = TRUE;}
function LlsetLogout(){global $LLSET_IS_LOGIN;
LlsetLoginSessionSet('');
$LLSET_IS_LOGIN = FALSE;}
$LLSET_USER_IS_LOGIN = array();
function LlsetUserIsLogin($ses_label,$jump_url = ''){global $LLSET_USER_IS_LOGIN;
if (!isset($LLSET_USER_IS_LOGIN[$ses_label])){$wks = explode("\t", LlsetLoginSessionGet($ses_label));
$ses_id       = isset($wks[0]) ? $wks[0] : '';
$ses_pwd_ango = isset($wks[1]) ? $wks[1] : '';
$LLSET_USER_IS_LOGIN[$ses_label] = strlen($ses_id) > 0 && strlen($ses_pwd_ango) > 0;}
if ($jump_url == '' || $LLSET_USER_IS_LOGIN[$ses_label]){return $LLSET_USER_IS_LOGIN[$ses_label];}
else{header("Location: ${jump_url}");
exit;}}
$LLSET_USER_LOGIN_REC = array();
function LlsetUserLogin($ses_label,$id,$pwd,$rec = array(),$tbl = '',$tfid = ''){global $LLSET_USER_IS_LOGIN;
global $LLSET_USER_LOGIN_REC;
$pwd_crypt = LlsetPwdToAngo($id, $pwd);
LlsetLoginSessionSet($id."\t".$pwd_crypt, $ses_label);
$LLSET_USER_IS_LOGIN[$ses_label] = TRUE;
LlsetUserLoginInfoSet($ses_label, $rec);
$rtn = TRUE;
if ($tbl != ''){$rtn = LlsetDbSetFld($tbl, 'login_id', $id, $tfid, LlsetFieldDateTime());}
return $rtn;}
function LlsetUserLogout($ses_label){global $LLSET_USER_IS_LOGIN;
LlsetLoginSessionSet('', $ses_label);
LlsetUserLoginInfoSet($ses_label, array());
$LLSET_USER_IS_LOGIN[$ses_label] = FALSE;}
function LlsetUserLoginInfoSet($ses_label,$rec){LlsetSessionSet('LOGIN_INFO_'.$ses_label, serialize($rec));}
function LlsetUserLoginInfoGet($ses_label){$str = LlsetSessionGet('LOGIN_INFO_'.$ses_label);
return $str != '' ? unserialize($str) : array();}
function LlsetSetFidp($id,$pwd){global $LLSET_ALL;
$setfld = array();
$tbl    = 'fidp';
$tblfld = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
foreach ($tblfld as $fid => $finfo){$setfld[$fid] = '';}
$setfld['id']  = $id;
$setfld['pwd'] = LlsetPwdToAngo($id, $pwd);
if (!LlsetUpdIns1($tbl, '', LLTBF_WILD_CARD, $setfld, 1)){return FALSE;}
return TRUE;}
function LlsetGetRegCodes($mail){$tm  = time();
$dt1 = LlutlDateTime($tm);
$dt2 = LlutlDateTime($tm + 86400);
$s1  = sprintf('%02d', $dt1['day']);
$s2  = sprintf('%02d', $dt2['day']);
return array(0 => LlutlCryptOneTimePwd($mail, $s1),1 => LlutlCryptOneTimePwd($mail, $s2),);}
function LlsetJumpNotfound($html = 'notfound.html'){$jump_url = LLUTL_URL_PTOP.$html;
header("Location: ${jump_url}");
exit;}
function LlsetChk2Exist($tbl,&$ips,&$chks,$errmax = 10){global $LLSET_ALL;
$flds = $tbl != '' ? $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD] : '';
$cfld = array();
$ecnt  = 0;
foreach ($chks as $fid => $fname){if ($tbl == '' || isset($flds[$fid])){if (!LlsetChkExist($ips, 'i_'.$fid)){$cfld[] = $fname != '' ? $fname : $flds[$fid][LLSET_FI_NAME];
$ecnt ++; if ($ecnt >= $errmax) { break; }}}}
if (sizeof($cfld) > 0){return LlutlMsgf('chk2exist01', join(', ', $cfld));}
return '';}
function LlsetChk2Len($tbl,&$ips,&$chks){global $LLSET_ALL;
$flds = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
foreach ($chks as $fid => $finfo){$fnm = $flds[$fid][LLSET_FI_NAME];
$val = $ips['i_'.$fid];
if ($val == '') { continue; }
$wks = explode(',', $finfo);
$l1  = LlutlGetNum0(isset($wks[0]) ? $wks[0] : 0);
$l2  = LlutlGetNum0(isset($wks[1]) ? $wks[1] : 0);
$len = strlen($val);
if ($l1 != 0 && $l2 != 0){if ($len < $l1 || $len > $l2){return LlutlMsgf('chk2roma02', $fnm, $l1, $l2);}}
else if ($l1 == 0 && $l2 != 0){if ($len > $l2){return LlutlMsgf('chk2roma02', $fnm, $l2);}}
else if ($l1 != 0 && $l2 == 0){if ($len < $l1){return LlutlMsgf('chk2roma02', $fnm, $l1);}}}
return '';}
function LlsetChk2Roma($flds,&$ips,&$chks,$form = '',$fnms = array()){foreach ($chks as $fid => $finfo){$fnm  = '';
$val  = '';
$fids = array();
$vals = array();
if ($finfo == 'date'){$fids = explode(',', $fid);
if (isset($fnms[$fid])){$fnm  = strstr($fnms[$fids[0]], LlutlMsg('chk2roma01'))
? str_replace(LlutlMsg('chk2roma01'), '', $fnms[$fids[0]])
: $fnms[$fids[0]].', '.$fnms[$fids[1]].', '.$fnms[$fids[2]];}
else{$fnm  = strstr($flds[$fids[0]][LLSET_FI_NAME], LlutlMsg('chk2roma01'))
? str_replace(LlutlMsg('chk2roma01'), '', $flds[$fids[0]][LLSET_FI_NAME])
: $flds[$fids[0]][LLSET_FI_NAME].', '.$flds[$fids[1]][LLSET_FI_NAME].', '.$flds[$fids[2]][LLSET_FI_NAME];}
$vals[0] = $ips['i_'.$fids[0]];
$vals[1] = $ips['i_'.$fids[1]];
$vals[2] = $ips['i_'.$fids[2]];
$val = join('', $vals);}
else{if (isset($fnms[$fid])){$fnm = $fnms[$fid];}
else{$fnm = $flds[$fid][LLSET_FI_NAME];}
$val = $ips['i_'.$fid];}
if ($val == '') { continue; }
if (!LlutlChkEnglishOnly($val)){return LlutlMsgf('chk2roma02', $fnm);}
if ($finfo == 'alpha'){if (!LlutlChkEnglishOnly($val)){return LlutlMsgf('chk2roma02', $fnm);}}
else if (substr($finfo, 0, 3) == 'num'){$cs = unpack('C*', $val);
foreach ($cs as $cc){$c = chr($cc);
if (!preg_match('/[0-9-]/', $c)){return LlutlMsgf('chk2roma03', $fnm);}}
$wks = explode(',', $finfo);
if (sizeof($wks) > 1){$wmin = isset($wks[1]) ? LlutlGetNum($wks[1]) : '';
$wmax = isset($wks[2]) ? LlutlGetNum($wks[2]) : '';
if ($wmin != '' && $wmin > $val){return $wmax == ''	? LlutlMsgf('chk2roma04', $fnm, $wmin)
: LlutlMsgf('chk2roma06', $fnm, $wmin, $wmax);}
if ($wmax != '' && $wmax < $val){return $wmin == ''	? LlutlMsgf('chk2roma05', $fnm, $wmax)
: LlutlMsgf('chk2roma06', $fnm, $wmin, $wmax);}}}
else if ($finfo == 'tel' ||
$finfo == 'itel'){$cs = unpack('C*', $val);
foreach ($cs as $cc){$c = chr($cc);
if (!preg_match('/[0-9-+()]/', $c)){return LlutlMsgf('chk2roma07', $fnm);}}}
else if ($finfo == 'pcode'){if (strlen($val) != 7){return LlutlMsgf('chk2roma08', $fnm);}
$cs = unpack('C*', $val);
foreach ($cs as $cc){$c = chr($cc);
if (!preg_match('/[0-9]/', $c)){return LlutlMsgf('chk2roma08', $fnm);}}}
else if ($finfo == 'mail'){if (strpos($val, '@') === false || strpos($val, '.') === false){return LlutlMsgf('chk2roma09', $fnm);}}
else if ($finfo == 'url'){if (substr($val, 0, 4) != 'http' || strpos($val, ':') === false || strpos($val, '/') === false || strpos($val, '.') === false){return LlutlMsgf('chk2roma10', $fnm);}}
else if ($finfo == 'login_id' || $finfo == 'login_pwd'){if (strlen($val) < 4 || strlen($val) > 20 || !LlutlChkEnglishOnly($val)){return LlutlMsgf('chk2roma11', $fnm, '4', '20');}}
else if ($finfo == 'id'){if (strlen($val) < 1 || strlen($val) > 20 || !LlutlChkEnglishOnly($val)){return LlutlMsgf('chk2roma11', $fnm, '1', '20');}
$cs = unpack('C*', $val);
foreach ($cs as $cc){$c = chr($cc);
if (!preg_match('/[0-9A-Za-z]/', $c)){return LlutlMsgf('chk2roma11', $fnm, '1', '20');}}}
else if ($finfo == 'date'){if (!LlutlDateCheck(LlutlGetNum0($vals[0]), LlutlGetNum0($vals[1]), LlutlGetNum0($vals[2]))){return LlutlMsgf('chk2roma12', $fnm);}}
else if ($finfo == 'yyyy-mm-dd'){$ertn = LlutlMsgf('chk2roma13', $fnm);
$cs = unpack('C*', $val);
foreach ($cs as $cc){$c = chr($cc);
if (!preg_match('/[0-9-]/', $c)) { return $ertn; }}
$idt   = LlutlDateStrToAry($val);
$szidt = sizeof($idt);
if ($szidt != 3) { return $ertn; }
if (!LlutlDateCheck($idt[0], $idt[1], $idt[2])) { return $ertn; }}
else if ($finfo == 'yyyy-mm-dd hh:mi:ss'){$ertn = LlutlMsgf('chk2roma14', $fnm);
$cs = unpack('C*', $val);
foreach ($cs as $cc){$c = chr($cc);
if (!preg_match('/[0-9-: ]/', $c)) { return $ertn; }}
$idt   = LlutlDateStrToAry($val);
$szidt = sizeof($idt);
if ($szidt != 3 && $szidt != 6) { return $ertn; }
if (!LlutlDateCheck($idt[0], $idt[1], $idt[2])) { return $ertn; }
if ($szidt == 6){if ($idt[3] < 0 || $idt[3] > 59 || $idt[4] < 0 || $idt[4] > 59 || $idt[5] < 0 || $idt[5] > 59) { return $ertn; }}}}
return '';}
function LlsetChk2Code($flds,&$ips,&$chks){foreach ($chks as $fid => $wflds){$nfld = 2;
$fnm  = '';
if (is_array($wflds)){$nfld = $wflds[0];
$fnm  = $wflds[1];}
else{$nfld = $wflds;
$fnm  = $flds[$fid][LLSET_FI_NAME];}
$fvals = str_replace("\r", '', trim($ips['i_'.$fid]));
foreach (explode("\n", $fvals) as $line){if (trim($line) == '') { continue; }
$cols = explode(',', $line);
if (sizeof($cols) < $nfld){return LlutlMsgf('chk2code01', $fnm);}
$code = trim($cols[0]);
$cs = unpack('C*', $code);
$cnt = 0;
foreach ($cs as $cc){$c = chr($cc);
if (($cnt == 0 && !preg_match('/[A-Za-z]/', $c)) || ($cnt > 0 && !preg_match('/[0-9A-Za-z]/', $c))){return LlutlMsgf('chk2code02', $fnm);}
$cnt ++;}}}
return '';}
function LlsetChk2LoginIdPwd(&$flds,&$ips,$tbl,$fid_id,$fid_p1,$fid_p2,$fid_key = '',$val_key = ''){$login_id = $ips['i_'.$fid_id];
if ($login_id != ''){$emsg = LlsetChk2Unique($flds, $ips, $tbl, $fid_id, $fid_key, $val_key);
if ($emsg != '') { return $emsg; }}
if (strcmp($ips['i_'.$fid_p1], $ips['i_'.$fid_p2]) != 0){$fnm1 = $flds[$fid_p1][LLSET_FI_NAME];
$fnm2 = $flds[$fid_p2][LLSET_FI_NAME];
return LlutlMsgf('inchk0002', $fnm1, $fnm2);}
return '';}
function LlsetChk2Unique(&$flds,&$ips,$tbl,$fid_id,$fid_key = '',$val_key = '',$add_jkns = array()){$val = $ips['i_'.$fid_id];
$db  = LlsetDbConnect();
$sql = "where ${fid_id} = '${val}'";
if ($fid_key != '') { $sql .= " and ${fid_key} <> '${val_key}'"; }
foreach ($add_jkns as $jk => $jv){$sql .= " and ${jk} = '${jv}'";}
$recs = LldbSelectFlds($db, array($fid_id), LlsetDbTbl($tbl), $sql, 0, 1);
if (sizeof($recs) > 0){$fnm = $flds[$fid_id][LLSET_FI_NAME];
return LlutlMsgf('inchk0004', $fnm);}
return '';}
function LlsetChk2DbForeignKey($flds,&$ips,&$chks,$fnms = array()){$db = LlsetDbConnect();
foreach ($chks as $fid => $finfo){$wks   = explode(':', $finfo);
$dbtbl = $wks[0];
$dbfid = $wks[1];
$ival  = $ips['i_'.$fid];
$recs = LldbSelectFlds($db, array($dbfid), LlsetDbTbl($dbtbl), "where ${dbfid} = ${ival}", 0, 1);
if (sizeof($recs) <= 0){$fnm = isset($fnms[$fid]) ? $fnms[$fid] : $flds[$fid][LLSET_FI_NAME];
return LlutlMsgf('chk2dbforeignkey01', $fnm);}}
return '';}
function LlsetChk3Exist(&$ips,&$chks,$errmax = 10){return LlsetChk2Exist('', $ips, $chks, $errmax);}
function LlsetChk3Roma(&$ips,&$chks,$form = ''){$p_flds = array();
$p_chks = array();
$p_fnms = array();
foreach ($chks as $fid => $finfos){$p_chks[$fid] = $finfos[0];
$p_fnms[$fid] = $finfos[1];}
return LlsetChk2Roma($p_flds, $ips, $p_chks, '', $p_fnms);}
function LlsetChkExist(&$ips,$fid){global $_FILES;
if (isset($_FILES[$fid]['name']) && strlen($_FILES[$fid]['name']) > 0) { return TRUE; }
if (!isset($ips[$fid])) { return FALSE; }
if (is_array($ips[$fid])){if (sizeof($ips[$fid]) <= 0)   { return FALSE; }}
else{if ($ips[$fid] == '')   { return FALSE; }}
return TRUE;}
function LlsetEscapeTagForIn($str,$fi_type){return $fi_type == 'tarea' || $fi_type == 'html' ? LlutlHtmlEscapeTagForTarea($str) : LlutlHtmlEscapeTagForText($str);}
function LlsetReplacePageList(&$html,&$rep,$offset,$nline,$kensu,$npage,$page,$pkensu,$nplst = 6,$plmgn = 2,$label = 'PLST'){$cnt1 = $offset + 1;       if ($kensu <= 0)    { $cnt1 = 0; }
$cnt2 = $offset + $pkensu; if ($cnt2 > $kensu) { $cnt2 = $kensu; }
$page_prev = $page - 1; if ($page_prev < 1)      { $page_prev = 1; }
$page_next = $page + 1; if ($page_next > $npage) { $page_next = $npage; }
$rep[LLUTL_REP_MARK.$label.'_KENSU'.LLUTL_REP_MARK] = $kensu;
$rep[LLUTL_REP_MARK.$label.'_CNT1'.LLUTL_REP_MARK]  = $cnt1;
$rep[LLUTL_REP_MARK.$label.'_CNT2'.LLUTL_REP_MARK]  = $cnt2;
$rep[LLUTL_REP_MARK.$label.'_NLINE'.LLUTL_REP_MARK] = $nline;
$rep[LLUTL_REP_MARK.$label.'_PAGE'.LLUTL_REP_MARK]  = $page;
$rep[LLUTL_REP_MARK.$label.'_PAGE_PREV'.LLUTL_REP_MARK] = $page_prev;
$rep[LLUTL_REP_MARK.$label.'_PAGE_NEXT'.LLUTL_REP_MARK] = $page_next;
$html = LlutlReplaceIf('IF_'.$label.'_KENSU_ZERO', $kensu <= 0, $html);
$html = LlutlReplaceIf('IF_'.$label.'_PAGE_PREV', $page_prev < $page, $html);
$html = LlutlReplaceIf('IF_'.$label.'_PAGE_NEXT', $page_next > $page, $html);
if ($npage < $nplst) { $nplst = $npage; }
$plsa  = $plmgn + 1;
$pldv  = $nplst - (2 * $plmgn);
$plst1 = $pldv > 0 ? (int)(($page - $plsa) / $pldv) * $pldv + 1 : 1;
if      ($page >= $plst1 + ($nplst - $plmgn)) { $plst1 += (int)($nplst / 2); }
else if ($page <= $plst1 + ($plmgn - 1))      { $plst1 -= (int)($nplst / 2); }  //LlutlDebugWrite('1 : '.$plst1.LlutlHtmlXhtmlTag('<br>'));

if ($plst1 > $npage - $nplst + 1) { $plst1 = $npage - $nplst + 1; } 			//LlutlDebugWrite('2 : '.$plst1.LlutlHtmlXhtmlTag('<br>'));

if ($plst1 < 1)                   { $plst1 = 1; } 								//LlutlDebugWrite('3 : '.$plst1.LlutlHtmlXhtmlTag('<br>'));

$rep[LLUTL_REP_MARK.$label.'_TPAGE'.LLUTL_REP_MARK] = 1;
$rep[LLUTL_REP_MARK.$label.'_BPAGE'.LLUTL_REP_MARK] = $npage;
$html = LlutlReplaceIf('IF_'.$label.'_TPAGE', $plst1 > 1, $html);
$html = LlutlReplaceIf('IF_'.$label.'_BPAGE', $plst1 + $nplst - 1 < $npage, $html);
$html = LlutlReplaceIf('IF_'.$label.'_1PAGE', $npage <= 1, $html);
$new_htmls = array();
$lststr = 'LIST_'.$label;
$htmls = explode('<!--'.LLUTL_REP_MARK.$lststr.LLUTL_REP_MARK.'-->', $html);
$hcnt  = 0;
foreach ($htmls as $wkhtml){if (($hcnt + 1) % 2 == 0){$srchtml = $wkhtml;
$dsthtml = '';
for ($i = 0; $i < $nplst; $i ++){$line = $srchtml;
$lrep = array();
$plst_page = $plst1 + $i;
$lrep[LLUTL_REP_MARK.$lststr.'_PAGE'.LLUTL_REP_MARK] = $plst_page;
$line = LlutlReplaceIf('IF_'.$lststr.'_PAGE', $page == $plst_page, $line);
$dsthtml .= str_replace(array_keys($lrep), array_values($lrep), $line);}
$wkhtml = $dsthtml;}
$new_htmls[] = $wkhtml;
$hcnt ++;}
$html = join('', $new_htmls);}
function LlsetPrintVersion(){$p1 = LlutlPara('p1', '');
if ($p1 == 'info'){print("##LTOOL##\n");
print(LLSET_WB_VER."\n");
print(LlsetIsLimit() ? "ON\n" : "OFF\n");}
else if ($p1 == 'set1'){print("##LTOOL##\n");
print(LlsetLimitSet1());}
else if ($p1 == 'set2'){$tm30     = LlutlPara('p2', '');
$tm30_pwd = LlutlPara('p3', '');
$rtn = LlsetLimitSet2($tm30, $tm30_pwd);
print("##LTOOL##\n");
print($rtn ? 'OK' : 'NG');}
else if ($p1 == 'reset'){$tm30     = LlutlPara('p2', '');
$tm30_pwd = LlutlPara('p3', '');
$rtn = FALSE;
print("##LTOOL##\n");
print($rtn ? 'OK' : 'NG');}
else{print('LITTLE-NET WEB TOOL : '.LLSET_WB_VER);}}
function LlsetLimitSet1(){return (int)(time() / 30);}
function LlsetLimitSet2($tm30,$tm30_pwd,$reset = FALSE){$tm30_2 = (int)(time() / 30);
$tm30_1 = $tm30_2 - 2;
if ($tm30 < $tm30_1 || $tm30_2 < $tm30){LlutlLog(__FILE__, __LINE__, 'check time error');
return FALSE;}
if (strcmp(LlutlCryptOneTimePwd2($tm30), $tm30_pwd) != 0){LlutlLog(__FILE__, __LINE__, 'check pwd error');
return FALSE;}
$key = $reset ? 0 : LlsetLimitKey();
$lid = LlidfOpen(LlsetLimitPath());
LlidfSet($lid, $key);
LlidfClose($lid);
LlutlLog(__FILE__, __LINE__, $reset ? 'reset limit' : 'set limit');
return TRUE;}
function LlsetIsLimit(){$lid = LlidfOpen(LlsetLimitPath());
$key = LlutlGetNum0(LlidfGet($lid));
LlidfClose($lid);
if ($key == LlsetLimitKey()) { return FALSE; }
return TRUE;}
function LlsetLimitKey(){$n = array('0' => 11, '1' => 75, '2' => 43, '3' => 15, '4' => 77, '5' => 41,'6' => 22, '7' => 85, '8' => 53, '9' => 28, 'A' => 81, 'B' => 54,'C' => 37, 'D' => 95, 'E' => 62, 'F' => 33, 'G' => 91, 'H' => 68,'I' => 44, 'J' => 15, 'K' => 72, 'L' => 47, 'M' => 11, 'N' => 76,'O' => 53, 'P' => 25, 'Q' => 81, 'R' => 58, 'S' => 22, 'T' => 85,'U' => 67, 'V' => 31, 'W' => 99, 'X' => 68, 'Y' => 35, 'Z' => 93,);
$cs = unpack('C*', strtoupper(__FILE__));
$num = 0;
foreach ($cs as $wc){$c = chr($wc);
if (isset($n[$c])) { $num += $n[$c]; }}
return $num * 21;}
function LlsetLimitPath(){return LlsetNewIdPath('v'.'a'.'l', 'k'.'e'.'y'.'_');}
function LlsetFormMenu(&$html,&$rep){if (TRUE){$exdir       = 'extool';
$sdir        = LLUTL_DIR_WB.$exdir;
$slists      = LlutlGlob($sdir, 'awstats');
$url_awstats = '';
if (isset($slists[0])){$dirnm_aw    = $slists[0];
$user        = LlutlCryptOneTimePwd2(LLUTL_SITE_ID);
$pwd         = LlutlCryptOneTimePwd2((int)(time() / 86400));
$base_url    = LLUTL_URL_PTOP2.LLUTL_DIRNM_WB."/${exdir}/${dirnm_aw}/wwwroot/cgi-bin/awstats.pl";
$url_awstats = str_replace('://', "://${user}:${pwd}@", $base_url);

LlutlWriteBasicAuthFiles(TOP_DIR.LLUTL_DIRNM_WB."/${exdir}/${dirnm_aw}", 'AWStats', $user, $pwd);}
$html = LlutlReplaceIf('IF_AWSTATS', $url_awstats != '', $html);
$rep['##URL_AWSTATS##'] = $url_awstats;}
return TRUE;}
function LlsetFormEtcSet01(&$html,&$rep,$fdef = array()){global $LLSET_ALL;
$tbl   = 'fetc';
$norec = !LlsetExistGetF($tbl);
$def   = $norec ? $fdef : LlsetGetF($tbl);
$tblfld = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
foreach ($tblfld as $fid => $finfo){$ufid = strtoupper($fid);
$is_a = $finfo[LLSET_FI_TYPE] == 'check';
$ival = LlsetPara('i_'.$fid, $is_a, isset($def[$fid]) ? $def[$fid] : ($is_a ? array() : ''));
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
else{$rep['##I_'.$ufid.'##'] = LlsetEscapeTagForIn($ival, $finfo[LLSET_FI_TYPE]);}}
$html = LlutlReplaceIf('IF_NOREC', $norec, $html);
return TRUE;}
function LlsetFormEtcSet02(&$html,&$rep){global $LLSET_ALL;
$ips   = LlutlParaToArray('i_');
$m_msg  = LlutlMsgf('formset01');
$m_err  = FALSE;
$m_hdn  = array('p_act' => 'menu');
if (!LlsetIsUpdateMode($html, $rep, $m_msg, $m_err, $m_hdn)) { return FALSE; }
$tbl    = 'fetc';
$setfld = array();
$tblfld = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
foreach ($tblfld as $fid => $finfo){$ival = isset($ips['i_'.$fid]) ? $ips['i_'.$fid] : '';
if ($finfo[LLSET_FI_TYPE] == 'int' && $ival == ''){$ival = 0;}
$setfld[$fid] = is_array($ival) ? LlsetMfldAryToStr($ival) : $ival;}
if (!LlsetUpdIns1($tbl, '', LLTBF_WILD_CARD, $setfld, 1)){$m_msg = LlutlMsgf('formset02');
$m_err = TRUE;
$m_hdn = array('p_act' => 'etc_set01') + $ips;}
if (LlutlPara('p_inq_num_reset', '') == '1'){CinquiryResetInqNum();}
LlsetReplaceFormMsg($html, $rep, $m_msg, $m_err, $m_hdn);
return TRUE;}
function LlsetFormEtcSet022(&$html,&$rep,$rtn_act,&$m_msg,&$m_err,&$m_hdn){global $LLSET_ALL;
$ips   = LlutlParaToArray('i_');
$m_msg  = LlutlMsgf('formset01');
$m_err  = FALSE;
$m_hdn  = array('p_act' => $rtn_act);
if (!LlsetIsUpdateMode($html, $rep, $m_msg, $m_err, $m_hdn)) { return FALSE; }
$tbl    = 'fetc';
$setfld = array();
$tblfld = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
foreach ($tblfld as $fid => $finfo){$ival = isset($ips['i_'.$fid]) ? $ips['i_'.$fid] : '';
$setfld[$fid] = $ival;}
if (!LlsetUpdIns1($tbl, '', LLTBF_WILD_CARD, $setfld, 1)){$m_msg = LlutlMsgf('formset02');
$m_err = TRUE;
$m_hdn = array('p_act' => 'etc_set01') + $ips;}
return TRUE;}
function LlsetFormCodeSet01(&$html,&$rep,$prefix = 'list_'){global $LLSET_ALL;
$fld = LlutlPara('p_fld', '');
$tbl      = 'fetc';
$def      = LlsetGetF($tbl);
$def_code = isset($def[$prefix.$fld]) ? $def[$prefix.$fld] : '';
$ival = LlsetPara('i_code', FALSE, $def_code);
$rep['##I_CODE##'] = LlsetEscapeTagForIn($ival, 'tarea');
$rep['##P_FLD##']  = LlsetEscapeTagForIn($fld,  'text');
$html = LlutlReplaceCase2('CASE_FLD', $fld, $html);
return TRUE;}
function LlsetFormCodeSet02(&$html,&$rep,$prefix = 'list_'){global $LLSET_ALL;
$fld  = LlutlPara('p_fld', '');
$code = LlutlPara('i_code', '');
$m_err  = FALSE;
$tbl    = 'fetc';
$fid    = $prefix.$fld;
$setfld = LlsetGetF($tbl);
$setfld[$fid] = $code;
$old_list = LlsetGetListFromTblFld($tbl, $fid);
if (!LlsetUpdIns1($tbl, '', LLTBF_WILD_CARD, $setfld, 1)) { $m_err = TRUE; }
LlsetClearGetF();
$new_list = LlsetGetListFromTblFld($tbl, $fid);
$htmls = explode('<!--##LIST##-->', $html);
$html1 = '';
$cnt   = 0;
foreach ($new_list as $val => $text){$line = $htmls[1];
$lrep = array();
$cnt ++;
$lrep['##LIST_IDX##']  = $cnt;
$lrep['##LIST_VAL##']  = $val;
$lrep['##LIST_TEXT##'] = str_replace("'", '"', $text);
$html1 .= str_replace(array_keys($lrep), array_values($lrep), $line);}
$html = $htmls[0] . $html1 . $htmls[2];
$rep['##NLIST##'] = $cnt;
$set_idx = 0;
$idx     = 1;
foreach ($new_list as $val => $text){if (!isset($old_list[$val])){$set_idx = $idx;
break;}
$idx ++;}
$rep['##SET_IDX##'] = $set_idx;
$rep['##P_FLD##'] = $fld;
$html = LlutlReplaceIf('IF_ERR', $m_err, $html);
return $m_err ? FALSE : TRUE;}
function LlsetFormPsetSet01(&$html,&$rep,$fdef = array()){global $LLSET_ALL;
$tbl    = 'fpset';
$tblfld = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
$def    = LlsetExistGetF($tbl) ? LlsetGetF($tbl) : $fdef;
$p_key  = isset($def[LLSET_KEY_FID]) ? $def[LLSET_KEY_FID] : 0;
$max_file_size = 1024;
foreach ($tblfld as $fid => $finfo){$ufid = strtoupper($fid);
$is_a = $finfo[LLSET_FI_TYPE] == 'check';
$ival = LlsetPara('i_'.$fid, $is_a, isset($def[$fid]) ? $def[$fid] : ($is_a ? array() : ''));
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
return TRUE;}
function LlsetFormPsetSet02(&$html,&$rep){global $LLSET_ALL;
$ips   = LlutlParaToArray('i_');
$m_msg = LlutlMsgf('psetset01');
$m_err = FALSE;
$m_hdn = array('p_act' => '');
if (!LlsetIsUpdateMode($html, $rep, $m_msg, $m_err, $m_hdn)) { return FALSE; }
$tbl    = 'fpset';
$setfld = array();
$tblfld = $LLSET_ALL[$tbl][LLSET_AI_TBL][LLSET_TI_FLD];
foreach ($tblfld as $fid => $finfo){$ival = isset($ips['i_'.$fid]) ? $ips['i_'.$fid] : '';
if ($finfo[LLSET_FI_TYPE] == 'int' && $ival == ''){$ival = 0;}
$setfld[$fid] = is_array($ival) ? LlsetMfldAryToStr($ival) : $ival;}
if (!LlsetUpdIns1($tbl, '', LLTBF_WILD_CARD, $setfld, 1)){$m_msg = LlutlMsgf('psetset02');
$m_err = TRUE;
$m_hdn = array('p_act' => 'pset_set01') + $ips;}
else{global $LLSET_UPD_INS1_KEY;
$my_key = $LLSET_UPD_INS1_KEY;
if (!LlsetImageUpload($tbl, $my_key, $m_msg)){$m_err  = TRUE;}}
LlsetReplaceFormMsg($html, $rep, $m_msg, $m_err, $m_hdn);
LlsetWriteFileListTable($tbl);
return TRUE;}
function LlsetFormGmapSet(&$html,&$rep){global $LLSET_LIST_GMAP_JPN;
global $LLSET_LIST_GMAP_KEN;
global $LLSET_LIST_GMAP_ADDR;
$rep['##GMAP_P_INFO##'] = LlutlPara('p_info', '');
$rep['##GMAP_P_FORM##'] = LlutlPara('p_form', '');
$rep['##GMAP_P_FLD##']  = LlutlPara('p_fld', '');
$rep['##GMAP_P_FLD2##'] = LlutlPara('p_fld2', '');
$ken                    = LlutlPara('p_ken', '');
$addr                   = LlutlPara('p_addr', '');
$min_lat = $LLSET_LIST_GMAP_JPN[0];
$min_lng = $LLSET_LIST_GMAP_JPN[1];
$max_lat = $LLSET_LIST_GMAP_JPN[2];
$max_lng = $LLSET_LIST_GMAP_JPN[3];
if (TRUE){if (defined('LLSET_LIST_GMAP_DEF_KEN') && isset($LLSET_LIST_GMAP_KEN[LLSET_LIST_GMAP_DEF_KEN])){$wgdef   = $LLSET_LIST_GMAP_KEN[LLSET_LIST_GMAP_DEF_KEN];
$min_lat = $wgdef[0];
$min_lng = $wgdef[1];
$max_lat = $wgdef[2];
$max_lng = $wgdef[3];}
if ($ken != '' && isset($LLSET_LIST_GMAP_KEN[$ken])){$wgdef   = $LLSET_LIST_GMAP_KEN[$ken];
$min_lat = $wgdef[0];
$min_lng = $wgdef[1];
$max_lat = $wgdef[2];
$max_lng = $wgdef[3];
if ($addr != '' && isset($LLSET_LIST_GMAP_ADDR[$ken])){foreach ($LLSET_LIST_GMAP_ADDR[$ken] as $kaddr => $wgdef){$lkaddr = strlen($kaddr);
if (strncmp($addr, $kaddr, $lkaddr) == 0){$min_lat = $wgdef[0];
$min_lng = $wgdef[1];
$max_lat = $wgdef[0];
$max_lng = $wgdef[1];
break;}}}}}
$rep['##GMAP_MIN_LAT_DEF##'] = $min_lat;
$rep['##GMAP_MIN_LNG_DEF##'] = $min_lng;
$rep['##GMAP_MAX_LAT_DEF##'] = $max_lat;
$rep['##GMAP_MAX_LNG_DEF##'] = $max_lng;
return TRUE;}
function LlsetGmapInfoFromAddr($addr,$zoom = LLSET_GMAP_MAX_ZOOM_DEF){$ginfo = '';
if ($addr != ''){$r = LlsetGmapLatLngFromAddr($addr);
$lat = $r['lat'];
$lng = $r['lng'];
if ($lat != LLSET_GMAP_ERRNUM && $lng != LLSET_GMAP_ERRNUM){$ginfo = "${lat}, ${lng}, ${zoom}, ${lat}, ${lng}";}}
return $ginfo;}
function LlsetGmapLatLngFromAddr($addr){$paddr = rawurlencode(mb_convert_encoding($addr, 'UTF-8', LLUTL_ENCODING));
$url   = "http://maps.google.com/maps/geo?q=${paddr}&output=csv&sensor=false";

$lines = file($url);
$f     = explode(',', array_pop($lines));
return array('addr' => $addr,'lat'  => isset($f[2]) ? $f[2] : LLSET_GMAP_ERRNUM,'lng'  => isset($f[3]) ? $f[3] : LLSET_GMAP_ERRNUM,);}
function LlsetFormSql(&$html,&$rep){global $LLSET_ALL;
$db   = LlsetDbConnect();
$fext = '.cgi';
$msgs = array();
$tgbr = LlutlHtmlXhtmlTag('<br>');
$case = LlutlPara('p_case', 'top');
$msgs[] = strtoupper($case);
$html = LlutlReplaceCase2('CASE_CASE', $case, $html);
if ($case == 'top'){;}
else if ($case == 'sql'){$sqls = LlutlPara('i_sql', '');
$sqls = str_replace("\\'", "'", $sqls);
$sqls = trim($sqls);
$sqls = substr($sqls, -1) == ';' ? $sqls."\r\n" : $sqls.";\r\n";
$msg  = '';
foreach (explode(";\r\n", $sqls) as $sql){$sql = trim($sql);
if (strlen($sql) > 0){$recs = array();
$emsg = LldbExecPhpCodeMsg($db, $sql, 0, 100, $recs);
if ($emsg != '') { $msg .= $tgbr.$emsg; }
if (sizeof($recs) > 0){$cnt = 0;
foreach ($recs as $rec){$msg .= "Rec.$cnt".$tgbr;
foreach ($rec as $fnam => $fval){$msg .= "<nowrap>$fnam=[".$fval."]</nowrap>".$tgbr;}
$cnt ++;}}}}
$rep['##MSG##'] = $msg != '' ? $msg : 'SQL文を実行しました。';}
else if ($case == 'backup'){$nline = 100000;
foreach ($LLSET_ALL as $tbl => $tinfo){if (substr($tbl, 0, 1) != 't') { continue; }
$rtbl  = LlsetDbTbl($tbl);
$sflds = array_keys($tinfo[LLSET_AI_TBL][LLSET_TI_FLD]);
$recs  = LldbSelectFlds($db, $sflds, $rtbl, '', 0, $nline);
$path = LLSET_DIR_BKUP.$tbl.$fext;
LlutlMkDir(dirname($path), LLUTL_MODE_MKDIR);
$fp = fopen($path, "w");
foreach ($recs as $rec){$str = LlsetKeyAryToStr($rec);
fwrite($fp, $str."\n");}
fclose($fp);
$msgs[] = sprintf('%s : %d records', $rtbl, sizeof($recs));}
$rep['##MSG##'] = join("${tgbr}\n", $msgs);}
else if ($case == 'restore'){foreach ($LLSET_ALL as $tbl => $tinfo){if (substr($tbl, 0, 1) != 't') { continue; }
$recs = array();
$rtbl = LlsetDbTbl($tbl);
$path = LLSET_DIR_BKUP.$tbl.$fext;
$lines = file($path);
foreach ($lines as $line){if (substr($line, -1) == "\n") { $line = substr($line, 0, -1); }
$recs[] = LlsetStrToKeyAry($line);}
$cnt = LldbInsertArray($db, $rtbl, $recs);
$msgs[] = sprintf('%s : %d records --> insert %d records', $rtbl, sizeof($recs), $cnt);}
$rep['##MSG##'] = join("${tgbr}\n", $msgs);}
return TRUE;}
function LlsetKeyAryToStr(&$ary){$wks = array();
foreach ($ary as $k => $v){$ck = str_replace( array("\n", "\r", "\t"), array(LLTBF_MARK_LF, LLTBF_MARK_CR, LLTBF_MARK_TAB), $k);
$cv = str_replace( array("\n", "\r", "\t"), array(LLTBF_MARK_LF, LLTBF_MARK_CR, LLTBF_MARK_TAB), $v);
$wks[] = $ck."\t".$cv;}
return implode("\t", $wks);}
function LlsetStrToKeyAry(&$str){$ary = array();
$cnt = 0;
$k   = '';
foreach (explode("\t", $str) as $cs){$s = str_replace(array(LLTBF_MARK_LF, LLTBF_MARK_CR, LLTBF_MARK_TAB), array("\n", "\r", "\t"), $cs);
if ($cnt % 2 == 0){$k = $s;}
else{$ary[$k] = $s;}
$cnt ++;}
return $ary;}
function LlsetSetCommonFields(&$rec,$def = array(),$kwds = array(),$tims = array()){foreach (array_keys($rec) as $fid){if (substr($fid, -5) == '_kana')	{ $rec[$fid] = LlutlConvForKanaArea($rec[$fid]); }}
if (sizeof($kwds) > 0){$vals = array();
foreach ($kwds as $kwd){$vals[] = LlsetConvKwdStr($kwd);}
$rec['sel_kwd'] = join("\n", $vals);}
if (isset($rec['gmap_info'])){$rec['sel_gmap_clat'] = LLSET_GMAP_ERRNUM;
$rec['sel_gmap_clng'] = LLSET_GMAP_ERRNUM;
$rec['sel_gmap_zoom'] = LLSET_GMAP_ERRNUM;
$rec['sel_gmap_plat'] = LLSET_GMAP_ERRNUM;
$rec['sel_gmap_plng'] = LLSET_GMAP_ERRNUM;
if (trim($rec['gmap_info']) != ''){$vals = explode(',', $rec['gmap_info']);
$clat = isset($vals[0]) ? LlutlGetNum0($vals[0]) : LLSET_GMAP_ERRNUM;
$clng = isset($vals[1]) ? LlutlGetNum0($vals[1]) : LLSET_GMAP_ERRNUM;
$zoom = isset($vals[2]) ? LlutlGetNum0($vals[2]) : LLSET_GMAP_ERRNUM;
$plat = isset($vals[3]) ? LlutlGetNum0($vals[3]) : LLSET_GMAP_ERRNUM;
$plng = isset($vals[4]) ? LlutlGetNum0($vals[4]) : LLSET_GMAP_ERRNUM;
if ( -90.0 <= $clat && $clat <=  90.0 &&
-180.0 <= $clng && $clng <= 180.0 &&
0   <= $zoom && $zoom <=  20   &&
-90.0 <= $plat && $plat <=  90.0 &&
-180.0 <= $plng && $plng <= 180.0 ){$rec['sel_gmap_clat'] = $clat;
$rec['sel_gmap_clng'] = $clng;
$rec['sel_gmap_zoom'] = $zoom;
$rec['sel_gmap_plat'] = $plat;
$rec['sel_gmap_plng'] = $plng;}}
$wlat = $rec['sel_gmap_plat'];
$rec['sel_gmap_set'] = (-90.0 <= $wlat && $wlat <=  90.0) ? 1 : 0;}
foreach ($tims as $tfid){$ndt = LlutlDateTime(time());
if (isset($rec[$tfid])){if (trim($rec[$tfid]) != ''){$rdt = LlutlDateStrToAry($rec[$tfid]);
$idx = 0;
foreach (array('year', 'mon', 'day', 'hour', 'min', 'sec') as $did){if (isset($rdt[$idx])) { $ndt[$did] = $rdt[$idx]; }
$idx ++;}}
$rec[$tfid] = sprintf('%04d-%02d-%02d %02d:%02d:%02d',$ndt['year'], $ndt['mon'], $ndt['day'], $ndt['hour'], $ndt['min'], $ndt['sec']);}}}
function LlsetSetGmapFieldAuto(&$rec,$fid,$addr,$zoom){if (isset($rec[$fid]) && $rec[$fid] == ''){if (trim($addr) != ''){$rec[$fid] = LlsetGmapInfoFromAddr($addr, $zoom);}}}
function LlsetConvKwdStr($str){$str = LlutlStripTags($str);
$str = mb_convert_kana($str, "asKCV", LLUTL_ENCODING);
$str = LlutlStrToUpper($str);
return $str;}
function LlsetToH($s){return bin2hex($s);}
function LlsetToS($h){return pack('H*', $h);}
function LlsetLatDistance(){return 111263.283;}
function LlsetLngDistance($lat){return 6378150 * cos($lat / 180 * M_PI) * 2 * M_PI / 360;}
function LlsetGetSendMailConnectParaFromMc($ps){$smc = array();
if ($ps['mc_send_type'] == LLSET_MC_SEND_TYPE_SMTP || $ps['mc_send_type'] == LLSET_MC_SEND_TYPE_POP_SMTP){$mc_secure = '';
$wks = is_array($ps['mc_secure']) ? $ps['mc_secure'] : LlsetMfldStrToAry($ps['mc_secure']);
foreach ($wks as $v){$v = trim($v);
if ($v != '') { $mc_secure = $v; break; }}
$smc['SMTP'] = array();
$smc['SMTP']['SMTPAuth'] = TRUE;
if ($mc_secure != '') { $smc['SMTP']['SMTPSecure'] = $mc_secure; }
$smc['SMTP']['Host']     = $ps['mc_host'];
$smc['SMTP']['Port']     = $ps['mc_smtp_port'];
$smc['SMTP']['Username'] = $ps['mc_username'];
$smc['SMTP']['Password'] = $ps['mc_password'];}
if ($ps['mc_send_type'] == LLSET_MC_SEND_TYPE_POP_SMTP){$smc['POP'] = array();
$smc['POP']['Host']     = $ps['mc_host'];
$smc['POP']['Port']     = $ps['mc_pop_port'];
$smc['POP']['Username'] = $ps['mc_username'];
$smc['POP']['Password'] = $ps['mc_password'];}
return $smc;}
?>