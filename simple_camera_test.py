#!/usr/bin/env python3
"""
Simple CS1000X Camera Test - Minimal Flask server to test camera connections
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import cv2
import time

app = Flask(__name__)
CORS(app)

# Test cameras
cameras = {
    'basement': {'ip': '192.168.0.198', 'mac': '7C:67:AB:23:DF:1E'},
    'lab': {'ip': '192.168.1.118', 'mac': '7C:67:AB:40:A1:5C'}
}

@app.route('/')
def index():
    print("=== PAGE REQUEST RECEIVED ===")
    return """
<!DOCTYPE html>
<html>
<head>
    <title>CS1000X Camera Test</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background: #1e3c72; color: white; }
        button { padding: 15px 30px; margin: 10px; font-size: 16px; cursor: pointer; }
        .log { background: #000; padding: 15px; margin: 20px 0; height: 300px; overflow-y: auto; font-family: monospace; }
        .success { color: #4CAF50; }
        .error { color: #f44336; }
        .info { color: #2196F3; }
    </style>
</head>
<body>
    <h1>🏠 CS1000X Camera Connection Test</h1>
    
    <h3>Your Cameras:</h3>
    <p>🏠 Basement: 192.168.0.198 (7C:67:AB:23:DF:1E)</p>
    <p>🔬 Lab: 192.168.1.118 (7C:67:AB:40:A1:5C)</p>
    
    <button onclick="testFlask()">Test Flask Server</button>
    <button onclick="testBasementCamera()">Test Basement Camera</button>
    <button onclick="testLabCamera()">Test Lab Camera</button>
    <button onclick="scanPorts()">Scan Camera Ports</button>
    <button onclick="clearLog()">Clear Log</button>
    
    <div class="log" id="log"></div>
    
    <script>
        function log(message, type = 'info') {
            const logDiv = document.getElementById('log');
            const timestamp = new Date().toLocaleTimeString();
            const className = type === 'success' ? 'success' : type === 'error' ? 'error' : 'info';
            logDiv.innerHTML += `<div class="${className}">[${timestamp}] ${message}</div>`;
            logDiv.scrollTop = logDiv.scrollHeight;
        }
        
        function clearLog() {
            document.getElementById('log').innerHTML = '';
        }
        
        async function testFlask() {
            log('Testing Flask server connection...', 'info');
            log('Sending request to /api/test...', 'info');
            try {
                const response = await fetch('/api/test');
                log(`Response status: ${response.status}`, 'info');
                
                if (response.ok) {
                    const data = await response.json();
                    log('Flask server OK: ' + JSON.stringify(data), 'success');
                } else {
                    log(`Flask server error: HTTP ${response.status}`, 'error');
                }
            } catch (error) {
                log('Flask server error: ' + error.message, 'error');
                log('Make sure Flask server is running on port 5001', 'error');
            }
        }
        
        async function testBasementCamera() {
            log('Testing Basement Camera (192.168.0.198)...', 'info');
            await testCamera('basement', '192.168.0.198');
        }
        
        async function testLabCamera() {
            log('Testing Lab Camera (192.168.1.118)...', 'info');
            await testCamera('lab', '192.168.1.118');
        }
        
        async function scanPorts() {
            log('Scanning common camera ports on 192.168.1.118...', 'info');
            try {
                const response = await fetch('/api/scan-ports', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        ip: '192.168.1.118'
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    log(`Port scan results: ${JSON.stringify(data.open_ports)}`, 'success');
                    data.open_ports.forEach(port => {
                        log(`Port ${port} is OPEN`, 'success');
                    });
                } else {
                    log(`Port scan failed: ${data.error}`, 'error');
                }
            } catch (error) {
                log(`Port scan error: ${error.message}`, 'error');
            }
        }
        
        async function testCamera(cameraId, ip) {
            try {
                const response = await fetch('/api/test-camera', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        camera_id: cameraId,
                        ip: ip,
                        username: 'admin',
                        password: ''
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    log(`Camera ${cameraId} test result: ${data.message}`, 'success');
                    if (data.details) {
                        log(`Details: ${JSON.stringify(data.details)}`, 'info');
                    }
                } else {
                    log(`Camera ${cameraId} test failed: ${data.error}`, 'error');
                }
            } catch (error) {
                log(`Camera ${cameraId} test error: ${error.message}`, 'error');
            }
        }
        
        // Initialize
        log('CS1000X Camera Test ready', 'success');
        log('Click "Test Flask Server" first to verify connection', 'info');
    </script>
</body>
</html>
    """

@app.route('/api/test')
def test_api():
    print("=== API TEST REQUEST RECEIVED ===")
    print("Flask API endpoint called successfully!")
    result = {
        'success': True,
        'message': 'Flask server is working!',
        'cameras': len(cameras),
        'time': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    print(f"Returning: {result}")
    return jsonify(result)

@app.route('/api/test-camera', methods=['POST'])
def test_camera():
    print("=== CAMERA TEST REQUEST ===")
    try:
        data = request.json
        print(f"Testing camera: {data}")
        
        camera_id = data.get('camera_id')
        ip = data.get('ip')
        username = data.get('username', 'admin')
        password = data.get('password', '')
        
        print(f"Attempting to connect to {camera_id} at {ip}")
        
        # Test RTSP URLs
        rtsp_urls = [
            f"rtsp://{username}:{password}@{ip}:554/live",
            f"rtsp://{username}:{password}@{ip}:554/stream1",
            f"rtsp://{username}:{password}@{ip}:554/h264",
            f"rtsp://{ip}:554/live"
        ]
        
        results = []
        for rtsp_url in rtsp_urls:
            print(f"Testing RTSP URL: {rtsp_url}")
            try:
                cap = cv2.VideoCapture(rtsp_url)
                cap.set(cv2.CAP_PROP_TIMEOUT, 3000)  # 3 second timeout
                
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        height, width = frame.shape[:2]
                        results.append({
                            'url': rtsp_url,
                            'success': True,
                            'resolution': f"{width}x{height}"
                        })
                        print(f"SUCCESS: {rtsp_url} - {width}x{height}")
                        cap.release()
                        break
                    else:
                        results.append({
                            'url': rtsp_url,
                            'success': False,
                            'error': 'Could not read frame'
                        })
                        print(f"FAILED: {rtsp_url} - Could not read frame")
                else:
                    results.append({
                        'url': rtsp_url,
                        'success': False,
                        'error': 'Could not open stream'
                    })
                    print(f"FAILED: {rtsp_url} - Could not open stream")
                
                cap.release()
            except Exception as e:
                results.append({
                    'url': rtsp_url,
                    'success': False,
                    'error': str(e)
                })
                print(f"ERROR: {rtsp_url} - {str(e)}")
        
        # Check if any succeeded
        successful = [r for r in results if r.get('success')]
        
        if successful:
            return jsonify({
                'success': True,
                'message': f'Camera {camera_id} connected successfully!',
                'working_url': successful[0]['url'],
                'resolution': successful[0]['resolution'],
                'details': results
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Could not connect to camera {camera_id}',
                'details': results
            })
            
    except Exception as e:
        print(f"Camera test error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/scan-ports', methods=['POST'])
def scan_ports():
    print("=== PORT SCAN REQUEST ===")
    try:
        data = request.json
        ip = data.get('ip')
        print(f"Scanning ports on {ip}")
        
        # Common camera ports
        ports_to_scan = [80, 8080, 8081, 554, 1935, 443, 8443, 9000, 37777]
        open_ports = []
        
        import socket
        
        for port in ports_to_scan:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)  # 2 second timeout
                result = sock.connect_ex((ip, port))
                sock.close()
                
                if result == 0:
                    open_ports.append(port)
                    print(f"Port {port}: OPEN")
                else:
                    print(f"Port {port}: CLOSED")
                    
            except Exception as e:
                print(f"Port {port}: ERROR - {str(e)}")
        
        print(f"Open ports found: {open_ports}")
        
        return jsonify({
            'success': True,
            'ip': ip,
            'open_ports': open_ports,
            'scanned_ports': ports_to_scan
        })
        
    except Exception as e:
        print(f"Port scan error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("=" * 50)
    print("🔧 CS1000X Camera Connection Test")
    print("=" * 50)
    print("Web interface: http://localhost:5001")
    print("This will test your camera connections")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5001, debug=True)
