# Roku CS1000X Camera Monitor - Setup Guide

## Overview
This application allows you to monitor Roku CS1000X cameras directly from your PC. The CS1000X is a different camera system than V380 and uses its own protocols for streaming.

## Installation

### 1. Install Python Dependencies
```bash
pip install -r requirements_v380.txt
```
(Same requirements work for Roku cameras)

### 2. Run the Application
```bash
python roku_camera_monitor.py
```

## Roku CS1000X Camera Setup

### 1. Find Your Camera's IP Address
- **Option 1**: Use the built-in network scanner in the app
- **Option 2**: Check your router's admin panel for connected devices
- **Option 3**: Use the Roku camera app to check network settings

### 2. Camera Configuration
Roku CS1000X cameras typically use:

1. **Default Settings**:
   - Username: `admin`
   - Password: (check camera label or app)
   - HTTP Port: `8080` or `80`
   - RTSP Port: `554`

2. **Enable Streaming**:
   - Use Roku camera app to enable RTSP streaming
   - Ensure camera is connected to WiFi
   - Note the camera's IP address from the app

## Using the Application

### Connection Settings
1. **Camera IP**: Enter your Roku camera's local IP address
2. **HTTP Port**: Usually 8080 for Roku cameras
3. **RTSP Port**: Usually 554 (standard RTSP port)
4. **Username/Password**: Set in camera configuration

### Features
- **Network Scan**: Automatically find cameras on your network
- **Test Connection**: Verify camera accessibility before connecting
- **Live Video**: Real-time camera feed display
- **Recording**: Save video files to your PC
- **Snapshots**: Capture still images
- **Camera Info**: Display connection and stream details

## Roku CS1000X Specific Information

### Common RTSP URLs for CS1000X
The app automatically tries these formats:
- `rtsp://username:password@IP:554/live`
- `rtsp://username:password@IP:554/stream1`
- `rtsp://username:password@IP:554/h264`
- `rtsp://username:password@IP:554/cam1/h264`

### Typical Network Settings
- **IP Range**: Usually 192.168.1.x or 192.168.0.x
- **Ports**: HTTP on 8080, RTSP on 554
- **Protocol**: Supports both HTTP and RTSP streaming

## Troubleshooting

### Common Issues

1. **"Connection Failed"**
   - Verify camera IP address is correct
   - Ensure camera and PC are on same network
   - Check if camera is powered on and connected to WiFi
   - Try different ports (80, 8080, 8000)

2. **"RTSP Stream Not Accessible"**
   - Camera may not have RTSP enabled
   - Username/password might be incorrect
   - Try accessing camera's web interface first
   - Check camera app for streaming settings

3. **Video Lag or No Video**
   - Network congestion
   - Camera may be in sleep mode
   - Try different stream quality settings
   - Restart camera and try again

### Roku Camera App Integration
1. **Use Roku App First**: Set up camera with official Roku app
2. **Enable Streaming**: Look for "PC Access" or "RTSP" settings
3. **Note Credentials**: Write down username/password from app
4. **Check Network Info**: Find IP address in app settings

### Network Requirements
- Camera and PC must be on same local network
- Stable WiFi connection for camera
- Router should allow device-to-device communication

## Differences from V380 Cameras

### Protocol Differences
- **Roku CS1000X**: Uses standard RTSP/HTTP protocols
- **Authentication**: Usually simpler than V380
- **Stream Paths**: Different URL formats than V380
- **Quality**: May support different resolution options

### Setup Differences
- **Roku App**: Use official Roku camera app for initial setup
- **Network**: May use different default IP ranges
- **Streaming**: Often easier to enable than older V380 cameras

## Advanced Configuration

### Multiple Cameras
- Run multiple instances of the application
- Each camera needs unique IP address
- Use different windows for each camera feed

### Recording Settings
- Videos saved as AVI files with XVID codec
- Snapshots saved as JPG files
- Files named with timestamp for organization

### Network Optimization
- Use wired connection for PC if possible
- Ensure strong WiFi signal for cameras
- Close other network-intensive applications

## Security Notes
- Change default camera passwords
- Use cameras only on trusted networks
- Keep camera firmware updated
- Monitor who has access to camera feeds

## File Locations
- **Recordings**: Saved in same directory as the application
- **Snapshots**: Saved in same directory as the application
- **Logs**: Displayed in the application's info panel

## Technical Specifications

### Supported Features
- **Live Streaming**: Real-time video feed
- **Recording**: Local video file saving
- **Snapshots**: Still image capture
- **Multiple Formats**: Various RTSP stream types

### System Requirements
- **Python 3.7+** with OpenCV, Tkinter, PIL
- **Windows/Mac/Linux** compatible
- **Network Connection** to camera subnet
- **Sufficient Storage** for recordings

The Roku CS1000X cameras are generally more modern and easier to work with than older V380 cameras, so you should have better success with streaming and connectivity!
