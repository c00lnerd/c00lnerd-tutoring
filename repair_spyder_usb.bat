@echo off
title Repair Spyder on USB Drive
echo ========================================
echo    Repair Spyder on USB Drive
echo ========================================
echo.

set WINPY_DIR=D:\WPy64-312101
set SPYDER_PATH=%WINPY_DIR%\Spyder.exe
set PYTHON_PATH=%WINPY_DIR%\python\python.exe

echo Since Spyder worked before, let's restore it to working condition.
echo.

echo Step 1: Verify Spyder files exist
if not exist "%SPYDER_PATH%" (
    echo ✗ Spyder.exe not found at: %SPYDER_PATH%
    echo The installation may be corrupted. Consider reinstalling.
    pause
    exit
)
echo ✓ Spyder.exe found

echo.
echo Step 2: Clear Spyder configuration (common fix)
echo This will reset Spyder to default settings...

REM Clear user-specific Spyder configs
if exist "%USERPROFILE%\.spyder-py3" (
    echo Backing up and clearing .spyder-py3 config...
    ren "%USERPROFILE%\.spyder-py3" ".spyder-py3-backup-%date:~-4,4%%date:~-10,2%%date:~-7,2%-%time:~0,2%%time:~3,2%" 2>nul
)

if exist "%APPDATA%\spyder-py3" (
    echo Backing up and clearing AppData spyder config...
    ren "%APPDATA%\spyder-py3" "spyder-py3-backup-%date:~-4,4%%date:~-10,2%%date:~-7,2%-%time:~0,2%%time:~3,2%" 2>nul
)

echo.
echo Step 3: Register WinPython distribution
echo This fixes path issues for USB installations...
cd /d "%WINPY_DIR%"

if exist "%WINPY_DIR%\WinPython Control Panel.exe" (
    echo Running WinPython Control Panel to register distribution...
    start /wait "" "%WINPY_DIR%\WinPython Control Panel.exe"
    echo Please use the Control Panel to:
    echo 1. Click "Register distribution"
    echo 2. Close the Control Panel
    echo 3. Press any key here to continue...
    pause
) else (
    echo WinPython Control Panel not found, skipping registration...
)

echo.
echo Step 4: Set environment for USB execution
set PYTHONHOME=%WINPY_DIR%\python
set PYTHONPATH=%WINPY_DIR%\python\Lib;%WINPY_DIR%\python\Lib\site-packages
set PATH=%WINPY_DIR%\python;%WINPY_DIR%\python\Scripts;%PATH%

echo Environment variables set for this session.

echo.
echo Step 5: Launch Spyder with proper environment
echo Launching Spyder from its directory with fixed paths...
cd /d "%WINPY_DIR%"

echo Starting Spyder...
start "" "%SPYDER_PATH%"

echo.
echo Waiting 5 seconds to check if Spyder started...
timeout /t 5 /nobreak >nul

tasklist /fi "imagename eq Spyder.exe" 2>nul | find /i "Spyder.exe" >nul
if %errorlevel%==0 (
    echo ✓ SUCCESS: Spyder is running!
    echo Check your taskbar or Alt+Tab to find the Spyder window.
) else (
    echo ✗ Spyder still not starting. Trying alternative method...
    
    echo.
    echo Step 6: Launch via Python directly
    echo This bypasses the Spyder.exe wrapper...
    "%PYTHON_PATH%" -c "import sys; sys.path.insert(0, r'%WINPY_DIR%\python\Lib\site-packages'); import spyder.app.start; spyder.app.start.main()" 2>nul
    
    if %errorlevel%==0 (
        echo ✓ Spyder launched via Python!
    ) else (
        echo ✗ Still having issues. The installation may need to be refreshed.
        echo.
        echo Recommendations:
        echo 1. Copy your working PC Spyder installation to USB
        echo 2. Download fresh WinPython and extract to D:\
        echo 3. Use Jupyter Notebook as alternative
    )
)

echo.
echo Press any key to exit...
pause
