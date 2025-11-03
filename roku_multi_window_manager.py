#!/usr/bin/env python3
"""
Roku Multi-Window Camera Manager
Opens separate browser windows for each camera using Roku's web interface
"""

import webbrowser
import time
import json
import subprocess
import os
from urllib.parse import urlencode

class RokuMultiWindowManager:
    def __init__(self):
        self.roku_base_url = 'https://my.roku.com/smarthome'
        self.camera_windows = {}
        self.browsers = {
            'chrome': [
                'chrome.exe',
                'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
                'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
            ],
            'edge': [
                'msedge.exe',
                'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
            ],
            'firefox': [
                'firefox.exe',
                'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
            ]
        }
    
    def find_browser(self, preferred='chrome'):
        """Find available browser executable"""
        for browser_name, paths in self.browsers.items():
            if preferred and browser_name != preferred:
                continue
            
            for path in paths:
                if os.path.exists(path):
                    return path
                
                # Try to find in PATH
                try:
                    subprocess.run([path.split('\\')[-1], '--version'], 
                                 capture_output=True, timeout=2)
                    return path.split('\\')[-1]
                except:
                    continue
        
        # Fallback to any available browser
        if preferred:
            return self.find_browser(preferred=None)
        
        return None
    
    def open_camera_window(self, camera_name, camera_id=None, position=None, size=None):
        """Open a dedicated browser window for a specific camera"""
        print(f"🪟 Opening window for camera: {camera_name}")
        
        # Build the URL for the specific camera
        if camera_id:
            # If we have a specific camera ID, try to navigate directly
            url = f"{self.roku_base_url}?camera={camera_id}"
        else:
            # Otherwise, open the main Smart Home page
            url = self.roku_base_url
        
        # Find browser
        browser_path = self.find_browser()
        if not browser_path:
            print("❌ No browser found, using default")
            webbrowser.open(url)
            return
        
        # Build browser command with window positioning
        cmd = [browser_path]
        
        # Add Chrome-specific flags for window management
        if 'chrome' in browser_path.lower():
            cmd.extend([
                '--new-window',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                f'--app={url}',  # App mode for cleaner interface
            ])
            
            # Add window positioning if specified
            if position and size:
                x, y = position
                width, height = size
                cmd.append(f'--window-position={x},{y}')
                cmd.append(f'--window-size={width},{height}')
        
        elif 'edge' in browser_path.lower():
            cmd.extend([
                '--new-window',
                f'--app={url}'
            ])
        
        else:
            cmd.extend([
                '--new-window',
                url
            ])
        
        try:
            # Launch the browser window
            process = subprocess.Popen(cmd)
            
            # Store window info
            self.camera_windows[camera_name] = {
                'process': process,
                'url': url,
                'camera_id': camera_id,
                'position': position,
                'size': size
            }
            
            print(f"✅ Opened {camera_name} window: {url}")
            return process
            
        except Exception as e:
            print(f"❌ Failed to open window for {camera_name}: {e}")
            # Fallback to default browser
            webbrowser.open(url)
    
    def open_multi_camera_layout(self, cameras=None):
        """Open multiple camera windows in a organized layout"""
        print("🎥 OPENING MULTI-CAMERA LAYOUT")
        print("=" * 40)
        
        # Default cameras if none provided
        if not cameras:
            cameras = [
                {'name': 'Basement Camera', 'id': 'SOS2000V3AD89EB106D4'},
                {'name': 'Living Room', 'id': None},
                {'name': 'Becky', 'id': None}
            ]
        
        # Calculate window positions for a grid layout
        screen_width = 1920  # Adjust based on your screen
        screen_height = 1080
        
        window_width = screen_width // 2
        window_height = screen_height // 2
        
        positions = [
            (0, 0),  # Top-left
            (window_width, 0),  # Top-right
            (0, window_height),  # Bottom-left
            (window_width, window_height)  # Bottom-right
        ]
        
        # Open windows for each camera
        for i, camera in enumerate(cameras):
            if i < len(positions):
                position = positions[i]
                size = (window_width, window_height)
            else:
                position = None
                size = None
            
            self.open_camera_window(
                camera['name'], 
                camera.get('id'), 
                position, 
                size
            )
            
            # Small delay between window opens
            time.sleep(1)
        
        print(f"✅ Opened {len(cameras)} camera windows")
    
    def open_control_dashboard(self):
        """Open a control dashboard for managing camera windows"""
        dashboard_html = self.create_dashboard_html()
        
        # Save dashboard to temp file
        dashboard_path = os.path.join(os.getcwd(), 'camera_dashboard.html')
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(dashboard_html)
        
        # Open dashboard
        dashboard_url = f'file:///{dashboard_path.replace(os.sep, "/")}'
        webbrowser.open(dashboard_url)
        
        print(f"🎛️ Control dashboard opened: {dashboard_url}")
    
    def create_dashboard_html(self):
        """Create HTML for the camera control dashboard"""
        return '''
<!DOCTYPE html>
<html>
<head>
    <title>CS1000X Camera Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #1a1a1a; color: white; }
        .header { text-align: center; margin-bottom: 30px; }
        .camera-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .camera-card { 
            background: #2d2d2d; 
            border-radius: 10px; 
            padding: 20px; 
            border: 2px solid #4CAF50;
        }
        .camera-name { font-size: 18px; font-weight: bold; margin-bottom: 10px; }
        .camera-actions { margin-top: 15px; }
        .btn { 
            background: #4CAF50; 
            color: white; 
            border: none; 
            padding: 10px 15px; 
            border-radius: 5px; 
            cursor: pointer; 
            margin-right: 10px;
            margin-bottom: 5px;
        }
        .btn:hover { background: #45a049; }
        .btn-secondary { background: #666; }
        .btn-secondary:hover { background: #555; }
        .status { margin: 10px 0; padding: 5px; border-radius: 3px; }
        .status.online { background: #4CAF50; }
        .status.offline { background: #f44336; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎥 CS1000X Camera Dashboard</h1>
        <p>Manage your Roku Smart Home camera windows</p>
    </div>
    
    <div class="camera-grid">
        <div class="camera-card">
            <div class="camera-name">🏠 Basement Camera</div>
            <div class="status online">● Connected via Roku Smart Home</div>
            <div class="camera-actions">
                <button class="btn" onclick="openCamera('basement')">📱 Open Window</button>
                <button class="btn btn-secondary" onclick="openRokuHome()">🌐 Roku Home</button>
            </div>
        </div>
        
        <div class="camera-card">
            <div class="camera-name">🛋️ Living Room</div>
            <div class="status offline">● Check Roku Smart Home</div>
            <div class="camera-actions">
                <button class="btn" onclick="openCamera('living')">📱 Open Window</button>
                <button class="btn btn-secondary" onclick="openRokuHome()">🌐 Roku Home</button>
            </div>
        </div>
        
        <div class="camera-card">
            <div class="camera-name">👤 Becky</div>
            <div class="status online">● Live Stream Active</div>
            <div class="camera-actions">
                <button class="btn" onclick="openCamera('becky')">📱 Open Window</button>
                <button class="btn btn-secondary" onclick="openRokuHome()">🌐 Roku Home</button>
            </div>
        </div>
        
        <div class="camera-card">
            <div class="camera-name">⚙️ System Controls</div>
            <div class="status">Management Tools</div>
            <div class="camera-actions">
                <button class="btn" onclick="openAllCameras()">🎥 Open All Cameras</button>
                <button class="btn" onclick="openGridLayout()">📊 Grid Layout</button>
                <button class="btn btn-secondary" onclick="closeAllWindows()">❌ Close All</button>
            </div>
        </div>
    </div>
    
    <script>
        function openCamera(camera) {
            const urls = {
                'basement': 'https://my.roku.com/smarthome?camera=SOS2000V3AD89EB106D4',
                'living': 'https://my.roku.com/smarthome',
                'becky': 'https://my.roku.com/smarthome'
            };
            
            window.open(urls[camera] || 'https://my.roku.com/smarthome', '_blank', 
                       'width=800,height=600,scrollbars=yes,resizable=yes');
        }
        
        function openRokuHome() {
            window.open('https://my.roku.com/smarthome', '_blank');
        }
        
        function openAllCameras() {
            openCamera('basement');
            setTimeout(() => openCamera('living'), 1000);
            setTimeout(() => openCamera('becky'), 2000);
        }
        
        function openGridLayout() {
            // Open cameras in specific positions
            const cameras = ['basement', 'living', 'becky'];
            cameras.forEach((camera, index) => {
                setTimeout(() => {
                    const x = (index % 2) * 800;
                    const y = Math.floor(index / 2) * 600;
                    window.open(
                        `https://my.roku.com/smarthome`, 
                        `camera_${camera}`,
                        `width=800,height=600,left=${x},top=${y},scrollbars=yes,resizable=yes`
                    );
                }, index * 1000);
            });
        }
        
        function closeAllWindows() {
            alert('Close camera windows manually or use browser task manager');
        }
    </script>
</body>
</html>
        '''
    
    def close_all_windows(self):
        """Close all managed camera windows"""
        print("🔒 Closing all camera windows...")
        
        for camera_name, window_info in self.camera_windows.items():
            try:
                process = window_info['process']
                process.terminate()
                print(f"✅ Closed {camera_name} window")
            except:
                print(f"⚠️ Could not close {camera_name} window")
        
        self.camera_windows.clear()

def main():
    """Demo the multi-window camera manager"""
    manager = RokuMultiWindowManager()
    
    print("🎥 CS1000X Multi-Window Camera Manager")
    print("=" * 50)
    
    choice = input("""
Choose an option:
1. Open control dashboard
2. Open single camera window
3. Open multi-camera grid layout
4. Open all cameras
Choice (1-4): """)
    
    if choice == "1":
        manager.open_control_dashboard()
    elif choice == "2":
        manager.open_camera_window("Basement Camera", "SOS2000V3AD89EB106D4")
    elif choice == "3":
        manager.open_multi_camera_layout()
    elif choice == "4":
        cameras = [
            {'name': 'Basement Camera', 'id': 'SOS2000V3AD89EB106D4'},
            {'name': 'Living Room', 'id': None},
            {'name': 'Becky', 'id': None}
        ]
        for camera in cameras:
            manager.open_camera_window(camera['name'], camera.get('id'))
            time.sleep(1)
    else:
        print("Opening control dashboard...")
        manager.open_control_dashboard()

if __name__ == "__main__":
    main()
