@echo off
echo Starting Portable Python Learning Environment...
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

REM Start web server using simple approach
echo Starting course website...
cd /d "%BATCH_DIR%Python_Course"
start "Python Course Website" cmd /k "python -m http.server 8000"

REM Wait and open browser
timeout /t 3 /nobreak >nul
echo Opening website in browser...
start http://localhost:8000

REM Launch WinPython Control Panel for Spyder access
echo.
echo Launching WinPython Control Panel...
if exist "%BATCH_DIR%WPy64-312101\WinPython Control Panel.exe" (
    start "WinPython Control Panel" "%BATCH_DIR%WPy64-312101\WinPython Control Panel.exe"
    echo.
    echo ========================================
    echo SUCCESS! Python Learning Kit Started!
    echo ========================================
    echo 1. Website opened at: http://localhost:8000
    echo 2. WinPython Control Panel opened
    echo 3. Click "Spyder" button in the control panel
    echo 4. Keep this window open while learning
    echo ========================================
) else (
    echo ERROR: WinPython Control Panel not found!
    echo Trying alternative Spyder launch methods...
    
    REM Try direct Spyder launch
    if exist "%BATCH_DIR%WPy64-312101\Spyder.exe" (
        echo Found Spyder.exe, launching...
        start "Spyder IDE" "%BATCH_DIR%WPy64-312101\Spyder.exe"
    ) else if exist "%BATCH_DIR%WPy64-312101\Scripts\spyder.exe" (
        echo Found spyder.exe in Scripts, launching...
        start "Spyder IDE" "%BATCH_DIR%WPy64-312101\Scripts\spyder.exe"
    ) else (
        echo Could not find Spyder executable!
        echo Please run debug_winpython.bat to see folder structure
    )
)

echo.
echo Press any key to close this launcher...
pause
