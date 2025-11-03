@echo off
title Python Course Learning Kit
echo ========================================
echo    Portable Python Course Environment
echo ========================================
echo.

REM Set up Python paths for WPy64-312101
set WINPY_DIR=%~dp0WPy64-312101
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
timeout /t 2 /nobreak >nul

if exist "%SPYDER_PATH%" (
    start "" "%SPYDER_PATH%"
    echo Spyder launched successfully!
) else (
    echo Launching Python IDLE...
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
