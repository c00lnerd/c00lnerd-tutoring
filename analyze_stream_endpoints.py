#!/usr/bin/env python3
"""
Analyze the successful stream endpoints to extract actual streaming URLs
"""

import requests
import re
import json
from roku_stealth_client import RokuStealthClient

def analyze_successful_endpoints():
    """Re-analyze the successful streaming endpoints with detailed inspection"""
    print("🔍 ANALYZING SUCCESSFUL STREAM ENDPOINTS")
    print("=" * 60)
    
    # We know these endpoints work
    successful_endpoints = [
        'https://my.roku.com/account/devices/SOS2000V3AD89EB106D4/stream',
        'https://my.roku.com/account/devices/SOS2000V3AD89EB106D4/live'
    ]
    
    # Create authenticated session (you'll need to run this after authentication)
    client = RokuStealthClient()
    
    print("⚠️  This requires an authenticated session.")
    print("Run this after successful Roku authentication.")
    print()
    
    for endpoint in successful_endpoints:
        print(f"🎯 ANALYZING: {endpoint}")
        print("-" * 50)
        
        try:
            # Make request with authenticated session
            response = client.session.get(endpoint, timeout=15)
            
            print(f"Status: {response.status_code}")
            print(f"Content-Type: {response.headers.get('content-type', 'unknown')}")
            print(f"Content-Length: {len(response.content)} bytes")
            
            # Save raw response for inspection
            endpoint_name = endpoint.split('/')[-1]
            filename = f"detailed_{endpoint_name}_response.html"
            
            with open(filename, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(response.text)
            print(f"💾 Saved to: {filename}")
            
            # Look for streaming indicators in the response
            content = response.text.lower()
            
            streaming_indicators = [
                'rtmp://', 'rtsp://', 'stream', 'video', 'live', 
                '.m3u8', '.ts', '.mp4', 'hls', 'webrtc'
            ]
            
            found_indicators = []
            for indicator in streaming_indicators:
                if indicator in content:
                    found_indicators.append(indicator)
            
            if found_indicators:
                print(f"🎥 Streaming indicators found: {found_indicators}")
            else:
                print("⚠️  No obvious streaming indicators in content")
            
            # Look for any URLs in the response
            urls = re.findall(r'https?://[^\s"\'<>]+', response.text)
            if urls:
                print(f"🌐 URLs found in response ({len(urls)} total):")
                unique_urls = list(set(urls))[:10]  # Show first 10 unique
                for url in unique_urls:
                    print(f"   {url}")
            
            # Look for JavaScript that might contain streaming logic
            js_patterns = [
                r'var\s+streamUrl\s*=\s*["\']([^"\']+)["\']',
                r'streamUrl:\s*["\']([^"\']+)["\']',
                r'videoUrl:\s*["\']([^"\']+)["\']',
                r'liveUrl:\s*["\']([^"\']+)["\']'
            ]
            
            for pattern in js_patterns:
                matches = re.findall(pattern, response.text, re.IGNORECASE)
                if matches:
                    print(f"🎯 JavaScript stream URL found: {matches}")
            
            # Look for form data or hidden inputs that might contain stream info
            form_inputs = re.findall(r'<input[^>]*name=["\']([^"\']*stream[^"\']*)["\'][^>]*value=["\']([^"\']+)["\']', response.text, re.IGNORECASE)
            if form_inputs:
                print(f"📝 Form inputs with stream data: {form_inputs}")
            
            # Check if this is a streaming page that requires interaction
            if 'play' in content or 'start' in content or 'stream' in content:
                print("🎬 This appears to be a streaming control page")
                
                # Look for buttons or links that might start streaming
                play_buttons = re.findall(r'<[^>]*(?:onclick|href)[^>]*(?:play|start|stream)[^>]*>', response.text, re.IGNORECASE)
                if play_buttons:
                    print(f"🎮 Found play/start controls: {len(play_buttons)} elements")
            
            print()
            
        except Exception as e:
            print(f"❌ Error analyzing {endpoint}: {e}")
            print()

def test_direct_streaming():
    """Test if the successful endpoints are direct streaming URLs"""
    print("🎥 TESTING DIRECT STREAMING")
    print("=" * 40)
    
    endpoints = [
        'https://my.roku.com/account/devices/SOS2000V3AD89EB106D4/stream',
        'https://my.roku.com/account/devices/SOS2000V3AD89EB106D4/live'
    ]
    
    for endpoint in endpoints:
        print(f"🎯 Testing direct stream: {endpoint}")
        
        # Test if this URL can be used directly in video players
        print(f"📺 Try this URL in VLC or other video player:")
        print(f"   {endpoint}")
        print()
        
        # Test different HTTP methods
        methods = ['GET', 'POST', 'HEAD']
        for method in methods:
            try:
                if method == 'GET':
                    response = requests.get(endpoint, timeout=5, stream=True)
                elif method == 'POST':
                    response = requests.post(endpoint, timeout=5)
                elif method == 'HEAD':
                    response = requests.head(endpoint, timeout=5)
                
                print(f"   {method}: {response.status_code} - {response.headers.get('content-type', 'unknown')}")
                
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    if any(video_type in content_type for video_type in ['video/', 'application/octet-stream', 'multipart/x-mixed-replace']):
                        print(f"   🎥 POTENTIAL DIRECT STREAM! Content-Type: {content_type}")
                
            except Exception as e:
                print(f"   {method}: Error - {e}")
        
        print()

if __name__ == "__main__":
    print("🎯 Stream Endpoint Analyzer")
    print("=" * 40)
    
    choice = input("Choose analysis:\n1. Detailed endpoint analysis (requires auth)\n2. Test direct streaming\nChoice (1/2): ")
    
    if choice == "1":
        analyze_successful_endpoints()
    elif choice == "2":
        test_direct_streaming()
    else:
        print("Running both analyses...")
        test_direct_streaming()
        print("\n" + "="*60 + "\n")
        analyze_successful_endpoints()
