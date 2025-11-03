#!/usr/bin/env python3
"""
Quick port scanner for CS1000X camera
"""
import socket
import sys

def test_port(ip, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False

def scan_camera_ports(ip):
    print(f"Scanning ports on {ip}...")
    
    # Common camera ports
    ports_to_test = [
        (80, "HTTP"),
        (81, "HTTP Alt"),
        (443, "HTTPS"),
        (554, "RTSP"),
        (1935, "RTMP"),
        (8000, "HTTP Alt"),
        (8080, "HTTP Proxy"),
        (8081, "HTTP Alt"),
        (8554, "RTSP Alt"),
        (8888, "HTTP Alt"),
        (9000, "HTTP Alt"),
        (10554, "RTSP Alt"),
        (88, "Kerberos/HTTP"),
        (7070, "HTTP Alt")
    ]
    
    open_ports = []
    
    for port, description in ports_to_test:
        if test_port(ip, port):
            open_ports.append((port, description))
            print(f"✅ Port {port} ({description}) - OPEN")
        else:
            print(f"❌ Port {port} ({description}) - CLOSED")
    
    print(f"\nSummary for {ip}:")
    if open_ports:
        print("Open ports found:")
        for port, desc in open_ports:
            print(f"  - {port} ({desc})")
    else:
        print("No common camera ports are open")
    
    return open_ports

if __name__ == "__main__":
    camera_ip = "192.168.0.198"
    scan_camera_ports(camera_ip)
