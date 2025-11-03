@echo off
echo Debugging WinPython Structure...
echo.

set BATCH_DIR=%~dp0

echo Current Directory: %BATCH_DIR%
echo.

echo Checking WPy64-312101 folder contents:
if exist "%BATCH_DIR%WPy64-312101" (
    echo WPy64-312101 folder exists!
    echo.
    echo Contents of WPy64-312101:
    dir "%BATCH_DIR%WPy64-312101" /b
    echo.
    
    echo Looking for Spyder executables:
    if exist "%BATCH_DIR%WPy64-312101\Spyder.exe" (
        echo FOUND: Spyder.exe in root
    ) else (
        echo NOT FOUND: Spyder.exe in root
    )
    
    if exist "%BATCH_DIR%WPy64-312101\Scripts\spyder.exe" (
        echo FOUND: spyder.exe in Scripts folder
    ) else (
        echo NOT FOUND: spyder.exe in Scripts folder
    )
    
    if exist "%BATCH_DIR%WPy64-312101\WinPython Control Panel.exe" (
        echo FOUND: WinPython Control Panel.exe
    ) else (
        echo NOT FOUND: WinPython Control Panel.exe
    )
    
    echo.
    echo Checking for Python executable:
    if exist "%BATCH_DIR%WPy64-312101\python.exe" (
        echo FOUND: python.exe in root
    ) else (
        echo NOT FOUND: python.exe in root
    )
    
    echo.
    echo Checking subdirectories:
    for /d %%i in ("%BATCH_DIR%WPy64-312101\*") do (
        echo Subdirectory: %%~ni
    )
    
) else (
    echo ERROR: WPy64-312101 folder not found!
)

echo.
pause
