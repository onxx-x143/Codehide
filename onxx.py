#!/data/data/com.termux/files/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import zlib
import base64
import argparse
import random
import string
import subprocess
from pathlib import Path

# ============ कॉन्फ़िगरेशन ============
REPO_URL = "https://github.com/onxx-x143"   # आपकी GitHub रिपो
# =======================================

# ============ रंगीन बैनर (Raw String + ANSI कोड) ============
BANNER_LINES = [
    r"   _____  ____  _   _  __  __",
    r"  / _ \ \/ / _ \| \ | | \ \/ /",
    r" | | | \  / (_) |  \| |  \  / ",
    r" | |_| /  \__, | |\  |  /  \ ",
    r"  \___/_/\_\ /_/ |_| \_| /_/\_\ ",
    r"    onxx – Code Obfuscator v1.0"
]
COLORS = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']
# ============================================================

def print_banner():
    for line, color in zip(BANNER_LINES, COLORS):
        print(color + line)
    print("\033[0m")   # रंग रीसेट
    print("   \033[90mHide your code. Protect your logic.\033[0m\n")

def open_repo():
    """सभी संभावित तरीकों से URL को ब्राउज़र में खोलने की कोशिश करता है"""
    try:
        # Termux (Android)
        subprocess.run(["termux-open-url", REPO_URL], check=False, capture_output=True)
        print(f"\033[92m[✔]\033[0m Opening repository in browser...")
        return
    except (FileNotFoundError, subprocess.SubprocessError):
        pass

    try:
        # Linux / Desktop (xdg-open)
        subprocess.run(["xdg-open", REPO_URL], check=False, capture_output=True)
        print(f"\033[92m[✔]\033[0m Opening repository in browser...")
        return
    except (FileNotFoundError, subprocess.SubprocessError):
        pass

    try:
        # Android (am start)
        subprocess.run(["am", "start", "-a", "android.intent.action.VIEW", "-d", REPO_URL], check=False, capture_output=True)
        print(f"\033[92m[✔]\033[0m Opening repository in browser...")
        return
    except (FileNotFoundError, subprocess.SubprocessError):
        pass

    try:
        # Windows (start)
        subprocess.run(["start", REPO_URL], shell=True, check=False, capture_output=True)
        print(f"\033[92m[✔]\033[0m Opening repository in browser...")
        return
    except (FileNotFoundError, subprocess.SubprocessError):
        pass

    # अगर कुछ काम न करे तो बस URL प्रिंट करें
    print(f"\033[93m[!]\033[0m Could not open browser automatically. Please visit: {REPO_URL}")

def detect_type(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        first = f.readline().strip()
        if first.startswith('#!'):
            if 'python' in first.lower():
                return 'python'
            if 'bash' in first.lower() or 'sh' in first.lower():
                return 'bash'
    ext = os.path.splitext(filepath)[1].lower()
    if ext in ['.py', '.pyw']:
        return 'python'
    if ext in ['.sh', '.bash']:
        return 'bash'
    return 'bash'

def obfuscate_python(source_code):
    compressed = zlib.compress(source_code.encode('utf-8'))
    encoded = base64.b64encode(compressed).decode('ascii')
    var1 = ''.join(random.choices(string.ascii_lowercase, k=8))
    var2 = ''.join(random.choices(string.ascii_lowercase, k=8))
    wrapper = f'''import zlib, base64
{var1} = "{encoded}"
{var2} = zlib.decompress(base64.b64decode({var1}))
exec({var2})
'''
    return wrapper

def obfuscate_bash(source_code):
    encoded = base64.b64encode(source_code.encode('utf-8')).decode('ascii')
    wrapper = f'''#!/data/data/com.termux/files/usr/bin/bash
{encoded} | base64 -d | bash
'''
    return wrapper

def main():
    parser = argparse.ArgumentParser(description='Obfuscate any script for Termux', add_help=False)
    parser.add_argument('-f', '--file', help='Input script file')
    parser.add_argument('-o', '--output', help='Output file (default: <input>_obf)')
    parser.add_argument('-h', '--help', action='store_true', help='Show this help')
    args, unknown = parser.parse_known_args()

    if len(sys.argv) == 1 or args.help:
        print_banner()
        parser.print_help()
        sys.exit(0)

    # 👇 सबसे पहले रिपोजिटरी खोलें
    open_repo()

    if not args.file and unknown:
        args.file = unknown[0]

    if not args.file:
        print_banner()
        print("\033[91m[!]\033[0m Error: No input file provided.")
        sys.exit(1)

    input_file = Path(args.file)
    if not input_file.exists():
        print(f"\033[91m[!]\033[0m Error: File '{input_file}' not found.")
        sys.exit(1)

    if args.output:
        output_file = Path(args.output)
    else:
        stem = input_file.stem
        suffix = input_file.suffix
        output_file = input_file.parent / f"{stem}_obf{suffix}"

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            source = f.read()
    except Exception as e:
        print(f"\033[91m[!]\033[0m Error reading file: {e}")
        sys.exit(1)

    script_type = detect_type(input_file)
    if script_type == 'python':
        obfuscated = obfuscate_python(source)
    else:
        obfuscated = obfuscate_bash(source)

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(obfuscated)
        os.chmod(output_file, 0o755)
        print(f"\033[92m[✔]\033[0m Obfuscated successfully: {output_file}")
        print(f"\033[92m[✔]\033[0m Type: {script_type.upper()}")
    except Exception as e:
        print(f"\033[91m[!]\033[0m Error writing output: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
