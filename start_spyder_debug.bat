@echo off
title Debug Spyder Launch
echo ========================================
echo    Spyder Debug Launcher
echo ========================================
echo.

REM Set up Python paths for WPy64-312101
set WINPY_DIR=%~dp0WPy64-312101
set SPYDER_PATH=%WINPY_DIR%\Spyder.exe

echo Checking Spyder installation...
if not exist "%SPYDER_PATH%" (
    echo Spyder not found at: %SPYDER_PATH%
    pause
    exit
)

echo Found Spyder at: %SPYDER_PATH%
echo.

echo Method 1: Direct launch with start command
start "" "%SPYDER_PATH%"
timeout /t 5 /nobreak >nul

echo.
echo Method 2: Launch without start command (if Method 1 failed)
echo Press any key to try Method 2, or close this window if Spyder opened...
pause

"%SPYDER_PATH%"

echo.
echo Method 3: Launch from Spyder directory
cd /d "%WINPY_DIR%"
echo Current directory: %CD%
Spyder.exe

pause
