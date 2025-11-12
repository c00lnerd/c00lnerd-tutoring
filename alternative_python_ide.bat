@echo off
title Alternative Python IDE Launcher
echo ========================================
echo    Alternative Python IDE Options
echo ========================================
echo.

REM Set up paths
set WINPY_DIR=%~dp0WPy64-312101
set PYTHON_PATH=%WINPY_DIR%\python\python.exe

echo Since Spyder isn't working, here are alternatives:
echo.
echo 1. Python IDLE (Built-in IDE)
echo 2. Jupyter Notebook (Web-based)
echo 3. Jupyter Lab (Advanced web-based)
echo 4. VS Code (If available)
echo 5. Python Command Line
echo 6. Try installing Spyder via pip
echo.

set /p choice="Choose an option (1-6): "

if "%choice%"=="1" (
    echo Launching Python IDLE...
    start "" "%PYTHON_PATH%" -m idlelib.idle
) else if "%choice%"=="2" (
    echo Launching Jupyter Notebook...
    cd /d "%~dp0"
    start "" "%WINPY_DIR%\Jupyter Notebook.exe"
) else if "%choice%"=="3" (
    echo Launching Jupyter Lab...
    cd /d "%~dp0"
    start "" "%WINPY_DIR%\Jupyter Lab.exe"
) else if "%choice%"=="4" (
    echo Launching VS Code...
    start "" "%WINPY_DIR%\VS Code.exe"
) else if "%choice%"=="5" (
    echo Launching Python Command Line...
    start "" cmd /k ""%PYTHON_PATH%""
) else if "%choice%"=="6" (
    echo Installing Spyder via pip...
    "%PYTHON_PATH%" -m pip install spyder
    echo.
    echo Now trying to launch Spyder...
    "%PYTHON_PATH%" -m spyder
) else (
    echo Invalid choice. Exiting...
)

echo.
pause
