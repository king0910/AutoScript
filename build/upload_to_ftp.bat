@echo off
setlocal enabledelayedexpansion 
::设置参数
set "ftp_site=%FTPSIT%"
set "ftp_port=%FTPPORT%"
set "ftp_id=%FTPUSER%"
set "ftp_pwd=%FTPPWD%"
set "ftp_local_dir=.\"
set "ftp_filename=%1"
set "ftp_remotepath=%2"

python upload_to_ftp.py %ftp_filename% %ftp_remotepath% %ftp_site% %ftp_id% %ftp_pwd% %ftp_port%

::判断ftp执行结果，目前判断语句还有问题
IF %errorlevel% EQU 0 (
@echo upload to ftp succeed!
@echo on
@exit /b 0
)ELSE (
@echo upload to ftp failed!
@echo on
@exit /b 1)