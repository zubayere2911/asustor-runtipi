#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASUSTOR Package Version Manager

Manages version revisions for ASUSTOR packages when the upstream app version
hasn't changed but package modifications require a new release.

Version Format:
- Base version: X.Y.Z (from Runtipi upstream)
- With revision: X.Y.Z.rN (when package changes without app version change)

Examples:
- First release of v4.6.5: 4.6.5
- Second release (package changes only): 4.6.5.r1
- Third release (package changes only): 4.6.5.r2
- New Runtipi version: 4.6.6 (revision resets)

Usage:
    python version-manager.py --check           # Check if revision needed
    python version-manager.py --get-next        # Get next version (with revision if needed)
    python version-manager.py --update          # Update config.json with next version
    python version-manager.py --set 4.6.5       # Set base version (check for revision)
"""

import sys
import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Optional, Tuple

__version__ = '1.0.0'

# Paths
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_FILE = PROJECT_ROOT / 'apk' / 'CONTROL' / 'config.json'


class Colors:
    """ANSI color codes for terminal output."""
    RESET = '\033[0m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    GRAY = '\033[90m'
    
    @classmethod
    def enable(cls):
        if sys.platform == 'win32':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except Exception:
                cls.RESET = cls.GREEN = cls.CYAN = cls.YELLOW = ''
                cls.RED = cls.BLUE = cls.GRAY = ''


def print_info(msg): print(f"{Colors.CYAN}🔹 {msg}{Colors.RESET}")
def print_success(msg): print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")
def print_warn(msg): print(f"{Colors.YELLOW}⚠️  {msg}{Colors.RESET}")
def print_error(msg): print(f"{Colors.RED}❌ {msg}{Colors.RESET}")


class VersionManager:
    """Manages ASUSTOR package versions with revision support."""
    
    # Version pattern: X.Y.Z or X.Y.Z.rN
    VERSION_PATTERN = re.compile(r'^(\d+\.\d+\.\d+)(?:\.r(\d+))?$')
    
    def __init__(self, config_path: Path = CONFIG_FILE):
        self.config_path = config_path
        
    def get_current_version(self) -> str:
        """Get current version from config.json."""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config['general']['version']
    
    def set_version(self, version: str):
        """Update version in config.json."""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        config['general']['version'] = version
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
    
    def parse_version(self, version: str) -> Tuple[str, Optional[int]]:
        """Parse version into base version and revision number.
        
        Returns:
            Tuple of (base_version, revision) where revision is None if no revision
        """
        match = self.VERSION_PATTERN.match(version)
        if not match:
            raise ValueError(f"Invalid version format: {version}")
        base = match.group(1)
        revision = int(match.group(2)) if match.group(2) else None
        return base, revision
    
    def format_version(self, base: str, revision: Optional[int]) -> str:
        """Format base version and revision into version string."""
        if revision is None or revision == 0:
            return base
        return f"{base}.r{revision}"
    
    def get_git_tags(self) -> list:
        """Get list of git tags (version tags only)."""
        try:
            result = subprocess.run(
                ['git', 'tag', '-l', 'v*'],
                capture_output=True,
                text=True,
                cwd=PROJECT_ROOT
            )
            if result.returncode == 0:
                tags = [t.strip() for t in result.stdout.strip().split('\n') if t.strip()]
                return sorted(tags, key=self._version_sort_key, reverse=True)
        except Exception as e:
            print_warn(f"Could not get git tags: {e}")
        return []
    
    def _version_sort_key(self, tag: str) -> tuple:
        """Create a sort key for version tags."""
        # Remove 'v' prefix
        version = tag[1:] if tag.startswith('v') else tag
        try:
            base, revision = self.parse_version(version)
            parts = [int(p) for p in base.split('.')]
            return (*parts, revision or 0)
        except ValueError:
            return (0, 0, 0, 0)
    
    def get_latest_tag_for_base(self, base_version: str) -> Optional[str]:
        """Get the latest tag for a specific base version.
        
        Examples:
            - For base 4.6.5, might return "v4.6.5.r2" if that's the latest
            - Returns None if no tags exist for this base version
        """
        tags = self.get_git_tags()
        matching_tags = []
        
        for tag in tags:
            version = tag[1:] if tag.startswith('v') else tag
            try:
                tag_base, tag_revision = self.parse_version(version)
                if tag_base == base_version:
                    matching_tags.append((tag, tag_revision or 0))
            except ValueError:
                continue
        
        if not matching_tags:
            return None
        
        # Sort by revision and return the latest
        matching_tags.sort(key=lambda x: x[1], reverse=True)
        return matching_tags[0][0]
    
    def check_needs_revision(self, target_base: str) -> Tuple[bool, Optional[int]]:
        """Check if a revision is needed for the target base version.
        
        Returns:
            Tuple of (needs_revision, next_revision_number)
            - (False, None) if this is a new base version
            - (True, N) if revision rN is needed
        """
        latest_tag = self.get_latest_tag_for_base(target_base)
        
        if latest_tag is None:
            # No existing tag for this base version
            return (False, None)
        
        # Parse the latest tag
        version = latest_tag[1:] if latest_tag.startswith('v') else latest_tag
        _, current_revision = self.parse_version(version)
        
        # Need next revision
        next_revision = (current_revision or 0) + 1
        return (True, next_revision)
    
    def get_next_version(self, target_base: Optional[str] = None) -> str:
        """Get the next version to use.
        
        If target_base is provided, uses that as the base version.
        Otherwise, extracts the base version from current config.
        """
        if target_base is None:
            current = self.get_current_version()
            target_base, _ = self.parse_version(current)
        
        needs_revision, next_rev = self.check_needs_revision(target_base)
        
        if needs_revision:
            return self.format_version(target_base, next_rev)
        return target_base
    
    def check_changes_since_tag(self, tag: str) -> bool:
        """Check if there are changes in apk/ folder since the given tag."""
        try:
            result = subprocess.run(
                ['git', 'diff', '--quiet', tag, '--', 'apk/'],
                capture_output=True,
                cwd=PROJECT_ROOT
            )
            # Exit code 0 = no changes, 1 = changes exist
            return result.returncode != 0
        except Exception as e:
            print_warn(f"Could not check changes: {e}")
            return True  # Assume changes if we can't check


def main():
    Colors.enable()
    
    parser = argparse.ArgumentParser(
        description='ASUSTOR Package Version Manager',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python version-manager.py --check              # Check if revision needed
    python version-manager.py --get-next           # Get next version
    python version-manager.py --get-next --base 4.6.5  # Get next for specific base
    python version-manager.py --update             # Update config.json
    python version-manager.py --set 4.7.0          # Set base version (auto-revision)
"""
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--check', action='store_true',
                      help='Check if revision is needed for current version')
    group.add_argument('--get-next', action='store_true',
                      help='Get the next version (with revision if needed)')
    group.add_argument('--update', action='store_true',
                      help='Update config.json with next version')
    group.add_argument('--bump-revision', action='store_true',
                      help='Increment revision of current version (4.6.5 → 4.6.5.r1 → 4.6.5.r2)')
    group.add_argument('--set', metavar='VERSION',
                      help='Set base version (auto-adds revision if needed)')
    group.add_argument('--current', action='store_true',
                      help='Show current version from config.json')
    group.add_argument('--tags', action='store_true',
                      help='List all version tags')
    
    parser.add_argument('--base', metavar='VERSION',
                       help='Base version to use (with --get-next)')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Only output the version (for scripts)')
    parser.add_argument('--version', '-V', action='version',
                       version=f'Version Manager v{__version__}')
    
    args = parser.parse_args()
    vm = VersionManager()
    
    try:
        if args.current:
            version = vm.get_current_version()
            if args.quiet:
                print(version)
            else:
                print_info(f"Current version: {version}")
                base, rev = vm.parse_version(version)
                print_info(f"Base: {base}, Revision: {rev or 'none'}")
        
        elif args.tags:
            tags = vm.get_git_tags()
            if args.quiet:
                for tag in tags:
                    print(tag)
            else:
                print_info("Version tags:")
                for tag in tags[:10]:  # Show last 10
                    print(f"  {tag}")
                if len(tags) > 10:
                    print(f"  ... and {len(tags) - 10} more")
        
        elif args.check:
            current = vm.get_current_version()
            base, _ = vm.parse_version(current)
            needs_rev, next_rev = vm.check_needs_revision(base)
            
            if args.quiet:
                print("true" if needs_rev else "false")
            else:
                if needs_rev:
                    print_warn(f"Revision needed: {base} → {base}.r{next_rev}")
                    latest = vm.get_latest_tag_for_base(base)
                    print_info(f"Latest tag for {base}: {latest}")
                else:
                    print_success(f"No revision needed - {base} is a new version")
        
        elif args.get_next:
            base = args.base
            if base is None:
                current = vm.get_current_version()
                base, _ = vm.parse_version(current)
            
            next_version = vm.get_next_version(base)
            
            if args.quiet:
                print(next_version)
            else:
                needs_rev, _ = vm.check_needs_revision(base)
                if needs_rev:
                    print_info(f"Base version: {base}")
                    print_info(f"Next version: {next_version}")
                    print_warn("Revision added because tag already exists")
                else:
                    print_success(f"Next version: {next_version} (new)")
        
        elif args.update:
            current = vm.get_current_version()
            base, _ = vm.parse_version(current)
            next_version = vm.get_next_version(base)
            
            if not args.quiet:
                print_info(f"Current: {current}")
                print_info(f"Next: {next_version}")
            
            vm.set_version(next_version)
            
            if args.quiet:
                print(next_version)
            else:
                print_success(f"Updated config.json to {next_version}")
        
        elif args.bump_revision:
            current = vm.get_current_version()
            base, current_rev = vm.parse_version(current)
            
            # Increment revision
            next_rev = (current_rev or 0) + 1
            next_version = vm.format_version(base, next_rev)
            
            if not args.quiet:
                print_info(f"Current: {current}")
                print_info(f"Next: {next_version}")
            
            vm.set_version(next_version)
            
            if args.quiet:
                print(next_version)
            else:
                print_success(f"Bumped revision: {current} → {next_version}")
        
        elif args.set:
            target_base = args.set
            # Validate format
            if not re.match(r'^\d+\.\d+\.\d+$', target_base):
                print_error(f"Invalid base version format: {target_base}")
                print_info("Expected format: X.Y.Z (e.g., 4.6.5)")
                sys.exit(1)
            
            next_version = vm.get_next_version(target_base)
            
            if not args.quiet:
                needs_rev, _ = vm.check_needs_revision(target_base)
                if needs_rev:
                    print_warn(f"Tag for {target_base} exists, adding revision")
                print_info(f"Setting version to: {next_version}")
            
            vm.set_version(next_version)
            
            if args.quiet:
                print(next_version)
            else:
                print_success(f"Updated config.json to {next_version}")
    
    except Exception as e:
        print_error(str(e))
        sys.exit(1)


if __name__ == '__main__':
    main()
