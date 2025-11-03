@echo off
echo Starting Portable Python Learning Environment (Simple Version)...
echo.

REM Get the current directory
set BATCH_DIR=%~dp0

echo Current Directory: %BATCH_DIR%

REM Start web server using WinPython Control Panel approach
echo Starting course website...
cd /d "%BATCH_DIR%Python_Course"
start "Python Course Website" cmd /k "python -m http.server 8000"

REM Wait and open browser
timeout /t 3 /nobreak >nul
echo Opening website in browser...
start http://localhost:8000

REM Start Spyder using WinPython Control Panel
echo Starting WinPython Control Panel...
if exist "%BATCH_DIR%WPy64-312101\WinPython Control Panel.exe" (
    start "WinPython Control Panel" "%BATCH_DIR%WPy64-312101\WinPython Control Panel.exe"
    echo.
    echo ========================================
    echo Instructions:
    echo 1. Website should open automatically
    echo 2. In WinPython Control Panel, click "Spyder"
    echo 3. Keep this window open while using the course
    echo ========================================
) else (
    echo ERROR: WinPython Control Panel not found!
    echo Please check that WPy64-312101 folder is present.
)

echo.
pause
