@echo on

cd C:\www.korea-copy.com\minju\ftpdata

"C:\Program Files (x86)\WinSCP\WinScp.exe" /console /script=C:\www.korea-copy.com\bin\get_munhak_complete.winscp /parameter %date:~0,4% %date:~5,2% %date:~8,2%

if exist Munhak_complete.txt (
   echo "Munhak_complete.txt exist"
  "C:\Program Files (x86)\WinSCP\WinScp.exe" /console /script=C:\www.korea-copy.com\bin\get_munhak.winscp /parameter %date:~0,4% %date:~5,2% %date:~8,2%
  cd C:\www.korea-copy.com\bin
  php C:\www.korea-copy.com\bin\mailrecv_test2.php
) else (
  echo "munhak_complete.txt nothing"
)


cd C:\www.korea-copy.com\bin
