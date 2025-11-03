#!/usr/bin/env python3
"""
CS1000X Web Server - Enhanced Backend for Web-based Camera Monitor
Handles CORS, camera communication, stream proxying, and multi-camera support
"""

from flask import Flask, jsonify, request, Response, send_from_directory
from flask_cors import CORS
import requests
import cv2
import threading
import time
import socket
import subprocess
import platform
import json
import os
from urllib.parse import urlparse
import base64
import numpy as np
from roku_cloud_connector import RokuCloudConnector
from screen_capture_streamer import ScreenCaptureStreamer
from roku_direct_client import RokuDirectClient
from roku_stealth_client import RokuStealthClient
from roku_authenticated_streamer import RokuAuthenticatedStreamer
from roku_multi_window_manager import RokuMultiWindowManager

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables
active_streams = {}
camera_configs = {}
roku_connector = RokuCloudConnector()
screen_streamer = ScreenCaptureStreamer()
roku_direct = RokuDirectClient()
roku_stealth = RokuStealthClient()
roku_authenticated_streamer = None  # Will be initialized after authentication
roku_window_manager = RokuMultiWindowManager()
known_cameras = {
    'cs1000x-basement': {
        'model': 'CS1000X',
        'mac': '7C:67:AB:23:DF:1E',
        'ip': '192.168.0.198',
        'network': 'SummersBasement',
        'device_id': 'SOS2000V3AD89EB106D4',
        'firmware': '7.0.0 • build 26-FD',
        'activation': '09/16/2023',
        'location': 'Basement',
        'default_ports': {'http': 8080, 'rtsp': 554}
    },
    'cs1000x-lab': {
        'model': 'CS1000X',
        'mac': '7C:67:AB:40:A1:5C',
        'ip': '192.168.1.118',
        'network': 'SummersLab',
        'device_id': 'SOS2133V1AD65D83D69A',
        'firmware': '7.2.0 • build 41-FD',
        'activation': '10/26/2025',
        'location': 'Lab',
        'default_ports': {'http': 8080, 'rtsp': 554}
    }
}

@app.route('/')
def index():
    """Serve the main web interface"""
    print("=== SERVING INDEX PAGE ===")
    import os
    
    # Use absolute path to ensure we find the file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_dir = os.path.join(current_dir, 'public', 'simulations', 'interactive', 'cs1000x-monitor')
    file_path = os.path.join(html_dir, 'index.html')
    
    print(f"Current directory: {current_dir}")
    print(f"Looking for HTML file at: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")
    
    if os.path.exists(file_path):
        print("Serving HTML file from:", html_dir)
        return send_from_directory(html_dir, 'index.html')
    else:
        # Fallback: create a simple working interface
        return """
<!DOCTYPE html>
<html>
<head>
    <title>CS1000X Camera Monitor</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background: #1e3c72; color: white; }
        .container { max-width: 800px; margin: 0 auto; }
        button { padding: 10px 20px; margin: 10px; font-size: 16px; }
        .log { background: #000; padding: 10px; margin: 10px 0; height: 200px; overflow-y: auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏠 CS1000X Camera Monitor</h1>
        <p>Direct Flask Server Interface</p>
        
        <button onclick="testConnection()">Test Connection</button>
        <button onclick="connectCamera()">Connect to Lab Camera</button>
        
        <div class="log" id="log"></div>
        
        <script>
            function log(message) {
                document.getElementById('log').innerHTML += new Date().toLocaleTimeString() + ': ' + message + '<br>';
            }
            
            async function testConnection() {
                log('Testing Flask server...');
                try {
                    const response = await fetch('/api/system-info');
                    const data = await response.json();
                    log('Flask server OK: ' + JSON.stringify(data));
                } catch (error) {
                    log('Error: ' + error.message);
                }
            }
            
            async function connectCamera() {
                log('Connecting to Lab camera...');
                try {
                    const response = await fetch('/api/connect', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            camera_id: 'cs1000x-lab',
                            ip: '192.168.1.118',
                            http_port: 8080,
                            rtsp_port: 554,
                            username: 'admin',
                            password: ''
                        })
                    });
                    const data = await response.json();
                    log('Connection result: ' + JSON.stringify(data));
                } catch (error) {
                    log('Connection error: ' + error.message);
                }
            }
            
            log('CS1000X Monitor ready');
        </script>
    </div>
</body>
</html>
        """

@app.route('/api/known-cameras')
def get_known_cameras():
    """Get list of known cameras"""
    return jsonify({
        'success': True,
        'cameras': known_cameras
    })

@app.route('/api/scan-network')
def scan_network():
    """Scan local network for CS1000X and other cameras"""
    try:
        # Get local network range
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        network_base = '.'.join(local_ip.split('.')[:-1]) + '.'
        
        found_cameras = []
        common_ports = [8080, 80, 8000, 8081, 554]
        
        def check_ip_port(ip, port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.8)  # Longer timeout for CS1000X
                result = sock.connect_ex((ip, port))
                sock.close()
                
                if result == 0:
                    # Try to identify if it's a camera
                    try:
                        response = requests.get(f"http://{ip}:{port}", timeout=3)
                        camera_type = 'Unknown Camera'
                        
                        # Check for specific camera types
                        response_text = response.text.lower()
                        if any(keyword in response_text for keyword in ['cs1000x', 'roku']):
                            camera_type = 'CS1000X Camera'
                        elif any(keyword in response_text for keyword in ['v380', 'netcam']):
                            camera_type = 'V380 Camera'
                        elif any(keyword in response_text for keyword in ['camera', 'ipcam', 'webcam']):
                            camera_type = 'IP Camera'
                        
                        return {
                            'ip': ip, 
                            'port': port, 
                            'type': camera_type,
                            'response_code': response.status_code
                        }
                    except:
                        # Even if we can't identify it, it might be a camera
                        return {
                            'ip': ip, 
                            'port': port, 
                            'type': 'Unknown Device',
                            'response_code': None
                        }
                return None
            except:
                return None
        
        # Use threading to speed up scanning
        threads = []
        results = []
        
        def scan_range(start, end):
            for i in range(start, end):
                ip = network_base + str(i)
                # Prioritize known camera IP
                if ip == '192.168.0.198':
                    for port in [8080, 554, 80]:
                        result = check_ip_port(ip, port)
                        if result:
                            results.append(result)
                else:
                    for port in common_ports:
                        result = check_ip_port(ip, port)
                        if result:
                            results.append(result)
                            break  # Only add first working port per IP
        
        # Split scanning into chunks for faster processing
        chunk_size = 25
        for i in range(1, 255, chunk_size):
            thread = threading.Thread(target=scan_range, args=(i, min(i + chunk_size, 255)))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete (with timeout)
        for thread in threads:
            thread.join(timeout=15)
        
        # Add known cameras that weren't found
        found_ips = [cam['ip'] for cam in results]
        for camera_id, camera_info in known_cameras.items():
            if camera_info['ip'] not in found_ips:
                results.append({
                    'ip': camera_info['ip'],
                    'port': camera_info['default_ports']['http'],
                    'type': f"{camera_info['model']} (Known)",
                    'mac': camera_info['mac'],
                    'network': camera_info['network']
                })
        
        return jsonify({
            'success': True,
            'cameras': results,
            'network': network_base + '0/24',
            'scan_time': time.time()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/discover-ports/<ip>')
def discover_camera_ports(ip):
    """Discover open ports on camera"""
    try:
        common_camera_ports = [80, 81, 554, 1935, 8000, 8080, 8081, 8554, 8888, 9000]
        open_ports = []
        
        for port in common_camera_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                sock.close()
                
                if result == 0:
                    open_ports.append(port)
            except:
                continue
        
        return jsonify({
            'success': True,
            'ip': ip,
            'open_ports': open_ports,
            'total_found': len(open_ports)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/test-connection', methods=['POST'])
def test_connection():
    """Test connection to a specific camera"""
    try:
        data = request.json
        ip = data.get('ip')
        http_port = data.get('http_port', 8080)
        rtsp_port = data.get('rtsp_port', 554)
        username = data.get('username', 'admin')
        password = data.get('password', '')
        
        results = {}
        
        # Test HTTP connection
        try:
            http_url = f"http://{ip}:{http_port}"
            response = requests.get(http_url, timeout=5)
            results['http'] = {
                'success': True,
                'status_code': response.status_code,
                'url': http_url,
                'response_size': len(response.content)
            }
        except Exception as e:
            results['http'] = {
                'success': False,
                'error': str(e)
            }
        
        # Test RTSP connection with CS1000X specific URLs
        rtsp_urls = [
            f"rtsp://{username}:{password}@{ip}:{rtsp_port}/live",
            f"rtsp://{username}:{password}@{ip}:{rtsp_port}/stream1",
            f"rtsp://{username}:{password}@{ip}:{rtsp_port}/h264",
            f"rtsp://{username}:{password}@{ip}:{rtsp_port}/cam1/h264",
            f"rtsp://{username}:{password}@{ip}:{rtsp_port}/cam/realmonitor?channel=1&subtype=0",
            f"rtsp://{ip}:{rtsp_port}/live",
            f"rtsp://{ip}:{rtsp_port}/stream1"
        ]
        
        rtsp_results = []
        for rtsp_url in rtsp_urls:
            try:
                cap = cv2.VideoCapture(rtsp_url)
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        height, width = frame.shape[:2]
                        rtsp_results.append({
                            'url': rtsp_url,
                            'success': True,
                            'resolution': f"{width}x{height}",
                            'fps': cap.get(cv2.CAP_PROP_FPS)
                        })
                        cap.release()
                        break  # Use first working stream
                    else:
                        rtsp_results.append({
                            'url': rtsp_url,
                            'success': False,
                            'error': 'Could not read frame'
                        })
                else:
                    rtsp_results.append({
                        'url': rtsp_url,
                        'success': False,
                        'error': 'Could not open stream'
                    })
                cap.release()
            except Exception as e:
                rtsp_results.append({
                    'url': rtsp_url,
                    'success': False,
                    'error': str(e)
                })
        
        results['rtsp'] = rtsp_results
        
        # Check if this is a known camera
        if ip in [cam['ip'] for cam in known_cameras.values()]:
            for camera_id, camera_info in known_cameras.items():
                if camera_info['ip'] == ip:
                    results['known_camera'] = camera_info
                    break
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/connect', methods=['POST'])
def connect_camera():
    """Connect to camera and start streaming"""
    try:
        print("=== CONNECT REQUEST RECEIVED ===")
        data = request.json
        print(f"Request data: {data}")
        
        camera_id = data.get('camera_id', f"camera_{int(time.time())}")
        ip = data.get('ip')
        http_port = data.get('http_port', 8080)
        rtsp_port = data.get('rtsp_port', 554)
        username = data.get('username', 'admin')
        password = data.get('password', '')
        
        print(f"Connecting to camera: {camera_id} at {ip}:{http_port}")
        print(f"RTSP settings: {username}@{ip}:{rtsp_port}")
        
        # Store camera configuration
        camera_configs[camera_id] = data
        
        # Try multiple RTSP URLs and ports for CS1000X compatibility
        rtsp_ports = [rtsp_port, 1935, 8554, 88, 8000, 8888]
        rtsp_paths = ["/live", "/stream1", "/h264", "/cam1/h264", "/stream", "/video", "/ch01", "/channel1"]
        
        rtsp_urls = []
        for port in rtsp_ports:
            for path in rtsp_paths:
                rtsp_urls.extend([
                    f"rtsp://{username}:{password}@{ip}:{port}{path}",
                    f"rtsp://{ip}:{port}{path}"
                ])
        
        # Also try HTTP streaming alternatives
        http_stream_urls = [
            f"http://{ip}:{http_port}/video",
            f"http://{ip}:{http_port}/stream",
            f"http://{ip}:{http_port}/live",
            f"http://{ip}:{http_port}/mjpeg",
            f"http://{ip}:{http_port}/cgi-bin/mjpg/video.cgi",
            f"http://{ip}:81/video",
            f"http://{ip}:8081/video"
        ]
        rtsp_urls.extend(http_stream_urls)
        
        for rtsp_url in rtsp_urls:
            try:
                print(f"Attempting RTSP connection: {rtsp_url}")
                cap = cv2.VideoCapture(rtsp_url)
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce latency
                # Removed CAP_PROP_TIMEOUT - not available in all OpenCV versions
                
                if cap.isOpened():
                    print(f"RTSP stream opened: {rtsp_url}")
                    ret, frame = cap.read()
                    if ret:
                        print(f"Successfully read frame from: {rtsp_url}")
                        active_streams[camera_id] = {
                            'cap': cap,
                            'url': rtsp_url,
                            'connected': True,
                            'resolution': frame.shape[:2],
                            'fps': cap.get(cv2.CAP_PROP_FPS),
                            'connect_time': time.time()
                        }
                        
                        return jsonify({
                            'success': True,
                            'camera_id': camera_id,
                            'stream_url': f"/api/stream/{camera_id}",
                            'resolution': f"{frame.shape[1]}x{frame.shape[0]}",
                            'rtsp_url': rtsp_url
                        })
                    else:
                        print(f"Could not read frame from: {rtsp_url}")
                else:
                    print(f"Could not open RTSP stream: {rtsp_url}")
                
                cap.release()
            except Exception as e:
                print(f"RTSP connection error for {rtsp_url}: {str(e)}")
                continue
        
        return jsonify({
            'success': False,
            'error': 'Could not establish RTSP connection with any URL format'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/disconnect/<camera_id>', methods=['POST'])
def disconnect_camera(camera_id):
    """Disconnect from camera"""
    try:
        if camera_id in active_streams:
            active_streams[camera_id]['cap'].release()
            del active_streams[camera_id]
        
        if camera_id in camera_configs:
            del camera_configs[camera_id]
        
        return jsonify({
            'success': True,
            'message': f'Camera {camera_id} disconnected'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/stream/<camera_id>')
def stream_camera(camera_id):
    """Stream camera feed as MJPEG"""
    def generate_frames():
        if camera_id not in active_streams:
            return
        
        cap = active_streams[camera_id]['cap']
        frame_count = 0
        
        while camera_id in active_streams:
            try:
                ret, frame = cap.read()
                if not ret:
                    # Try to reconnect
                    time.sleep(0.1)
                    continue
                
                # Resize frame for web streaming
                height, width = frame.shape[:2]
                if width > 1280:  # Limit max width for web
                    scale = 1280 / width
                    new_width = int(width * scale)
                    new_height = int(height * scale)
                    frame = cv2.resize(frame, (new_width, new_height))
                
                # Add timestamp overlay
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.7, (255, 255, 255), 2)
                
                # Add camera info overlay
                if camera_id in camera_configs:
                    config = camera_configs[camera_id]
                    info_text = f"CS1000X - {config.get('ip', 'Unknown IP')}"
                    cv2.putText(frame, info_text, (10, frame.shape[0] - 10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Encode frame as JPEG
                encode_params = [cv2.IMWRITE_JPEG_QUALITY, 85]
                ret, buffer = cv2.imencode('.jpg', frame, encode_params)
                if not ret:
                    continue
                
                frame_bytes = buffer.tobytes()
                
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                
                frame_count += 1
                time.sleep(0.033)  # ~30 FPS
                
            except Exception as e:
                print(f"Stream error for {camera_id}: {e}")
                break
    
    if camera_id not in active_streams:
        return jsonify({'error': 'Camera not connected'}), 404
    
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/snapshot/<camera_id>')
def take_snapshot(camera_id):
    """Take a snapshot from the camera"""
    try:
        if camera_id not in active_streams:
            return jsonify({'error': 'Camera not connected'}), 404
        
        cap = active_streams[camera_id]['cap']
        ret, frame = cap.read()
        
        if ret:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"cs1000x_snapshot_{camera_id}_{timestamp}.jpg"
            
            # Create snapshots directory if it doesn't exist
            os.makedirs('snapshots', exist_ok=True)
            filepath = os.path.join('snapshots', filename)
            
            cv2.imwrite(filepath, frame)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'filepath': filepath,
                'timestamp': timestamp,
                'resolution': f"{frame.shape[1]}x{frame.shape[0]}"
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Could not capture frame'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/camera-info/<camera_id>')
def get_camera_info(camera_id):
    """Get camera information and status"""
    try:
        if camera_id not in active_streams:
            return jsonify({'connected': False})
        
        stream_info = active_streams[camera_id]
        config = camera_configs.get(camera_id, {})
        
        # Calculate uptime
        uptime = time.time() - stream_info.get('connect_time', time.time())
        
        return jsonify({
            'connected': True,
            'camera_id': camera_id,
            'url': stream_info['url'],
            'resolution': f"{stream_info['resolution'][1]}x{stream_info['resolution'][0]}",
            'fps': stream_info.get('fps', 'Unknown'),
            'uptime': f"{int(uptime)} seconds",
            'config': config
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/active-cameras')
def get_active_cameras():
    """Get list of currently active camera streams"""
    try:
        active_list = []
        for camera_id, stream_info in active_streams.items():
            config = camera_configs.get(camera_id, {})
            uptime = time.time() - stream_info.get('connect_time', time.time())
            
            active_list.append({
                'camera_id': camera_id,
                'ip': config.get('ip', 'Unknown'),
                'resolution': f"{stream_info['resolution'][1]}x{stream_info['resolution'][0]}",
                'uptime': int(uptime),
                'stream_url': f"/api/stream/{camera_id}"
            })
        
        return jsonify({
            'success': True,
            'active_cameras': active_list,
            'count': len(active_list)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/roku-auth', methods=['POST'])
def roku_authenticate():
    """Authenticate with Roku cloud services"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'error': 'Username and password required'
            })
        
        print(f"Attempting Roku authentication for {username}")
        success = roku_connector.authenticate_with_roku(username, password)
        
        if success:
            # Get camera list
            cameras = roku_connector.get_camera_list()
            return jsonify({
                'success': True,
                'message': 'Roku authentication successful',
                'cameras': cameras,
                'device_id': roku_connector.device_id
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Roku authentication failed'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/roku-cameras')
def get_roku_cameras():
    """Get cameras from Roku cloud"""
    try:
        if not roku_connector.access_token:
            return jsonify({
                'success': False,
                'error': 'Not authenticated with Roku'
            })
        
        cameras = roku_connector.get_camera_list()
        return jsonify({
            'success': True,
            'cameras': cameras
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/roku-stream/<camera_id>')
def get_roku_stream(camera_id):
    """Get stream URL for Roku camera"""
    try:
        if not roku_connector.access_token:
            return jsonify({
                'success': False,
                'error': 'Not authenticated with Roku'
            })
        
        stream_url = roku_connector.get_camera_stream_url(camera_id)
        
        if stream_url:
            return jsonify({
                'success': True,
                'stream_url': stream_url
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Could not get stream URL'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/roku-direct-auth', methods=['POST'])
def roku_direct_authenticate():
    """Phone-free authentication with Roku servers"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'error': 'Username and password required'
            })
        
        print(f"🔐 Direct Roku authentication for {username} (no phone required)")
        
        # Try direct API authentication first
        success = roku_direct.authenticate_with_roku_account(username, password)
        
        if success:
            # Discover cameras immediately
            cameras = roku_direct.discover_cameras()
            return jsonify({
                'success': True,
                'message': 'Direct Roku authentication successful - no phone required!',
                'cameras': cameras,
                'device_id': roku_direct.device_id,
                'access_token': roku_direct.access_token[:20] + '...' if roku_direct.access_token else None,
                'method': 'direct_api'
            })
        else:
            print("🥷 Direct API failed, trying stealth browser simulation...")
            
            # Fallback to stealth browser simulation
            stealth_success = roku_stealth.test_stealth_authentication(username, password)
            
            if stealth_success:
                # Initialize authenticated streamer
                global roku_authenticated_streamer
                roku_authenticated_streamer = RokuAuthenticatedStreamer(roku_stealth.session)
                
                # Try to discover cameras via web interface
                cameras = roku_stealth.discover_cameras_via_web()
                
                # If cameras found, try to get stream URLs immediately
                if cameras and len(cameras) > 0:
                    first_camera = cameras[0]
                    if 'stream_urls' in first_camera and first_camera['stream_urls']:
                        print(f"🎥 Stream URLs found: {first_camera['stream_urls']}")
                    
                    # Add authenticated streaming endpoints
                    first_camera['authenticated_stream_endpoints'] = [
                        '/api/roku-authenticated-stream',
                        '/api/roku-authenticated-live'
                    ]
                
                return jsonify({
                    'success': True,
                    'message': 'Stealth browser authentication successful - no phone required!',
                    'cameras': cameras,
                    'access_token': roku_stealth.access_token[:20] + '...' if roku_stealth.access_token else None,
                    'method': 'stealth_browser',
                    'authenticated_streaming': True
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Both direct API and stealth browser authentication failed'
                })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/roku-direct-cameras')
def get_roku_direct_cameras():
    """Get cameras via direct Roku connection (no phone required)"""
    try:
        if not roku_direct.access_token:
            return jsonify({
                'success': False,
                'error': 'Not authenticated with Roku (direct method)'
            })
        
        cameras = roku_direct.discover_cameras()
        return jsonify({
            'success': True,
            'cameras': cameras,
            'method': 'direct_roku_api'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/roku-direct-stream/<camera_id>')
def get_roku_direct_stream(camera_id):
    """Get stream URL via direct Roku connection (no phone required)"""
    try:
        if not roku_direct.access_token:
            return jsonify({
                'success': False,
                'error': 'Not authenticated with Roku (direct method)'
            })
        
        stream_url = roku_direct.get_camera_stream_url(camera_id)
        
        if stream_url:
            return jsonify({
                'success': True,
                'stream_url': stream_url,
                'method': 'direct_roku_api',
                'phone_required': False
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Could not get direct stream URL'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/roku-test')
def test_roku_connection():
    """Test Roku cloud connectivity"""
    try:
        result = roku_connector.test_connection()
        return jsonify({
            'success': result,
            'device_id': roku_connector.device_id,
            'message': 'Roku connectivity test completed'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/screen-capture/start', methods=['POST'])
def start_screen_capture():
    """Start screen capture of Samsung Galaxy/phone mirroring window"""
    try:
        data = request.json or {}
        window_title = data.get('window_title')
        
        # Find phone mirroring windows
        phone_windows = screen_streamer.find_samsung_dex_window()
        
        if phone_windows:
            # If specific window requested, find it
            target_hwnd = None
            if window_title:
                for hwnd, title in phone_windows:
                    if window_title.lower() in title.lower():
                        target_hwnd = hwnd
                        break
            else:
                # Use first found window
                target_hwnd = phone_windows[0][0]
            
            if target_hwnd:
                screen_streamer.start_capture(target_hwnd)
                return jsonify({
                    'success': True,
                    'message': 'Screen capture started',
                    'stream_url': '/api/screen-stream',
                    'window_title': win32gui.GetWindowText(target_hwnd) if 'win32gui' in globals() else 'Phone Screen'
                })
        
        # Fallback to full screen
        screen_streamer.start_capture()
        return jsonify({
            'success': True,
            'message': 'Full screen capture started',
            'stream_url': '/api/screen-stream'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/screen-capture/stop', methods=['POST'])
def stop_screen_capture():
    """Stop screen capture"""
    try:
        screen_streamer.stop_capture()
        return jsonify({
            'success': True,
            'message': 'Screen capture stopped'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/screen-capture/windows')
def get_available_windows():
    """Get list of available phone mirroring windows"""
    try:
        phone_windows = screen_streamer.find_samsung_dex_window()
        windows_list = []
        
        for hwnd, title in phone_windows:
            try:
                import win32gui
                rect = win32gui.GetWindowRect(hwnd)
                windows_list.append({
                    'title': title,
                    'size': f"{rect[2]-rect[0]}x{rect[3]-rect[1]}",
                    'hwnd': hwnd
                })
            except:
                windows_list.append({
                    'title': title,
                    'size': 'unknown',
                    'hwnd': hwnd
                })
        
        return jsonify({
            'success': True,
            'windows': windows_list
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/roku-authenticated-stream')
def roku_authenticated_stream():
    """Stream from authenticated Roku endpoint (stream)"""
    try:
        if not roku_authenticated_streamer:
            return jsonify({'error': 'Not authenticated with Roku'}), 404
        
        return roku_authenticated_streamer.create_mjpeg_stream('stream')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/roku-authenticated-live')
def roku_authenticated_live():
    """Stream from authenticated Roku endpoint (live)"""
    try:
        if not roku_authenticated_streamer:
            return jsonify({'error': 'Not authenticated with Roku'}), 404
        
        return roku_authenticated_streamer.create_mjpeg_stream('live')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test-roku-stream-content')
def test_roku_stream_content():
    """Test what the authenticated streaming endpoints return"""
    if not roku_authenticated_streamer:
        return jsonify({'error': 'Not authenticated with Roku'}), 404
    
    results = {}
    
    endpoints = [
        'https://my.roku.com/account/devices/SOS2000V3AD89EB106D4/stream',
        'https://my.roku.com/account/devices/SOS2000V3AD89EB106D4/live'
    ]
    
    for endpoint in endpoints:
        try:
            response = roku_authenticated_streamer.session.get(endpoint, timeout=10)
            
            endpoint_name = endpoint.split('/')[-1]
            results[endpoint_name] = {
                'status': response.status_code,
                'content_type': response.headers.get('content-type', 'unknown'),
                'content_length': len(response.content),
                'has_video_keywords': any(keyword in response.text.lower() 
                                        for keyword in ['video', 'stream', 'mp4', 'm3u8', 'rtmp', 'rtsp']),
                'content_preview': response.text[:500] + '...' if len(response.text) > 500 else response.text
            }
            
            # Look for video URLs in the content
            video_patterns = [
                r'https://[^\s"\'<>]*\.(?:mp4|m3u8|ts)',
                r'"(?:video|stream)Url":\s*"([^"]*)"',
                r'src="([^"]*(?:video|stream)[^"]*)"',
                r'rtmp://[^\s"\'<>]+',
                r'rtsp://[^\s"\'<>]+',
                r'wss://[^\s"\'<>]*stream[^\s"\'<>]*'
            ]
            
            found_urls = []
            for pattern in video_patterns:
                matches = re.findall(pattern, response.text, re.IGNORECASE)
                found_urls.extend(matches)
            
            if found_urls:
                results[endpoint_name]['video_urls'] = found_urls
                print(f"🎯 Found video URLs in {endpoint_name}: {found_urls}")
                
        except Exception as e:
            results[endpoint_name] = {'error': str(e)}
    
    return jsonify(results)

@app.route('/api/test-smarthome-api')
def test_smarthome_api():
    """Test the Smart Home API discovery"""
    if not roku_authenticated_streamer:
        return jsonify({'error': 'Not authenticated with Roku'}), 404
    
    try:
        from roku_smarthome_api import RokuSmartHomeAPI
        
        smarthome_api = RokuSmartHomeAPI(roku_authenticated_streamer.session)
        cameras = smarthome_api.discover_smarthome_cameras()
        
        return jsonify({
            'success': True,
            'cameras_found': len(cameras),
            'cameras': cameras,
            'message': 'Smart Home API discovery completed'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/open-camera-dashboard')
def open_camera_dashboard():
    """Open the camera control dashboard"""
    try:
        roku_window_manager.open_control_dashboard()
        return jsonify({
            'success': True,
            'message': 'Camera dashboard opened'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/open-camera-window/<camera_name>')
def open_camera_window(camera_name):
    """Open a specific camera window"""
    try:
        camera_configs = {
            'basement': {'name': 'Basement Camera', 'id': 'SOS2000V3AD89EB106D4'},
            'living': {'name': 'Living Room', 'id': None},
            'becky': {'name': 'Becky', 'id': None}
        }
        
        camera_config = camera_configs.get(camera_name.lower())
        if not camera_config:
            return jsonify({
                'success': False,
                'error': f'Unknown camera: {camera_name}'
            }), 404
        
        roku_window_manager.open_camera_window(
            camera_config['name'], 
            camera_config['id']
        )
        
        return jsonify({
            'success': True,
            'message': f'Opened window for {camera_config["name"]}'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/open-multi-camera-layout')
def open_multi_camera_layout():
    """Open multiple camera windows in grid layout"""
    try:
        cameras = [
            {'name': 'Basement Camera', 'id': 'SOS2000V3AD89EB106D4'},
            {'name': 'Living Room', 'id': None},
            {'name': 'Becky', 'id': None}
        ]
        
        roku_window_manager.open_multi_camera_layout(cameras)
        
        return jsonify({
            'success': True,
            'message': f'Opened {len(cameras)} camera windows in grid layout'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/screen-stream')
def screen_stream():
    """Stream captured screen as MJPEG"""
    try:
        if not screen_streamer.capturing:
            return jsonify({'error': 'Screen capture not active'}), 404
        
        return Response(screen_streamer.get_mjpeg_stream(),
                       mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/system-info')
def get_system_info():
    """Get system information"""
    try:
        return jsonify({
            'success': True,
            'system': {
                'platform': platform.system(),
                'python_version': platform.python_version(),
                'opencv_version': cv2.__version__,
                'server_time': time.strftime("%Y-%m-%d %H:%M:%S"),
                'uptime': time.time()
            },
            'cameras': {
                'known_count': len(known_cameras),
                'active_count': len(active_streams),
                'total_configs': len(camera_configs)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("=" * 60)
    print("🏠 CS1000X Home Camera Monitor Server")
    print("=" * 60)
    print(f"Web interface: http://localhost:5000")
    print(f"API endpoints: http://localhost:5000/api/")
    print(f"Known cameras: {len(known_cameras)}")
    print("=" * 60)
    
    # Create necessary directories
    os.makedirs('snapshots', exist_ok=True)
    os.makedirs('recordings', exist_ok=True)
    
    # Start the Flask server
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
