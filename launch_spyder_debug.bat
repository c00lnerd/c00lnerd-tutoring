@echo off
echo Testing Spyder Launch...
echo.

set BATCH_DIR=%~dp0

echo Batch Directory: %BATCH_DIR%

echo.
echo Attempting to launch Spyder with detailed output...
echo.

REM Try launching Spyder with visible console output
echo Method 1: Direct Spyder.exe launch
"%BATCH_DIR%WPy64-312101\Spyder.exe"

echo.
echo If Spyder didn't start, trying WinPython Control Panel...
pause

echo Method 2: WinPython Control Panel
"%BATCH_DIR%WPy64-312101\WinPython Control Panel.exe"

echo.
pause
