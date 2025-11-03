#!/usr/bin/env python3
"""
Screen Capture Streamer - Capture Samsung Galaxy screen showing CS1000X app
and stream it through the existing camera monitoring system
"""

import cv2
import numpy as np
import time
import threading
from PIL import ImageGrab, Image
import win32gui
import win32con
import win32ui
from ctypes import windll
from flask import Response
import io

class ScreenCaptureStreamer:
    def __init__(self):
        self.capturing = False
        self.current_frame = None
        self.target_window = None
        self.capture_region = None
        self.fps = 30
        
    def find_samsung_dex_window(self):
        """Find Samsung DeX, Smart View, or phone mirroring window"""
        possible_titles = [
            'Samsung DeX',
            'Smart View',
            'Samsung Smart View',
            'Phone Screen',
            'Your Phone',
            'Samsung Flow',
            'SideSync',
            'Samsung SideSync',
            'Vysor',
            'scrcpy'
        ]
        
        def enum_window_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                for title in possible_titles:
                    if title.lower() in window_title.lower():
                        windows.append((hwnd, window_title))
            return True
        
        windows = []
        win32gui.EnumWindows(enum_window_callback, windows)
        
        if windows:
            print(f"Found {len(windows)} potential phone screen windows:")
            for i, (hwnd, title) in enumerate(windows):
                rect = win32gui.GetWindowRect(hwnd)
                print(f"{i+1}. {title} - Size: {rect[2]-rect[0]}x{rect[3]-rect[1]}")
            
            return windows
        else:
            print("No phone mirroring windows found. Available windows:")
            self.list_all_windows()
            return []
    
    def list_all_windows(self):
        """List all visible windows for manual selection"""
        def enum_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:  # Only show windows with titles
                    rect = win32gui.GetWindowRect(hwnd)
                    size = f"{rect[2]-rect[0]}x{rect[3]-rect[1]}"
                    windows.append((hwnd, title, size))
            return True
        
        windows = []
        win32gui.EnumWindows(enum_callback, windows)
        
        # Sort by title
        windows.sort(key=lambda x: x[1])
        
        print("\nAll visible windows:")
        for i, (hwnd, title, size) in enumerate(windows[:20]):  # Show first 20
            print(f"{i+1:2d}. {title[:50]:<50} ({size})")
        
        if len(windows) > 20:
            print(f"... and {len(windows)-20} more windows")
    
    def capture_window(self, hwnd):
        """Capture specific window content"""
        try:
            # Get window dimensions
            rect = win32gui.GetWindowRect(hwnd)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]
            
            # Get window device context
            hwndDC = win32gui.GetWindowDC(hwnd)
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()
            
            # Create bitmap
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
            saveDC.SelectObject(saveBitMap)
            
            # Copy window content
            result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)
            
            if result:
                # Convert to numpy array
                bmpinfo = saveBitMap.GetInfo()
                bmpstr = saveBitMap.GetBitmapBits(True)
                
                img = np.frombuffer(bmpstr, dtype='uint8')
                img.shape = (height, width, 4)  # BGRA format
                
                # Convert BGRA to BGR (remove alpha channel)
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                
                # Clean up
                win32gui.DeleteObject(saveBitMap.GetHandle())
                saveDC.DeleteDC()
                mfcDC.DeleteDC()
                win32gui.ReleaseDC(hwnd, hwndDC)
                
                return img
            else:
                print("PrintWindow failed, trying alternative method...")
                return self.capture_screen_region(rect)
                
        except Exception as e:
            print(f"Window capture error: {e}")
            return None
    
    def capture_screen_region(self, rect):
        """Fallback: capture screen region"""
        try:
            # Use PIL to capture screen region
            screenshot = ImageGrab.grab(bbox=rect)
            
            # Convert PIL to OpenCV format
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            return img
            
        except Exception as e:
            print(f"Screen region capture error: {e}")
            return None
    
    def start_capture(self, window_hwnd=None):
        """Start capturing the selected window or screen region"""
        if window_hwnd:
            self.target_window = window_hwnd
            print(f"Starting capture of window: {win32gui.GetWindowText(window_hwnd)}")
        else:
            print("Starting full screen capture")
        
        self.capturing = True
        capture_thread = threading.Thread(target=self._capture_loop)
        capture_thread.daemon = True
        capture_thread.start()
    
    def _capture_loop(self):
        """Main capture loop"""
        while self.capturing:
            try:
                if self.target_window:
                    frame = self.capture_window(self.target_window)
                else:
                    # Full screen capture
                    screenshot = ImageGrab.grab()
                    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                
                if frame is not None:
                    # Resize if too large (for web streaming)
                    height, width = frame.shape[:2]
                    if width > 1280:
                        scale = 1280 / width
                        new_width = int(width * scale)
                        new_height = int(height * scale)
                        frame = cv2.resize(frame, (new_width, new_height))
                    
                    # Add timestamp
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    cv2.putText(frame, f"CS1000X Screen Capture - {timestamp}", 
                               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    
                    self.current_frame = frame
                
                time.sleep(1.0 / self.fps)  # Control frame rate
                
            except Exception as e:
                print(f"Capture loop error: {e}")
                time.sleep(1)
    
    def stop_capture(self):
        """Stop capturing"""
        self.capturing = False
        print("Screen capture stopped")
    
    def get_mjpeg_stream(self):
        """Generate MJPEG stream for web viewing"""
        while self.capturing:
            if self.current_frame is not None:
                # Encode frame as JPEG
                ret, buffer = cv2.imencode('.jpg', self.current_frame, 
                                         [cv2.IMWRITE_JPEG_QUALITY, 85])
                if ret:
                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            time.sleep(1.0 / self.fps)

def main():
    """Interactive setup for screen capture"""
    streamer = ScreenCaptureStreamer()
    
    print("🏠 CS1000X Screen Capture Streamer")
    print("="*50)
    print("This will capture your Samsung Galaxy screen showing the CS1000X app")
    print()
    
    # Find phone mirroring windows
    phone_windows = streamer.find_samsung_dex_window()
    
    if phone_windows:
        print("\nSelect phone mirroring window:")
        for i, (hwnd, title) in enumerate(phone_windows):
            print(f"{i+1}. {title}")
        
        try:
            choice = int(input(f"Choose window (1-{len(phone_windows)}): ")) - 1
            if 0 <= choice < len(phone_windows):
                selected_hwnd = phone_windows[choice][0]
                print(f"Selected: {phone_windows[choice][1]}")
                
                # Start capture
                streamer.start_capture(selected_hwnd)
                
                print("\n✅ Screen capture started!")
                print("📱 Open CS1000X app on your Samsung Galaxy")
                print("🌐 View stream at: http://localhost:5000/api/screen-stream")
                print("Press Ctrl+C to stop...")
                
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    streamer.stop_capture()
                    print("\n🛑 Capture stopped")
            else:
                print("Invalid selection")
        except ValueError:
            print("Invalid input")
    else:
        print("\n⚠️  No phone mirroring windows found.")
        print("\nTo use this tool:")
        print("1. Connect your Samsung Galaxy to PC")
        print("2. Enable screen mirroring (DeX, Smart View, etc.)")
        print("3. Open CS1000X app on your phone")
        print("4. Run this script again")
        print("\nAlternatively, you can capture the full screen:")
        
        if input("Capture full screen? (y/n): ").lower() == 'y':
            streamer.start_capture()
            print("Full screen capture started - Press Ctrl+C to stop")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                streamer.stop_capture()

if __name__ == "__main__":
    main()
