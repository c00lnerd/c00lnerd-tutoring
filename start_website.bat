@echo off
echo.
echo ========================================
echo   C00lnerd Tutoring Website - LATEST
echo ========================================
echo.
echo Starting local web server for UPDATED website...
echo This includes Lesson 12: Fractals and Recursion!
echo.
echo INSTRUCTIONS:
echo 1. Wait for "Serving HTTP" message below
echo 2. Open your web browser
echo 3. Go to: http://localhost:8000
echo 4. Press Ctrl+C here to stop the server
echo.
echo ========================================
echo.

cd /d "%~dp0dist"
echo Serving from: %CD%
python -m http.server 8000
