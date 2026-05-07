@echo off

set CURR_DIR=%~dp0
set FILE=FeiTV.exe
set ICON=icon.ico
set TARGET_PATH=%CURR_DIR%%FILE%
set ICON_PATH=%CURR_DIR%%ICON%

echo %TARGET_PATH%
echo %ICON_PATH%

powershell -Command "$shell = New-Object -ComObject WScript.Shell; $shortcut = $shell.CreateShortcut([Environment]::GetFolderPath('Desktop')+'\FeiTV.lnk'); $shortcut.TargetPath = $env:TARGET_PATH; $shortcut.WorkingDirectory = $env:CURR_DIR; $shortcut.IconLocation = $env:ICON_PATH; $shortcut.Save();"