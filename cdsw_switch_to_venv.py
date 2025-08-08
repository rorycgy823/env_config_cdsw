#!/usr/bin/env python3
"""
CDSW Python 3.12 Virtual Environment Switcher
============================================

This script provides direct methods to switch to and use your Python 3.12 
virtual environment within CDSW workbooks without kernel selection.

Author: AI Assistant
Date: 2025
"""

def switch_to_python312_venv():
    """
    Method 1: Programmatically switch to Python 3.12 virtual environment
    """
    print("=== Switching to Python 3.12 Virtual Environment ===")
    
    import sys
    import os
    
    # Define the path to your Python 3.12 virtual environment
    # Adjust this path to match your actual venv location
    venv_path = os.path.expanduser("~/venvs/py312")
    
    print(f"Attempting to switch to virtual environment at: {venv_path}")
    
    # Check if the virtual environment exists
    if not os.path.exists(venv_path):
        print("Virtual environment not found. Creating it now...")
        create_python312_venv()
        return
    
    # Update the PATH to use the virtual environment's Python
    venv_bin_path = os.path.join(venv_path, "bin")
    os.environ['PATH'] = venv_bin_path + ":" + os.environ.get('PATH', '')
    
    # Set VIRTUAL_ENV environment variable
    os.environ['VIRTUAL_ENV'] = venv_path
    
    # Update sys.path to include the virtual environment's site-packages
    python_version = "3.12"  # Adjust if needed
    site_packages_path = os.path.join(venv_path, "lib", f"python{python_version}", "site-packages")
    
    if os.path.exists(site_packages_path):
        # Remove existing site-packages paths that might be from Python 3.6
        sys.path = [p for p in sys.path if "python3.6" not in p]
        
        # Insert the venv site-packages at the beginning
        if site_packages_path not in sys.path:
            sys.path.insert(0, site_packages_path)
            print(f"Added {site_packages_path} to sys.path")
    else:
        print(f"Warning: Site-packages path not found: {site_packages_path}")
    
    # Update sys.executable to point to the venv Python
    venv_python = os.path.join(venv_bin_path, "python")
    if os.path.exists(venv_python):
        sys.executable = venv_python
        print(f"Set sys.executable to: {venv_python}")
    
    # Verify the switch
    print("\nVerification:")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"VIRTUAL_ENV: {os.environ.get('VIRTUAL_ENV', 'Not set')}")
    
    return True

def create_python312_venv():
    """
    Method 2: Create Python 3.12 virtual environment if it doesn't exist
    """
    print("=== Creating Python 3.12 Virtual Environment ===")
    
    import os
    import subprocess
    
    # Define paths
    venv_path = os.path.expanduser("~/venvs/py312")
    
    # Check if Python 3.12 is available
    try:
        result = subprocess.run(["python3.12", "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"Found Python 3.12: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Python 3.12 not found. Installing...")
        install_python312()
    
    # Create virtual environment
    print(f"Creating virtual environment at {venv_path}...")
    try:
        subprocess.run(["python3.12", "-m", "venv", venv_path], check=True)
        print("Virtual environment created successfully!")
        
        # Upgrade pip in the virtual environment
        pip_path = os.path.join(venv_path, "bin", "pip")
        subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
        print("Pip upgraded successfully!")
        
        return venv_path
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        return None

def install_python312():
    """
    Method 3: Install Python 3.12 if not available
    """
    print("=== Installing Python 3.12 ===")
    
    import subprocess
    
    try:
        # Update package lists
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        
        # Install required packages
        subprocess.run(["sudo", "apt-get", "install", "-y", 
                       "software-properties-common"], check=True)
        
        # Add deadsnakes PPA
        subprocess.run(["sudo", "add-apt-repository", "-y", "ppa:deadsnakes/ppa"], 
                      check=True)
        
        # Update package lists again
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        
        # Install Python 3.12
        subprocess.run(["sudo", "apt-get", "install", "-y",
                       "python3.12", "python3.12-dev", "python3.12-venv"], 
                      check=True)
        
        print("Python 3.12 installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing Python 3.12: {e}")
        return False

def execute_in_venv(command):
    """
    Method 4: Execute a command using the Python 3.12 virtual environment
    
    Usage:
    execute_in_venv("pip install pandas")
    execute_in_venv("python -c 'import sys; print(sys.version)'")
    """
    import subprocess
    import os
    
    venv_path = os.path.expanduser("~/venvs/py312")
    venv_bin_path = os.path.join(venv_path, "bin")
    
    # Modify the command to use the virtual environment
    if command.startswith("python"):
        command = command.replace("python", os.path.join(venv_bin_path, "python"), 1)
    elif command.startswith("pip"):
        command = command.replace("pip", os.path.join(venv_bin_path, "pip"), 1)
    
    # Set environment variables for the subprocess
    env = os.environ.copy()
    env['PATH'] = venv_bin_path + ":" + env.get('PATH', '')
    env['VIRTUAL_ENV'] = venv_path
    
    print(f"Executing in venv: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, 
                              text=True, env=env, check=True)
        print("Output:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Stderr: {e.stderr}")
        return None

def setup_ipython_magic():
    """
    Method 5: Set up IPython magic commands for easier venv management
    """
    print("=== Setting up IPython Magic Commands ===")
    
    try:
        # This would typically be used in a Jupyter notebook
        from IPython.core.magic import register_line_magic
        import os
        import sys
        
        @register_line_magic
        def venv(line):
            """Magic command to execute commands in the virtual environment"""
            return execute_in_venv(line)
        
        @register_line_magic
        def switch_venv(line):
            """Magic command to switch to the virtual environment"""
            switch_to_python312_venv()
            
        print("IPython magic commands registered:")
        print("  %venv <command>    - Execute command in venv")
        print("  %switch_venv       - Switch to Python 3.12 venv")
        return True
    except ImportError:
        print("IPython not available. Magic commands not registered.")
        return False

def verify_python312_setup():
    """
    Method 6: Comprehensive verification of Python 3.12 setup
    """
    print("=== Verifying Python 3.12 Setup ===")
    
    import sys
    import os
    import subprocess
    
    # Check current Python version
    print(f"Current Python version: {sys.version}")
    print(f"Current Python executable: {sys.executable}")
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print(f"In virtual environment: {in_venv}")
    if in_venv:
        print(f"Virtual environment: {sys.prefix}")
    
    # Check VIRTUAL_ENV environment variable
    venv_env = os.environ.get('VIRTUAL_ENV', 'Not set')
    print(f"VIRTUAL_ENV environment variable: {venv_env}")
    
    # Check PATH
    path_entries = os.environ.get('PATH', '').split(':')
    venv_paths = [p for p in path_entries if 'venv' in p or 'py312' in p]
    print(f"Virtual environment paths in PATH: {venv_paths}")
    
    # Try to import a Python 3.12 specific module
    try:
        import zoneinfo  # Available in Python 3.9+
        print("✓ zoneinfo module available (Python 3.9+ feature)")
    except ImportError:
        print("✗ zoneinfo module not available (likely still using Python 3.6)")
    
    # Try to import a Python 3.12 specific feature
    try:
        # Python 3.12 has some new features, but let's check version directly
        version_info = sys.version_info
        if version_info.major >= 3 and version_info.minor >= 12:
            print(f"✓ Python version is 3.12 or higher ({version_info.major}.{version_info.minor})")
        else:
            print(f"✗ Python version is less than 3.12 ({version_info.major}.{version_info.minor})")
    except Exception as e:
        print(f"Error checking Python version: {e}")

# Main execution function
def main():
    """
    Main function demonstrating all methods
    """
    print("CDSW Python 3.12 Virtual Environment Switcher")
    print("=" * 50)
    print("This script provides methods to use Python 3.12 in CDSW without kernel selection.")
    print()
    
    # Method 1: Switch to venv
    print("Method 1: Switch to Python 3.12 virtual environment")
    print("-" * 30)
    switch_to_python312_venv()
    
    print("\n" + "=" * 50 + "\n")
    
    # Method 2: Verify setup
    print("Method 2: Verify Python 3.12 setup")
    print("-" * 30)
    verify_python312_setup()
    
    print("\n" + "=" * 50)
    print("Usage in CDSW:")
    print("1. Run switch_to_python312_venv() in your first notebook cell")
    print("2. All subsequent cells will use Python 3.12")
    print("3. Use execute_in_venv('command') to run specific commands in the venv")

if __name__ == "__main__":
    main()
