@echo off
echo.
echo ========================================
echo   C00lnerd Python Course - Complete Setup
echo ========================================
echo.
echo Starting Python learning environment...
echo.
echo This will:
echo 1. Start Spyder (Python IDE)  
echo 2. Open the course website with Lesson 12
echo.
echo ========================================
echo.

REM Set up environment variables like the original
set SPYDER_PATH=%~dp0WPy64-312101\Scripts\spyder.exe
set PYTHON_PATH=%~dp0WPy64-312101\python.exe

REM Start the web server from the NEW dist folder
echo Starting course website server...
if exist "%~dp0dist" (
    cd /d "%~dp0dist"
    echo Serving from: %CD%
    start /B python -m http.server 8000
) else (
    echo Warning: dist folder not found, trying Python_Course folder...
    cd /d "%~dp0Python_Course"
    start /B python -m http.server 8000
)

REM Wait a moment for server to start
timeout /t 3 /nobreak >nul

REM Open the website in default browser
echo Opening course website...
start http://localhost:8000

REM Start Spyder using the same logic as working version
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
echo Setup Complete!
echo.
echo - Spyder is starting for Python coding
echo - Website is available at: http://localhost:8000
echo - Press any key to close this window
echo ========================================
pause >nul
