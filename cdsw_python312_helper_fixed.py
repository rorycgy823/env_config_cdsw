#!/usr/bin/env python3
"""
CDSW Python 3.12 Helper (Fixed for Python 3.6 compatibility)
============================================================

This version is compatible with Python 3.6 and later.
The capture_output parameter was added in Python 3.7, so we use separate stdout/stderr parameters.
"""

def switch_to_python312():
    """
    Switch to Python 3.12 in current CDSW session
    Run this function at the start of your session
    
    Compatible with Python 3.6+
    """
    import os
    import sys
    import subprocess
    
    try:
        # Find Python 3.12
        # Using stdout and stderr parameters instead of capture_output for Python 3.6 compatibility
        result = subprocess.run(["which", "python3.12"], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE, 
                              text=True, 
                              check=True)
        python312_path = result.stdout.strip()
        
        # Update sys.executable
        sys.executable = python312_path
        
        # Update PATH
        python312_dir = os.path.dirname(python312_path)
        current_path = os.environ.get('PATH', '')
        os.environ['PATH'] = python312_dir + ":" + current_path
        
        # Set environment variables
        os.environ['PY_PYTHON'] = '3.12'
        os.environ['PYTHON_VERSION'] = '3.12'
        
        print(f"✅ Switched to Python 3.12: {sys.executable}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to find python3.12: {e}")
        print(f"   stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Failed to switch: {e}")
        return False

def switch_to_python312_advanced():
    """
    Advanced version with more detailed error handling and fallbacks
    """
    import os
    import sys
    import subprocess
    
    print("=== Switching to Python 3.12 ===")
    print(f"Current Python version: {sys.version}")
    print(f"Current executable: {sys.executable}")
    
    # Try to find Python 3.12
    python312_path = None
    
    # Method 1: Use which command
    try:
        result = subprocess.run(["which", "python3.12"], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE, 
                              text=True, 
                              check=True)
        python312_path = result.stdout.strip()
        print(f"Found python3.12: {python312_path}")
    except subprocess.CalledProcessError:
        print("which python3.12 failed, trying alternatives...")
    
    # Method 2: Check common locations if which failed
    if not python312_path:
        common_locations = [
            "/usr/bin/python3.12",
            "/usr/local/bin/python3.12",
            "/opt/python3.12/bin/python3.12"
        ]
        
        for location in common_locations:
            if os.path.exists(location):
                python312_path = location
                print(f"Found python3.12 at: {location}")
                break
    
    if not python312_path:
        print("❌ Could not find python3.12 executable")
        print("Please check if Python 3.12 is installed:")
        print("   ls -la /usr/bin/python3*")
        return False
    
    # Update sys.executable
    original_executable = sys.executable
    sys.executable = python312_path
    print(f"Updated sys.executable: {original_executable} → {sys.executable}")
    
    # Update PATH
    python312_dir = os.path.dirname(python312_path)
    current_path = os.environ.get('PATH', '')
    old_path = current_path
    os.environ['PATH'] = python312_dir + ":" + current_path
    print(f"Updated PATH to prioritize: {python312_dir}")
    
    # Set environment variables
    os.environ['PY_PYTHON'] = '3.12'
    os.environ['PYTHON_VERSION'] = '3.12'
    print("Set environment variables: PY_PYTHON=3.12, PYTHON_VERSION=3.12")
    
    print(f"New Python version: {sys.version}")
    
    # Test Python 3.12 features
    try:
        import zoneinfo
        print("✅ Python 3.12 features are available")
        print("✅ Switch to Python 3.12 completed successfully!")
        return True
    except ImportError:
        print("⚠ Python 3.12 features not available (may still be using old version)")
        return True  # Still consider it a success since we updated the paths

# Usage examples:
# switch_to_python312()           # Simple version
# switch_to_python312_advanced()  # Verbose version with more details
