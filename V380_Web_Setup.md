# V380 Camera Monitor - Web Version Setup

## Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements_v380.txt
```

### 2. Start the Web Server
```bash
python v380_web_server.py
```

### 3. Open Your Browser
Navigate to: **http://localhost:5000**

## Two Versions Available

### 🖥️ Python GUI Version (Spyder)
- **File**: `v380_camera_monitor.py`
- **Best for**: Desktop use, direct control, offline operation
- **Features**: Native GUI, local recording, full camera control

### 🌐 Web Version (Browser)
- **File**: `v380_web_server.py` + web interface
- **Best for**: Remote access, mobile devices, modern UI
- **Features**: Web-based interface, CORS handling, API endpoints

## Web Version Features

### 🎯 Modern Web Interface
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Streaming**: Live MJPEG video feed
- **Professional UI**: Glass-morphism design with animations
- **Touch-friendly**: Mobile-optimized controls

### 🔧 Advanced Capabilities
- **Network Scanner**: Automatically discover V380 cameras
- **Connection Testing**: Verify camera accessibility
- **Multiple Stream Formats**: RTSP, MJPEG, snapshot refresh
- **CORS Proxy**: Handles cross-origin requests
- **API Endpoints**: RESTful API for integration

### 📱 Cross-Platform Access
- **Any Browser**: Chrome, Firefox, Safari, Edge
- **Any Device**: Windows, Mac, Linux, iOS, Android
- **Remote Access**: Access from anywhere on your network
- **No Installation**: Just open a web browser

## API Endpoints

The web server provides these API endpoints:

### Camera Discovery
- `GET /api/scan-network` - Scan for cameras on network
- `POST /api/test-connection` - Test camera connectivity

### Camera Control
- `POST /api/connect` - Connect to camera
- `POST /api/disconnect/<camera_id>` - Disconnect camera
- `GET /api/camera-info/<camera_id>` - Get camera status

### Streaming
- `GET /api/stream/<camera_id>` - MJPEG video stream
- `GET /api/snapshot/<camera_id>` - Take snapshot
- `GET /api/proxy-image?url=<url>` - Proxy images (CORS)

## Usage Comparison

| Feature | Python GUI | Web Version |
|---------|------------|-------------|
| **Installation** | Python + packages | Python + packages |
| **Interface** | Tkinter desktop | Modern web UI |
| **Mobile Support** | No | Yes |
| **Remote Access** | No | Yes |
| **Recording** | Local files | Browser download |
| **Multi-camera** | Multiple instances | Single interface |
| **CORS Issues** | None | Handled by server |
| **Offline Use** | Yes | Requires server |

## Network Configuration

### For Local Use
- Server runs on `localhost:5000`
- Camera and PC on same network
- No firewall configuration needed

### For Remote Access
1. **Find Server IP**: `ipconfig` (Windows) or `ifconfig` (Linux/Mac)
2. **Access Remotely**: `http://YOUR_SERVER_IP:5000`
3. **Firewall**: Allow port 5000 if needed
4. **Router**: Port forwarding for internet access (optional)

## Troubleshooting

### Web Version Issues

1. **"Cannot connect to server"**
   - Ensure `v380_web_server.py` is running
   - Check `http://localhost:5000` is accessible
   - Verify no other service using port 5000

2. **"CORS errors in browser"**
   - Server handles CORS automatically
   - Try different browser if issues persist
   - Check browser console for specific errors

3. **"Camera not found"**
   - Use network scanner first
   - Verify camera IP and ports
   - Test connection before connecting

4. **"Video not loading"**
   - Camera may not support MJPEG
   - Try different stream paths
   - Check camera web interface settings

### Performance Tips

1. **Reduce Latency**
   - Use wired connection for camera
   - Lower video quality if needed
   - Close other network-intensive apps

2. **Multiple Cameras**
   - Each camera gets unique ID
   - Server can handle multiple streams
   - Monitor server CPU usage

3. **Mobile Optimization**
   - Use WiFi instead of cellular
   - Enable hardware acceleration in browser
   - Close other browser tabs

## Security Considerations

### Network Security
- **Local Network Only**: Don't expose to internet without VPN
- **Change Default Passwords**: Update camera credentials
- **Firewall Rules**: Restrict access to trusted devices
- **HTTPS**: Consider SSL certificate for production use

### Camera Security
- **Firmware Updates**: Keep camera firmware current
- **Strong Passwords**: Use complex camera passwords
- **Network Isolation**: Consider separate IoT network
- **Access Logs**: Monitor connection attempts

## Development Notes

### Extending the Web Interface
- **Frontend**: HTML/CSS/JavaScript in `index.html`
- **Backend**: Flask API in `v380_web_server.py`
- **Streaming**: OpenCV + Flask Response streaming
- **CORS**: Flask-CORS handles cross-origin requests

### Adding Features
- **Recording**: Implement server-side video recording
- **Authentication**: Add user login system
- **Database**: Store camera configurations
- **Notifications**: Email/SMS alerts for motion detection

## File Structure
```
V380 Camera Monitor/
├── v380_camera_monitor.py          # Python GUI version
├── v380_web_server.py              # Web server backend
├── requirements_v380.txt           # Dependencies
├── V380_Setup_Guide.md            # GUI version guide
├── V380_Web_Setup.md              # This file
└── public/simulations/interactive/v380-monitor/
    └── index.html                  # Web interface
```

## Next Steps

1. **Test Both Versions**: Try GUI and web versions
2. **Configure Camera**: Set up RTSP access on your V380
3. **Network Setup**: Ensure camera and PC connectivity
4. **Choose Version**: Pick GUI for desktop or web for flexibility
5. **Customize**: Modify interface or add features as needed

The web version provides modern, cross-platform access to your V380 cameras with a professional interface that works on any device with a web browser!
