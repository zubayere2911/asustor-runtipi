#!/usr/bin/env python3
"""
ASUSTOR Dev Center Upload Script (Experimental)

This script attempts to upload APK packages to ASUSTOR Dev Center
using web scraping. This is EXPERIMENTAL and may break at any time
if ASUSTOR changes their website.

Usage:
    python devcenter-upload.py --username USER --password PASS --apk package.apk
    python devcenter-upload.py --dry-run --apk package.apk

Environment variables:
    ASUSTOR_USERNAME: Dev Center username
    ASUSTOR_PASSWORD: Dev Center password

WARNING: This approach may violate ASUSTOR's Terms of Service.
         Use at your own risk and prefer manual upload when possible.
"""

import argparse
import os
import sys
import re
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Tuple

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required packages not installed.")
    print("Please install them with: pip install requests beautifulsoup4")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
BASE_URL = "https://developer.asustor.com"
LOGIN_URL = f"{BASE_URL}/user/login"
APP_MGT_URL = f"{BASE_URL}/app/mgt"
LOGOUT_URL = f"{BASE_URL}/user/logout"

# Common headers to mimic browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}


class DevCenterUploader:
    """Handles authentication and upload to ASUSTOR Dev Center."""
    
    def __init__(self, username: str, password: str, dry_run: bool = False):
        self.username = username
        self.password = password
        self.dry_run = dry_run
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.logged_in = False
        
    def _get_csrf_token(self, html: str) -> Optional[str]:
        """Extract CSRF token from HTML page."""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Try common CSRF token patterns
        patterns = [
            ('input', {'name': '_token'}),
            ('input', {'name': 'csrf_token'}),
            ('input', {'name': '_csrf'}),
            ('input', {'name': 'authenticity_token'}),
            ('meta', {'name': 'csrf-token'}),
        ]
        
        for tag, attrs in patterns:
            element = soup.find(tag, attrs)
            if element:
                return element.get('value') or element.get('content')
        
        # Try to find in JavaScript
        csrf_match = re.search(r'csrf[_-]?token["\']?\s*[:=]\s*["\']([^"\']+)["\']', html, re.I)
        if csrf_match:
            return csrf_match.group(1)
            
        return None
    
    def _extract_form_fields(self, html: str, form_id: str = None) -> Dict[str, str]:
        """Extract all hidden form fields."""
        soup = BeautifulSoup(html, 'html.parser')
        
        if form_id:
            form = soup.find('form', {'id': form_id})
        else:
            form = soup.find('form')
        
        if not form:
            return {}
        
        fields = {}
        for input_tag in form.find_all('input', type='hidden'):
            name = input_tag.get('name')
            value = input_tag.get('value', '')
            if name:
                fields[name] = value
        
        return fields
    
    def login(self) -> bool:
        """Authenticate to ASUSTOR Dev Center."""
        if self.dry_run:
            logger.info("[DRY-RUN] Would login with username: %s", self.username)
            self.logged_in = True
            return True
        
        logger.info("Fetching login page...")
        try:
            response = self.session.get(LOGIN_URL, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error("Failed to fetch login page: %s", e)
            return False
        
        # Extract form fields and CSRF token
        form_fields = self._extract_form_fields(response.text)
        csrf_token = self._get_csrf_token(response.text)
        
        # Prepare login data
        login_data = {
            **form_fields,
            'username': self.username,
            'password': self.password,
            'email': self.username,  # Some forms use email instead
        }
        
        if csrf_token:
            login_data['_token'] = csrf_token
            login_data['csrf_token'] = csrf_token
        
        logger.info("Attempting login...")
        try:
            response = self.session.post(
                LOGIN_URL,
                data=login_data,
                timeout=30,
                allow_redirects=True
            )
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error("Login request failed: %s", e)
            return False
        
        # Check if login was successful
        # Common indicators: redirect to dashboard, presence of logout link, absence of login form
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check for error messages
        error_indicators = [
            soup.find(class_=re.compile(r'error|alert-danger|invalid', re.I)),
            soup.find(text=re.compile(r'invalid|incorrect|failed', re.I)),
        ]
        
        if any(error_indicators):
            logger.error("Login failed - invalid credentials or error message detected")
            return False
        
        # Check for success indicators
        logout_link = soup.find('a', href=re.compile(r'logout', re.I))
        dashboard = soup.find(text=re.compile(r'dashboard|my apps|app management', re.I))
        
        if logout_link or dashboard or 'login' not in response.url.lower():
            logger.info("Login successful!")
            self.logged_in = True
            return True
        
        # Check if we're still on login page
        if 'login' in response.url.lower():
            logger.error("Login failed - still on login page")
            return False
        
        # Assume success if no clear failure
        logger.info("Login appears successful (no error detected)")
        self.logged_in = True
        return True
    
    def logout(self):
        """Logout from Dev Center."""
        if self.dry_run:
            logger.info("[DRY-RUN] Would logout")
            return
        
        if not self.logged_in:
            return
        
        try:
            self.session.get(LOGOUT_URL, timeout=10)
            logger.info("Logged out successfully")
        except requests.RequestException:
            pass  # Ignore logout errors
    
    def get_app_list(self) -> list:
        """Get list of apps from Dev Center."""
        if self.dry_run:
            logger.info("[DRY-RUN] Would fetch app list")
            return [{'name': 'io.runtipi', 'id': 'mock-id'}]
        
        if not self.logged_in:
            logger.error("Not logged in")
            return []
        
        try:
            response = self.session.get(APP_MGT_URL, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error("Failed to fetch app list: %s", e)
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        apps = []
        
        # Try to find app entries (adjust selectors based on actual page structure)
        app_elements = soup.find_all(class_=re.compile(r'app[-_]?item|package[-_]?row', re.I))
        
        if not app_elements:
            # Try alternative: look for table rows with app data
            app_elements = soup.find_all('tr', class_=re.compile(r'app|package', re.I))
        
        if not app_elements:
            # Try to find any links containing app names
            app_elements = soup.find_all('a', href=re.compile(r'/app/\d+|/package/', re.I))
        
        for element in app_elements:
            app_name = element.get_text(strip=True) or element.get('data-name', '')
            app_id = element.get('data-id', '') or element.get('href', '')
            if app_name:
                apps.append({'name': app_name, 'id': app_id})
        
        logger.info("Found %d apps", len(apps))
        return apps
    
    def find_upload_url(self, app_id: str = None) -> Optional[str]:
        """Find the upload URL for a specific app or new app."""
        if self.dry_run:
            return f"{BASE_URL}/app/upload/mock"
        
        if not self.logged_in:
            return None
        
        # First try the app management page
        try:
            response = self.session.get(APP_MGT_URL, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error("Failed to fetch app management page: %s", e)
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for upload links/buttons
        upload_patterns = [
            r'/app/upload',
            r'/package/upload',
            r'/app/\d+/update',
            r'/upload',
        ]
        
        for pattern in upload_patterns:
            link = soup.find('a', href=re.compile(pattern, re.I))
            if link:
                href = link.get('href', '')
                if href.startswith('/'):
                    return BASE_URL + href
                return href
        
        # Try to find upload form
        form = soup.find('form', action=re.compile(r'upload', re.I))
        if form:
            action = form.get('action', '')
            if action.startswith('/'):
                return BASE_URL + action
            return action or None
        
        # Default fallback - common upload endpoints
        common_endpoints = [
            f"{BASE_URL}/app/upload",
            f"{BASE_URL}/app/add",
            f"{BASE_URL}/package/upload",
        ]
        
        for endpoint in common_endpoints:
            try:
                response = self.session.get(endpoint, timeout=10)
                if response.status_code == 200 and 'upload' in response.text.lower():
                    return endpoint
            except requests.RequestException:
                continue
        
        return None
    
    def upload_apk(self, apk_path: Path, changelog: str = "") -> Tuple[bool, str]:
        """Upload APK file to Dev Center."""
        if not apk_path.exists():
            return False, f"APK file not found: {apk_path}"
        
        if self.dry_run:
            logger.info("[DRY-RUN] Would upload: %s", apk_path)
            logger.info("[DRY-RUN] File size: %.2f MB", apk_path.stat().st_size / 1024 / 1024)
            if changelog:
                logger.info("[DRY-RUN] Changelog: %s", changelog[:100])
            return True, "[DRY-RUN] Upload simulated successfully"
        
        if not self.logged_in:
            return False, "Not logged in"
        
        # Find upload URL
        upload_url = self.find_upload_url()
        if not upload_url:
            return False, "Could not find upload URL"
        
        logger.info("Upload URL: %s", upload_url)
        
        # Get upload page for CSRF token and form fields
        try:
            response = self.session.get(upload_url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            return False, f"Failed to fetch upload page: {e}"
        
        form_fields = self._extract_form_fields(response.text)
        csrf_token = self._get_csrf_token(response.text)
        
        if csrf_token:
            form_fields['_token'] = csrf_token
        
        # Add changelog if provided
        if changelog:
            form_fields['changelog'] = changelog
            form_fields['change_log'] = changelog
            form_fields['release_notes'] = changelog
        
        # Prepare file upload
        logger.info("Uploading %s (%.2f MB)...", apk_path.name, apk_path.stat().st_size / 1024 / 1024)
        
        try:
            with open(apk_path, 'rb') as f:
                files = {
                    'file': (apk_path.name, f, 'application/octet-stream'),
                    'apk': (apk_path.name, f, 'application/octet-stream'),
                    'package': (apk_path.name, f, 'application/octet-stream'),
                }
                
                # Try with the first file field that might work
                for file_field, file_data in files.items():
                    f.seek(0)  # Reset file pointer
                    response = self.session.post(
                        upload_url,
                        data=form_fields,
                        files={file_field: file_data},
                        timeout=300,  # 5 minutes for large files
                    )
                    
                    if response.status_code in (200, 201, 302):
                        break
                    
        except requests.RequestException as e:
            return False, f"Upload request failed: {e}"
        except IOError as e:
            return False, f"Failed to read APK file: {e}"
        
        # Check response
        if response.status_code in (200, 201, 302):
            # Check for success indicators
            if 'success' in response.text.lower() or 'uploaded' in response.text.lower():
                return True, "Upload successful!"
            if 'error' in response.text.lower() or 'failed' in response.text.lower():
                # Try to extract error message
                soup = BeautifulSoup(response.text, 'html.parser')
                error = soup.find(class_=re.compile(r'error|alert', re.I))
                if error:
                    return False, f"Upload failed: {error.get_text(strip=True)}"
            # Assume success on redirect
            if response.status_code == 302:
                return True, "Upload completed (redirected)"
            return True, "Upload completed"
        
        return False, f"Upload failed with status {response.status_code}"
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Upload APK packages to ASUSTOR Dev Center',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--apk', '-a',
        type=Path,
        required=True,
        help='Path to APK file to upload'
    )
    
    parser.add_argument(
        '--username', '-u',
        type=str,
        default=os.environ.get('ASUSTOR_USERNAME', ''),
        help='ASUSTOR Dev Center username (or set ASUSTOR_USERNAME env var)'
    )
    
    parser.add_argument(
        '--password', '-p',
        type=str,
        default=os.environ.get('ASUSTOR_PASSWORD', ''),
        help='ASUSTOR Dev Center password (or set ASUSTOR_PASSWORD env var)'
    )
    
    parser.add_argument(
        '--changelog', '-c',
        type=str,
        default='',
        help='Changelog/release notes for this version'
    )
    
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Simulate upload without actually uploading'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Validate inputs
    if not args.apk.exists():
        logger.error("APK file not found: %s", args.apk)
        sys.exit(1)
    
    if not args.dry_run and (not args.username or not args.password):
        logger.error("Username and password are required (use -u/-p or environment variables)")
        sys.exit(1)
    
    # Perform upload
    logger.info("=" * 60)
    logger.info("ASUSTOR Dev Center Upload (Experimental)")
    logger.info("=" * 60)
    
    if args.dry_run:
        logger.info("DRY-RUN MODE - No actual upload will be performed")
    
    logger.info("APK: %s", args.apk)
    logger.info("")
    
    with DevCenterUploader(args.username, args.password, args.dry_run) as uploader:
        # Login
        if not uploader.login():
            logger.error("Login failed!")
            sys.exit(1)
        
        # List apps (optional, for verification)
        apps = uploader.get_app_list()
        if apps:
            logger.info("Your apps: %s", ', '.join(a['name'] for a in apps[:5]))
        
        # Upload
        success, message = uploader.upload_apk(args.apk, args.changelog)
        
        if success:
            logger.info("✅ %s", message)
            sys.exit(0)
        else:
            logger.error("❌ %s", message)
            sys.exit(1)


if __name__ == '__main__':
    main()
