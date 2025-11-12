@echo off
title Force Spyder to Stay Visible
echo ========================================
echo    Force Spyder Launcher
echo ========================================
echo.

REM Set up paths - using D: drive as shown in your diagnostic
set WINPY_DIR=D:\WPy64-312101
set SPYDER_PATH=%WINPY_DIR%\Spyder.exe
set PYTHON_PATH=%WINPY_DIR%\python\python.exe

echo Spyder is starting but closing immediately. Trying different launch methods...
echo.

echo Method 1: Launch with working directory set
cd /d "%WINPY_DIR%"
echo Current directory: %CD%
echo Launching Spyder from its own directory...
start /wait /max "Spyder IDE" "%SPYDER_PATH%"
timeout /t 3 /nobreak >nul

echo.
echo Method 2: Launch Spyder via Python module (if Method 1 didn't work)
echo This bypasses the .exe wrapper and runs Spyder directly through Python...
"%PYTHON_PATH%" -c "import spyder; spyder.main()"

echo.
echo Method 3: Launch with environment variables
set SPYDER_DEV=True
set PYTHONPATH=%WINPY_DIR%\python\Lib\site-packages
"%SPYDER_PATH%"

echo.
echo If none of these work, Spyder may have a configuration issue.
echo Try deleting Spyder's config folder and restarting.
pause
