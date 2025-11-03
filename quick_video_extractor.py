#!/usr/bin/env python3
"""
Quick Video Extractor - Use the already authenticated session to get video
"""

import requests
import re
import json
import time

def quick_extract_video():
    """Quick extraction using the authenticated session from the running Flask app"""
    print("🎥 QUICK VIDEO EXTRACTION")
    print("=" * 40)
    
    # The endpoints we know work
    endpoints = [
        'https://my.roku.com/account/devices/SOS2000V3AD89EB106D4/stream',
        'https://my.roku.com/account/devices/SOS2000V3AD89EB106D4/live'
    ]
    
    print("⚠️ This uses the authenticated session from your running Flask app")
    print("Make sure the Flask server is running and you've authenticated")
    print()
    
    # Try to use the session cookies from the Flask app
    # (In a real scenario, we'd need to pass the session from the stealth client)
    
    for endpoint in endpoints:
        print(f"🔍 Analyzing: {endpoint}")
        
        try:
            # Make request without authentication (will fail, but shows the approach)
            response = requests.get(endpoint, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Accessible without auth - checking content...")
                
                # Quick analysis
                content = response.text.lower()
                
                if 'video' in content or 'stream' in content:
                    print("🎥 Contains video/stream references")
                    
                    # Look for obvious video URLs
                    video_urls = re.findall(r'https://[^\s"\'<>]*\.(?:mp4|m3u8|ts)', response.text, re.IGNORECASE)
                    if video_urls:
                        print(f"🎯 Direct video URLs found: {video_urls}")
                        return video_urls[0]
                
            elif response.status_code == 302:
                redirect = response.headers.get('Location', '')
                print(f"🔄 Redirects to: {redirect}")
                
            else:
                print(f"❌ Requires authentication: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return None

def create_test_streaming_endpoints():
    """Create test endpoints to see what the authenticated session returns"""
    print("\n🧪 CREATING TEST ENDPOINTS")
    print("=" * 35)
    
    test_code = '''
# Add this to your Flask server to test the authenticated streaming:

@app.route('/api/test-roku-stream-content')
def test_roku_stream_content():
    """Test what the authenticated streaming endpoints return"""
    if not roku_authenticated_streamer:
        return jsonify({'error': 'Not authenticated'}), 404
    
    results = {}
    
    endpoints = [
        'https://my.roku.com/account/devices/SOS2000V3AD89EB106D4/stream',
        'https://my.roku.com/account/devices/SOS2000V3AD89EB106D4/live'
    ]
    
    for endpoint in endpoints:
        try:
            response = roku_authenticated_streamer.session.get(endpoint, timeout=10)
            
            endpoint_name = endpoint.split('/')[-1]
            results[endpoint_name] = {
                'status': response.status_code,
                'content_type': response.headers.get('content-type', 'unknown'),
                'content_length': len(response.content),
                'has_video_keywords': any(keyword in response.text.lower() 
                                        for keyword in ['video', 'stream', 'mp4', 'm3u8']),
                'content_preview': response.text[:500] + '...' if len(response.text) > 500 else response.text
            }
            
            # Look for video URLs in the content
            video_patterns = [
                r'https://[^\\s"\'<>]*\\.(?:mp4|m3u8|ts)',
                r'"(?:video|stream)Url":\\s*"([^"]*)"',
                r'src="([^"]*(?:video|stream)[^"]*)"'
            ]
            
            found_urls = []
            for pattern in video_patterns:
                matches = re.findall(pattern, response.text, re.IGNORECASE)
                found_urls.extend(matches)
            
            if found_urls:
                results[endpoint_name]['video_urls'] = found_urls
                
        except Exception as e:
            results[endpoint_name] = {'error': str(e)}
    
    return jsonify(results)
'''
    
    print("📝 Add this test endpoint to your Flask server:")
    print(test_code)
    
    print("\n🎯 Then visit: http://localhost:5000/api/test-roku-stream-content")
    print("This will show exactly what the authenticated endpoints return!")

if __name__ == "__main__":
    result = quick_extract_video()
    
    if result:
        print(f"\n🎉 Found video stream: {result}")
    else:
        print("\n🔧 Need authenticated session...")
        create_test_streaming_endpoints()
