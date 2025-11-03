#!/usr/bin/env python3
"""
Roku API Analyzer - Deep analysis of CS1000X/Roku communication
This will help us understand the actual API endpoints and authentication
"""

import requests
import json
import time
import base64
import hashlib
import uuid
import hmac
from urllib.parse import urlparse, parse_qs, urlencode
import re

class RokuAPIAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.device_id = self.generate_realistic_device_id()
        self.app_version = "3.2.1"  # Common CS1000X app version
        self.api_endpoints = []
        
        # Samsung Galaxy S23 headers (very important for authentication)
        self.session.headers.update({
            'User-Agent': 'CS1000X/3.2.1 (Linux; Android 13; SM-S911B Build/TP1A.220624.014) Mobile/1.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'X-Requested-With': 'com.roku.camera',
            'X-App-Version': self.app_version,
            'X-Device-ID': self.device_id,
            'X-Platform': 'android',
            'X-OS-Version': '13'
        })
    
    def generate_realistic_device_id(self):
        """Generate device ID that matches real CS1000X app format"""
        # CS1000X apps often use specific formats
        mac_style = ':'.join([f'{uuid.uuid4().hex[i:i+2]}' for i in range(0, 12, 2)])
        return f"android_{mac_style}_{int(time.time())}"
    
    def discover_roku_domains(self):
        """Discover all Roku-related domains and subdomains"""
        print("🔍 Discovering Roku API domains...")
        
        # Known Roku domains and likely subdomains
        base_domains = ['roku.com', 'rokutime.com']
        subdomains = [
            'api', 'camera-api', 'cloud', 'services', 'my', 'scpl', 
            'auth', 'login', 'mobile', 'app', 'device', 'stream',
            'video', 'live', 'rtmp', 'hls', 'webrtc', 'p2p',
            'cs1000x', 'camera', 'security', 'home'
        ]
        
        discovered_endpoints = []
        
        for domain in base_domains:
            for subdomain in subdomains:
                test_url = f"https://{subdomain}.{domain}"
                try:
                    response = self.session.head(test_url, timeout=5)
                    if response.status_code != 404:
                        discovered_endpoints.append({
                            'url': test_url,
                            'status': response.status_code,
                            'server': response.headers.get('server', 'unknown')
                        })
                        print(f"✅ Found: {test_url} (Status: {response.status_code})")
                except:
                    continue
        
        return discovered_endpoints
    
    def analyze_mobile_app_patterns(self):
        """Analyze common mobile app API patterns"""
        print("📱 Analyzing mobile app API patterns...")
        
        # Common mobile API patterns
        api_patterns = [
            '/api/v1/auth/login',
            '/api/v1/auth/token',
            '/api/v1/user/login',
            '/api/v1/device/register',
            '/api/v1/device/list',
            '/api/v1/camera/list',
            '/api/v1/camera/{id}/stream',
            '/api/v1/camera/{id}/live',
            '/mobile/api/auth',
            '/mobile/api/devices',
            '/camera/api/v1/auth',
            '/camera/api/v1/devices',
            '/auth/oauth/token',
            '/oauth2/token',
            '/login',
            '/token'
        ]
        
        # Test against discovered domains
        working_endpoints = []
        
        for pattern in api_patterns:
            # Test against common base URLs
            test_urls = [
                f"https://api.roku.com{pattern}",
                f"https://camera-api.roku.com{pattern}",
                f"https://services.roku.com{pattern}",
                f"https://my.roku.com{pattern}",
                f"https://scpl.roku.com{pattern}"
            ]
            
            for url in test_urls:
                try:
                    response = self.session.get(url, timeout=5)
                    if response.status_code not in [404, 502, 503]:
                        working_endpoints.append({
                            'url': url,
                            'status': response.status_code,
                            'content_type': response.headers.get('content-type', ''),
                            'response_size': len(response.content)
                        })
                        print(f"🎯 API Endpoint: {url} (Status: {response.status_code})")
                        
                        # Save response for analysis
                        if response.status_code == 200:
                            self.save_response_analysis(url, response)
                            
                except Exception as e:
                    continue
        
        return working_endpoints
    
    def save_response_analysis(self, url, response):
        """Save API response for detailed analysis"""
        try:
            filename = f"api_response_{urlparse(url).netloc}_{int(time.time())}.json"
            analysis = {
                'url': url,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'content': response.text[:1000],  # First 1000 chars
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            with open(filename, 'w') as f:
                json.dump(analysis, f, indent=2)
            
            print(f"💾 Saved response analysis: {filename}")
            
        except Exception as e:
            print(f"Failed to save analysis: {e}")
    
    def test_authentication_methods(self):
        """Test various authentication methods"""
        print("🔐 Testing authentication methods...")
        
        # Common authentication endpoints
        auth_endpoints = [
            'https://api.roku.com/api/v1/auth/login',
            'https://services.roku.com/api/v1/auth/login',
            'https://my.roku.com/api/v1/auth/login',
            'https://scpl.roku.com/api/v1/auth/login',
            'https://camera-api.roku.com/api/v1/auth/login'
        ]
        
        # Test different auth payload formats
        auth_payloads = [
            {
                'username': 'test@example.com',
                'password': 'test123',
                'device_id': self.device_id,
                'app_version': self.app_version
            },
            {
                'email': 'test@example.com',
                'password': 'test123',
                'deviceId': self.device_id,
                'platform': 'android'
            },
            {
                'user': 'test@example.com',
                'pass': 'test123',
                'device': self.device_id,
                'type': 'mobile'
            }
        ]
        
        auth_results = []
        
        for endpoint in auth_endpoints:
            for payload in auth_payloads:
                try:
                    response = self.session.post(endpoint, json=payload, timeout=10)
                    
                    result = {
                        'endpoint': endpoint,
                        'payload_format': list(payload.keys()),
                        'status_code': response.status_code,
                        'response': response.text[:200]
                    }
                    
                    auth_results.append(result)
                    
                    if response.status_code not in [404, 502, 503]:
                        print(f"🔑 Auth response: {endpoint} -> {response.status_code}")
                        if 'token' in response.text.lower() or 'auth' in response.text.lower():
                            print(f"🎯 POTENTIAL AUTH ENDPOINT: {endpoint}")
                            
                except Exception as e:
                    continue
        
        return auth_results
    
    def analyze_cs1000x_specific_patterns(self):
        """Look for CS1000X-specific API patterns"""
        print("🏠 Analyzing CS1000X-specific patterns...")
        
        # CS1000X might use specific identifiers
        cs1000x_patterns = [
            '/cs1000x/api/v1/auth',
            '/camera/cs1000x/auth',
            '/api/cs1000x/login',
            '/api/v1/cs1000x/devices',
            '/security/api/v1/auth',
            '/home/api/v1/auth',
            '/iot/api/v1/auth'
        ]
        
        # Your actual camera device IDs
        device_patterns = [
            '/api/v1/device/SOS2000V3AD89EB106D4',  # Basement camera
            '/api/v1/device/SOS2133V1AD65D83D69A',  # Lab camera
            '/api/v1/camera/7C:67:AB:23:DF:1E',     # Basement MAC
            '/api/v1/camera/7C:67:AB:40:A1:5C'      # Lab MAC
        ]
        
        all_patterns = cs1000x_patterns + device_patterns
        results = []
        
        for pattern in all_patterns:
            test_urls = [
                f"https://api.roku.com{pattern}",
                f"https://camera-api.roku.com{pattern}",
                f"https://scpl.roku.com{pattern}",
                f"https://services.roku.com{pattern}"
            ]
            
            for url in test_urls:
                try:
                    response = self.session.get(url, timeout=5)
                    if response.status_code not in [404, 502, 503]:
                        results.append({
                            'url': url,
                            'status': response.status_code,
                            'content': response.text[:100]
                        })
                        print(f"🏠 CS1000X pattern found: {url} -> {response.status_code}")
                except:
                    continue
        
        return results
    
    def generate_comprehensive_report(self):
        """Generate a comprehensive analysis report"""
        print("\n" + "="*60)
        print("🏠 CS1000X ROKU API ANALYSIS REPORT")
        print("="*60)
        
        # Run all analysis methods
        domains = self.discover_roku_domains()
        endpoints = self.analyze_mobile_app_patterns()
        auth_results = self.test_authentication_methods()
        cs1000x_results = self.analyze_cs1000x_specific_patterns()
        
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'device_id': self.device_id,
            'discovered_domains': domains,
            'api_endpoints': endpoints,
            'authentication_tests': auth_results,
            'cs1000x_patterns': cs1000x_results,
            'summary': {
                'total_domains_found': len(domains),
                'total_endpoints_found': len(endpoints),
                'auth_endpoints_tested': len(auth_results),
                'cs1000x_patterns_found': len(cs1000x_results)
            }
        }
        
        # Save comprehensive report
        with open('roku_api_analysis_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 ANALYSIS COMPLETE:")
        print(f"   • Domains discovered: {len(domains)}")
        print(f"   • API endpoints found: {len(endpoints)}")
        print(f"   • Auth methods tested: {len(auth_results)}")
        print(f"   • CS1000X patterns: {len(cs1000x_results)}")
        print(f"\n💾 Full report saved: roku_api_analysis_report.json")
        
        return report

def main():
    analyzer = RokuAPIAnalyzer()
    
    print("🏠 CS1000X Roku API Deep Analysis")
    print("This will discover the actual API endpoints used by CS1000X cameras")
    print("No phone required - direct server communication!")
    print()
    
    # Run comprehensive analysis
    report = analyzer.generate_comprehensive_report()
    
    print("\n🎯 NEXT STEPS:")
    print("1. Review the generated report file")
    print("2. Look for working authentication endpoints")
    print("3. Test discovered APIs with your actual Roku credentials")
    print("4. Implement direct camera access without phone dependency")

if __name__ == "__main__":
    main()
