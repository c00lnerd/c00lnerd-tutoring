#!/usr/bin/env python3
"""
Mobile App Network Interceptor - Capture CS1000X/Roku mobile app API calls
This will help us understand how the mobile app communicates with Roku servers
"""

import socket
import threading
import time
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import subprocess
import os

class ProxyHandler(BaseHTTPRequestHandler):
    """HTTP/HTTPS proxy to intercept mobile app traffic"""
    
    def do_GET(self):
        self.handle_request('GET')
    
    def do_POST(self):
        self.handle_request('POST')
    
    def do_PUT(self):
        self.handle_request('PUT')
    
    def do_DELETE(self):
        self.handle_request('DELETE')
    
    def handle_request(self, method):
        """Intercept and log all requests"""
        try:
            # Log the request
            print(f"\n{'='*60}")
            print(f"📱 INTERCEPTED {method} REQUEST")
            print(f"{'='*60}")
            print(f"URL: {self.path}")
            print(f"Headers: {dict(self.headers)}")
            
            # Read request body if present
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                body = self.rfile.read(content_length)
                print(f"Body: {body.decode('utf-8', errors='ignore')}")
            
            # Check if this looks like a Roku/camera API call
            if any(keyword in self.path.lower() for keyword in ['roku', 'camera', 'stream', 'auth', 'login', 'device']):
                print("🎯 POTENTIAL CAMERA API CALL DETECTED!")
                
                # Save to file for analysis
                with open('intercepted_api_calls.log', 'a') as f:
                    f.write(f"\n{time.strftime('%Y-%m-%d %H:%M:%S')} - {method} {self.path}\n")
                    f.write(f"Headers: {dict(self.headers)}\n")
                    if content_length > 0:
                        f.write(f"Body: {body.decode('utf-8', errors='ignore')}\n")
                    f.write("-" * 60 + "\n")
            
            # Send a basic response to keep the app happy
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "intercepted"}')
            
        except Exception as e:
            print(f"Error handling request: {e}")
            self.send_error(500)

class MobileAppInterceptor:
    def __init__(self):
        self.proxy_port = 8888
        self.ssl_port = 8889
        self.running = False
        
    def start_proxy_server(self):
        """Start HTTP/HTTPS proxy server"""
        print(f"🚀 Starting mobile app interceptor...")
        print(f"HTTP Proxy: localhost:{self.proxy_port}")
        print(f"HTTPS Proxy: localhost:{self.ssl_port}")
        
        # Start HTTP proxy
        http_server = HTTPServer(('localhost', self.proxy_port), ProxyHandler)
        http_thread = threading.Thread(target=http_server.serve_forever)
        http_thread.daemon = True
        http_thread.start()
        
        print("✅ HTTP proxy started")
        
        # Instructions for user
        print("\n" + "="*60)
        print("📱 MOBILE APP INTERCEPTION SETUP")
        print("="*60)
        print("To intercept your Samsung Galaxy's CS1000X app traffic:")
        print()
        print("METHOD 1 - WiFi Proxy (Easiest):")
        print("1. On your Samsung Galaxy, go to WiFi settings")
        print("2. Long press your WiFi network → Modify")
        print("3. Advanced → Proxy → Manual")
        print(f"4. Proxy hostname: {self.get_local_ip()}")
        print(f"5. Proxy port: {self.proxy_port}")
        print("6. Save and open CS1000X app")
        print()
        print("METHOD 2 - USB Debugging (Advanced):")
        print("1. Enable Developer Options on your phone")
        print("2. Enable USB Debugging")
        print("3. Connect phone to PC via USB")
        print("4. Use ADB port forwarding")
        print()
        print("METHOD 3 - Screen Mirroring Analysis:")
        print("1. Use Samsung DeX or screen mirroring")
        print("2. Monitor network traffic while using app")
        print("3. Capture API endpoints and authentication")
        print()
        print("All intercepted API calls will be logged to 'intercepted_api_calls.log'")
        print("="*60)
        
        self.running = True
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping interceptor...")
            http_server.shutdown()
    
    def get_local_ip(self):
        """Get local IP address for proxy configuration"""
        try:
            # Connect to a remote address to get local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "192.168.1.XXX"  # Fallback
    
    def analyze_samsung_dex(self):
        """Instructions for using Samsung DeX to analyze the app"""
        print("\n" + "="*60)
        print("📱 SAMSUNG DEX ANALYSIS METHOD")
        print("="*60)
        print("Since you mentioned using Samsung Galaxy screen mirroring:")
        print()
        print("1. ENABLE SAMSUNG DEX:")
        print("   - Connect phone to PC via USB-C to HDMI")
        print("   - Or use wireless DeX if supported")
        print("   - Or use 'Smart View' to mirror screen")
        print()
        print("2. NETWORK MONITORING:")
        print("   - Install Wireshark on PC")
        print("   - Monitor network interface while using CS1000X app")
        print("   - Filter for HTTP/HTTPS traffic from your phone's IP")
        print()
        print("3. APP ANALYSIS:")
        print("   - Open CS1000X app on mirrored screen")
        print("   - Login and view cameras")
        print("   - Watch network traffic for API endpoints")
        print()
        print("4. LOOK FOR:")
        print("   - Authentication URLs (login, token)")
        print("   - Camera list APIs")
        print("   - Stream URLs (RTMP, HLS, WebRTC)")
        print("   - Device registration calls")
        print()
        print("This is probably the most practical approach!")
        print("="*60)

def main():
    interceptor = MobileAppInterceptor()
    
    print("🏠 CS1000X Mobile App Network Interceptor")
    print("This tool helps capture API calls from the CS1000X mobile app")
    print()
    
    choice = input("Choose method:\n1. Start proxy server\n2. Samsung DeX analysis guide\n3. Both\nChoice (1-3): ")
    
    if choice in ['1', '3']:
        print("\nStarting proxy server...")
        interceptor.start_proxy_server()
    
    if choice in ['2', '3']:
        interceptor.analyze_samsung_dex()
        
    if choice not in ['1', '2', '3']:
        print("Invalid choice. Showing Samsung DeX guide:")
        interceptor.analyze_samsung_dex()

if __name__ == "__main__":
    main()
