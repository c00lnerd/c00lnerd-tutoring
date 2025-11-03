#!/usr/bin/env python3
"""
Roku Stream Finder - Try different approaches to find CS1000X stream URLs
"""

import requests
import json
import time
import re

class RokuStreamFinder:
    def __init__(self, session):
        self.session = session
        self.device_id = 'SOS2000V3AD89EB106D4'
        
    def try_stream_endpoints(self):
        """Try various streaming-related endpoints"""
        print("🎥 Trying streaming endpoints...")
        
        # Potential streaming endpoints
        stream_endpoints = [
            f'https://my.roku.com/api/v1/devices/{self.device_id}/stream',
            f'https://my.roku.com/api/v1/devices/{self.device_id}/live',
            f'https://my.roku.com/api/v1/devices/{self.device_id}/video',
            f'https://my.roku.com/api/v1/cameras/{self.device_id}/stream',
            f'https://my.roku.com/api/v1/cameras/{self.device_id}/live',
            f'https://my.roku.com/devices/{self.device_id}/stream',
            f'https://my.roku.com/cameras/{self.device_id}/stream',
            f'https://api.roku.com/v1/devices/{self.device_id}/stream',
            f'https://services.roku.com/api/v1/devices/{self.device_id}/stream',
            f'https://stream.roku.com/devices/{self.device_id}',
            f'https://video.roku.com/devices/{self.device_id}',
            f'https://live.roku.com/devices/{self.device_id}'
        ]
        
        found_streams = []
        
        for endpoint in stream_endpoints:
            try:
                print(f"Testing: {endpoint}")
                response = self.session.get(endpoint, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ Stream endpoint accessible: {endpoint}")
                    
                    # Try to parse as JSON
                    try:
                        data = response.json()
                        print(f"📊 JSON response: {json.dumps(data, indent=2)[:300]}...")
                        
                        # Look for stream URLs in JSON
                        stream_urls = self.extract_streams_from_json(data)
                        if stream_urls:
                            found_streams.extend(stream_urls)
                            
                    except json.JSONDecodeError:
                        # Not JSON, look for URLs in text
                        stream_urls = self.extract_streams_from_text(response.text)
                        if stream_urls:
                            found_streams.extend(stream_urls)
                
                elif response.status_code == 302:
                    print(f"🔄 Redirect from {endpoint} to: {response.headers.get('Location', 'unknown')}")
                    redirect_url = response.headers.get('Location')
                    if redirect_url and 'stream' in redirect_url.lower():
                        found_streams.append(redirect_url)
                
                elif response.status_code not in [404, 403]:
                    print(f"📄 Response {response.status_code}: {response.text[:100]}...")
                
                time.sleep(0.5)  # Be nice to their servers
                
            except Exception as e:
                print(f"Error testing {endpoint}: {e}")
                continue
        
        return found_streams
    
    def extract_streams_from_json(self, data):
        """Extract stream URLs from JSON data"""
        streams = []
        
        def search_json(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    
                    # Check if this looks like a stream URL
                    if isinstance(value, str) and self.is_stream_url(value):
                        streams.append(value)
                        print(f"🎯 Found stream in JSON at {current_path}: {value}")
                    
                    # Recursively search nested objects
                    if isinstance(value, (dict, list)):
                        search_json(value, current_path)
                        
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    search_json(item, f"{path}[{i}]")
        
        search_json(data)
        return streams
    
    def extract_streams_from_text(self, text):
        """Extract stream URLs from text content"""
        streams = []
        
        # Stream URL patterns
        patterns = [
            r'rtmp://[^\s"\'<>]+',
            r'rtsp://[^\s"\'<>]+',
            r'https://[^\s"\'<>]*stream[^\s"\'<>]*',
            r'wss://[^\s"\'<>]*stream[^\s"\'<>]*',
            r'https://[^\s"\'<>]*video[^\s"\'<>]*\.m3u8',
            r'https://[^\s"\'<>]*live[^\s"\'<>]*\.m3u8'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if self.is_stream_url(match):
                    streams.append(match)
                    print(f"🎯 Found stream URL: {match}")
        
        return streams
    
    def is_stream_url(self, url):
        """Check if URL looks like a streaming URL"""
        if not isinstance(url, str):
            return False
        
        stream_indicators = [
            'rtmp://', 'rtsp://', 'stream', 'video', 'live', 
            '.m3u8', '.ts', '.flv', '.mp4'
        ]
        
        url_lower = url.lower()
        return any(indicator in url_lower for indicator in stream_indicators)
    
    def try_device_control_endpoints(self):
        """Try device control endpoints that might reveal streaming info"""
        print("🎮 Trying device control endpoints...")
        
        control_endpoints = [
            f'https://my.roku.com/api/v1/devices/{self.device_id}/status',
            f'https://my.roku.com/api/v1/devices/{self.device_id}/info',
            f'https://my.roku.com/api/v1/devices/{self.device_id}/config',
            f'https://my.roku.com/api/v1/devices/{self.device_id}/capabilities',
            f'https://my.roku.com/devices/{self.device_id}/status',
            f'https://my.roku.com/devices/{self.device_id}/info'
        ]
        
        device_info = {}
        
        for endpoint in control_endpoints:
            try:
                print(f"Testing control endpoint: {endpoint}")
                response = self.session.get(endpoint, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ Control endpoint accessible: {endpoint}")
                    
                    try:
                        data = response.json()
                        device_info[endpoint] = data
                        print(f"📊 Device info: {json.dumps(data, indent=2)[:200]}...")
                        
                        # Look for streaming capabilities
                        if 'stream' in str(data).lower() or 'video' in str(data).lower():
                            print("🎥 Found streaming references in device info!")
                            
                    except json.JSONDecodeError:
                        print(f"📄 Text response: {response.text[:200]}...")
                
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error testing control endpoint: {e}")
                continue
        
        return device_info
    
    def find_all_streams(self):
        """Try all methods to find stream URLs"""
        print("🔍 COMPREHENSIVE STREAM SEARCH")
        print("=" * 50)
        
        all_streams = []
        
        # Method 1: Direct streaming endpoints
        streams1 = self.try_stream_endpoints()
        all_streams.extend(streams1)
        
        # Method 2: Device control endpoints
        device_info = self.try_device_control_endpoints()
        
        # Method 3: Look for streaming in device info
        for endpoint, info in device_info.items():
            streams2 = self.extract_streams_from_json(info)
            all_streams.extend(streams2)
        
        # Remove duplicates
        unique_streams = list(set(all_streams))
        
        print(f"\n🎯 FINAL RESULTS:")
        print(f"Found {len(unique_streams)} unique stream URLs:")
        for i, stream in enumerate(unique_streams, 1):
            print(f"   {i}. {stream}")
        
        return unique_streams

def main():
    """Test the stream finder with an authenticated session"""
    print("🎥 CS1000X Stream Finder")
    print("This requires an authenticated Roku session")
    print("Run this after successful stealth authentication")

if __name__ == "__main__":
    main()
