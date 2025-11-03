#!/usr/bin/env python3
"""
Roku Stealth Client - Advanced browser simulation for CS1000X camera access
Uses sophisticated techniques to bypass bot detection
"""

import requests
import json
import time
import re
from urllib.parse import urlparse, parse_qs, urlencode
import base64
import hashlib
import uuid
import random

class RokuStealthClient:
    def __init__(self):
        self.session = requests.Session()
        self.access_token = None
        self.user_id = None
        
        # Generate realistic device fingerprint
        self.device_fingerprint = self.generate_device_fingerprint()
        
        # Realistic browser headers (Chrome on Windows)
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Cache-Control': 'max-age=0'
        })
        
        # Add realistic timing delays
        self.min_delay = 1.0
        self.max_delay = 3.0
    
    def generate_device_fingerprint(self):
        """Generate realistic browser fingerprint"""
        screen_resolutions = ['1920x1080', '1366x768', '1536x864', '1440x900']
        timezones = ['America/New_York', 'America/Chicago', 'America/Denver', 'America/Los_Angeles']
        
        return {
            'screen_resolution': random.choice(screen_resolutions),
            'timezone': random.choice(timezones),
            'language': 'en-US',
            'platform': 'Win32',
            'cookie_enabled': True,
            'do_not_track': False
        }
    
    def human_delay(self):
        """Add human-like delays between requests"""
        delay = random.uniform(self.min_delay, self.max_delay)
        time.sleep(delay)
    
    def simulate_browser_behavior(self):
        """Simulate realistic browser behavior before authentication"""
        print("🤖 Simulating realistic browser behavior...")
        
        # Step 1: Visit Roku homepage (like a real user)
        try:
            self.session.get('https://www.roku.com', timeout=10)
            self.human_delay()
            print("✅ Visited Roku homepage")
        except:
            pass
        
        # Step 2: Visit account/login page naturally
        try:
            response = self.session.get('https://my.roku.com', timeout=10)
            self.human_delay()
            print("✅ Visited my.roku.com")
            
            # Look for login links and follow them
            if 'sign in' in response.text.lower() or 'login' in response.text.lower():
                login_links = re.findall(r'href=["\']([^"\']*(?:signin|login)[^"\']*)["\']', response.text, re.IGNORECASE)
                if login_links:
                    login_url = login_links[0]
                    if not login_url.startswith('http'):
                        login_url = 'https://my.roku.com' + login_url
                    
                    print(f"✅ Found login URL: {login_url}")
                    return login_url
        except:
            pass
        
        # Fallback login URLs
        return 'https://my.roku.com/account/signin'
    
    def extract_form_data(self, html_content, form_action_url):
        """Extract all form data including hidden fields"""
        form_data = {}
        
        # Extract hidden input fields
        hidden_inputs = re.findall(
            r'<input[^>]*type=["\']hidden["\'][^>]*name=["\']([^"\']+)["\'][^>]*value=["\']([^"\']*)["\']',
            html_content, re.IGNORECASE
        )
        
        for name, value in hidden_inputs:
            form_data[name] = value
            print(f"Found hidden field: {name} = {value[:20]}...")
        
        # Look for CSRF tokens in meta tags
        csrf_meta = re.search(r'<meta[^>]*name=["\']csrf-token["\'][^>]*content=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
        if csrf_meta:
            form_data['_token'] = csrf_meta.group(1)
            print(f"Found CSRF meta token: {csrf_meta.group(1)[:20]}...")
        
        return form_data
    
    def authenticate_like_browser(self, username, password):
        """Authenticate using realistic browser simulation"""
        print(f"🌐 Browser-style authentication for {username}")
        
        try:
            # Step 1: Simulate realistic browsing behavior
            login_url = self.simulate_browser_behavior()
            
            # Step 2: Get the login page
            print(f"📄 Getting login page: {login_url}")
            login_response = self.session.get(login_url, timeout=10)
            self.human_delay()
            
            if login_response.status_code != 200:
                print(f"❌ Login page not accessible: {login_response.status_code}")
                return False
            
            print(f"✅ Login page loaded ({len(login_response.text)} bytes)")
            
            # Step 3: Extract form data
            form_data = self.extract_form_data(login_response.text, login_url)
            
            # Step 4: Find form action
            form_action = self.find_form_action(login_response.text)
            if not form_action:
                form_action = login_url
            
            print(f"📝 Form action: {form_action}")
            
            # Step 5: Prepare login data
            login_data = {
                'email': username,
                'password': password,
                **form_data  # Include all hidden fields and tokens
            }
            
            # Update headers for form submission
            self.session.headers.update({
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://my.roku.com',
                'Referer': login_url,
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1'
            })
            
            print("🔐 Submitting login form...")
            self.human_delay()  # Human-like delay before submission
            
            # Step 6: Submit form
            auth_response = self.session.post(form_action, data=login_data, allow_redirects=True, timeout=15)
            
            print(f"Auth response status: {auth_response.status_code}")
            print(f"Auth response URL: {auth_response.url}")
            print(f"Auth response content-type: {auth_response.headers.get('content-type', 'unknown')}")
            
            # Step 7: Check for successful authentication
            return self.check_authentication_success(auth_response)
            
        except Exception as e:
            print(f"❌ Browser authentication error: {e}")
            return False
    
    def find_form_action(self, html_content):
        """Find the form action URL"""
        # Look for login form action
        form_patterns = [
            r'<form[^>]*action=["\']([^"\']*(?:signin|login|auth)[^"\']*)["\']',
            r'<form[^>]*action=["\']([^"\']+)["\']'
        ]
        
        for pattern in form_patterns:
            match = re.search(pattern, html_content, re.IGNORECASE)
            if match:
                action = match.group(1)
                if not action.startswith('http'):
                    action = 'https://my.roku.com' + action
                return action
        
        return None
    
    def check_authentication_success(self, response):
        """Check if authentication was successful"""
        # Check URL for success indicators
        success_urls = ['dashboard', 'account', 'home', 'profile']
        for indicator in success_urls:
            if indicator in response.url.lower():
                print(f"✅ Authentication successful - redirected to {indicator}")
                self.access_token = "authenticated_browser_session"
                return True
        
        # Check for authentication cookies
        auth_cookies = ['auth', 'session', 'token', 'login']
        for cookie in self.session.cookies:
            for auth_indicator in auth_cookies:
                if auth_indicator in cookie.name.lower():
                    print(f"✅ Authentication successful - found auth cookie: {cookie.name}")
                    self.access_token = f"cookie_{cookie.name}_{cookie.value[:20]}"
                    return True
        
        # Check HTML content for success indicators
        html_lower = response.text.lower()
        success_indicators = ['welcome', 'dashboard', 'logout', 'my account', 'signed in']
        for indicator in success_indicators:
            if indicator in html_lower:
                print(f"✅ Authentication successful - found indicator: {indicator}")
                self.access_token = "authenticated_browser_session"
                return True
        
        # Check for absence of login form
        if 'password' not in html_lower and 'sign in' not in html_lower:
            print("✅ Authentication likely successful - no login form present")
            self.access_token = "authenticated_browser_session"
            return True
        
        print("❌ Authentication appears to have failed")
        return False
    
    def discover_cameras_via_web(self):
        """Try to discover cameras through web interface"""
        if not self.access_token:
            return []
        
        print("📹 Searching for cameras via web interface...")
        
        # Common camera/device pages
        camera_urls = [
            'https://my.roku.com/account/devices',
            'https://my.roku.com/devices',
            'https://my.roku.com/cameras',
            'https://my.roku.com/account/cameras',
            'https://my.roku.com/home',
            'https://my.roku.com/dashboard'
        ]
        
        for url in camera_urls:
            try:
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    # Look for camera-related content
                    if self.find_camera_references(response.text):
                        print(f"✅ Found camera references at: {url}")
                        return self.extract_camera_info(response.text)
                self.human_delay()
            except:
                continue
        
        return []
    
    def find_camera_references(self, html_content):
        """Look for camera references in HTML"""
        camera_keywords = ['camera', 'cs1000x', 'device', 'stream', 'video']
        html_lower = html_content.lower()
        
        for keyword in camera_keywords:
            if keyword in html_lower:
                return True
        return False
    
    def extract_camera_info(self, html_content):
        """Extract camera information from HTML"""
        cameras = []
        
        # Look for specific device ID first
        target_device_id = 'SOS2000V3AD89EB106D4'
        if target_device_id in html_content:
            print(f"✅ Found target device ID: {target_device_id}")
            cameras.append({
                'id': target_device_id,
                'type': 'CS1000X',
                'name': 'Basement Camera',
                'source': 'device_id_match'
            })
        
        # Look for device IDs, MAC addresses, or camera names
        device_patterns = [
            r'S0S\d+V\d+[A-F0-9]+',  # CS1000X device ID pattern (updated)
            r'SOS\d+V\d+[A-F0-9]+',  # Alternative CS1000X device ID pattern
            r'[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}',  # MAC address
            r'CS1000X[^<]*',  # CS1000X references
        ]
        
        for pattern in device_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                cameras.append({
                    'id': match,
                    'type': 'CS1000X',
                    'source': 'web_extraction'
                })
        
        return cameras
    
    def try_direct_device_access(self):
        """Try to access the camera directly using known device ID"""
        if not self.access_token:
            return []
        
        print("🎯 Trying direct device access with known device ID...")
        
        device_id = 'SOS2000V3AD89EB106D4'
        
        # Try various device/camera API endpoints with the specific device ID
        device_endpoints = [
            f'https://my.roku.com/api/v1/devices/{device_id}',
            f'https://my.roku.com/api/v1/cameras/{device_id}',
            f'https://my.roku.com/devices/{device_id}',
            f'https://my.roku.com/cameras/{device_id}',
            f'https://api.roku.com/v1/devices/{device_id}',
            f'https://services.roku.com/api/v1/devices/{device_id}',
            f'https://my.roku.com/account/devices/{device_id}',
        ]
        
        for endpoint in device_endpoints:
            try:
                print(f"Testing device endpoint: {endpoint}")
                response = self.session.get(endpoint, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ Device endpoint accessible: {endpoint}")
                    print(f"📄 Response content preview: {response.text[:300]}...")
                    
                    # Save full response for analysis
                    with open(f'device_response_{device_id}.html', 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print(f"💾 Saved full response to device_response_{device_id}.html")
                    
                    # Try to extract stream information
                    stream_found = False
                    
                    # Enhanced stream URL patterns
                    stream_patterns = [
                        r'rtmp://[^\s"\'<>]+',
                        r'rtsp://[^\s"\'<>]+',
                        r'https://[^\s"\'<>]*stream[^\s"\'<>]*',
                        r'wss://[^\s"\'<>]*stream[^\s"\'<>]*',
                        r'https://[^\s"\'<>]*video[^\s"\'<>]*',
                        r'https://[^\s"\'<>]*live[^\s"\'<>]*',
                        r'https://[^\s"\'<>]*camera[^\s"\'<>]*',
                        r'"url":\s*"([^"]*stream[^"]*)"',
                        r'"stream_url":\s*"([^"]*)"',
                        r'"video_url":\s*"([^"]*)"',
                        r'"live_url":\s*"([^"]*)"'
                    ]
                    
                    all_stream_urls = []
                    for pattern in stream_patterns:
                        matches = re.findall(pattern, response.text, re.IGNORECASE)
                        if matches:
                            all_stream_urls.extend(matches)
                            stream_found = True
                    
                    if stream_found:
                        print(f"🎯 Found potential stream URLs: {all_stream_urls}")
                        return [{
                            'id': device_id,
                            'type': 'CS1000X',
                            'name': 'Basement Camera',
                            'stream_urls': all_stream_urls,
                            'source': 'direct_device_api'
                        }]
                    
                    # Look for any JSON data that might contain streaming info
                    try:
                        json_data = response.json()
                        print(f"📊 Found JSON data: {json.dumps(json_data, indent=2)[:500]}...")
                        
                        # Search JSON for stream-related keys
                        def find_stream_keys(obj, path=""):
                            results = []
                            if isinstance(obj, dict):
                                for key, value in obj.items():
                                    current_path = f"{path}.{key}" if path else key
                                    if any(keyword in key.lower() for keyword in ['stream', 'video', 'url', 'live', 'camera']):
                                        results.append((current_path, value))
                                    if isinstance(value, (dict, list)):
                                        results.extend(find_stream_keys(value, current_path))
                            elif isinstance(obj, list):
                                for i, item in enumerate(obj):
                                    results.extend(find_stream_keys(item, f"{path}[{i}]"))
                            return results
                        
                        stream_keys = find_stream_keys(json_data)
                        if stream_keys:
                            print("🔍 Found stream-related JSON keys:")
                            for path, value in stream_keys:
                                print(f"   {path}: {value}")
                            
                            return [{
                                'id': device_id,
                                'type': 'CS1000X',
                                'name': 'Basement Camera',
                                'json_data': json_data,
                                'stream_keys': stream_keys,
                                'source': 'direct_device_api'
                            }]
                    except:
                        pass
                    
                    return [{
                        'id': device_id,
                        'type': 'CS1000X',
                        'name': 'Basement Camera',
                        'source': 'direct_device_api'
                    }]
                
                elif response.status_code != 404:
                    print(f"Device endpoint responded: {endpoint} -> {response.status_code}")
                
                self.human_delay()
                
            except Exception as e:
                print(f"Device endpoint error {endpoint}: {e}")
                continue
        
        return []
    
    def test_stealth_authentication(self, username, password):
        """Test the complete stealth authentication process"""
        print("🥷 Starting Stealth Authentication (Advanced Browser Simulation)")
        print("="*70)
        
        success = self.authenticate_like_browser(username, password)
        
        if success:
            print("✅ Stealth authentication successful!")
            
            # Try direct device access first (most targeted)
            cameras = self.try_direct_device_access()
            
            if not cameras:
                # Fallback to web interface discovery
                cameras = self.discover_cameras_via_web()
            
            # If we found cameras but no stream URLs, try Smart Home API first
            if cameras and not any('stream_urls' in cam for cam in cameras):
                print("🏠 Trying Smart Home API discovery...")
                try:
                    from roku_smarthome_api import RokuSmartHomeAPI
                    smarthome_api = RokuSmartHomeAPI(self.session)
                    smarthome_cameras = smarthome_api.discover_smarthome_cameras()
                    
                    if smarthome_cameras:
                        # Replace or merge with Smart Home cameras
                        cameras = smarthome_cameras
                        print(f"✅ Found {len(smarthome_cameras)} cameras via Smart Home API!")
                    else:
                        # Fallback to targeted stream search
                        print("🎥 No Smart Home cameras found, trying targeted stream search...")
                        from roku_targeted_stream_finder import RokuTargetedStreamFinder
                        stream_finder = RokuTargetedStreamFinder(self.session)
                        found_streams = stream_finder.find_streams_systematically()
                        
                        if not found_streams:
                            # Try stream activation as last resort
                            print("🎬 Trying stream activation...")
                            found_streams = stream_finder.try_stream_activation()
                        
                        if found_streams:
                            # Add stream URLs to the first camera
                            cameras[0]['stream_urls'] = found_streams
                            cameras[0]['source'] = 'targeted_stream_search'
                            print(f"✅ Found {len(found_streams)} stream URLs via targeted search!")
                except Exception as e:
                    print(f"Smart Home API error: {e}")
            
            if cameras:
                print(f"📹 Found {len(cameras)} cameras")
                for camera in cameras:
                    print(f"   - {camera.get('name', camera['id'])}: {camera['source']}")
                    if 'stream_urls' in camera:
                        print(f"     Stream URLs: {camera['stream_urls']}")
                return True
            else:
                print("⚠️ Authentication successful but no cameras found")
                return True  # Still a success - authentication worked
        else:
            print("❌ Stealth authentication failed")
            return False

def main():
    client = RokuStealthClient()
    
    print("🥷 CS1000X Stealth Client - Advanced Browser Simulation")
    print("="*60)
    print("This uses sophisticated browser simulation to bypass bot detection")
    print()
    
    # Test without credentials first
    print("🧪 Testing stealth capabilities...")
    print("Ready for authentication testing with real credentials!")

if __name__ == "__main__":
    main()
