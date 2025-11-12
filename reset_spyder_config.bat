@echo off
title Reset Spyder Configuration
echo ========================================
echo    Reset Spyder Configuration
echo ========================================
echo.

echo This will reset Spyder's configuration to fix startup issues.
echo.
echo WARNING: This will delete your Spyder settings and preferences.
echo Press Ctrl+C to cancel, or any other key to continue...
pause

echo.
echo Locating Spyder configuration folders...

REM Common Spyder config locations
set CONFIG1=%USERPROFILE%\.spyder-py3
set CONFIG2=%APPDATA%\spyder-py3
set CONFIG3=%LOCALAPPDATA%\spyder-py3

echo Checking for config folders...

if exist "%CONFIG1%" (
    echo Found config at: %CONFIG1%
    echo Renaming to backup...
    ren "%CONFIG1%" ".spyder-py3-backup-%date:~-4,4%%date:~-10,2%%date:~-7,2%"
)

if exist "%CONFIG2%" (
    echo Found config at: %CONFIG2%
    echo Renaming to backup...
    ren "%CONFIG2%" "spyder-py3-backup-%date:~-4,4%%date:~-10,2%%date:~-7,2%"
)

if exist "%CONFIG3%" (
    echo Found config at: %CONFIG3%
    echo Renaming to backup...
    ren "%CONFIG3%" "spyder-py3-backup-%date:~-4,4%%date:~-10,2%%date:~-7,2%"
)

echo.
echo Configuration reset complete!
echo Now trying to launch Spyder with fresh config...

REM Launch Spyder
set WINPY_DIR=D:\WPy64-312101
cd /d "%WINPY_DIR%"
start "" "%WINPY_DIR%\Spyder.exe"

echo.
echo Spyder should now start with default settings.
echo If it still doesn't work, there may be a deeper system issue.
pause
