@echo off
title Spyder Diagnostic Tool
echo ========================================
echo    Spyder Diagnostic Tool
echo ========================================
echo.

REM Set up paths
set WINPY_DIR=%~dp0WPy64-312101
set SPYDER_PATH=%WINPY_DIR%\Spyder.exe
set PYTHON_PATH=%WINPY_DIR%\python\python.exe

echo 1. Checking file existence...
if exist "%SPYDER_PATH%" (
    echo ✓ Spyder.exe found at: %SPYDER_PATH%
) else (
    echo ✗ Spyder.exe NOT found at: %SPYDER_PATH%
    goto :end
)

echo.
echo 2. Checking file properties...
dir "%SPYDER_PATH%"

echo.
echo 3. Checking Python installation...
if exist "%PYTHON_PATH%" (
    echo ✓ Python found at: %PYTHON_PATH%
    "%PYTHON_PATH%" --version
) else (
    echo ✗ Python NOT found at: %PYTHON_PATH%
)

echo.
echo 4. Testing Spyder with verbose output...
echo Running: "%SPYDER_PATH%" --help
"%SPYDER_PATH%" --help
echo Exit code: %ERRORLEVEL%

echo.
echo 5. Trying to launch Spyder with error capture...
echo Running Spyder and capturing any error messages...
"%SPYDER_PATH%" 2>&1
echo Spyder exit code: %ERRORLEVEL%

echo.
echo 6. Alternative: Try launching Python directly...
echo If Spyder fails, we can try Python IDLE or command line...
echo Press 1 for IDLE, 2 for Python command line, or any other key to exit
set /p choice="Your choice: "

if "%choice%"=="1" (
    echo Launching Python IDLE...
    "%PYTHON_PATH%" -m idlelib.idle
) else if "%choice%"=="2" (
    echo Launching Python command line...
    "%PYTHON_PATH%"
)

:end
echo.
echo Diagnostic complete. Press any key to exit...
pause
