#!/usr/bin/env python3
"""
V380 Web Server - Backend for Web-based Camera Monitor
Handles CORS, camera communication, and stream proxying
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

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables
active_streams = {}
camera_configs = {}

@app.route('/')
def index():
    """Serve the main web interface"""
    return send_from_directory('public/simulations/interactive/v380-monitor', 'index.html')

@app.route('/api/scan-network')
def scan_network():
    """Scan local network for V380 cameras"""
    try:
        # Get local network range
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        network_base = '.'.join(local_ip.split('.')[:-1]) + '.'
        
        found_cameras = []
        common_ports = [8080, 80, 8000, 8081]
        
        def check_ip_port(ip, port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((ip, port))
                sock.close()
                
                if result == 0:
                    # Try to identify if it's a camera
                    try:
                        response = requests.get(f"http://{ip}:{port}", timeout=2)
                        if any(keyword in response.text.lower() for keyword in 
                              ['v380', 'camera', 'ipcam', 'webcam', 'netcam']):
                            return {'ip': ip, 'port': port, 'type': 'V380 Camera'}
                    except:
                        # Even if we can't identify it, it might be a camera
                        return {'ip': ip, 'port': port, 'type': 'Unknown Device'}
                return None
            except:
                return None
        
        # Use threading to speed up scanning
        threads = []
        results = []
        
        def scan_range(start, end):
            for i in range(start, end):
                ip = network_base + str(i)
                for port in common_ports:
                    result = check_ip_port(ip, port)
                    if result:
                        results.append(result)
        
        # Split scanning into chunks
        chunk_size = 50
        for i in range(1, 255, chunk_size):
            thread = threading.Thread(target=scan_range, args=(i, min(i + chunk_size, 255)))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete (with timeout)
        for thread in threads:
            thread.join(timeout=10)
        
        return jsonify({
            'success': True,
            'cameras': results,
            'network': network_base + '0/24'
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
                'url': http_url
            }
        except Exception as e:
            results['http'] = {
                'success': False,
                'error': str(e)
            }
        
        # Test RTSP connection
        rtsp_urls = [
            f"rtsp://{username}:{password}@{ip}:{rtsp_port}/live",
            f"rtsp://{username}:{password}@{ip}:{rtsp_port}/stream1",
            f"rtsp://{username}:{password}@{ip}:{rtsp_port}/cam/realmonitor?channel=1&subtype=0",
            f"rtsp://{ip}:{rtsp_port}/live"
        ]
        
        rtsp_results = []
        for rtsp_url in rtsp_urls:
            try:
                cap = cv2.VideoCapture(rtsp_url)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        height, width = frame.shape[:2]
                        rtsp_results.append({
                            'url': rtsp_url,
                            'success': True,
                            'resolution': f"{width}x{height}"
                        })
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
        data = request.json
        camera_id = data.get('camera_id', 'default')
        ip = data.get('ip')
        http_port = data.get('http_port', 8080)
        rtsp_port = data.get('rtsp_port', 554)
        username = data.get('username', 'admin')
        password = data.get('password', '')
        stream_path = data.get('stream_path', '/live')
        
        # Store camera configuration
        camera_configs[camera_id] = data
        
        # Try to establish RTSP connection
        rtsp_url = f"rtsp://{username}:{password}@{ip}:{rtsp_port}{stream_path}"
        
        cap = cv2.VideoCapture(rtsp_url)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                active_streams[camera_id] = {
                    'cap': cap,
                    'url': rtsp_url,
                    'connected': True,
                    'resolution': frame.shape[:2]
                }
                
                return jsonify({
                    'success': True,
                    'camera_id': camera_id,
                    'stream_url': f"/api/stream/{camera_id}",
                    'resolution': f"{frame.shape[1]}x{frame.shape[0]}"
                })
        
        cap.release()
        return jsonify({
            'success': False,
            'error': 'Could not establish RTSP connection'
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
        
        while camera_id in active_streams:
            try:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Encode frame as JPEG
                ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                if not ret:
                    continue
                
                frame_bytes = buffer.tobytes()
                
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                
                time.sleep(0.033)  # ~30 FPS
                
            except Exception as e:
                print(f"Stream error: {e}")
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
            filename = f"v380_snapshot_{camera_id}_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'timestamp': timestamp
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
        
        return jsonify({
            'connected': True,
            'camera_id': camera_id,
            'url': stream_info['url'],
            'resolution': f"{stream_info['resolution'][1]}x{stream_info['resolution'][0]}",
            'config': config
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/proxy-image')
def proxy_image():
    """Proxy camera images to avoid CORS issues"""
    try:
        url = request.args.get('url')
        if not url:
            return jsonify({'error': 'URL parameter required'}), 400
        
        response = requests.get(url, timeout=10)
        
        return Response(
            response.content,
            mimetype=response.headers.get('content-type', 'image/jpeg')
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting V380 Web Server...")
    print("Web interface will be available at: http://localhost:5000")
    print("API endpoints available at: http://localhost:5000/api/")
    
    # Create necessary directories
    os.makedirs('snapshots', exist_ok=True)
    os.makedirs('recordings', exist_ok=True)
    
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
