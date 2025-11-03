@echo off
echo Starting Portable Python Learning Environment...
echo.

REM Get the current directory where this batch file is located
set BATCH_DIR=%~dp0

echo Batch Directory: %BATCH_DIR%

REM Check if Python_Course folder exists
if not exist "%BATCH_DIR%Python_Course" (
    echo ERROR: Python_Course folder not found!
    echo Please make sure the Python_Course folder is in the same directory as this batch file.
    pause
    exit /b 1
)

REM Check if WPy64-312101 folder exists
if not exist "%BATCH_DIR%WPy64-312101" (
    echo ERROR: WPy64-312101 folder not found!
    echo Please make sure the WPy64-312101 folder is in the same directory as this batch file.
    pause
    exit /b 1
)

REM Start the Python HTTP server for the course website using WinPython
echo Starting course website...
REM Use the python subdirectory we found
if exist "%BATCH_DIR%WPy64-312101\python\python.exe" (
    start "Python Course Website" "%BATCH_DIR%WPy64-312101\python\python.exe" -m http.server 8000 -d "%BATCH_DIR%Python_Course"
) else (
    echo Python not found in expected location, trying simple approach...
    cd /d "%BATCH_DIR%Python_Course"
    start "Python Course Website" cmd /k "python -m http.server 8000"
)

REM Wait a moment for the server to start
echo Waiting for web server to start...
timeout /t 5 /nobreak >nul

REM Open the website in the default browser
echo Opening website in browser...
start http://localhost:8000

REM Start Spyder IDE using WinPython
echo Starting Spyder IDE...
echo Found Spyder.exe, launching now...
start "Spyder IDE" "%BATCH_DIR%WPy64-312101\Spyder.exe"

echo.
echo ========================================
echo Portable Python Learning Kit Started!
echo ========================================
echo Website: http://localhost:8000
echo Spyder IDE: Starting up...
echo.
echo Note: Spyder may take 30-60 seconds to initialize
echo Keep this window open while using the course
echo Press any key to close this window when done...
echo ========================================
echo.
pause
