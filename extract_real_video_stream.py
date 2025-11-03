#!/usr/bin/env python3
"""
Extract Real Video Stream - Parse the authenticated endpoints to get actual video
"""

import requests
import re
import json
from roku_stealth_client import RokuStealthClient

def extract_video_stream():
    """Extract the actual video stream from authenticated endpoints"""
    print("🎥 EXTRACTING REAL VIDEO STREAM")
    print("=" * 50)
    
    # First, authenticate to get session
    print("🔐 Authenticating with Roku...")
    client = RokuStealthClient()
    
    # You'll need to provide credentials
    username = input("Enter Roku email: ")
    password = input("Enter Roku password: ")
    
    success = client.authenticate_like_browser(username, password)
    
    if not success:
        print("❌ Authentication failed")
        return
    
    print("✅ Authentication successful!")
    
    # The working endpoints we discovered
    endpoints = [
        'https://my.roku.com/account/devices/SOS2000V3AD89EB106D4/stream',
        'https://my.roku.com/account/devices/SOS2000V3AD89EB106D4/live'
    ]
    
    for endpoint in endpoints:
        print(f"\n🔍 ANALYZING: {endpoint}")
        print("-" * 40)
        
        try:
            # Get the page content
            response = client.session.get(endpoint, timeout=15)
            
            if response.status_code == 200:
                print(f"✅ Page accessible: {len(response.text)} bytes")
                
                # Save the response for analysis
                endpoint_name = endpoint.split('/')[-1]
                filename = f"video_page_{endpoint_name}.html"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"💾 Saved to: {filename}")
                
                # Look for video-related content
                content = response.text
                
                # Method 1: Look for direct video URLs
                video_patterns = [
                    r'src=["\']([^"\']*\.mp4[^"\']*)["\']',
                    r'src=["\']([^"\']*\.m3u8[^"\']*)["\']',
                    r'src=["\']([^"\']*stream[^"\']*)["\']',
                    r'data-src=["\']([^"\']*video[^"\']*)["\']',
                    r'"videoUrl":\s*"([^"]*)"',
                    r'"streamUrl":\s*"([^"]*)"',
                    r'"liveUrl":\s*"([^"]*)"'
                ]
                
                found_videos = []
                for pattern in video_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        found_videos.extend(matches)
                        print(f"🎯 Video URL pattern found: {matches}")
                
                # Method 2: Look for JavaScript streaming code
                js_patterns = [
                    r'new\s+MediaSource\(\)',
                    r'createObjectURL\(',
                    r'WebRTC',
                    r'RTCPeerConnection',
                    r'getUserMedia',
                    r'videojs\(',
                    r'jwplayer\(',
                    r'Hls\.js'
                ]
                
                streaming_tech = []
                for pattern in js_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        streaming_tech.append(pattern)
                        print(f"🎬 Streaming technology found: {pattern}")
                
                # Method 3: Look for iframe or embed tags
                iframe_pattern = r'<iframe[^>]*src=["\']([^"\']*)["\'][^>]*>'
                iframes = re.findall(iframe_pattern, content, re.IGNORECASE)
                if iframes:
                    print(f"📺 Iframe sources found: {iframes}")
                    
                    # Test iframe sources
                    for iframe_src in iframes:
                        if not iframe_src.startswith('http'):
                            iframe_src = 'https://my.roku.com' + iframe_src
                        
                        print(f"🔍 Testing iframe: {iframe_src}")
                        try:
                            iframe_response = client.session.get(iframe_src, timeout=10)
                            if iframe_response.status_code == 200:
                                content_type = iframe_response.headers.get('content-type', '')
                                print(f"   ✅ Iframe accessible: {content_type}")
                                
                                if 'video' in content_type or 'octet-stream' in content_type:
                                    print(f"   🎥 DIRECT VIDEO STREAM FOUND: {iframe_src}")
                                    return iframe_src
                        except:
                            pass
                
                # Method 4: Look for WebSocket connections
                websocket_patterns = [
                    r'new\s+WebSocket\(["\']([^"\']*)["\']',
                    r'ws://[^\s"\'<>]+',
                    r'wss://[^\s"\'<>]+'
                ]
                
                for pattern in websocket_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        print(f"🔌 WebSocket found: {matches}")
                
                # Method 5: Look for AJAX/fetch calls that might get stream URLs
                ajax_patterns = [
                    r'fetch\(["\']([^"\']*stream[^"\']*)["\']',
                    r'fetch\(["\']([^"\']*video[^"\']*)["\']',
                    r'\.get\(["\']([^"\']*stream[^"\']*)["\']',
                    r'ajax\([^}]*url:\s*["\']([^"\']*stream[^"\']*)["\']'
                ]
                
                for pattern in ajax_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        print(f"📡 AJAX stream endpoint found: {matches}")
                        
                        # Test these endpoints
                        for ajax_url in matches:
                            if not ajax_url.startswith('http'):
                                ajax_url = 'https://my.roku.com' + ajax_url
                            
                            print(f"🔍 Testing AJAX endpoint: {ajax_url}")
                            try:
                                ajax_response = client.session.get(ajax_url, timeout=10)
                                if ajax_response.status_code == 200:
                                    print(f"   ✅ AJAX endpoint accessible")
                                    
                                    # Check if it returns a stream URL
                                    try:
                                        ajax_data = ajax_response.json()
                                        print(f"   📊 JSON response: {json.dumps(ajax_data, indent=2)[:300]}...")
                                        
                                        # Look for stream URLs in JSON
                                        if 'stream' in str(ajax_data).lower() or 'video' in str(ajax_data).lower():
                                            print(f"   🎯 STREAM DATA FOUND IN AJAX RESPONSE!")
                                            return ajax_data
                                    except:
                                        content_type = ajax_response.headers.get('content-type', '')
                                        if 'video' in content_type:
                                            print(f"   🎥 DIRECT VIDEO STREAM: {ajax_url}")
                                            return ajax_url
                            except:
                                pass
                
                # Method 6: Look for form submissions that might start streaming
                form_patterns = [
                    r'<form[^>]*action=["\']([^"\']*stream[^"\']*)["\']',
                    r'<form[^>]*action=["\']([^"\']*video[^"\']*)["\']'
                ]
                
                for pattern in form_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        print(f"📝 Form action found: {matches}")
                
                if found_videos:
                    print(f"\n🎯 POTENTIAL VIDEO STREAMS:")
                    for i, video in enumerate(found_videos, 1):
                        print(f"   {i}. {video}")
                    return found_videos[0]  # Return first found video
                
            else:
                print(f"❌ Page not accessible: {response.status_code}")
        
        except Exception as e:
            print(f"❌ Error analyzing {endpoint}: {e}")
    
    print("\n⚠️ No direct video streams found in HTML pages")
    print("💡 The endpoints might require JavaScript interaction or POST requests")
    return None

def test_streaming_interaction():
    """Try to interact with the streaming pages to start video"""
    print("\n🎬 TESTING STREAMING INTERACTION")
    print("=" * 40)
    
    # This would simulate clicking play buttons, submitting forms, etc.
    print("This requires analyzing the saved HTML files for interactive elements")
    print("Check the saved video_page_*.html files for:")
    print("1. Play buttons or start streaming links")
    print("2. JavaScript that loads when the page is ready")
    print("3. Form submissions that might initiate streaming")

if __name__ == "__main__":
    result = extract_video_stream()
    
    if result:
        print(f"\n🎉 SUCCESS! Found video stream: {result}")
        print("\n🎯 NEXT STEPS:")
        print("1. Test this URL in VLC Media Player")
        print("2. Or integrate it into the Flask streaming system")
    else:
        print("\n🔍 No direct streams found - trying interaction analysis...")
        test_streaming_interaction()
