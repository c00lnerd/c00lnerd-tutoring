#!/usr/bin/env python3
"""
Analyze the device response file for stream URLs and camera data
"""

import re
import json
import os

def analyze_device_response():
    """Analyze the saved device response for streaming information"""
    device_id = 'SOS2000V3AD89EB106D4'
    filename = f'device_response_{device_id}.html'
    
    if not os.path.exists(filename):
        print(f"❌ Response file not found: {filename}")
        return
    
    print(f"🔍 Analyzing device response: {filename}")
    
    try:
        # Read file with error handling for encoding issues
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        print(f"📄 File size: {len(content)} characters")
        print(f"📄 Content preview (first 500 chars):")
        print("-" * 50)
        print(content[:500])
        print("-" * 50)
        
        # Look for stream URLs
        stream_patterns = [
            r'rtmp://[^\s"\'<>]+',
            r'rtsp://[^\s"\'<>]+',
            r'https://[^\s"\'<>]*stream[^\s"\'<>]*',
            r'wss://[^\s"\'<>]*stream[^\s"\'<>]*',
            r'https://[^\s"\'<>]*video[^\s"\'<>]*',
            r'https://[^\s"\'<>]*live[^\s"\'<>]*',
            r'"url":\s*"([^"]*stream[^"]*)"',
            r'"stream_url":\s*"([^"]*)"',
            r'"video_url":\s*"([^"]*)"',
            r'"live_url":\s*"([^"]*)"'
        ]
        
        found_streams = []
        for pattern in stream_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                found_streams.extend(matches)
                print(f"🎯 Pattern '{pattern[:30]}...' found: {matches}")
        
        if found_streams:
            print(f"\n🎥 STREAM URLs FOUND:")
            for i, url in enumerate(found_streams, 1):
                print(f"   {i}. {url}")
        else:
            print("\n⚠️ No stream URLs found with standard patterns")
        
        # Look for JSON data
        try:
            # Try to find JSON objects in the content
            json_matches = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', content)
            for i, json_str in enumerate(json_matches[:5]):  # Check first 5 JSON objects
                try:
                    json_data = json.loads(json_str)
                    print(f"\n📊 JSON Object {i+1}:")
                    print(json.dumps(json_data, indent=2)[:300] + "...")
                    
                    # Look for stream-related keys
                    def find_stream_keys(obj, path=""):
                        results = []
                        if isinstance(obj, dict):
                            for key, value in obj.items():
                                if any(keyword in key.lower() for keyword in ['stream', 'video', 'url', 'live', 'camera', 'rtmp', 'rtsp']):
                                    results.append((f"{path}.{key}" if path else key, value))
                                if isinstance(value, (dict, list)):
                                    results.extend(find_stream_keys(value, f"{path}.{key}" if path else key))
                        elif isinstance(obj, list):
                            for idx, item in enumerate(obj):
                                results.extend(find_stream_keys(item, f"{path}[{idx}]"))
                        return results
                    
                    stream_keys = find_stream_keys(json_data)
                    if stream_keys:
                        print("🔍 Stream-related keys found:")
                        for path, value in stream_keys:
                            print(f"   {path}: {value}")
                
                except json.JSONDecodeError:
                    continue
        except Exception as e:
            print(f"JSON analysis error: {e}")
        
        # Look for any URLs at all
        all_urls = re.findall(r'https?://[^\s"\'<>]+', content)
        if all_urls:
            print(f"\n🌐 All URLs found ({len(all_urls)} total):")
            unique_urls = list(set(all_urls))[:10]  # Show first 10 unique URLs
            for url in unique_urls:
                print(f"   {url}")
        
        # Look for device-specific information
        device_info_patterns = [
            r'SOS2000V3AD89EB106D4[^"\'<>\s]*',
            r'7C:67:AB:23:DF:1E[^"\'<>\s]*',
            r'"name":\s*"([^"]*)"',
            r'"status":\s*"([^"]*)"',
            r'"type":\s*"([^"]*)"'
        ]
        
        print(f"\n📱 Device Information:")
        for pattern in device_info_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                print(f"   Pattern '{pattern[:20]}...': {matches}")
        
    except Exception as e:
        print(f"❌ Error analyzing file: {e}")

if __name__ == "__main__":
    analyze_device_response()
