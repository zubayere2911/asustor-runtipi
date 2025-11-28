#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASUSTOR APK Builder - ARM64 Variant Generator

This script creates an ARM64 variant of the Runtipi package
by temporarily modifying config.json and building the APK.

Usage:
    python build-arm64.py [--destination <folder>] [--verbose]
"""

import json
import subprocess
import sys
from pathlib import Path

# Resolve paths
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_FILE = PROJECT_ROOT / 'apk' / 'CONTROL' / 'config.json'
BUILD_SCRIPT = SCRIPT_DIR / 'build.py'

# ARM64 model filter (AS33v2, AS11TL, AS12, AS33, AS11)
ARM64_MODELS = ["33xx", "11xx", "1axx", "3axx", "12xx"]


class Colors:
    RESET = '\033[0m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'

    @classmethod
    def enable(cls):
        if sys.platform == 'win32':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except Exception:
                cls.RESET = cls.MAGENTA = cls.CYAN = cls.GREEN = cls.YELLOW = ''


def main():
    Colors.enable()
    
    print()
    print(f"{Colors.MAGENTA}╔══════════════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.MAGENTA}║       ASUSTOR APK Builder - ARM64 Variant Generator         ║{Colors.RESET}")
    print(f"{Colors.MAGENTA}╚══════════════════════════════════════════════════════════════╝{Colors.RESET}")
    print()
    
    # Backup original config
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config_backup = f.read()
    
    print(f"{Colors.CYAN}🔹 Backed up original config.json{Colors.RESET}")
    
    try:
        # Load and modify config for ARM64
        config = json.loads(config_backup)
        original_arch = config['general']['architecture']
        
        if original_arch == 'arm64':
            print(f"{Colors.YELLOW}⚠️  Config is already set to arm64{Colors.RESET}")
        else:
            config['general']['architecture'] = 'arm64'
            config['general']['model'] = ARM64_MODELS
            
            # Save modified config
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            print(f"{Colors.CYAN}🔹 Modified config.json for ARM64{Colors.RESET}")
            print(f"{Colors.CYAN}🔹 Added model filter: {', '.join(ARM64_MODELS)}{Colors.RESET}")
        
        # Build ARM64 variant - pass through command line args
        print()
        cmd = [sys.executable, str(BUILD_SCRIPT)] + sys.argv[1:]
        subprocess.run(cmd, check=True)
        
    finally:
        # Restore original config
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            f.write(config_backup)
        
        print()
        print(f"{Colors.CYAN}🔹 Restored original config.json{Colors.RESET}")
    
    print()
    print(f"{Colors.GREEN}✅ ARM64 variant build complete!{Colors.RESET}")
    print()


if __name__ == '__main__':
    main()
