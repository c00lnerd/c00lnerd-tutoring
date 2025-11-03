#!/usr/bin/env python3
"""
Roku Authenticated Streamer - Use authenticated session to proxy camera streams
"""

import requests
import time
from flask import Response
import io

class RokuAuthenticatedStreamer:
    def __init__(self, authenticated_session):
        self.session = authenticated_session
        self.device_id = 'SOS2000V3AD89EB106D4'
        
        # The working streaming endpoints we discovered
        self.stream_endpoints = [
            f'https://my.roku.com/account/devices/{self.device_id}/stream',
            f'https://my.roku.com/account/devices/{self.device_id}/live'
        ]
    
    def get_authenticated_stream(self, endpoint_type='stream'):
        """Get stream using authenticated session"""
        if endpoint_type == 'live':
            url = self.stream_endpoints[1]
        else:
            url = self.stream_endpoints[0]
        
        print(f"🎥 Getting authenticated stream from: {url}")
        
        try:
            # Make authenticated request
            response = self.session.get(url, stream=True, timeout=30)
            
            if response.status_code == 200:
                print(f"✅ Stream response received: {response.headers.get('content-type', 'unknown')}")
                return response
            else:
                print(f"❌ Stream request failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Stream error: {e}")
            return None
    
    def create_mjpeg_stream(self, endpoint_type='stream'):
        """Create MJPEG stream from authenticated Roku endpoint"""
        print(f"🎬 Creating MJPEG stream from Roku {endpoint_type} endpoint")
        
        def generate_frames():
            while True:
                try:
                    # Get authenticated stream response
                    stream_response = self.get_authenticated_stream(endpoint_type)
                    
                    if stream_response:
                        # Check if it's already a video stream
                        content_type = stream_response.headers.get('content-type', '')
                        
                        if 'video' in content_type or 'octet-stream' in content_type:
                            # Direct video stream - pass through
                            for chunk in stream_response.iter_content(chunk_size=8192):
                                if chunk:
                                    yield chunk
                        
                        elif 'multipart' in content_type:
                            # MJPEG stream - pass through
                            for chunk in stream_response.iter_content(chunk_size=8192):
                                if chunk:
                                    yield chunk
                        
                        else:
                            # HTML page - create a placeholder frame
                            placeholder_frame = self.create_placeholder_frame(
                                f"Roku {endpoint_type.title()} Endpoint Active",
                                "Authentication successful - endpoint accessible",
                                f"URL: {stream_response.url}"
                            )
                            
                            yield (b'--frame\r\n'
                                   b'Content-Type: image/jpeg\r\n\r\n' + 
                                   placeholder_frame + b'\r\n')
                            
                            time.sleep(1)  # Update every second
                    else:
                        # Connection failed - show error frame
                        error_frame = self.create_placeholder_frame(
                            "Stream Connection Failed",
                            "Could not connect to Roku stream endpoint",
                            "Check authentication status"
                        )
                        
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + 
                               error_frame + b'\r\n')
                        
                        time.sleep(2)
                
                except Exception as e:
                    print(f"Stream generation error: {e}")
                    time.sleep(1)
        
        return Response(generate_frames(),
                       mimetype='multipart/x-mixed-replace; boundary=frame')
    
    def create_placeholder_frame(self, title, message, details=""):
        """Create a placeholder JPEG frame"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create image
            img = Image.new('RGB', (640, 480), color='#1a1a1a')
            draw = ImageDraw.Draw(img)
            
            # Try to use a font, fallback to default
            try:
                font_large = ImageFont.truetype("arial.ttf", 24)
                font_medium = ImageFont.truetype("arial.ttf", 16)
                font_small = ImageFont.truetype("arial.ttf", 12)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Draw text
            draw.text((320, 180), title, fill='#4CAF50', font=font_large, anchor='mm')
            draw.text((320, 220), message, fill='white', font=font_medium, anchor='mm')
            if details:
                draw.text((320, 260), details, fill='#888', font=font_small, anchor='mm')
            
            # Add timestamp
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            draw.text((320, 320), f"Last updated: {timestamp}", fill='#666', font=font_small, anchor='mm')
            
            # Convert to JPEG bytes
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='JPEG', quality=85)
            return img_buffer.getvalue()
            
        except ImportError:
            # Fallback: create SVG as JPEG alternative
            svg_content = f'''<svg width="640" height="480" xmlns="http://www.w3.org/2000/svg">
                <rect width="640" height="480" fill="#1a1a1a"/>
                <text x="320" y="180" text-anchor="middle" fill="#4CAF50" font-size="24" font-family="Arial">
                    {title}
                </text>
                <text x="320" y="220" text-anchor="middle" fill="white" font-size="16" font-family="Arial">
                    {message}
                </text>
                <text x="320" y="260" text-anchor="middle" fill="#888" font-size="12" font-family="Arial">
                    {details}
                </text>
                <text x="320" y="320" text-anchor="middle" fill="#666" font-size="10" font-family="Arial">
                    {time.strftime("%Y-%m-%d %H:%M:%S")}
                </text>
            </svg>'''
            
            return svg_content.encode('utf-8')
    
    def test_stream_endpoints(self):
        """Test both stream endpoints"""
        print("🧪 TESTING AUTHENTICATED STREAM ENDPOINTS")
        print("=" * 50)
        
        for i, endpoint in enumerate(self.stream_endpoints):
            endpoint_name = 'stream' if i == 0 else 'live'
            print(f"\n🎯 Testing {endpoint_name} endpoint:")
            
            try:
                response = self.session.get(endpoint, timeout=10)
                print(f"   Status: {response.status_code}")
                print(f"   Content-Type: {response.headers.get('content-type', 'unknown')}")
                print(f"   Content-Length: {response.headers.get('content-length', 'unknown')}")
                
                if response.status_code == 200:
                    print(f"   ✅ Endpoint accessible")
                    
                    # Check if it might be a direct stream
                    content_type = response.headers.get('content-type', '').lower()
                    if any(video_type in content_type for video_type in 
                          ['video/', 'application/octet-stream', 'multipart/x-mixed-replace']):
                        print(f"   🎥 DIRECT VIDEO STREAM DETECTED!")
                    else:
                        print(f"   📄 HTML interface (requires interaction)")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")

def main():
    print("🎥 Roku Authenticated Streamer")
    print("This requires an authenticated Roku session")

if __name__ == "__main__":
    main()
