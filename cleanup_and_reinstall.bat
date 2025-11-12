@echo off
title WinPython Drive Reinstall Helper
echo ========================================
echo    WinPython Drive Reinstall Helper
echo ========================================
echo.

echo This will help you reinstall WinPython to work properly from the USB drive.
echo.

echo Current situation:
echo - WinPython works on PC (local installation)
echo - WinPython on D: drive (USB) has issues with Spyder
echo.

echo Step 1: Backup current course files
echo Creating backup of important files...

if exist "D:\WPy64-312101" (
    echo Found WinPython on D: drive
    
    REM Create backup directory
    if not exist "D:\WinPython_Backup" mkdir "D:\WinPython_Backup"
    
    echo Backing up any custom scripts or notebooks...
    if exist "D:\WPy64-312101\notebooks" (
        xcopy "D:\WPy64-312101\notebooks\*" "D:\WinPython_Backup\notebooks\" /E /I /Y >nul 2>&1
        echo ✓ Notebooks backed up
    )
    
    if exist "D:\WPy64-312101\scripts" (
        xcopy "D:\WPy64-312101\scripts\*" "D:\WinPython_Backup\scripts\" /E /I /Y >nul 2>&1
        echo ✓ Scripts backed up
    )
    
    echo.
    echo Step 2: Remove current WinPython installation
    echo WARNING: This will delete D:\WPy64-312101
    echo Press Ctrl+C to cancel, or any key to continue...
    pause
    
    echo Removing old installation...
    rmdir /s /q "D:\WPy64-312101" 2>nul
    if exist "D:\WPy64-312101" (
        echo ⚠ Could not fully remove old installation. You may need to delete manually.
    ) else (
        echo ✓ Old installation removed
    )
) else (
    echo No WinPython found on D: drive
)

echo.
echo Step 3: Download and install fresh WinPython
echo.
echo Please follow these steps:
echo.
echo 1. Go to: https://winpython.github.io/
echo 2. Download: WinPython 3.12.x (64-bit) - latest version
echo 3. Run the installer and choose D:\ as the installation location
echo 4. Make sure to select "Add to PATH" if prompted
echo 5. After installation, run test_new_installation.bat
echo.

echo Creating test script for after installation...
echo @echo off > test_new_installation.bat
echo title Test New WinPython Installation >> test_new_installation.bat
echo echo Testing new WinPython installation... >> test_new_installation.bat
echo. >> test_new_installation.bat
echo set WINPY_DIR=D:\WPy64-312101 >> test_new_installation.bat
echo if exist "%%WINPY_DIR%%\Spyder.exe" ( >> test_new_installation.bat
echo     echo ✓ Spyder found >> test_new_installation.bat
echo     cd /d "%%WINPY_DIR%%" >> test_new_installation.bat
echo     start "" "%%WINPY_DIR%%\Spyder.exe" >> test_new_installation.bat
echo     echo Spyder launched! >> test_new_installation.bat
echo ^) else ( >> test_new_installation.bat
echo     echo ✗ Spyder not found. Check installation path. >> test_new_installation.bat
echo ^) >> test_new_installation.bat
echo pause >> test_new_installation.bat

echo.
echo ✓ Created test_new_installation.bat
echo.
echo After installing WinPython, run: test_new_installation.bat
echo.
pause
