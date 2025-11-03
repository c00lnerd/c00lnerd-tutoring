#!/usr/bin/env python3
"""
Decode compressed device response and extract stream information
"""

import gzip
import json
import re
import os
from io import BytesIO

def decode_device_response():
    """Decode the compressed device response"""
    device_id = 'SOS2000V3AD89EB106D4'
    filename = f'device_response_{device_id}.html'
    
    if not os.path.exists(filename):
        print(f"❌ Response file not found: {filename}")
        return
    
    print(f"🔍 Decoding device response: {filename}")
    
    try:
        # Read the raw bytes
        with open(filename, 'rb') as f:
            raw_data = f.read()
        
        print(f"📄 Raw file size: {len(raw_data)} bytes")
        
        # Try to decompress if it's gzipped
        try:
            decompressed = gzip.decompress(raw_data)
            content = decompressed.decode('utf-8', errors='ignore')
            print("✅ Successfully decompressed gzipped content")
        except:
            # If not gzipped, try direct decode
            try:
                content = raw_data.decode('utf-8', errors='ignore')
                print("✅ Decoded as plain text")
            except:
                print("❌ Could not decode content")
                return
        
        print(f"📄 Decoded content size: {len(content)} characters")
        print(f"📄 Content preview (first 1000 chars):")
        print("-" * 60)
        print(content[:1000])
        print("-" * 60)
        
        # Save decoded content for inspection
        decoded_filename = f'decoded_device_response_{device_id}.html'
        with open(decoded_filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"💾 Saved decoded content to: {decoded_filename}")
        
        # Now analyze the decoded content
        analyze_content(content)
        
    except Exception as e:
        print(f"❌ Error decoding file: {e}")

def analyze_content(content):
    """Analyze the decoded content for streaming information"""
    print("\n🔍 ANALYZING DECODED CONTENT:")
    print("=" * 50)
    
    # Look for stream URLs with enhanced patterns
    stream_patterns = [
        r'rtmp://[^\s"\'<>]+',
        r'rtsp://[^\s"\'<>]+',
        r'https://[^\s"\'<>]*stream[^\s"\'<>]*',
        r'wss://[^\s"\'<>]*stream[^\s"\'<>]*',
        r'https://[^\s"\'<>]*video[^\s"\'<>]*',
        r'https://[^\s"\'<>]*live[^\s"\'<>]*',
        r'https://[^\s"\'<>]*camera[^\s"\'<>]*',
        r'"url":\s*"([^"]*)"',
        r'"stream_url":\s*"([^"]*)"',
        r'"video_url":\s*"([^"]*)"',
        r'"live_url":\s*"([^"]*)"',
        r'"rtmp_url":\s*"([^"]*)"',
        r'"hls_url":\s*"([^"]*)"'
    ]
    
    found_streams = []
    for pattern in stream_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            found_streams.extend(matches)
            print(f"🎯 Found with pattern '{pattern[:30]}...': {matches}")
    
    if found_streams:
        print(f"\n🎥 POTENTIAL STREAM URLs:")
        unique_streams = list(set(found_streams))
        for i, url in enumerate(unique_streams, 1):
            print(f"   {i}. {url}")
    
    # Look for CS1000X specific information
    cs1000x_patterns = [
        r'SOS2000V3AD89EB106D4[^"\'<>\s]*',
        r'CS1000X[^"\'<>\s]*',
        r'7C:67:AB:23:DF:1E[^"\'<>\s]*',
        r'"device_id":\s*"([^"]*)"',
        r'"name":\s*"([^"]*)"',
        r'"status":\s*"([^"]*)"',
        r'"model":\s*"([^"]*)"'
    ]
    
    print(f"\n📱 CS1000X DEVICE INFO:")
    for pattern in cs1000x_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            print(f"   {pattern[:30]}...: {matches}")
    
    # Look for any JSON structures
    print(f"\n📊 JSON DATA ANALYSIS:")
    try:
        # Find potential JSON objects
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        json_matches = re.findall(json_pattern, content)
        
        print(f"Found {len(json_matches)} potential JSON objects")
        
        for i, json_str in enumerate(json_matches[:3]):  # Analyze first 3
            try:
                json_data = json.loads(json_str)
                print(f"\nJSON Object {i+1}:")
                print(json.dumps(json_data, indent=2)[:500] + "...")
                
                # Look for streaming-related keys
                streaming_keys = []
                def find_keys(obj, path=""):
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            current_path = f"{path}.{key}" if path else key
                            if any(keyword in key.lower() for keyword in 
                                  ['stream', 'video', 'url', 'live', 'camera', 'rtmp', 'rtsp', 'hls']):
                                streaming_keys.append((current_path, value))
                            if isinstance(value, (dict, list)):
                                find_keys(value, current_path)
                    elif isinstance(obj, list):
                        for idx, item in enumerate(obj):
                            find_keys(item, f"{path}[{idx}]")
                
                find_keys(json_data)
                
                if streaming_keys:
                    print("🎥 Streaming-related keys:")
                    for path, value in streaming_keys:
                        print(f"   {path}: {value}")
                
            except json.JSONDecodeError:
                continue
    except Exception as e:
        print(f"JSON analysis error: {e}")
    
    # Look for all URLs
    all_urls = re.findall(r'https?://[^\s"\'<>]+', content)
    if all_urls:
        unique_urls = list(set(all_urls))
        print(f"\n🌐 ALL URLs FOUND ({len(unique_urls)} unique):")
        for url in unique_urls[:15]:  # Show first 15
            print(f"   {url}")
    
    # Look for form data or API endpoints
    api_patterns = [
        r'/api/[^\s"\'<>]+',
        r'/stream[^\s"\'<>]*',
        r'/video[^\s"\'<>]*',
        r'/live[^\s"\'<>]*'
    ]
    
    print(f"\n🔗 API ENDPOINTS:")
    for pattern in api_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            unique_matches = list(set(matches))
            print(f"   {pattern}: {unique_matches}")

if __name__ == "__main__":
    decode_device_response()
