@echo off
set path=C:\Python27;%path%
set path=D:\Python27;%path%
set path=E:\Python27;%path%

::项目名称，用来作为压缩包名称和编译结果目录名称，各工程项目根据自己的编译结果修改
set BuildProjectTagName=ProjX

::生成版本信息
svn info --xml
set CodeManageType=%errorlevel%
if %CodeManageType% equ 0 goto SVNGETVER
if %CodeManageType% equ 1 goto GITGETVER

:SVNGETVER
echo SVNGETVER
::svn方式获取版本信息文件
cd ..
svn info --xml>./build/Version.xml
cd build
goto MKREMOTDIR

:GITGETVER
echo GITGETVER
::git方式获取版本信息文件
For /f "tokens=1* delims=_" %%1 in ('reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Git_is1" /v "InstallLocation"^| findstr /i "InstallLocation"') Do (
  For /f "tokens=1*" %%3  in ("%%~2") Do (
    SET GIT_PATH=%%4
  )
)

COPY /y "./git_ver.sh" "../git_ver.sh"

SET GIT_PATH="%GIT_PATH%bin\sh.exe" --login -i
cd ..
call %GIT_PATH% ./git_ver.sh
del git_ver.sh /Q
xcopy /y .\Version.xml .\build\
cd ./build
goto MKREMOTDIR

:MKREMOTDIR
xcopy .\Version.xml ..\bin\ /y

::检查vs编译环境
if not exist "%VS90COMNTOOLS%vsvars32.bat" goto missing
call "%VS90COMNTOOLS%vsvars32.bat"

::编译前的文件拷贝
cd ..\
call mkbin.bat
cd .\build

::编译
cd ..\
call vcbuild.exe ".\%BuildProjectTagName%.sln"   "%1|Win32" /rebuild
cd .\build

::依赖项拷贝
call .\copy_dll_to_bin.bat %1

::打包
rd .\BuildResult /s /q
:::执行文件拷贝
mkdir .\BuildResult
mkdir .\BuildResult\%BuildProjectTagName%

xcopy /e /exclude:ExcludeFileList.txt /y ..\bin .\BuildResult\%BuildProjectTagName%\
:::调试文件拷贝
mkdir .\BuildResult\pdb
xcopy ..\bin\*.pdb .\BuildResult\pdb\

xcopy ..\Depend\mysql\*.pdb .\BuildResult\pdb\ /y
xcopy ..\Depend\sh\*.pdb .\BuildResult\pdb\ /y

call .\zip_bin.bat %BuildProjectTagName% 

goto :eof

:missing 
echo the visual studio install is missing. 
goto :eof
