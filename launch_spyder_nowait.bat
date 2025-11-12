@echo off
title Launch Spyder (No Wait)
echo ========================================
echo    Launch Spyder Without Waiting
echo ========================================
echo.

REM Set up paths
set WINPY_DIR=D:\WPy64-312101
set SPYDER_PATH=%WINPY_DIR%\Spyder.exe

echo Method 1: Launch Spyder without waiting (should work)
cd /d "%WINPY_DIR%"
echo Current directory: %CD%
echo Launching Spyder...
start "" "%SPYDER_PATH%"
echo Spyder launch command sent!

timeout /t 5 /nobreak >nul

echo.
echo Checking if Spyder is now running...
tasklist /fi "imagename eq Spyder.exe" 2>nul | find /i "Spyder.exe" >nul
if %errorlevel%==0 (
    echo ✓ SUCCESS: Spyder.exe is running in Task Manager!
    echo Check your taskbar - Spyder should be visible now.
) else (
    echo ✗ Spyder.exe not found in Task Manager
    echo Trying alternative launch method...
    
    echo.
    echo Method 2: Launch with explicit window state
    start /max "" "%SPYDER_PATH%"
    timeout /t 3 /nobreak >nul
    
    echo Checking again...
    tasklist /fi "imagename eq Spyder.exe" 2>nul | find /i "Spyder.exe" >nul
    if %errorlevel%==0 (
        echo ✓ SUCCESS: Spyder is now running!
    ) else (
        echo ✗ Still not working. This may be a deeper issue.
        echo Try running reset_spyder_config.bat next.
    )
)

echo.
echo Press any key to exit...
pause
