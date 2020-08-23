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
define('LLSET_TOOL_TITLE', SET_SITE_TITLE.'の管理');
define('LLSET_PATH_HTACCESS', TOP_DIR.'.htaccess');
define('LLSET_PATH_HTPASSWD', TOP_DIR.'.htpasswd');
define('LLSET_DIR_ACCLOG', LLSET_DIR_SDAT.'acclog/');
define('LLSET_PATH_ACCLOG_IMG', LLSET_DIR_SDAT.'../acclog.gif');
define('LLSET_DISP_OFF', 0);
define('LLSET_DISP_ON',  1);
$LLSET_LIST_DISP = array(LLSET_DISP_ON  => '表示',LLSET_DISP_OFF => '非表示',);
define('LLSET_USER_TYPE_STOP',		0);
define('LLSET_USER_TYPE_NORMAL',	1);
define('LLSET_USER_TYPE_ADMIN',		2);
$LLSET_LIST_USER_TYPE = array(LLSET_USER_TYPE_NORMAL	=> '通常',LLSET_USER_TYPE_ADMIN	=> '管理者',LLSET_USER_TYPE_STOP	=> '停止',);
define('LLSET_AUTH_NAME_ENC_SJIS',	'SJIS-win');
define('LLSET_AUTH_NAME_ENC_UTF8',	'UTF-8');
define('LLSET_AUTH_NAME_ENC_EUC',	'eucJP-win');
$LLSET_LIST_AUTH_NAME_ENC = array(LLSET_AUTH_NAME_ENC_SJIS	=> '英字／日本語＝SJIS（推奨）',LLSET_AUTH_NAME_ENC_UTF8	=> '英字／日本語＝UTF8',LLSET_AUTH_NAME_ENC_EUC		=> '英字／日本語＝EUC',);
$LLSET_LIST = array('DISP'			=> &$LLSET_LIST_DISP,'USER_TYPE'		=> &$LLSET_LIST_USER_TYPE,'AUTH_NAME_ENC'	=> &$LLSET_LIST_AUTH_NAME_ENC,);
$LLSET_STRING = array();
$LLSET_ORDER_DEF = array('admin_sinfo_list' => array('fid=ins_time;type=text;desc=N'		=> '登録日時（旧～新）','fid=ins_time;type=text;desc=Y'		=> '登録日時（新～旧）','fid=user;type=text;desc=N'			=> 'ユーザー名（A～Z）','fid=user;type=text;desc=Y'			=> 'ユーザー名（Z～A）',),);
$LLSET_NLINE_DEF = array('admin_sinfo_list'		=> 20,);
define('LLSET_ADMIN_IMG_MAX_W',	150);
define('LLSET_ADMIN_IMG_MAX_H',	150);
$LLSET_UPLOAD_IMG_ETC_FILE_TAG = array('pdf'	=> '#ALT# (#FEXT# FILE)',);
$LLSET_FLD_FSINFO = array('user'			=> array('text',    '', 0, 0, 'ユーザー名',			'', ''),'pwd'			=> array('tarea',   '', 0, 0, 'パスワード',			'', ''),'user_type'		=> array('radio',   '', 0, 0, 'ユーザータイプ',		'', '', &$LLSET_LIST_USER_TYPE),'cmt'			=> array('text',    '', 0, 0, 'コメント',			'', ''),'ins_time'		=> array('datetime','', 0, 0, '登録日時',			'', ''),'upd_time'		=> array('datetime','', 0, 0, '更新日時',			'', ''),'remote_addr'	=> array('text',    '', 0, 0, 'REMORE ADDR',		'', ''),'user_agent'	=> array('text',    '', 0, 0, 'USER AGENT',			'', ''),);
$LLSET_TBL_FSINFO = array('fsinfo', &$LLSET_FLD_FSINFO, &$NULLS, 0, '', '', '', '',);
$LLSET_FLD_FETC = array('auth_name'			=> array('text', '', 0, 0, 'エリア名（メッセージ）', '', ''),'auth_name_enc'		=> array('sel',  '', 0, 0, 'エリア名文字コード',     '', '', &$LLSET_LIST_AUTH_NAME_ENC),'log_save'			=> array('text', '', 0, 0, 'アクセス記録保存件数',   '', ''),);
$LLSET_DEF_FETC = array('auth_name'			=>	'','auth_name_enc'		=>	LLSET_AUTH_NAME_ENC_SJIS,'log_save'			=>	'100',);
$LLSET_TBL_FETC = array('fetc', &$LLSET_FLD_FETC, &$LLSET_NULLS, 0, '', '', '', '',);
$LLSET_ALL = array('fsinfo'	=> array(&$LLSET_TBL_FSINFO,		''),'fetc'		=> array(&$LLSET_TBL_FETC,			''),);
?>