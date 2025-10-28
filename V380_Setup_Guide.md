# V380 Camera Monitor - Setup Guide

## Overview
This application allows you to monitor V380 cameras directly from your PC without needing a phone app. It connects via RTSP (Real Time Streaming Protocol) and provides live video feed, recording, and snapshot capabilities.

## Installation

### 1. Install Python Dependencies
```bash
pip install -r requirements_v380.txt
```

### 2. Run the Application
```bash
python v380_camera_monitor.py
```

## Camera Setup

### 1. Find Your Camera's IP Address
- **Option 1**: Use the built-in network scanner in the app
- **Option 2**: Check your router's admin panel for connected devices
- **Option 3**: Use network scanning tools like Advanced IP Scanner

### 2. Camera Configuration
Most V380 cameras need to be configured for RTSP access:

1. **Connect via Phone App First** (temporarily):
   - Use the V380 app to set up WiFi and enable RTSP
   - Go to camera settings → Network → RTSP
   - Enable RTSP streaming
   - Note the username/password

2. **Common Default Settings**:
   - Username: `admin`
   - Password: (often blank or `123456`)
   - HTTP Port: `8080`
   - RTSP Port: `554`

## Using the Application

### Connection Settings
1. **Camera IP**: Enter your camera's local IP address
2. **HTTP Port**: Usually 8080 for V380 cameras
3. **RTSP Port**: Usually 554 (standard RTSP port)
4. **Username/Password**: Set in camera configuration

### Features
- **Network Scan**: Automatically find cameras on your network
- **Test Connection**: Verify camera accessibility before connecting
- **Live Video**: Real-time camera feed display
- **Recording**: Save video files to your PC
- **Snapshots**: Capture still images
- **Camera Info**: Display connection and stream details

### Controls
- **Connect**: Start video stream from camera
- **Disconnect**: Stop video stream
- **Start/Stop Recording**: Record video to AVI files
- **Take Snapshot**: Save current frame as JPG

## Troubleshooting

### Common Issues

1. **"Connection Failed"**
   - Verify camera IP address is correct
   - Ensure camera and PC are on same network
   - Check if RTSP is enabled on camera
   - Try different RTSP URL formats (app tries multiple automatically)

2. **"RTSP Stream Not Accessible"**
   - Camera may not have RTSP enabled
   - Username/password might be incorrect
   - Firewall blocking connection
   - Camera may be using non-standard RTSP path

3. **Video Lag or Stuttering**
   - Network congestion
   - Camera quality settings too high
   - Try reducing video quality in camera settings

### RTSP URL Formats
The app automatically tries these common V380 RTSP formats:
- `rtsp://username:password@IP:554/live`
- `rtsp://username:password@IP:554/stream1`
- `rtsp://username:password@IP:554/cam/realmonitor?channel=1&subtype=0`
- `rtsp://IP:554/live` (no auth)
- `rtsp://IP:554/stream1` (no auth)

### Network Requirements
- Camera and PC must be on same local network
- Ports 554 (RTSP) and 8080 (HTTP) should be accessible
- Stable WiFi connection for camera

## Advanced Configuration

### Custom RTSP URLs
If your camera uses a different RTSP format, you can modify the `rtsp_urls` list in the `connect_camera()` method.

### Recording Settings
- Videos saved as AVI files with XVID codec
- Snapshots saved as JPG files
- Files named with timestamp: `v380_recording_YYYYMMDD_HHMMSS.avi`

### Quality Settings
- Adjust camera quality through camera's web interface
- Lower quality = less bandwidth usage
- Higher quality = better image but more network load

## Security Notes
- Change default camera passwords
- Use cameras only on trusted networks
- Consider setting up a separate IoT network for cameras
- Regularly update camera firmware

## Supported Camera Models
This application should work with most V380-compatible cameras including:
- V380 WiFi cameras
- Generic IP cameras with RTSP support
- Many Chinese-manufactured security cameras
- Cameras using similar protocols

## File Locations
- **Recordings**: Saved in same directory as the application
- **Snapshots**: Saved in same directory as the application
- **Logs**: Displayed in the application's info panel

## Technical Details
- **Video Codec**: Uses OpenCV for video processing
- **GUI Framework**: Tkinter (built into Python)
- **Streaming Protocol**: RTSP over TCP/UDP
- **Image Processing**: PIL/Pillow for image handling
- **Network**: Requests library for HTTP communication
