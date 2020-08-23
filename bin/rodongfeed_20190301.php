<?php
function proc_ftp_for_korea1($pdf_fname, $zip_fname, $pic_fname)
{
	$ftp = ftp_connect("123.111.233.94");
	if ($ftp === FALSE) {
		print "failure of the connect to ftp server (123.111.233.94).\n";
		return false;
	}

	$res = ftp_login($ftp, "kpm_news", "!kpmkpm201(");
	if ($res === FALSE) {
		print "failure of the login to ftp server (123.111.233.94).\n";
		ftp_close($ftp);
		return false;
	}

	$res = ftp_pasv($ftp, true);
	if ($res === FALSE) {
		print "failure of the change pasv mode.\n";
		ftp_close($ftp);
		return false;
	}

	ftp_set_option($ftp, FTP_TIMEOUT_SEC, 300);

	print "connected.(123.111.233.94)\n";

	$res = ftp_put($ftp, $pdf_fname, "C:/www.korea-copy.com/finish/".$pdf_fname, FTP_BINARY);
	if ($res === FALSE) {
		print "failure of the put file ($pdf_fname).\n";
		print_r(error_get_last());
		ftp_close($ftp);
		return false;
	}

	print "success of put the file $pdf_fname (123.111.233.94)\n";

	$res = ftp_put($ftp, $zip_fname, "C:/www.korea-copy.com/finish/".$zip_fname, FTP_BINARY);
	if ($res === FALSE) {
		print "failure of the put file ($zip_fname).\n";
		print_r(error_get_last());
		ftp_close($ftp);
		return false;
	}

	print "success of put the file $zip_fname (123.111.233.94)\n";

	$res = ftp_put($ftp, $pic_fname, "C:/www.korea-copy.com/finish/".$pic_fname, FTP_BINARY);
	if ($res === FALSE) {
		print "failure of the put file ($pic_fname).\n";
		print_r(error_get_last());
		ftp_close($ftp);
		return false;
	}

	print "success of put the file $pic_fname (123.111.233.94)\n";

	ftp_close($ftp);

	return true;
}

function main()
{
	$pdf_fname = date("Y.m.d") . ".pdf";
	$zip_fname = date("Y-m-d") . ".zip";
	$pic_fname = date("Y-m-d") . "(photo).zip";

	proc_ftp_for_korea1($pdf_fname, $zip_fname, $pic_fname);

	return true;
}

main();
exit;
?>
