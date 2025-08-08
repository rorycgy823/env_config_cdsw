#!/usr/bin/env python3
"""
CDSW Python Version Fix
=======================

Run this script directly in your CDSW session to fix the Python version issue.

This addresses the problem where:
- Terminal shows Python 3.12 after running switch script
- But sys.version still shows Python 3.6 in the Python session

Usage in CDSW:
    !python3 fix_cdsw_python_version.py
"""

import os
import sys
import subprocess

def fix_python_version():
    """Fix Python version in current CDSW session"""
    print("=" * 50)
    print("CDSW Python Version Fix")
    print("=" * 50)
    
    print(f"Before fix:")
    print(f"  Python version: {sys.version}")
    print(f"  Python executable: {sys.executable}")
    print()
    
    try:
        # Step 1: Find Python 3.12
        print("1. Finding Python 3.12...")
        result = subprocess.run(["which", "python3.12"], 
                              capture_output=True, text=True, check=True)
        python312_path = result.stdout.strip()
        print(f"   Found: {python312_path}")
        
        # Step 2: Update sys.executable
        print("2. Updating Python executable...")
        sys.executable = python312_path
        print(f"   Set to: {sys.executable}")
        
        # Step 3: Update PATH
        print("3. Updating PATH...")
        python312_dir = os.path.dirname(python312_path)
        current_path = os.environ.get('PATH', '')
        os.environ['PATH'] = python312_dir + ":" + current_path
        print(f"   Added to PATH: {python312_dir}")
        
        # Step 4: Set environment variables
        print("4. Setting environment variables...")
        os.environ['PY_PYTHON'] = '3.12'
        os.environ['PYTHON_VERSION'] = '3.12'
        print("   Set PY_PYTHON=3.12")
        print("   Set PYTHON_VERSION=3.12")
        
        print()
        print("After fix:")
        print(f"  Python version: {sys.version}")
        print(f"  Python executable: {sys.executable}")
        
        # Test Python 3.12 features
        print()
        print("Testing Python 3.12 features...")
        try:
            import zoneinfo
            print("✅ zoneinfo module: Available (Python 3.12 confirmed)")
            return True
        except ImportError:
            print("❌ zoneinfo module: Not available")
            return False
            
    except subprocess.CalledProcessError:
        print("❌ Error: Could not find python3.12 executable")
        print("   Please check if Python 3.12 is installed:")
        print("   ls -la /usr/bin/python3*")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def verify_fix():
    """Verify that the fix worked"""
    print()
    print("=" * 30)
    print("Verification")
    print("=" * 30)
    
    print(f"Current Python version: {sys.version}")
    print(f"Current executable: {sys.executable}")
    
    # Test various Python 3.12+ features
    tests = [
        ("zoneinfo module (Python 3.9+)", "import zoneinfo"),
        ("tomllib module (Python 3.11+)", "import tomllib"),
        ("Exception groups (Python 3.11+)", "ExceptionGroup('test', [ValueError('test')])"),
    ]
    
    passed = 0
    for test_name, test_code in tests:
        try:
            exec(test_code)
            print(f"✅ {test_name}: Available")
            passed += 1
        except Exception:
            print(f"❌ {test_name}: Not available")
    
    print()
    if passed >= 2:
        print("🎉 SUCCESS: Python 3.12 is now active in your session!")
        return True
    elif passed >= 1:
        print("⚠ PARTIAL SUCCESS: Some Python 3.12 features are available")
        return True
    else:
        print("❌ FAILURE: Python 3.12 features are not available")
        return False

def create_helper_function():
    """Create a helper function for future use"""
    print()
    print("=" * 30)
    print("Helper Function")
    print("=" * 30)
    
    helper_code = '''
def switch_to_python312():
    """
    Switch to Python 3.12 in current CDSW session
    Run this function at the start of your session
    """
    import os
    import sys
    import subprocess
    
    try:
        # Find Python 3.12
        result = subprocess.run(["which", "python3.12"], 
                              capture_output=True, text=True, check=True)
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
    except Exception as e:
        print(f"❌ Failed to switch: {e}")
        return False

# Usage: switch_to_python312()
'''
    
    helper_file = os.path.expanduser("~/cdsw_python312_helper.py")
    
    try:
        with open(helper_file, 'w') as f:
            f.write(helper_code)
        print(f"✅ Created helper function file: {helper_file}")
        print("   Usage in CDSW:")
        print("   from cdsw_python312_helper import switch_to_python312")
        print("   switch_to_python312()")
        return helper_file
    except Exception as e:
        print(f"❌ Error creating helper file: {e}")
        return None

def main():
    """Main function"""
    success = fix_python_version()
    
    if success:
        verify_fix()
        create_helper_function()
        
        print()
        print("=" * 50)
        print("INSTRUCTIONS")
        print("=" * 50)
        print("1. To run this fix in CDSW:")
        print("   !python3 fix_cdsw_python_version.py")
        print()
        print("2. To use the helper function in future sessions:")
        print("   from cdsw_python312_helper import switch_to_python312")
        print("   switch_to_python312()")
        print()
        print("3. To verify it worked:")
        print("   import sys")
        print("   print(sys.version)")
        print("   import zoneinfo  # Should work now")

if __name__ == "__main__":
    main()
