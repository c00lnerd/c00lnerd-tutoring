@echo off
title Copy Working Spyder to USB
echo ========================================
echo    Copy Working Spyder to USB
echo ========================================
echo.

echo Since Spyder works on your PC, let's copy that installation to USB.
echo.

echo Step 1: Find your working WinPython installation
echo Common locations for WinPython on PC:
echo.

set FOUND_WINPY=

REM Check common installation locations
if exist "C:\WPy64-312101" (
    echo ✓ Found: C:\WPy64-312101
    set FOUND_WINPY=C:\WPy64-312101
)

if exist "C:\WinPython\WPy64-312101" (
    echo ✓ Found: C:\WinPython\WPy64-312101
    set FOUND_WINPY=C:\WinPython\WPy64-312101
)

if exist "%USERPROFILE%\WPy64-312101" (
    echo ✓ Found: %USERPROFILE%\WPy64-312101
    set FOUND_WINPY=%USERPROFILE%\WPy64-312101
)

if exist "C:\Program Files\WinPython\WPy64-312101" (
    echo ✓ Found: C:\Program Files\WinPython\WPy64-312101
    set FOUND_WINPY=C:\Program Files\WinPython\WPy64-312101
)

if defined FOUND_WINPY (
    echo.
    echo Found working WinPython at: %FOUND_WINPY%
    echo.
    echo Step 2: Copy to USB drive
    echo This will replace the current D:\WPy64-312101 installation
    echo.
    echo WARNING: This will delete D:\WPy64-312101 and replace it
    echo Press Ctrl+C to cancel, or any key to continue...
    pause
    
    echo.
    echo Backing up any custom files from USB installation...
    if exist "D:\WPy64-312101\notebooks" (
        if not exist "D:\USB_Backup" mkdir "D:\USB_Backup"
        xcopy "D:\WPy64-312101\notebooks\*" "D:\USB_Backup\notebooks\" /E /I /Y >nul 2>&1
        echo ✓ Notebooks backed up to D:\USB_Backup\
    )
    
    echo.
    echo Removing old USB installation...
    if exist "D:\WPy64-312101" (
        rmdir /s /q "D:\WPy64-312101" 2>nul
    )
    
    echo.
    echo Copying working installation from PC to USB...
    echo This may take several minutes...
    xcopy "%FOUND_WINPY%\*" "D:\WPy64-312101\" /E /I /Y /H
    
    if %errorlevel%==0 (
        echo ✓ Copy completed successfully!
        
        echo.
        echo Step 3: Test the copied installation
        if exist "D:\WPy64-312101\Spyder.exe" (
            echo ✓ Spyder.exe found in copied installation
            echo.
            echo Launching Spyder to test...
            cd /d "D:\WPy64-312101"
            start "" "D:\WPy64-312101\Spyder.exe"
            
            echo.
            echo If Spyder opens successfully, the copy worked!
            echo Your working PC installation is now on the USB drive.
        ) else (
            echo ✗ Copy may have failed - Spyder.exe not found
        )
    ) else (
        echo ✗ Copy failed. You may need administrator privileges.
        echo Try running this script as Administrator.
    )
    
) else (
    echo.
    echo ✗ Could not find working WinPython installation on PC
    echo.
    echo Please manually locate your working WinPython folder and:
    echo 1. Copy the entire folder to D:\
    echo 2. Rename it to WPy64-312101
    echo 3. Test by running D:\WPy64-312101\Spyder.exe
    echo.
    echo Common places to look:
    echo - C:\WPy64-*
    echo - C:\WinPython\
    echo - %USERPROFILE%\WPy64-*
    echo - C:\Program Files\WinPython\
)

echo.
echo Press any key to exit...
pause
