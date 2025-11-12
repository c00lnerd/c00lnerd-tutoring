@echo off
title Create Truly Portable Spyder
echo ========================================
echo    Create Truly Portable Spyder
echo ========================================
echo.

echo This will create a Spyder installation that works on ANY PC
echo by downloading a fresh, portable version and configuring it properly.
echo.

set USB_DRIVE=D:
set WINPY_DIR=%USB_DRIVE%\WPy64-312101
set BACKUP_DIR=%USB_DRIVE%\WinPython_Backup

echo Step 1: Backup current installation (if any)
if exist "%WINPY_DIR%" (
    echo Backing up current installation...
    if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"
    
    REM Backup user files
    if exist "%WINPY_DIR%\notebooks" (
        xcopy "%WINPY_DIR%\notebooks\*" "%BACKUP_DIR%\notebooks\" /E /I /Y >nul 2>&1
        echo ✓ Notebooks backed up
    )
    if exist "%WINPY_DIR%\scripts" (
        xcopy "%WINPY_DIR%\scripts\*" "%BACKUP_DIR%\scripts\" /E /I /Y >nul 2>&1
        echo ✓ Scripts backed up
    )
)

echo.
echo Step 2: Download instructions for portable WinPython
echo.
echo For TRUE portability on any PC, you need to:
echo.
echo 1. Go to: https://winpython.github.io/
echo 2. Download: WinPython 3.12.x 64-bit (dot version)
echo    - Look for "WinPython64-3.12.x.xdot.exe" 
echo    - The "dot" version is more portable
echo 3. Run the installer and extract to: %USB_DRIVE%\
echo 4. This creates a fresh, portable installation
echo.

echo Step 3: Alternative - Thonny (Lightweight and Portable)
echo.
echo Thonny is designed for portability and works on any PC:
echo 1. Go to: https://thonny.org/
echo 2. Download: "Portable variant" for Windows
echo 3. Extract to: %USB_DRIVE%\Thonny\
echo 4. Much smaller and more reliable on different PCs
echo.

echo Step 4: Create portable launcher
echo Creating a launcher that will work on any PC...

echo @echo off > "%USB_DRIVE%\Start_Python_IDE.bat"
echo title Portable Python IDE Launcher >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo. >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo REM Auto-detect USB drive letter >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo for %%%%i in (D E F G H I J K L M N O P Q R S T U V W X Y Z) do ( >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo     if exist "%%%%i:\WPy64-312101\Spyder.exe" ( >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo         set USB_DRIVE=%%%%i: >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo         goto :found >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo     ) >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo     if exist "%%%%i:\Thonny\thonny.exe" ( >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo         set USB_DRIVE=%%%%i: >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo         set USE_THONNY=1 >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo         goto :found >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo     ) >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo ^) >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo echo No portable Python found on any drive >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo pause >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo exit >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo. >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo :found >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo if defined USE_THONNY ( >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo     start "" "%%USB_DRIVE%%\Thonny\thonny.exe" >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo ^) else ( >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo     cd /d "%%USB_DRIVE%%\WPy64-312101" >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo     start "" "%%USB_DRIVE%%\WPy64-312101\Spyder.exe" >> "%USB_DRIVE%\Start_Python_IDE.bat"
echo ^) >> "%USB_DRIVE%\Start_Python_IDE.bat"

echo ✓ Created portable launcher: %USB_DRIVE%\Start_Python_IDE.bat

echo.
echo Step 5: Current options for immediate use
echo.
echo While you download a fresh portable version, you can use:
echo.
echo A) Jupyter Notebook (should work portably):
set /p choice1="Try Jupyter now? (y/n): "
if /i "%choice1%"=="y" (
    if exist "%WINPY_DIR%\Jupyter Notebook.exe" (
        echo Launching Jupyter...
        cd /d "%WINPY_DIR%"
        start "" "%WINPY_DIR%\Jupyter Notebook.exe"
    ) else (
        echo Jupyter not found
    )
)

echo.
echo B) Python IDLE (lightweight, usually works):
set /p choice2="Try Python IDLE now? (y/n): "
if /i "%choice2%"=="y" (
    if exist "%WINPY_DIR%\python\python.exe" (
        echo Launching IDLE...
        start "" "%WINPY_DIR%\python\python.exe" -m idlelib.idle
    ) else (
        echo Python not found
    )
)

echo.
echo ========================================
echo  Summary for True Portability
echo ========================================
echo.
echo 1. Download fresh WinPython "dot" version OR Thonny
echo 2. Extract to USB drive root
echo 3. Use the created Start_Python_IDE.bat launcher
echo 4. This will work on ANY Windows PC
echo.
echo The launcher auto-detects the USB drive letter,
echo so it works regardless of which PC you plug into!
echo.
pause
