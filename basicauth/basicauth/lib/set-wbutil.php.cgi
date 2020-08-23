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
define('LLUTL_DIRNM_WB',			'basicauth');
define('LLUTL_DIRNM_BASE',			'base');
define('LLUTL_DIRNM_DATA',			'data');
define('LLUTL_DIRNM_DIMG',			'dimg');
define('LLUTL_DIRNM_WIMG',			'wimg');
define('LLUTL_DIR_WB',				TOP_DIR.LLUTL_DIRNM_WB.'/');
define('LLUTL_DIR_BASE',			LLUTL_DIR_WB.LLUTL_DIRNM_BASE.'/');
define('LLUTL_DIR_BASE_SDAT',		LLUTL_DIR_BASE.LLUTL_DIRNM_DATA.'/');
define('LLUTL_DIR_SDAT',			LLUTL_DIR_WB.MYDIRNM.'/'.LLUTL_DIRNM_DATA.'/');
define('LLUTL_DIR_DIMG',			LLUTL_DIR_WB.MYDIRNM.'/'.LLUTL_DIRNM_DIMG.'/');
define('LLUTL_DIR_WIMG',			LLUTL_DIR_WB.MYDIRNM.'/'.LLUTL_DIRNM_WIMG.'/');
define('LLUTL_FLIST_FILE_BASE_ETC',	LLUTL_DIR_BASE.'etc.txt');
define('LLUTL_SUEXEC',			true/*posix_getuid() == fileowner(__FILE__)*/);
define('LLUTL_STRIPSLASHES',	get_magic_quotes_gpc());
define('LLUTL_SITE_ID',			fileinode(__FILE__));
ini_set('display_errors',		TRUE);
define('LLUTL_CHK_HTML_IF',		TRUE);
define('LLUTL_FEXIST_TYPE',		0);
define('LLUTL_LOCK_TYPE',		0);
define('LLUTL_LOG_PATH',		LLUTL_DIR_BASE_SDAT.'/log/log');
define('LLUTL_SESSION_DIR',		LLUTL_DIR_BASE_SDAT.'/ses/');
define('LLUTL_MYACT_EXT',		array_pop(explode('.', MYACT)));
define('LLUTL_MYADMIN',			'basicauth.'.LLUTL_MYACT_EXT);
define('LLUTL_SITE_TITLE',		defined('SET_SITE_TITLE')    ? SET_SITE_TITLE : '');
define('LLUTL_URL_PTOP',		defined('SET_SITE_TOP_URL')  ? SET_SITE_TOP_URL : TOP_DIR);
define('LLUTL_URL_PTOP2',		defined('SET_SITE_TOP_URL2') ? SET_SITE_TOP_URL2 : TOP_DIR);
define('LLUTL_URL_ADMIN',		defined('SET_SITE_TOP_URL2') ? SET_SITE_TOP_URL2.LLUTL_DIRNM_WB.'/'.LLUTL_DIRNM_BASE.'/'.LLUTL_MYADMIN
: TOP_DIR.LLUTL_DIRNM_WB.'/'.LLUTL_DIRNM_BASE.'/'.LLUTL_MYADMIN);
define('LLUTL_DB_CONNECT_STR',	defined('SET_SITE_DB')       ? SET_SITE_DB : '');
define('LLUTL_MEMORY_LIMIT_MB',	256);
$mlimit = (int)str_replace('M', '000', ini_get('memory_limit'));
if (0 <= $mlimit && $mlimit < LLUTL_MEMORY_LIMIT_MB * 1000) { @ini_set('memory_limit', LLUTL_MEMORY_LIMIT_MB.'M'); }
if (LLUTL_SUEXEC){define('LLUTL_MODE_MKDIR',	0700);
define('LLUTL_MODE_MKFIL',	0600);
define('LLUTL_MODE_MKIMD',	0755);
define('LLUTL_MODE_MKIMG',	0644);
define('LLUTL_MODE_MKLGD',	0700);
define('LLUTL_MODE_MKLOG',	0600);}
else{define('LLUTL_MODE_MKDIR',	0755);
define('LLUTL_MODE_MKFIL',	0644);
define('LLUTL_MODE_MKIMD',	0755);
define('LLUTL_MODE_MKIMG',	0644);
define('LLUTL_MODE_MKLGD',	0777);
define('LLUTL_MODE_MKLOG',	0666);}
ini_set('session.name',				'pses');
ini_set('session.cache_limiter',	'none');
ini_set('session.gc_maxlifetime',	'3600');
ini_set('session.use_cookies',		1);
ini_set('session.use_only_cookies',	1);
ini_set('session.use_trans_sid',	0);
if (@constant('WBADMIN') === TRUE && @constant('SET_SITE_ADMIN_SSL_ONLY') === TRUE){ini_set('session.cookie_secure', 1);
ini_set('session.name',	'psec');}
if (file_exists(dirname(__FILE__).'/sample.php.cgi')){define('SET_SITE_UPDATE_MODE',	'SAMPLE');}
?>