@echo off
title Spyder Troubleshooter
echo ========================================
echo    Spyder Troubleshooter
echo ========================================
echo.

set WINPY_DIR=D:\WPy64-312101
set SPYDER_PATH=%WINPY_DIR%\Spyder.exe

echo This will try several solutions for Spyder not appearing:
echo.
echo 1. Check if Spyder is already running (hidden)
echo 2. Kill any existing Spyder processes
echo 3. Launch with different methods
echo 4. Check for window positioning issues
echo.

echo Step 1: Checking for existing Spyder processes...
tasklist /fi "imagename eq Spyder.exe" 2>nul | find /i "Spyder.exe" >nul
if %errorlevel%==0 (
    echo Found existing Spyder process! Killing it...
    taskkill /f /im Spyder.exe >nul 2>&1
    timeout /t 2 /nobreak >nul
) else (
    echo No existing Spyder processes found.
)

echo.
echo Step 2: Launching Spyder with window restoration...
cd /d "%WINPY_DIR%"

REM Try to restore any minimized windows first
powershell -command "Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.Interaction]::AppActivate('Spyder')" 2>nul

echo Launching Spyder...
start "" "%SPYDER_PATH%"

echo Waiting 3 seconds for Spyder to start...
timeout /t 3 /nobreak >nul

echo.
echo Step 3: Checking if Spyder started...
tasklist /fi "imagename eq Spyder.exe" 2>nul | find /i "Spyder.exe" >nul
if %errorlevel%==0 (
    echo ✓ Spyder is running! 
    echo.
    echo If you still can't see it, try:
    echo - Press Alt+Tab to cycle through windows
    echo - Check if it's minimized in the taskbar
    echo - Look for Spyder in the system tray (bottom right)
    echo - Try Win+D to show desktop, then click Spyder in taskbar
) else (
    echo ✗ Spyder failed to start.
    echo.
    echo Possible solutions:
    echo 1. Run reset_spyder_config.bat to reset settings
    echo 2. Try alternative_python_ide.bat for other options
    echo 3. Check Windows Event Viewer for error messages
    echo 4. Try running as Administrator
)

echo.
echo Press any key to exit...
pause
