<?php
//phpinfo();

$url = "http://www.dprkmedia.net/images/rodong/latest/l.jpg";

$basic = array(
'User-Agent: KPM latest pic agent 1.0',
'Content-Type: application/x-www-form-urlencoded',
'Authorization: Basic '.base64_encode('latestpic:d3JJaj48'),
);

$options = array('http' => array(
'method' => 'GET',
'header' => implode("\r\n", $basic)
));

//var_dump($options);
header("Content-Type: image/jpeg\r\n");
$ret =  file_get_contents($url, false, stream_context_create($options));
//var_dump($http_response_header);
print $ret;
