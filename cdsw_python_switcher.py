#!/usr/bin/env python3
"""
CDSW Python Version Switcher
============================

This script helps you switch between Python versions in CDSW environments
that have multiple Python versions installed.

Specifically designed for your case where both Python 3.6 and 3.12 are available.

Author: AI Assistant
Date: 2025
"""

import os
import sys
import subprocess
from pathlib import Path

def find_python_installations():
    """Find all Python installations in the system"""
    print("=== Finding Python Installations ===")
    
    # Common locations for Python installations
    common_paths = [
        "/usr/bin",
        "/usr/local/bin",
        "/opt/python",
        "/opt/anaconda3/bin",
        "/home/cdsw/.local/bin",
        "/usr/bin/python3*",
        "/usr/local/bin/python3*"
    ]
    
    python_versions = {}
    
    # Check for python3.6 and python3.12 specifically
    for version in ["3.6", "3.12"]:
        try:
            # Try direct command
            result = subprocess.run([f"python{version}", "--version"], 
                                  capture_output=True, text=True, check=True)
            python_versions[version] = {
                "command": f"python{version}",
                "version": result.stdout.strip(),
                "location": subprocess.run(["which", f"python{version}"], 
                                         capture_output=True, text=True, check=True).stdout.strip()
            }
            print(f"✓ Found Python {version}: {python_versions[version]['location']}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"⚠ Python {version} not found in PATH")
    
    # Also check general python3
    try:
        result = subprocess.run(["python3", "--version"], 
                              capture_output=True, text=True, check=True)
        python_versions["default"] = {
            "command": "python3",
            "version": result.stdout.strip(),
            "location": subprocess.run(["which", "python3"], 
                                     capture_output=True, text=True, check=True).stdout.strip()
        }
        print(f"✓ Found default python3: {python_versions['default']['location']}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠ Default python3 not found in PATH")
    
    return python_versions

def switch_to_python312_method1():
    """Method 1: Direct PATH manipulation"""
    print("=== Switching to Python 3.12 (Method 1: PATH Manipulation) ===")
    
    # First, find where python3.12 is located
    try:
        result = subprocess.run(["which", "python3.12"], 
                              capture_output=True, text=True, check=True)
        python312_path = result.stdout.strip()
        print(f"Found python3.12 at: {python312_path}")
        
        # Get the directory containing python3.12
        python312_dir = os.path.dirname(python312_path)
        print(f"Python 3.12 directory: {python312_dir}")
        
        # Update PATH to prioritize this directory
        current_path = os.environ.get('PATH', '')
        new_path = python312_dir + ":" + current_path
        os.environ['PATH'] = new_path
        
        print("✓ Updated PATH to prioritize Python 3.12")
        print(f"New PATH: {os.environ['PATH'][:100]}...")  # Show first 100 chars
        
        # Update sys.executable
        sys.executable = python312_path
        print(f"✓ Set sys.executable to: {sys.executable}")
        
        # Verify the switch
        verify_current_python()
        return True
        
    except subprocess.CalledProcessError:
        print("✗ Could not find python3.12 executable")
        return False

def switch_to_python312_method2():
    """Method 2: Using update-alternatives or direct symlink manipulation"""
    print("=== Switching to Python 3.12 (Method 2: Symlink Manipulation) ===")
    
    try:
        # Check if we can use update-alternatives
        result = subprocess.run(["which", "update-alternatives"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("update-alternatives is available")
            # This would require sudo, which might not be available in CDSW
            print("Note: This method typically requires sudo privileges")
        else:
            print("update-alternatives not available")
        
        # Find python3.12 location
        result = subprocess.run(["which", "python3.12"], 
                              capture_output=True, text=True, check=True)
        python312_path = result.stdout.strip()
        
        # Find python3 location
        result = subprocess.run(["which", "python3"], 
                              capture_output=True, text=True, check=True)
        python3_path = result.stdout.strip()
        
        print(f"Current python3: {python3_path}")
        print(f"Target python3.12: {python312_path}")
        
        # For CDSW, we'll create a local symlink in a user-writable directory
        local_bin = os.path.expanduser("~/local/bin")
        os.makedirs(local_bin, exist_ok=True)
        
        # Create symlink for python3 pointing to python3.12
        local_python3 = os.path.join(local_bin, "python3")
        if os.path.exists(local_python3):
            os.remove(local_python3)
        
        os.symlink(python312_path, local_python3)
        print(f"✓ Created symlink: {local_python3} -> {python312_path}")
        
        # Update PATH to prioritize our local bin
        current_path = os.environ.get('PATH', '')
        new_path = local_bin + ":" + current_path
        os.environ['PATH'] = new_path
        
        print("✓ Updated PATH to prioritize local Python 3.12")
        print(f"New PATH: {os.environ['PATH'][:100]}...")  # Show first 100 chars
        
        # Update sys.executable
        sys.executable = local_python3
        print(f"✓ Set sys.executable to: {sys.executable}")
        
        # Verify the switch
        verify_current_python()
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error in method 2: {e}")
        return False

def switch_to_python312_method3():
    """Method 3: Environment variable approach"""
    print("=== Switching to Python 3.12 (Method 3: Environment Variables) ===")
    
    try:
        # Find python3.12 location
        result = subprocess.run(["which", "python3.12"], 
                              capture_output=True, text=True, check=True)
        python312_path = result.stdout.strip()
        python312_dir = os.path.dirname(python312_path)
        
        # Set environment variables
        os.environ['PY_PYTHON'] = '3.12'
        os.environ['PYTHON_VERSION'] = '3.12'
        
        # Update PATH
        current_path = os.environ.get('PATH', '')
        new_path = python312_dir + ":" + current_path
        os.environ['PATH'] = new_path
        
        # Update sys.executable
        sys.executable = python312_path
        
        print(f"✓ Set PY_PYTHON=3.12")
        print(f"✓ Set PYTHON_VERSION=3.12")
        print(f"✓ Updated PATH and sys.executable to Python 3.12")
        
        # Verify the switch
        verify_current_python()
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error finding python3.12: {e}")
        return False

def verify_current_python():
    """Verify which Python version is currently active"""
    print("=== Verifying Current Python Version ===")
    
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    
    # Check if we can import Python 3.12 specific modules
    try:
        import zoneinfo  # Available in Python 3.9+
        print("✓ zoneinfo module available (Python 3.9+ feature)")
        zoneinfo_available = True
    except ImportError:
        print("✗ zoneinfo module not available (likely Python 3.6 or older)")
        zoneinfo_available = False
    
    # Check version directly
    version_info = sys.version_info
    print(f"Python version info: {version_info.major}.{version_info.minor}.{version_info.micro}")
    
    if version_info.major >= 3 and version_info.minor >= 12:
        print("✓ Currently using Python 3.12 or higher")
        return True
    elif version_info.major >= 3 and version_info.minor >= 9:
        print("⚠ Using Python 3.9-3.11 (not 3.12)")
        return False
    else:
        print("✗ Using Python 3.8 or older (likely 3.6)")
        return False

def create_persistent_switch_script():
    """Create a script that can be sourced to persistently switch Python versions"""
    print("=== Creating Persistent Switch Script ===")
    
    script_content = """#!/bin/bash
# CDSW Python 3.12 Switch Script
# Source this script to switch to Python 3.12: source ~/switch_to_python312.sh

# Find python3.12
PYTHON312_PATH=$(which python3.12 2>/dev/null)

if [ -z "$PYTHON312_PATH" ]; then
    echo "Error: python3.12 not found in PATH"
    return 1
fi

# Get the directory containing python3.12
PYTHON312_DIR=$(dirname "$PYTHON312_PATH")

# Update PATH to prioritize Python 3.12
export PATH="$PYTHON312_DIR:$PATH"

# Set Python version environment variables
export PY_PYTHON=3.12
export PYTHON_VERSION=3.12

# Verify the switch
echo "Switched to Python 3.12"
echo "Python executable: $(which python3)"
echo "Python version: $(python3 --version 2>&1)"
"""

    script_path = os.path.expanduser("~/switch_to_python312.sh")
    
    try:
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make it executable
        os.chmod(script_path, 0o755)
        
        print(f"✓ Created switch script at: {script_path}")
        print("To use it, run: source ~/switch_to_python312.sh")
        return script_path
    except Exception as e:
        print(f"✗ Error creating switch script: {e}")
        return None

def create_python312_alias():
    """Create aliases for Python 3.12"""
    print("=== Creating Python 3.12 Aliases ===")
    
    bashrc_content = """
# Python 3.12 aliases
alias python312='python3.12'
alias pip312='python3.12 -m pip'
alias python='/usr/bin/python3.12'
"""

    bashrc_path = os.path.expanduser("~/.bashrc_cdsw_python312")
    
    try:
        with open(bashrc_path, 'w') as f:
            f.write(bashrc_content)
        
        print(f"✓ Created alias file at: {bashrc_path}")
        print("To use it, run: source ~/.bashrc_cdsw_python312")
        return bashrc_path
    except Exception as e:
        print(f"✗ Error creating alias file: {e}")
        return None

def main():
    """Main function to orchestrate the Python switching process"""
    print("CDSW Python Version Switcher")
    print("=" * 40)
    print("This script helps you switch to Python 3.12 in CDSW")
    print()
    
    # 1. Find Python installations
    python_installs = find_python_installations()
    print()
    
    # 2. Try different switching methods
    print("Attempting to switch to Python 3.12...")
    print()
    
    # Try Method 1 first (most likely to work in CDSW)
    if switch_to_python312_method1():
        print("\n✓ Successfully switched to Python 3.12 using Method 1!")
    else:
        print("\n⚠ Method 1 failed, trying Method 2...")
        if switch_to_python312_method2():
            print("\n✓ Successfully switched to Python 3.12 using Method 2!")
        else:
            print("\n⚠ Method 2 failed, trying Method 3...")
            if switch_to_python312_method3():
                print("\n✓ Successfully switched to Python 3.12 using Method 3!")
            else:
                print("\n✗ All switching methods failed!")
    
    print("\n" + "=" * 40)
    
    # 3. Create persistent switching mechanisms
    create_persistent_switch_script()
    create_python312_alias()
    
    print("\n" + "=" * 40)
    print("Usage instructions:")
    print("1. Run this script in your CDSW session")
    print("2. To make the switch persistent, add this to your CDSW session startup:")
    print("   source ~/switch_to_python312.sh")
    print("3. Or add this to your project's environment variables:")
    print("   source ~/.bashrc_cdsw_python312")
    print("\nVerification commands:")
    print("python3 --version")
    print("python3 -c 'import sys; print(sys.version)'")
    print("python3 -c 'import zoneinfo; print(\"zoneinfo available\")'")

if __name__ == "__main__":
    main()
