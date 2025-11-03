@echo off
echo Starting Portable Python Learning Environment...
echo (Using the method that worked before)
echo.

REM Get current directory
set BATCH_DIR=%~dp0

REM Start web server the simple way that worked before
echo Starting course website...
cd /d "%BATCH_DIR%Python_Course"
start "Python Course Website" cmd /k "python -m http.server 8000"

REM Wait a bit
timeout /t 3 /nobreak >nul

REM Open browser
echo Opening website...
start http://localhost:8000

REM Launch WinPython Control Panel (the way that worked before)
echo.
echo Launching WinPython Control Panel...
start "WinPython Control Panel" "%BATCH_DIR%WPy64-312101\WinPython Control Panel.exe"

echo.
echo ========================================
echo SUCCESS! Everything should be running:
echo ========================================
echo 1. Website at: http://localhost:8000
echo 2. WinPython Control Panel opened
echo 3. Click "Spyder" in the control panel
echo.
echo This is the same method that worked before!
echo ========================================
echo.
pause
