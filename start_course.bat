@echo off
title Python Course Learning Kit
echo ========================================
echo    Portable Python Course Environment
echo ========================================
echo.

REM Set up Python paths for WPy64-312101
REM Check if WinPython is on D: drive (USB/external) or local directory
if exist "D:\WPy64-312101\Spyder.exe" (
    set WINPY_DIR=D:\WPy64-312101
) else (
    set WINPY_DIR=%~dp0WPy64-312101
)
set PYTHON_PATH=%WINPY_DIR%\python\python.exe
set SPYDER_PATH=%WINPY_DIR%\Spyder.exe

echo Checking Python installation...
if not exist "%PYTHON_PATH%" (
    echo Python not found at: %PYTHON_PATH%
    pause
    exit
)

echo Found Python at: %PYTHON_PATH%
echo.

echo Starting Python Course Website...
cd /d "%~dp0Python_Course"
start /min cmd /c ""%PYTHON_PATH%" -m http.server 8000"

echo Starting Spyder IDE...
echo Spyder path: %SPYDER_PATH%
timeout /t 2 /nobreak >nul

if exist "%SPYDER_PATH%" (
    echo Found Spyder at: %SPYDER_PATH%
    echo Attempting to launch Spyder...
    start "" "%SPYDER_PATH%"
    timeout /t 3 /nobreak >nul
    echo Spyder launch command executed!
    echo If Spyder doesn't appear, try running it manually from:
    echo %SPYDER_PATH%
) else (
    echo Spyder not found at: %SPYDER_PATH%
    echo Launching Python IDLE instead...
    start "" cmd /c ""%PYTHON_PATH%" -m idlelib.idle"
)

echo.
echo ========================================
echo  Ready to Learn Python!
echo ========================================
echo.
echo Website: http://localhost:8000
echo Python IDE: Running
echo.
pause

start http://localhost:8000
