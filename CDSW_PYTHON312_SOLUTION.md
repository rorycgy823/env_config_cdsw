# CDSW Python 3.12 Solution

## Problem
You have both Python 3.6 and 3.12 installed in your CDSW environment, but:
- Running the switch script updates the terminal to show Python 3.12
- But `sys.version` in your Python session still shows Python 3.6

## Root Cause
In CDSW, the shell environment and Python session environment are separate:
- Shell scripts update the terminal environment
- Python sessions use a specific kernel that may not respect shell PATH changes

## Solution

### Method 1: Run the Fix Script (Recommended)
Run this command directly in your CDSW session:

```bash
!python3 fix_cdsw_python_version.py
```

This will:
1. Find your Python 3.12 installation
2. Update your Python session to use Python 3.12
3. Verify the fix worked
4. Create a helper function for future use

### Method 2: Manual Fix in Python Session
Run this code in a CDSW Python cell:

```python
import os
import sys
import subprocess

# Find Python 3.12 (compatible with Python 3.6)
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

print(f"Switched to Python 3.12: {sys.executable}")

# Verify
import sys
print(f"Python version: {sys.version}")
```

### Method 3: Using the Helper Function
After running the fix script once, you can use the helper function:

```python
from cdsw_python312_helper import switch_to_python312
switch_to_python312()
```

### Method 4: Direct Copy-Paste Solution
If you're still having import issues, you can directly copy and paste this function into your CDSW session:

```python
def switch_to_python312():
    """
    Switch to Python 3.12 in current CDSW session
    Compatible with Python 3.6+
    """
    import os
    import sys
    import subprocess
    
    try:
        # Find Python 3.12 (compatible with Python 3.6)
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
        return False
    except Exception as e:
        print(f"❌ Failed to switch: {e}")
        return False

# Usage: switch_to_python312()
```

## Verification
After applying the fix, verify it worked:

```python
import sys
print(sys.version)

# Test Python 3.12 features
import zoneinfo
print("Python 3.12 is active!")
```

## Making It Persistent
To automatically apply this fix in every session:

1. In CDSW, go to your project settings
2. Under "Environment Variables" or "Session Properties"
3. Add this to your startup scripts:
   ```bash
   python3 /path/to/fix_cdsw_python_version.py
   ```

## Files Created
- `fix_cdsw_python_version.py` - Main fix script
- `cdsw_python312_helper.py` - Helper function (created by fix script)
- `switch_to_python312.sh` - Shell script for terminal use
- `test_python312.py` - Verification script

## Troubleshooting
If you still have issues:

1. Check if Python 3.12 is actually installed:
   ```bash
   ls -la /usr/bin/python3*
   ```

2. If Python 3.12 is not found, run:
   ```bash
   python3 cdsw_python312_installer.py
   ```

3. For permission issues, contact your CDSW administrator

## Contact
If problems persist, run the diagnostic script:
```bash
python3 cdsw_python_switcher.py --verbose
