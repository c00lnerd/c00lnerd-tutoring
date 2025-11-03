@echo off
echo Starting Portable Python Learning Environment (Alternative Method)...
echo.

set BATCH_DIR=%~dp0

REM Check folders exist
if not exist "%BATCH_DIR%Python_Course" (
    echo ERROR: Python_Course folder not found!
    pause
    exit /b 1
)

if not exist "%BATCH_DIR%WPy64-312101" (
    echo ERROR: WPy64-312101 folder not found!
    pause
    exit /b 1
)

REM Start web server
echo Starting course website...
cd /d "%BATCH_DIR%Python_Course"
start "Python Course Website" cmd /k "python -m http.server 8000"

REM Wait and open browser
timeout /t 3 /nobreak >nul
echo Opening website in browser...
start http://localhost:8000

REM Try WinPython Command Prompt approach
echo.
echo Starting WinPython Command Prompt...
echo You can launch Spyder from there by typing: spyder
echo.

start "WinPython Command Prompt" "%BATCH_DIR%WPy64-312101\WinPython Command Prompt.exe"

echo.
echo ========================================
echo Python Learning Kit Started!
echo ========================================
echo 1. Website: http://localhost:8000 (should open automatically)
echo 2. WinPython Command Prompt opened
echo 3. In the command prompt, type: spyder
echo 4. Press Enter to launch Spyder IDE
echo.
echo Alternative: Use WinPython Control Panel
echo ========================================

REM Also try Control Panel as backup
timeout /t 2 /nobreak >nul
if exist "%BATCH_DIR%WPy64-312101\WinPython Control Panel.exe" (
    echo Opening WinPython Control Panel as backup...
    start "WinPython Control Panel" "%BATCH_DIR%WPy64-312101\WinPython Control Panel.exe"
)

echo.
echo Press any key to close this launcher...
pause
