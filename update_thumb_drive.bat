@echo off
echo ===============================================
echo  Updating Python Course on Thumb Drive
echo ===============================================
echo.

REM Find the thumb drive (check common drive letters)
set THUMB_DRIVE=
for %%d in (D E F G H I J K L M N O P Q R S T U V W X Y Z) do (
    if exist "%%d:\Python_Course" (
        set THUMB_DRIVE=%%d:
        goto :found
    )
)

echo ERROR: Could not find thumb drive with Python_Course folder
echo Please make sure the thumb drive is connected and try again.
pause
exit /b 1

:found
echo Found thumb drive at %THUMB_DRIVE%
echo.

REM Check if dist folder exists
if not exist "dist" (
    echo Building website first...
    call npm run build
    if errorlevel 1 (
        echo ERROR: Build failed
        pause
        exit /b 1
    )
    echo.
)

echo Updating Python_Course folder on thumb drive...
echo Source: %CD%\dist
echo Target: %THUMB_DRIVE%\Python_Course
echo.

REM Copy files with robocopy
robocopy "dist" "%THUMB_DRIVE%\Python_Course" /E /PURGE

if errorlevel 8 (
    echo ERROR: Copy failed
    pause
    exit /b 1
)

echo.
echo ===============================================
echo  Update Complete!
echo ===============================================
echo.
echo The Python Course on your thumb drive has been updated with:
echo - Fixed navigation links (no more .html extensions)
echo - All 12 Python lessons (was 8 lessons before)
echo - Correct lesson progress indicators
echo - Updated course structure
echo.
echo You can now use the thumb drive on any computer!
echo.
pause
