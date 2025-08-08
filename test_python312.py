#!/usr/bin/env python3
"""
Test Script to Verify Python 3.12 Switch
========================================

Run this script to verify that you're using Python 3.12 in your CDSW environment.

Usage:
    python3 test_python312.py
"""

import sys
import os

def test_python_version():
    """Test and display Python version information"""
    print("=" * 50)
    print("Python 3.12 Verification Script")
    print("=" * 50)
    
    # Display Python version
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    
    # Check version info
    version_info = sys.version_info
    print(f"Version Info: {version_info.major}.{version_info.minor}.{version_info.micro}")
    
    # Verify it's Python 3.12
    if version_info.major == 3 and version_info.minor == 12:
        print("✅ SUCCESS: You are using Python 3.12!")
        return True
    elif version_info.major == 3 and version_info.minor > 12:
        print(f"✅ SUCCESS: You are using Python {version_info.major}.{version_info.minor} (newer than 3.12)!")
        return True
    else:
        print(f"❌ ISSUE: You are using Python {version_info.major}.{version_info.minor} (not 3.12)!")
        return False

def test_python312_features():
    """Test Python 3.12 specific features"""
    print("\n" + "=" * 50)
    print("Testing Python 3.12 Features")
    print("=" * 50)
    
    # Test 1: zoneinfo module (available since Python 3.9)
    try:
        import zoneinfo
        print("✅ zoneinfo module: Available (Python 3.9+ feature)")
        zoneinfo_available = True
    except ImportError:
        print("❌ zoneinfo module: Not available (likely Python 3.6 or older)")
        zoneinfo_available = False
    
    # Test 2: fcntl module (should be available in all Python 3.x)
    try:
        import fcntl
        print("✅ fcntl module: Available")
    except ImportError:
        print("❌ fcntl module: Not available")
    
    # Test 3: tomllib module (added in Python 3.11)
    try:
        import tomllib
        print("✅ tomllib module: Available (Python 3.11+ feature)")
    except ImportError:
        print("❌ tomllib module: Not available (Python < 3.11)")
    
    # Test 4: Exception groups (added in Python 3.11)
    try:
        # This is a simple test for exception groups
        exc_group = ExceptionGroup("test", [ValueError("test")])
        print("✅ Exception groups: Supported (Python 3.11+ feature)")
    except NameError:
        print("❌ Exception groups: Not supported (Python < 3.11)")
    
    return zoneinfo_available

def test_path_and_environment():
    """Test PATH and environment variables"""
    print("\n" + "=" * 50)
    print("Environment Information")
    print("=" * 50)
    
    # Display PATH
    path = os.environ.get('PATH', '')
    print(f"PATH (first 200 chars): {path[:200]}{'...' if len(path) > 200 else ''}")
    
    # Check for Python 3.12 in PATH
    path_entries = path.split(':')
    python312_in_path = any('3.12' in entry or 'python3.12' in entry for entry in path_entries)
    if python312_in_path:
        print("✅ Python 3.12 appears in PATH")
    else:
        print("⚠ Python 3.12 not obviously in PATH")
    
    # Check VIRTUAL_ENV
    virtual_env = os.environ.get('VIRTUAL_ENV', 'Not set')
    print(f"VIRTUAL_ENV: {virtual_env}")
    
    # Check PY_PYTHON
    py_python = os.environ.get('PY_PYTHON', 'Not set')
    print(f"PY_PYTHON: {py_python}")

def test_package_installation():
    """Test if we can install packages with pip"""
    print("\n" + "=" * 50)
    print("Package Installation Test")
    print("=" * 50)
    
    try:
        import subprocess
        import tempfile
        
        # Try to install a simple package
        result = subprocess.run([sys.executable, "-m", "pip", "install", "--dry-run", "requests"],
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ pip is working correctly")
        else:
            print(f"⚠ pip may have issues: {result.stderr[:100]}...")
            
    except Exception as e:
        print(f"❌ Error testing pip: {e}")

def main():
    """Main function"""
    print("Testing Python 3.12 Setup in CDSW")
    print()
    
    # Test 1: Version verification
    version_success = test_python_version()
    
    # Test 2: Feature testing
    features_available = test_python312_features()
    
    # Test 3: Environment
    test_path_and_environment()
    
    # Test 4: Package installation
    test_package_installation()
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    if version_success and features_available:
        print("🎉 SUCCESS: You have successfully switched to Python 3.12!")
        print("   You can now use Python 3.12 features and install packages.")
    elif version_success:
        print("✅ Python 3.12 is active, but some features may not be available.")
        print("   This might be due to environment configuration.")
    else:
        print("❌ Python 3.12 is not active.")
        print("   Please run 'source switch_to_python312.sh' to switch versions.")
        print("   Or check if Python 3.12 is properly installed.")

if __name__ == "__main__":
    main()
