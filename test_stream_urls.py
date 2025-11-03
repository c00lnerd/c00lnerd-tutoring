#!/usr/bin/env python3
"""
Test the discovered stream URLs
"""

import requests

def test_stream_urls():
    """Test if the discovered URLs are direct streams"""
    print("🎥 TESTING DISCOVERED STREAM URLS")
    print("=" * 50)
    
    # The URLs we found working
    stream_urls = [
        'https://my.roku.com/account/devices/SOS2000V3AD89EB106D4/stream',
        'https://my.roku.com/account/devices/SOS2000V3AD89EB106D4/live'
    ]
    
    for url in stream_urls:
        print(f"\n🎯 Testing: {url}")
        print("-" * 40)
        
        try:
            # Test HEAD request first (lightweight)
            response = requests.head(url, timeout=10)
            print(f"HEAD Status: {response.status_code}")
            print(f"Content-Type: {response.headers.get('content-type', 'unknown')}")
            print(f"Content-Length: {response.headers.get('content-length', 'unknown')}")
            
            # Check if it looks like a video stream
            content_type = response.headers.get('content-type', '').lower()
            
            if any(video_type in content_type for video_type in 
                  ['video/', 'application/octet-stream', 'multipart/x-mixed-replace']):
                print("🎥 ✅ LOOKS LIKE A DIRECT VIDEO STREAM!")
                print(f"📺 Try opening this URL in VLC Media Player:")
                print(f"   File → Open Network Stream → {url}")
            
            elif 'text/html' in content_type:
                print("📄 HTML page - likely a streaming control interface")
                
                # Get the actual page content
                get_response = requests.get(url, timeout=10)
                content = get_response.text.lower()
                
                # Look for streaming indicators
                if any(indicator in content for indicator in 
                      ['video', 'stream', 'player', 'rtmp', 'rtsp', 'm3u8']):
                    print("🎬 Contains streaming-related content")
                    
                    # Save for manual inspection
                    filename = f"stream_page_{url.split('/')[-1]}.html"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(get_response.text)
                    print(f"💾 Saved page content to: {filename}")
                
            else:
                print(f"❓ Unknown content type: {content_type}")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

def create_vlc_playlist():
    """Create VLC playlist file for easy testing"""
    print("\n🎵 CREATING VLC PLAYLIST")
    print("=" * 30)
    
    playlist_content = """#EXTM3U
#EXTINF:-1,CS1000X Basement Camera - Stream
https://my.roku.com/account/devices/SOS2000V3AD89EB106D4/stream
#EXTINF:-1,CS1000X Basement Camera - Live
https://my.roku.com/account/devices/SOS2000V3AD89EB106D4/live
"""
    
    with open('cs1000x_streams.m3u', 'w') as f:
        f.write(playlist_content)
    
    print("✅ Created VLC playlist: cs1000x_streams.m3u")
    print("📺 Open this file in VLC to test the streams!")

if __name__ == "__main__":
    test_stream_urls()
    create_vlc_playlist()
    
    print("\n🎯 NEXT STEPS:")
    print("1. Open VLC Media Player")
    print("2. File → Open Network Stream")
    print("3. Paste one of the URLs above")
    print("4. Or open the cs1000x_streams.m3u playlist file")
    print("\n⚠️  Note: These URLs might require authentication cookies")
    print("   If they don't work in VLC, they need to be accessed through")
    print("   an authenticated browser session or our Flask app.")
