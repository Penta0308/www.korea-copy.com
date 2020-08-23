@echo on

cd C:\www.korea-copy.com\minju\ftpdata

"C:\Program Files (x86)\WinSCP\WinScp.exe" /console /script=C:\www.korea-copy.com\bin\get_minju_complete.winscp /parameter %date:~0,4% %date:~5,2% %date:~8,2%

if exist minju_complete.txt (
   echo "minju_complete.txt exist"
  "C:\Program Files (x86)\WinSCP\WinScp.exe" /console /script=C:\www.korea-copy.com\bin\get_minju.winscp /parameter %date:~0,4% %date:~5,2% %date:~8,2%
  cd C:\www.korea-copy.com\bin
  php C:\www.korea-copy.com\bin\mailrecv_test.php
) else (
  echo "minju_complete.txt nothing"
)

cd C:\www.korea-copy.com\bin
