@echo off
title Building Offline Version for Thumbdrive
echo ========================================
echo    Building Offline Python Course
echo ========================================
echo.

echo This will build the website for offline use on the thumbdrive
echo and fix emoji encoding issues automatically.
echo.

node build-offline.js

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Copy contents of 'dist' folder
echo 2. Replace Python_Course folder on thumbdrive
echo 3. Test with start_course.bat
echo.
pause
