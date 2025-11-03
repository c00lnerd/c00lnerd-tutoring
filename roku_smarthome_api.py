#!/usr/bin/env python3
"""
Roku Smart Home API - Access cameras through the web Smart Home interface
"""

import requests
import json
import re
import time

class RokuSmartHomeAPI:
    def __init__(self, authenticated_session):
        self.session = authenticated_session
        self.base_url = 'https://my.roku.com/smarthome'
        self.api_base = 'https://owner.web.roku.com/smarthome/api/v1'
        self.websocket_url = 'wss://aspen-sockets.aspen.msc.roku.com'
        
    def discover_smarthome_cameras(self):
        """Discover cameras through Smart Home API"""
        print("🏠 DISCOVERING SMART HOME CAMERAS")
        print("=" * 50)
        
        cameras = []
        
        # Try the correct Smart Home API endpoints based on page source
        api_endpoints = [
            f'{self.api_base}/cameras',
            f'{self.api_base}/devices',
            f'{self.api_base}/streams',
            f'{self.api_base}/live',
            f'{self.api_base}/status',
            f'{self.api_base}/config',
            'https://owner.web.roku.com/api/v1/cameras',
            'https://owner.web.roku.com/api/v1/devices',
            f'{self.base_url}/api/v1/cameras',
            f'{self.base_url}/api/v1/devices'
        ]
        
        for endpoint in api_endpoints:
            try:
                print(f"🔍 Testing API: {endpoint}")
                response = self.session.get(endpoint, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ API accessible: {endpoint}")
                    
                    try:
                        data = response.json()
                        print(f"📊 JSON response: {json.dumps(data, indent=2)[:300]}...")
                        
                        # Look for camera data in response
                        cameras_found = self.extract_cameras_from_api(data, endpoint)
                        cameras.extend(cameras_found)
                        
                    except json.JSONDecodeError:
                        print(f"📄 HTML response: {response.text[:200]}...")
                        
                        # Look for cameras in HTML
                        html_cameras = self.extract_cameras_from_html(response.text, endpoint)
                        cameras.extend(html_cameras)
                
                elif response.status_code == 302:
                    redirect = response.headers.get('Location', '')
                    print(f"🔄 Redirects to: {redirect}")
                    
                else:
                    print(f"❌ {response.status_code}: {response.text[:100]}...")
                
                time.sleep(0.5)  # Be nice to their servers
                
            except Exception as e:
                print(f"❌ Error testing {endpoint}: {e}")
        
        # Also try the main Smart Home page
        try:
            print(f"\n🔍 Analyzing main Smart Home page...")
            response = self.session.get(self.base_url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Smart Home page accessible")
                
                # Save the page for analysis
                with open('smarthome_page.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"💾 Saved Smart Home page to: smarthome_page.html")
                
                # Extract cameras from the main page
                page_cameras = self.extract_cameras_from_html(response.text, self.base_url)
                cameras.extend(page_cameras)
                
                # Look for JavaScript API calls
                js_apis = self.extract_js_api_calls(response.text)
                if js_apis:
                    print(f"🔍 Found JavaScript API calls: {js_apis}")
                    
                    # Test the discovered API endpoints
                    for api_call in js_apis:
                        if not api_call.startswith('http'):
                            api_call = 'https://my.roku.com' + api_call
                        
                        try:
                            print(f"🧪 Testing discovered API: {api_call}")
                            api_response = self.session.get(api_call, timeout=5)
                            
                            if api_response.status_code == 200:
                                print(f"✅ Discovered API works: {api_call}")
                                
                                try:
                                    api_data = api_response.json()
                                    api_cameras = self.extract_cameras_from_api(api_data, api_call)
                                    cameras.extend(api_cameras)
                                except:
                                    pass
                        except:
                            pass
        
        except Exception as e:
            print(f"❌ Error analyzing Smart Home page: {e}")
        
        # Remove duplicates
        unique_cameras = []
        seen_ids = set()
        
        for camera in cameras:
            camera_id = camera.get('id', camera.get('device_id', str(len(unique_cameras))))
            if camera_id not in seen_ids:
                unique_cameras.append(camera)
                seen_ids.add(camera_id)
        
        print(f"\n🎯 SMART HOME DISCOVERY RESULTS:")
        print(f"Found {len(unique_cameras)} unique cameras:")
        for camera in unique_cameras:
            print(f"   - {camera.get('name', 'Unknown')}: {camera.get('source', 'unknown')}")
            if 'stream_url' in camera:
                print(f"     Stream: {camera['stream_url']}")
        
        return unique_cameras
    
    def extract_cameras_from_api(self, data, source):
        """Extract camera information from API JSON response"""
        cameras = []
        
        def search_for_cameras(obj, path=""):
            if isinstance(obj, dict):
                # Look for camera-like objects
                if any(key in obj for key in ['camera', 'device', 'stream', 'video']):
                    camera_info = {
                        'source': f'api_{source.split("/")[-1]}',
                        'raw_data': obj
                    }
                    
                    # Extract common fields
                    for field in ['id', 'device_id', 'name', 'status', 'type']:
                        if field in obj:
                            camera_info[field] = obj[field]
                    
                    # Look for streaming URLs
                    for stream_field in ['stream_url', 'video_url', 'live_url', 'rtmp_url']:
                        if stream_field in obj:
                            camera_info['stream_url'] = obj[stream_field]
                            print(f"🎥 Found stream URL: {obj[stream_field]}")
                    
                    cameras.append(camera_info)
                
                # Recursively search nested objects
                for key, value in obj.items():
                    if isinstance(value, (dict, list)):
                        search_for_cameras(value, f"{path}.{key}")
            
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    search_for_cameras(item, f"{path}[{i}]")
        
        search_for_cameras(data)
        return cameras
    
    def extract_cameras_from_html(self, html, source):
        """Extract camera information from HTML content"""
        cameras = []
        
        # Look for video elements
        video_pattern = r'<video[^>]*src=["\']([^"\']*)["\'][^>]*>'
        video_matches = re.findall(video_pattern, html, re.IGNORECASE)
        
        for video_src in video_matches:
            cameras.append({
                'source': f'html_video_{source.split("/")[-1]}',
                'stream_url': video_src,
                'type': 'video_element'
            })
            print(f"🎥 Found HTML video element: {video_src}")
        
        # Look for camera names and IDs
        camera_patterns = [
            r'"camera[^"]*":\s*"([^"]*)"',
            r'"device[^"]*":\s*"([^"]*)"',
            r'data-camera[^=]*=["\']([^"\']*)["\']',
            r'SOS2000V3AD89EB106D4'  # Your specific device ID
        ]
        
        for pattern in camera_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                cameras.append({
                    'source': f'html_pattern_{source.split("/")[-1]}',
                    'id': match,
                    'type': 'pattern_match'
                })
        
        return cameras
    
    def extract_js_api_calls(self, html):
        """Extract JavaScript API calls from HTML"""
        api_calls = []
        
        # Look for fetch() calls
        fetch_pattern = r'fetch\(["\']([^"\']*api[^"\']*)["\']'
        fetch_matches = re.findall(fetch_pattern, html, re.IGNORECASE)
        api_calls.extend(fetch_matches)
        
        # Look for AJAX calls
        ajax_pattern = r'\.get\(["\']([^"\']*api[^"\']*)["\']'
        ajax_matches = re.findall(ajax_pattern, html, re.IGNORECASE)
        api_calls.extend(ajax_matches)
        
        # Look for API endpoints in JavaScript
        api_pattern = r'["\']([^"\']*smarthome/api[^"\']*)["\']'
        api_matches = re.findall(api_pattern, html, re.IGNORECASE)
        api_calls.extend(api_matches)
        
        return list(set(api_calls))  # Remove duplicates
    
    def get_camera_stream_url(self, camera_id):
        """Get direct stream URL for a specific camera"""
        print(f"🎥 Getting stream URL for camera: {camera_id}")
        
        # Try various streaming endpoints
        stream_endpoints = [
            f'{self.api_base}/cameras/{camera_id}/stream',
            f'{self.api_base}/devices/{camera_id}/stream',
            f'{self.api_base}/uc/cameras/{camera_id}/stream',
            f'{self.base_url}/cameras/{camera_id}/stream',
            f'{self.base_url}/devices/{camera_id}/stream'
        ]
        
        for endpoint in stream_endpoints:
            try:
                print(f"🔍 Testing stream endpoint: {endpoint}")
                response = self.session.get(endpoint, timeout=10)
                
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    
                    if 'video' in content_type or 'octet-stream' in content_type:
                        print(f"🎥 DIRECT VIDEO STREAM FOUND: {endpoint}")
                        return endpoint
                    
                    elif 'json' in content_type:
                        try:
                            data = response.json()
                            if 'stream_url' in data:
                                print(f"🎯 Stream URL in JSON: {data['stream_url']}")
                                return data['stream_url']
                        except:
                            pass
                
            except Exception as e:
                continue
        
        return None

def main():
    print("🏠 Roku Smart Home API Explorer")
    print("This requires an authenticated session")

if __name__ == "__main__":
    main()
