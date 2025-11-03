@echo off
echo ================================================================
echo                CS1000X Home Camera Monitor
echo ================================================================
echo.
echo Starting CS1000X Camera Monitoring System...
echo.
echo This will start:
echo   - Web Server (Flask backend) on port 5000
echo   - Web Interface at http://localhost:5000
echo   - API endpoints for camera control
echo.
echo Your known CS1000X cameras:
echo   - Basement: 192.168.0.198 (SummersBasement)
echo   - Lab: 192.168.1.118 (SummersLab)
echo.
echo ================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ to run the camera monitor
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking Python dependencies...
python -c "import flask, cv2, requests" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing required Python packages...
    pip install flask flask-cors opencv-python requests pillow numpy
    if errorlevel 1 (
        echo ERROR: Failed to install required packages
        pause
        exit /b 1
    )
)

echo.
echo Starting CS1000X Web Server...
echo.
echo ================================================================
echo   WEB INTERFACE: http://localhost:5000
echo   API DOCS:      http://localhost:5000/api/
echo ================================================================
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the Python web server
python cs1000x_web_server.py

echo.
echo Camera monitor stopped.
pause
