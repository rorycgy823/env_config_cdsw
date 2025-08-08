# CDSW Python 3.12 Switching Guide

This guide provides instructions on how to switch to Python 3.12 in your CDSW environment when both Python 3.6 and 3.12 are available.

## Files Provided

1. `cdsw_python_switcher.py` - A Python script to automatically detect and switch Python versions
2. `switch_to_python312.sh` - A shell script to manually switch to Python 3.12
3. `cdsw_python312_installer.py` - A comprehensive installer (if needed)

## Method 1: Using the Shell Script (Recommended for CDSW Sessions)

This is the simplest and most reliable method for regular CDSW sessions.

### Steps:

1. **Make the script executable:**
   ```bash
   chmod +x switch_to_python312.sh
   ```

2. **Source the script to switch to Python 3.12:**
   ```bash
   source switch_to_python312.sh
   ```

3. **Verify the switch:**
   ```bash
   python3 --version
   python3 -c "import sys; print(sys.version)"
   python3 -c "import zoneinfo; print('zoneinfo module available')"
   ```

### What this does:
- Finds your Python 3.12 installation
- Updates your PATH to prioritize Python 3.12
- Sets environment variables to ensure Python 3.12 is used
- Creates convenient aliases (`python312`, `pip312`)

### To revert to original PATH:
```bash
export PATH=$ORIGINAL_PATH
```

## Method 2: Using the Python Script

If you prefer to use Python to manage the switch:

1. **Run the Python script:**
   ```bash
   python3 cdsw_python_switcher.py
   ```

2. **The script will:**
   - Automatically detect Python installations
   - Try different methods to switch to Python 3.12
   - Create persistent switching mechanisms

## Method 3: Manual Commands

If you prefer to run commands manually:

1. **Find Python 3.12:**
   ```bash
   which python3.12
   ```

2. **Get the directory:**
   ```bash
   dirname $(which python3.12)
   ```

3. **Update PATH:**
   ```bash
   export PATH="$(dirname $(which python3.12)):$PATH"
   ```

4. **Verify:**
   ```bash
   python3 --version
   ```

## Making the Switch Persistent

To make the Python 3.12 switch persistent across CDSW sessions:

1. **Add to your project's environment:**
   - In CDSW, go to your project settings
   - Under "Environment Variables", add a startup script that sources the switch script

2. **Or add to your .bashrc:**
   ```bash
   echo "source /path/to/switch_to_python312.sh" >> ~/.bashrc
   ```

## Verification Commands

After switching, use these commands to verify you're using Python 3.12:

```bash
# Check Python version
python3 --version

# Check full version info
python3 -c "import sys; print(sys.version)"

# Check if Python 3.9+ features are available
python3 -c "import zoneinfo; print('zoneinfo available')"

# Check which Python executable is being used
which python3

# Check pip version
python3 -m pip --version
```

## Troubleshooting

### If you get "python3.12: command not found":
1. Check if Python 3.12 is actually installed:
   ```bash
   ls -la /usr/bin/python3*
   ```

2. If not found, you may need to install it (use the `cdsw_python312_installer.py` script)

### If the switch doesn't persist:
1. Make sure you're sourcing the script (not just executing it):
   ```bash
   source switch_to_python312.sh  # Correct
   ./switch_to_python312.sh       # Incorrect
   ```

2. Add the source command to your CDSW session startup

### If you're still using Python 3.6:
1. Check your PATH:
   ```bash
   echo $PATH
   ```

2. Make sure the Python 3.12 directory comes first in PATH

## Additional Notes

- These scripts are designed specifically for CDSW environments
- They don't require sudo privileges
- They preserve your ability to switch back to Python 3.6 if needed
- The switch affects only your current session unless made persistent

## Support

If you continue to have issues:
1. Run the `cdsw_python_switcher.py` script with verbose output
2. Check the locations of your Python installations
3. Ensure you have read/execute permissions on the Python 3.12 executable
