<?php

error_reporting(E_ALL);

print "start.\n";

	$ftp = ftp_ssl_connect("175.45.176.12");
print "[0]";
	if ($ftp === FALSE) {
		print "failure of the connect to ftp server (175.45.176.12).\n";
		return false;
	}
print "[1]";

	$res = ftp_login($ftp, "kpeicftp", "kpeic123");
	if ($res === FALSE) {
		print "failure of the login to ftp server (175.45.176.12).\n";
		ftp_close($ftp);
		return false;
	}

print "[2]";

	$res = ftp_pasv($ftp, true);
	if ($res === FALSE) {
		print "failure of the change pasv mode.\n";
		ftp_close($ftp);
		return false;
	}

	print "[current directory]".ftp_pwd($ftp)."\n";

	$res = ftp_chdir($ftp, "media");
	if ($res === FALSE) {
		print "failure of the change directory (media).\n";
		ftp_close($ftp);
		return false;
	}

	print "[current directory]".ftp_pwd($ftp)."\n";

	print "connected.\n";

	$remote_pdf_fname = "Minju ".date("Y-m-d").".pdf";
	$local_pdf_fname = "C:\\www.korea-copy.com\\minju\\".date('Y')."\\data\\".$remote_pdf_fname;
	$remote_zip_fname = "Minju ".date("Y-n-j").".zip";
	$local_zip_fname = "C:\\www.korea-copy.com\\minju\\ftpdata\\".$remote_zip_fname;

	$res = ftp_get($ftp, "minju_complete.txt",  "minju_complete.txt", FTP_BINARY);
	if ($res === FALSE) {
		print "failure of the get complete file.\n";
		ftp_close($ftp);
		return false;
	}

	$res = ftp_get($ftp, $local_pdf_fname,  $remote_pdf_fname, FTP_BINARY);
	if ($res === FALSE) {
		print "failure of the get pdf file.\n";
		ftp_close($ftp);
		return false;
	}

	$res = ftp_get($ftp, $local_zip_fname,  $remote_zip_fname, FTP_BINARY);
	if ($res === FALSE) {
		print "failure of the get zip file.\n";
		ftp_close($ftp);
		return false;
	}

	print "download complete.\n";

	ftp_close($ftp);

print "done.\n";
exit;

