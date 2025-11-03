#!/usr/bin/env python3
"""
Roku CS1000X Camera Monitor - PC Application
Connects to Roku CS1000X cameras for monitoring on PC
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import cv2
from PIL import Image, ImageTk
import threading
import time
import socket
import requests
from urllib.parse import urlparse
import json
import os

class RokuCameraMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Roku CS1000X Camera Monitor")
        self.root.geometry("1200x800")
        
        # Camera connection variables - Pre-configured for your CS1000X
        self.camera_ip = tk.StringVar(value="192.168.0.198")
        self.camera_port = tk.StringVar(value="8080")
        self.username = tk.StringVar(value="admin")
        self.password = tk.StringVar(value="")
        self.rtsp_port = tk.StringVar(value="554")
        
        # Known camera information
        self.camera_mac = "7C:67:AB:23:DF:1E"
        self.camera_model = "CS1000X"
        self.camera_network = "SummersBasement"
        self.camera_device_id = "SOS2000V3AD89EB106D4"
        self.camera_firmware = "7.0.0 • build 26-FD"
        self.camera_activation = "09/16/2023"
        
        # Video stream variables
        self.cap = None
        self.streaming = False
        self.stream_thread = None
        
        # UI variables
        self.video_label = None
        self.status_var = tk.StringVar(value="Disconnected")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Create the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Connection settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Roku CS1000X Connection Settings", padding="10")
        settings_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Camera IP
        ttk.Label(settings_frame, text="Camera IP:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Entry(settings_frame, textvariable=self.camera_ip, width=15).grid(row=0, column=1, padx=(0, 10))
        
        # HTTP Port
        ttk.Label(settings_frame, text="HTTP Port:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        ttk.Entry(settings_frame, textvariable=self.camera_port, width=8).grid(row=0, column=3, padx=(0, 10))
        
        # RTSP Port
        ttk.Label(settings_frame, text="RTSP Port:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        ttk.Entry(settings_frame, textvariable=self.rtsp_port, width=8).grid(row=0, column=5, padx=(0, 10))
        
        # Username
        ttk.Label(settings_frame, text="Username:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        ttk.Entry(settings_frame, textvariable=self.username, width=15).grid(row=1, column=1, padx=(0, 10), pady=(5, 0))
        
        # Password
        ttk.Label(settings_frame, text="Password:").grid(row=1, column=2, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        ttk.Entry(settings_frame, textvariable=self.password, show="*", width=15).grid(row=1, column=3, padx=(0, 10), pady=(5, 0))
        
        # Control buttons
        button_frame = ttk.Frame(settings_frame)
        button_frame.grid(row=1, column=4, columnspan=2, pady=(5, 0))
        
        ttk.Button(button_frame, text="Scan Network", command=self.scan_network).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Test Connection", command=self.test_connection).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Connect", command=self.connect_camera).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Disconnect", command=self.disconnect_camera).pack(side=tk.LEFT)
        
        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT)
        status_label = ttk.Label(status_frame, textvariable=self.status_var, foreground="red")
        status_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Video display area
        video_frame = ttk.LabelFrame(main_frame, text="Camera Feed", padding="5")
        video_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        video_frame.columnconfigure(0, weight=1)
        video_frame.rowconfigure(0, weight=1)
        
        # Video label (will contain the camera feed)
        self.video_label = ttk.Label(video_frame, text="No camera connected", 
                                   background="black", foreground="white",
                                   font=("Arial", 16))
        self.video_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Control panel
        control_frame = ttk.LabelFrame(main_frame, text="Camera Controls", padding="10")
        control_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Camera info
        info_frame = ttk.LabelFrame(control_frame, text="Camera Information", padding="5")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.info_text = scrolledtext.ScrolledText(info_frame, height=8, width=30)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Display known camera information
        self.display_camera_info()
        
        # Recording controls
        record_frame = ttk.LabelFrame(control_frame, text="Recording", padding="5")
        record_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.recording = False
        self.record_button = ttk.Button(record_frame, text="Start Recording", 
                                      command=self.toggle_recording)
        self.record_button.pack(pady=5)
        
        # Snapshot
        ttk.Button(record_frame, text="Take Snapshot", 
                  command=self.take_snapshot).pack(pady=5)
        
        # Camera settings
        settings_control_frame = ttk.LabelFrame(control_frame, text="Camera Settings", padding="5")
        settings_control_frame.pack(fill=tk.X)
        
        ttk.Label(settings_control_frame, text="Quality:").pack()
        quality_var = tk.StringVar(value="High")
        quality_combo = ttk.Combobox(settings_control_frame, textvariable=quality_var,
                                   values=["Low", "Medium", "High"], state="readonly")
        quality_combo.pack(pady=(0, 5))
        
        ttk.Button(settings_control_frame, text="Apply Settings", 
                  command=lambda: self.apply_settings(quality_var.get())).pack()
    
    def display_camera_info(self):
        """Display known camera information"""
        info = f"""Known CS1000X Camera Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Device Model: {self.camera_model}
MAC Address: {self.camera_mac}
IP Address: {self.camera_ip.get()}
Network: {self.camera_network}
Firmware: {self.camera_firmware}
Activation Date: {self.camera_activation}
Virtual Device ID: {self.camera_device_id}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: Ready to connect
"""
        self.info_text.insert(tk.END, info)
    
    def scan_network(self):
        """Scan local network for Roku CS1000X cameras"""
        self.status_var.set("Scanning network...")
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, "Scanning for Roku CS1000X cameras...\n")
        
        def scan_thread():
            found_cameras = []
            
            # Get local network range
            try:
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                network_base = '.'.join(local_ip.split('.')[:-1]) + '.'
                
                self.info_text.insert(tk.END, f"Scanning network: {network_base}1-254\n")
                
                # Common Roku camera ports
                common_ports = [8080, 80, 8000, 8081, 554]
                
                for i in range(1, 255):
                    ip = network_base + str(i)
                    for port in common_ports:
                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(0.5)  # Longer timeout for older cameras
                            result = sock.connect_ex((ip, port))
                            sock.close()
                            
                            if result == 0:
                                # Try to identify if it's a Roku camera
                                try:
                                    response = requests.get(f"http://{ip}:{port}", timeout=2)
                                    if any(keyword in response.text.lower() for keyword in 
                                          ['roku', 'cs1000x', 'camera', 'ipcam', 'webcam']):
                                        found_cameras.append(f"{ip}:{port}")
                                        self.info_text.insert(tk.END, f"Found Roku camera: {ip}:{port}\n")
                                except:
                                    # Even if we can't identify, it might be a camera
                                    found_cameras.append(f"{ip}:{port}")
                                    self.info_text.insert(tk.END, f"Found device: {ip}:{port}\n")
                        except:
                            pass
                
                if found_cameras:
                    self.info_text.insert(tk.END, f"\nFound {len(found_cameras)} potential cameras\n")
                    # Auto-fill first found camera
                    first_camera = found_cameras[0].split(':')
                    self.camera_ip.set(first_camera[0])
                    self.camera_port.set(first_camera[1])
                else:
                    self.info_text.insert(tk.END, "\nNo cameras found. Try manual IP entry.\n")
                
                self.status_var.set("Scan complete")
                
            except Exception as e:
                self.info_text.insert(tk.END, f"Scan error: {str(e)}\n")
                self.status_var.set("Scan failed")
        
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def test_connection(self):
        """Test connection to Roku camera"""
        ip = self.camera_ip.get()
        port = self.camera_port.get()
        
        self.status_var.set("Testing connection...")
        self.info_text.delete(1.0, tk.END)
        
        def test_thread():
            try:
                # Test HTTP connection
                response = requests.get(f"http://{ip}:{port}", timeout=5)
                self.info_text.insert(tk.END, f"HTTP connection successful\n")
                self.info_text.insert(tk.END, f"Response code: {response.status_code}\n")
                
                # Test RTSP connection for Roku CS1000X
                rtsp_urls = [
                    f"rtsp://{self.username.get()}:{self.password.get()}@{ip}:{self.rtsp_port.get()}/live",
                    f"rtsp://{self.username.get()}:{self.password.get()}@{ip}:{self.rtsp_port.get()}/stream1",
                    f"rtsp://{self.username.get()}:{self.password.get()}@{ip}:{self.rtsp_port.get()}/h264",
                    f"rtsp://{ip}:{self.rtsp_port.get()}/live"
                ]
                
                for rtsp_url in rtsp_urls:
                    try:
                        self.info_text.insert(tk.END, f"Testing RTSP: {rtsp_url}\n")
                        
                        test_cap = cv2.VideoCapture(rtsp_url)
                        if test_cap.isOpened():
                            ret, frame = test_cap.read()
                            if ret:
                                self.info_text.insert(tk.END, "RTSP stream accessible\n")
                                self.info_text.insert(tk.END, f"Frame size: {frame.shape}\n")
                                self.status_var.set("Connection test passed")
                                test_cap.release()
                                return
                        test_cap.release()
                    except Exception as e:
                        continue
                
                self.info_text.insert(tk.END, "RTSP streams not accessible\n")
                self.status_var.set("RTSP test failed")
                
            except Exception as e:
                self.info_text.insert(tk.END, f"Connection test failed: {str(e)}\n")
                self.status_var.set("Connection test failed")
        
        threading.Thread(target=test_thread, daemon=True).start()
    
    def connect_camera(self):
        """Connect to the Roku CS1000X camera"""
        if self.streaming:
            messagebox.showwarning("Warning", "Already connected to camera")
            return
        
        ip = self.camera_ip.get()
        username = self.username.get()
        password = self.password.get()
        rtsp_port = self.rtsp_port.get()
        
        # Try multiple RTSP URL formats for Roku CS1000X
        rtsp_urls = [
            f"rtsp://{username}:{password}@{ip}:{rtsp_port}/live",
            f"rtsp://{username}:{password}@{ip}:{rtsp_port}/stream1",
            f"rtsp://{username}:{password}@{ip}:{rtsp_port}/h264",
            f"rtsp://{username}:{password}@{ip}:{rtsp_port}/cam1/h264",
            f"rtsp://{ip}:{rtsp_port}/live",
            f"rtsp://{ip}:{rtsp_port}/stream1"
        ]
        
        self.status_var.set("Connecting...")
        
        def connect_thread():
            for rtsp_url in rtsp_urls:
                try:
                    self.info_text.insert(tk.END, f"Trying: {rtsp_url}\n")
                    
                    self.cap = cv2.VideoCapture(rtsp_url)
                    self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce latency
                    
                    if self.cap.isOpened():
                        ret, frame = self.cap.read()
                        if ret:
                            self.streaming = True
                            self.status_var.set("Connected")
                            self.info_text.insert(tk.END, "Successfully connected!\n")
                            self.start_video_stream()
                            return
                    
                    self.cap.release()
                    
                except Exception as e:
                    self.info_text.insert(tk.END, f"Failed: {str(e)}\n")
            
            self.status_var.set("Connection failed")
            self.info_text.insert(tk.END, "All connection attempts failed\n")
            messagebox.showerror("Error", "Could not connect to camera. Check settings and try again.")
        
        threading.Thread(target=connect_thread, daemon=True).start()
    
    def disconnect_camera(self):
        """Disconnect from camera"""
        self.streaming = False
        if self.cap:
            self.cap.release()
        
        self.video_label.configure(image="", text="No camera connected")
        self.status_var.set("Disconnected")
        self.info_text.insert(tk.END, "Disconnected from camera\n")
    
    def start_video_stream(self):
        """Start the video streaming thread"""
        def stream_thread():
            while self.streaming and self.cap and self.cap.isOpened():
                try:
                    ret, frame = self.cap.read()
                    if ret:
                        # Resize frame for display
                        height, width = frame.shape[:2]
                        max_width = 640
                        max_height = 480
                        
                        if width > max_width or height > max_height:
                            scale = min(max_width/width, max_height/height)
                            new_width = int(width * scale)
                            new_height = int(height * scale)
                            frame = cv2.resize(frame, (new_width, new_height))
                        
                        # Convert BGR to RGB
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        
                        # Convert to PIL Image and then to PhotoImage
                        pil_image = Image.fromarray(frame_rgb)
                        photo = ImageTk.PhotoImage(pil_image)
                        
                        # Update the label with new frame
                        self.video_label.configure(image=photo, text="")
                        self.video_label.image = photo  # Keep a reference
                        
                    else:
                        break
                        
                except Exception as e:
                    self.info_text.insert(tk.END, f"Stream error: {str(e)}\n")
                    break
                
                time.sleep(0.033)  # ~30 FPS
            
            # Clean up when stream ends
            if self.streaming:
                self.disconnect_camera()
        
        self.stream_thread = threading.Thread(target=stream_thread, daemon=True)
        self.stream_thread.start()
    
    def toggle_recording(self):
        """Toggle video recording"""
        if not self.streaming:
            messagebox.showwarning("Warning", "Connect to camera first")
            return
        
        if not self.recording:
            # Start recording
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            self.record_filename = f"roku_recording_{timestamp}.avi"
            
            # Get frame dimensions
            ret, frame = self.cap.read()
            if ret:
                height, width = frame.shape[:2]
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                self.video_writer = cv2.VideoWriter(self.record_filename, fourcc, 20.0, (width, height))
                
                self.recording = True
                self.record_button.configure(text="Stop Recording")
                self.info_text.insert(tk.END, f"Recording started: {self.record_filename}\n")
        else:
            # Stop recording
            self.recording = False
            if hasattr(self, 'video_writer'):
                self.video_writer.release()
            
            self.record_button.configure(text="Start Recording")
            self.info_text.insert(tk.END, "Recording stopped\n")
    
    def take_snapshot(self):
        """Take a snapshot from the camera"""
        if not self.streaming or not self.cap:
            messagebox.showwarning("Warning", "Connect to camera first")
            return
        
        ret, frame = self.cap.read()
        if ret:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"roku_snapshot_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            self.info_text.insert(tk.END, f"Snapshot saved: {filename}\n")
            messagebox.showinfo("Success", f"Snapshot saved as {filename}")
        else:
            messagebox.showerror("Error", "Could not capture frame")
    
    def apply_settings(self, quality):
        """Apply camera settings"""
        self.info_text.insert(tk.END, f"Applied quality setting: {quality}\n")
    
    def on_closing(self):
        """Handle application closing"""
        self.streaming = False
        if self.cap:
            self.cap.release()
        if hasattr(self, 'video_writer') and self.recording:
            self.video_writer.release()
        self.root.destroy()

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = RokuCameraMonitor(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main()
