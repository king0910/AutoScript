set FTPSIT=127.0.0.1
set FTPPORT=21
set FTPUSER=k
set FTPPWD=k

::项目名称，用来作为压缩包名称和编译结果目录名称，各工程项目根据自己的编译结果修改
::eg ProjX
set BuildProjectTagName=ProjX
::ftp远程路径
::eg /ProjX/ 或者 /ProjX/trunk/
set RemotePath=/ProjX/

call build_pkg_windows.bat Release
call upload_to_ftp.bat %BuildProjectTagName%.zip %RemotePath%