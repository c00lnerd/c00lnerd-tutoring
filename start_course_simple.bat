@echo off
echo.
echo ========================================
echo   C00lnerd Python Course - UPDATED
echo ========================================
echo.

REM Copy the exact Spyder startup from the working version
echo Starting Spyder IDE...
timeout /t 2 /nobreak >nul

if exist "%SPYDER_PATH%" (
    start "" "%SPYDER_PATH%"
    echo Spyder launched successfully!
) else (
    echo Launching Python IDLE...
    start "" cmd /c ""%PYTHON_PATH%" -m idlelib.idle"
)

REM Start the NEW website server
echo Starting UPDATED course website (with Lesson 12)...
cd /d "%~dp0dist"
echo Serving from: %CD%
start /B python -m http.server 8001

REM Wait and open browser
timeout /t 3 /nobreak >nul
echo Opening updated website...
start http://localhost:8001

echo.
echo ========================================
echo Setup Complete!
echo.
echo - Spyder: Started using original method
echo - Website: http://localhost:8001 (NEW VERSION)
echo - Press any key to close this window
echo ========================================
pause >nul
