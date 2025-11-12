@echo off
title Portable Python Setup Guide
echo ========================================
echo    Portable Python Setup Guide
echo ========================================
echo.

echo For a truly portable Python setup that works from USB drives,
echo here are the best options:
echo.

echo OPTION 1: Fresh WinPython Install (Recommended)
echo ================================================
echo 1. Download WinPython from: https://winpython.github.io/
echo 2. Choose: WinPython 3.12.x 64-bit (dot version)
echo 3. Extract directly to D:\ (not D:\folder\)
echo 4. This creates D:\WPy64-312xxx\ automatically
echo.

echo OPTION 2: Portable Python Alternative
echo =====================================
echo 1. Download Portable Python from: https://portablepython.com/
echo 2. Or use Thonny (lightweight): https://thonny.org/
echo 3. These are designed specifically for USB drives
echo.

echo OPTION 3: Copy Working Installation
echo ===================================
echo If Spyder works on your PC:
echo 1. Find your working WinPython folder on PC
echo 2. Copy entire folder to D:\
echo 3. Run D:\WPy64-xxx\WinPython Control Panel.exe
echo 4. Use "Register distribution" to fix paths
echo.

echo Current Issues with USB Python:
echo - Path dependencies may be hardcoded to C:\
echo - Windows registry entries missing
echo - DLL dependencies not found
echo - Antivirus blocking execution from USB
echo.

echo IMMEDIATE WORKAROUND:
echo ====================
echo Use Python IDLE instead of Spyder:
echo 1. Run: D:\WPy64-312101\python\python.exe -m idlelib.idle
echo 2. Or use Jupyter: D:\WPy64-312101\Jupyter Notebook.exe
echo.

set /p choice="Press 1 to try IDLE now, 2 to try Jupyter, or any key to exit: "

if "%choice%"=="1" (
    echo Launching Python IDLE...
    if exist "D:\WPy64-312101\python\python.exe" (
        start "" "D:\WPy64-312101\python\python.exe" -m idlelib.idle
    ) else (
        echo Python not found on D: drive
    )
) else if "%choice%"=="2" (
    echo Launching Jupyter Notebook...
    if exist "D:\WPy64-312101\Jupyter Notebook.exe" (
        cd /d "D:\WPy64-312101"
        start "" "D:\WPy64-312101\Jupyter Notebook.exe"
    ) else (
        echo Jupyter not found on D: drive
    )
)

echo.
pause
