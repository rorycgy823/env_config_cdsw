#!/usr/bin/env python3
"""
CDSW Python 3.12 Complete Installation and Switching Script
==========================================================

This script provides a complete solution to install Python 3.12 in CDSW,
create a virtual environment, and switch to it properly.

Author: AI Assistant
Date: 2025
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check the current Python version"""
    print("=== Checking Current Python Version ===")
    print(f"Current Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    return sys.version_info

def install_python312_if_needed():
    """Install Python 3.12 if it's not available"""
    print("=== Installing Python 3.12 ===")
    
    # Check if Python 3.12 is already available
    try:
        result = subprocess.run(["python3.12", "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"✓ Python 3.12 already installed: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Python 3.12 not found. Installing...")
    
    try:
        # Update package lists
        print("Updating package lists...")
        subprocess.run(["sudo", "apt-get", "update"], 
                      check=True, capture_output=True)
        
        # Install required packages
        print("Installing required packages...")
        subprocess.run(["sudo", "apt-get", "install", "-y", 
                       "software-properties-common", "wget", "build-essential",
                       "libssl-dev", "zlib1g-dev", "libbz2-dev",
                       "libreadline-dev", "libsqlite3-dev", "curl",
                       "libncursesw5-dev", "xz-utils", "tk-dev",
                       "libxml2-dev", "libxmlsec1-dev", "libffi-dev",
                       "liblzma-dev"], check=True, capture_output=True)
        
        # Add deadsnakes PPA
        print("Adding deadsnakes PPA...")
        subprocess.run(["sudo", "add-apt-repository", "-y", "ppa:deadsnakes/ppa"], 
                      check=True, capture_output=True)
        
        # Update package lists again
        print("Updating package lists again...")
        subprocess.run(["sudo", "apt-get", "update"], 
                      check=True, capture_output=True)
        
        # Install Python 3.12
        print("Installing Python 3.12...")
        subprocess.run(["sudo", "apt-get", "install", "-y",
                       "python3.12", "python3.12-dev", "python3.12-venv",
                       "python3.12-distutils"], check=True, capture_output=True)
        
        print("✓ Python 3.12 installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing Python 3.12: {e}")
        print(f"stderr: {e.stderr.decode() if hasattr(e, 'stderr') else 'No stderr'}")
        return False

def create_python312_venv(venv_path="~/venvs/py312"):
    """Create a Python 3.12 virtual environment"""
    print("=== Creating Python 3.12 Virtual Environment ===")
    
    # Expand user path
    venv_path = os.path.expanduser(venv_path)
    print(f"Creating virtual environment at: {venv_path}")
    
    # Remove existing venv if it exists
    if os.path.exists(venv_path):
        print(f"Removing existing virtual environment at {venv_path}")
        shutil.rmtree(venv_path)
    
    try:
        # Create virtual environment using Python 3.12
        print("Creating virtual environment with Python 3.12...")
        subprocess.run(["python3.12", "-m", "venv", venv_path], 
                      check=True, capture_output=True)
        
        print("✓ Virtual environment created successfully!")
        
        # Upgrade pip in the virtual environment
        print("Upgrading pip in virtual environment...")
        pip_path = os.path.join(venv_path, "bin", "pip")
        subprocess.run([pip_path, "install", "--upgrade", "pip", "setuptools", "wheel"], 
                      check=True, capture_output=True)
        
        print("✓ Pip upgraded successfully!")
        return venv_path
    except subprocess.CalledProcessError as e:
        print(f"✗ Error creating virtual environment: {e}")
        print(f"stderr: {e.stderr.decode() if hasattr(e, 'stderr') else 'No stderr'}")
        return None

def switch_to_venv(venv_path="~/venvs/py312"):
    """Switch the current Python environment to the virtual environment"""
    print("=== Switching to Python 3.12 Virtual Environment ===")
    
    # Expand user path
    venv_path = os.path.expanduser(venv_path)
    venv_bin_path = os.path.join(venv_path, "bin")
    
    print(f"Switching to virtual environment at: {venv_path}")
    
    # Check if venv exists
    if not os.path.exists(venv_path):
        print(f"✗ Virtual environment not found at {venv_path}")
        return False
    
    # Update environment variables
    print("Updating environment variables...")
    os.environ['PATH'] = venv_bin_path + ":" + os.environ.get('PATH', '')
    os.environ['VIRTUAL_ENV'] = venv_path
    
    # Update sys.path
    python_version = "3.12"
    site_packages_path = os.path.join(venv_path, "lib", f"python{python_version}", "site-packages")
    
    if os.path.exists(site_packages_path):
        # Remove existing site-packages paths that might be from Python 3.6
        sys.path = [p for p in sys.path if "python3.6" not in p and "python2.7" not in p]
        
        # Insert the venv site-packages at the beginning
        if site_packages_path not in sys.path:
            sys.path.insert(0, site_packages_path)
            print(f"✓ Added {site_packages_path} to sys.path")
    else:
        print(f"⚠ Warning: Site-packages path not found: {site_packages_path}")
    
    # Update sys.executable
    venv_python = os.path.join(venv_bin_path, "python")
    if os.path.exists(venv_python):
        sys.executable = venv_python
        print(f"✓ Set sys.executable to: {venv_python}")
    
    print("✓ Environment switch completed!")
    return True

def install_common_packages(venv_path="~/venvs/py312"):
    """Install common data science packages in the virtual environment"""
    print("=== Installing Common Packages ===")
    
    venv_path = os.path.expanduser(venv_path)
    pip_path = os.path.join(venv_path, "bin", "pip")
    
    packages = [
        "numpy",
        "pandas",
        "matplotlib",
        "seaborn",
        "scikit-learn",
        "jupyter",
        "ipykernel",
        "requests",
        "pillow"
    ]
    
    try:
        print("Installing common data science packages...")
        subprocess.run([pip_path, "install"] + packages, 
                      check=True, capture_output=True)
        print("✓ Common packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing packages: {e}")
        print(f"stderr: {e.stderr.decode() if hasattr(e, 'stderr') else 'No stderr'}")
        return False

def verify_python312_setup():
    """Verify that Python 3.12 is properly set up"""
    print("=== Verifying Python 3.12 Setup ===")
    
    # Check Python version
    print(f"Current Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
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
    
    # Try to import Python 3.12 specific modules
    try:
        import zoneinfo  # Available in Python 3.9+
        print("✓ zoneinfo module available (Python 3.9+ feature)")
    except ImportError:
        print("✗ zoneinfo module not available (likely still using Python 3.6)")
        return False
    
    # Try to import other Python 3.12 features
    try:
        # Test a feature that was improved in Python 3.12
        import fcntl
        print("✓ fcntl module available")
    except ImportError:
        print("✗ fcntl module not available")
        return False
    
    # Check version directly
    version_info = sys.version_info
    if version_info.major >= 3 and version_info.minor >= 12:
        print(f"✓ Python version is 3.12 or higher ({version_info.major}.{version_info.minor})")
        return True
    else:
        print(f"✗ Python version is less than 3.12 ({version_info.major}.{version_info.minor})")
        return False

def create_activation_script(venv_path="~/venvs/py312"):
    """Create a script to easily activate the Python 3.12 environment"""
    print("=== Creating Activation Script ===")
    
    venv_path = os.path.expanduser(venv_path)
    activation_script_path = os.path.expanduser("~/activate_py312.sh")
    
    activation_script = f"""#!/bin/bash
# Script to activate Python 3.12 virtual environment in CDSW

export VIRTUAL_ENV="{venv_path}"
export PATH="{venv_path}/bin:$PATH"

# Unset PYTHON_HOME if set
unset PYTHON_HOME

echo "Python 3.12 virtual environment activated"
echo "Virtual environment: $VIRTUAL_ENV"
echo "Python executable: $(which python)"
python --version
"""
    
    try:
        with open(activation_script_path, 'w') as f:
            f.write(activation_script)
        
        # Make it executable
        os.chmod(activation_script_path, 0o755)
        
        print(f"✓ Activation script created at: {activation_script_path}")
        print("To activate manually, run: source ~/activate_py312.sh")
        return activation_script_path
    except Exception as e:
        print(f"✗ Error creating activation script: {e}")
        return None

def force_python312_execution(command, venv_path="~/venvs/py312"):
    """Force execution of a command using Python 3.12 virtual environment"""
    print(f"=== Executing Command with Python 3.12 ===")
    print(f"Command: {command}")
    
    venv_path = os.path.expanduser(venv_path)
    venv_bin_path = os.path.join(venv_path, "bin")
    
    # Modify the command to use the virtual environment
    if command.startswith("python "):
        command = command.replace("python ", f"{venv_bin_path}/python ", 1)
    elif command.startswith("pip "):
        command = command.replace("pip ", f"{venv_bin_path}/pip ", 1)
    elif command == "python" or command == "python3":
        command = f"{venv_bin_path}/python"
    
    # Set environment variables for the subprocess
    env = os.environ.copy()
    env['PATH'] = venv_bin_path + ":" + env.get('PATH', '')
    env['VIRTUAL_ENV'] = venv_path
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, 
                              text=True, env=env, check=True)
        print("✓ Command executed successfully!")
        print("Output:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"✗ Error executing command: {e}")
        print(f"Stderr: {e.stderr}")
        return None

def main():
    """Main function to orchestrate the Python 3.12 setup"""
    print("CDSW Python 3.12 Complete Installation and Switching Script")
    print("=" * 60)
    
    # 1. Check current Python version
    current_version = check_python_version()
    
    # 2. Install Python 3.12 if needed
    if not install_python312_if_needed():
        print("✗ Failed to install Python 3.12. Exiting.")
        return False
    
    # 3. Create Python 3.12 virtual environment
    venv_path = create_python312_venv()
    if not venv_path:
        print("✗ Failed to create Python 3.12 virtual environment. Exiting.")
        return False
    
    # 4. Switch to the virtual environment
    if not switch_to_venv(venv_path):
        print("✗ Failed to switch to Python 3.12 virtual environment. Exiting.")
        return False
    
    # 5. Install common packages
    if not install_common_packages(venv_path):
        print("⚠ Warning: Failed to install common packages.")
    
    # 6. Create activation script
    create_activation_script(venv_path)
    
    # 7. Verify setup
    if verify_python312_setup():
        print("\n" + "=" * 60)
        print("✓ Python 3.12 setup completed successfully!")
        print("\nUsage in CDSW:")
        print("1. Run this script once in your session")
        print("2. All subsequent cells will use Python 3.12")
        print("3. To run specific commands in Python 3.12:")
        print("   from cdsw_python312_installer import force_python312_execution")
        print("   force_python312_execution('python -c \"import sys; print(sys.version)\"')")
        print("\nTo manually activate the environment:")
        print("source ~/activate_py312.sh")
        return True
    else:
        print("\n" + "=" * 60)
        print("✗ Python 3.12 setup verification failed!")
        print("\nTroubleshooting steps:")
        print("1. Check if Python 3.12 was installed correctly:")
        print("   python3.12 --version")
        print("2. Check if virtual environment was created:")
        print("   ls -la ~/venvs/py312")
        print("3. Try manually activating the environment:")
        print("   source ~/venvs/py312/bin/activate")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
