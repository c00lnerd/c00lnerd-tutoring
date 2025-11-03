#!/usr/bin/env python3
"""
Targeted Roku Stream Finder - Focus on working endpoints only
"""

import requests
import json
import time
import re

class RokuTargetedStreamFinder:
    def __init__(self, session):
        self.session = session
        self.device_id = 'SOS2000V3AD89EB106D4'
        
    def find_streams_systematically(self):
        """Systematic approach to find stream URLs using only working domains"""
        print("🎯 TARGETED STREAM SEARCH")
        print("=" * 50)
        
        all_streams = []
        
        # Focus only on my.roku.com since we know it works
        base_urls = ['https://my.roku.com']
        
        # Comprehensive endpoint patterns
        endpoint_patterns = [
            # Direct streaming endpoints
            '/api/v1/devices/{}/stream',
            '/api/v1/devices/{}/live',
            '/api/v1/devices/{}/video',
            '/api/v1/devices/{}/feed',
            '/api/v1/devices/{}/rtmp',
            '/api/v1/devices/{}/hls',
            '/api/v1/cameras/{}/stream',
            '/api/v1/cameras/{}/live',
            '/api/v1/cameras/{}/video',
            
            # Device control that might reveal streams
            '/api/v1/devices/{}/status',
            '/api/v1/devices/{}/info',
            '/api/v1/devices/{}/config',
            '/api/v1/devices/{}/capabilities',
            '/api/v1/devices/{}/settings',
            '/api/v1/devices/{}/properties',
            
            # Web interface endpoints
            '/devices/{}/stream',
            '/devices/{}/live',
            '/devices/{}/video',
            '/cameras/{}/stream',
            '/cameras/{}/live',
            '/account/devices/{}/stream',
            '/account/devices/{}/live',
            
            # Possible streaming control endpoints
            '/api/v1/devices/{}/start-stream',
            '/api/v1/devices/{}/get-stream-url',
            '/api/v1/devices/{}/streaming-info',
            '/api/v1/devices/{}/media-info'
        ]
        
        for base_url in base_urls:
            for pattern in endpoint_patterns:
                endpoint = base_url + pattern.format(self.device_id)
                
                try:
                    print(f"🔍 Testing: {endpoint}")
                    response = self.session.get(endpoint, timeout=10)
                    
                    if response.status_code == 200:
                        print(f"✅ SUCCESS: {endpoint}")
                        
                        # Analyze the response
                        streams = self.analyze_response(response, endpoint)
                        all_streams.extend(streams)
                        
                        # Save successful responses for manual inspection
                        filename = f"successful_response_{endpoint.split('/')[-1]}.json"
                        try:
                            with open(filename, 'w') as f:
                                if 'application/json' in response.headers.get('content-type', ''):
                                    json.dump(response.json(), f, indent=2)
                                else:
                                    f.write(response.text)
                            print(f"💾 Saved response to: {filename}")
                        except:
                            pass
                    
                    elif response.status_code == 302:
                        redirect_url = response.headers.get('Location', '')
                        print(f"🔄 Redirect to: {redirect_url}")
                        if 'stream' in redirect_url.lower():
                            all_streams.append(redirect_url)
                    
                    elif response.status_code not in [404, 403]:
                        print(f"📄 Response {response.status_code}: {response.text[:100]}...")
                    
                    time.sleep(0.3)  # Be respectful
                    
                except Exception as e:
                    if "getaddrinfo failed" not in str(e):
                        print(f"❌ Error: {e}")
                    continue
        
        # Remove duplicates and return
        unique_streams = list(set(all_streams))
        
        print(f"\n🎯 TARGETED SEARCH RESULTS:")
        print(f"Found {len(unique_streams)} unique stream URLs:")
        for i, stream in enumerate(unique_streams, 1):
            print(f"   {i}. {stream}")
        
        return unique_streams
    
    def analyze_response(self, response, endpoint):
        """Analyze response for stream URLs"""
        streams = []
        
        try:
            # Try JSON first
            if 'application/json' in response.headers.get('content-type', ''):
                data = response.json()
                print(f"📊 JSON data found: {json.dumps(data, indent=2)[:300]}...")
                
                # Deep search for stream URLs in JSON
                streams.extend(self.extract_streams_from_json(data))
            else:
                # Analyze as text
                streams.extend(self.extract_streams_from_text(response.text))
                
        except Exception as e:
            print(f"Analysis error for {endpoint}: {e}")
        
        return streams
    
    def extract_streams_from_json(self, data):
        """Extract stream URLs from JSON data"""
        streams = []
        
        def search_json(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    
                    # Check for stream-related keys
                    if any(keyword in key.lower() for keyword in 
                          ['stream', 'video', 'live', 'rtmp', 'rtsp', 'hls', 'url']):
                        print(f"🔍 Stream-related key found: {current_path} = {value}")
                        
                        if isinstance(value, str) and self.is_stream_url(value):
                            streams.append(value)
                            print(f"🎯 Stream URL found: {value}")
                    
                    # Recursively search
                    if isinstance(value, (dict, list)):
                        search_json(value, current_path)
                        
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    search_json(item, f"{path}[{i}]")
        
        search_json(data)
        return streams
    
    def extract_streams_from_text(self, text):
        """Extract stream URLs from text"""
        streams = []
        
        # Enhanced patterns for stream URLs
        patterns = [
            r'rtmp://[^\s"\'<>]+',
            r'rtsp://[^\s"\'<>]+',
            r'https://[^\s"\'<>]*stream[^\s"\'<>]*',
            r'wss://[^\s"\'<>]*stream[^\s"\'<>]*',
            r'https://[^\s"\'<>]*\.m3u8[^\s"\'<>]*',
            r'https://[^\s"\'<>]*video[^\s"\'<>]*\.mp4',
            r'https://[^\s"\'<>]*live[^\s"\'<>]*',
            r'"url":\s*"([^"]*)"',
            r'"stream_url":\s*"([^"]*)"',
            r'"video_url":\s*"([^"]*)"',
            r'"live_url":\s*"([^"]*)"'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if self.is_stream_url(match):
                    streams.append(match)
                    print(f"🎯 Text stream URL found: {match}")
        
        return streams
    
    def is_stream_url(self, url):
        """Check if URL looks like a streaming URL"""
        if not isinstance(url, str) or len(url) < 10:
            return False
        
        stream_indicators = [
            'rtmp://', 'rtsp://', 'stream', 'video', 'live', 
            '.m3u8', '.ts', '.flv', '.mp4', 'hls'
        ]
        
        url_lower = url.lower()
        return any(indicator in url_lower for indicator in stream_indicators)
    
    def try_stream_activation(self):
        """Try to activate streaming on the device"""
        print("🎬 Trying to activate streaming...")
        
        activation_endpoints = [
            f'https://my.roku.com/api/v1/devices/{self.device_id}/start-stream',
            f'https://my.roku.com/api/v1/devices/{self.device_id}/enable-streaming',
            f'https://my.roku.com/api/v1/devices/{self.device_id}/request-stream',
            f'https://my.roku.com/devices/{self.device_id}/start-stream'
        ]
        
        for endpoint in activation_endpoints:
            try:
                print(f"🎬 Trying activation: {endpoint}")
                
                # Try POST request to activate streaming
                response = self.session.post(endpoint, json={
                    'action': 'start_stream',
                    'quality': 'high',
                    'format': 'rtmp'
                }, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ Activation successful: {endpoint}")
                    
                    try:
                        data = response.json()
                        print(f"📊 Activation response: {json.dumps(data, indent=2)}")
                        
                        # Look for stream URLs in activation response
                        streams = self.extract_streams_from_json(data)
                        if streams:
                            print(f"🎯 Stream URLs from activation: {streams}")
                            return streams
                    except:
                        print(f"📄 Activation text response: {response.text[:200]}...")
                
                time.sleep(0.5)
                
            except Exception as e:
                continue
        
        return []

def main():
    print("🎯 Targeted Roku Stream Finder")
    print("This requires an authenticated session")

if __name__ == "__main__":
    main()
