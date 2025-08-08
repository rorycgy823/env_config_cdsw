#!/bin/bash

# =================================================================
# CDSW Project Build Script to Set Default Python to 3.12
# =================================================================
# This script runs when the project environment is built.
# It configures the environment to use Python 3.12 as the default
# for all sessions, jobs, and applications within this project.
# =================================================================

set -e # Exit immediately if a command exits with a non-zero status.

echo "--- Starting Python 3.12 Configuration ---"

# --- Step 1: Verify that Python 3.12 is available ---
echo "Verifying python3.12 installation..."
if ! command -v python3.12 &> /dev/null; then
    echo "ERROR: python3.12 could not be found in the environment."
    echo "Please ensure the selected Runtime Engine has Python 3.12 installed."
    exit 1
fi
echo "Python 3.12 found at $(which python3.12)"


# --- Step 2: Use update-alternatives to set the default python3 ---
# This is the standard and safest way to manage multiple versions.
# It changes the /usr/bin/python3 symlink in a controlled manner.
# We give python3.12 a higher priority (e.g., 100) than the existing
# python3.6 (which we can assume has a lower priority).
echo "Configuring 'python3' to point to python3.12 using update-alternatives..."
# The command needs to be run with sudo, which is allowed in build scripts.
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 100
echo "'python3' default has been set."


# --- Step 3: Set the default pip3 to point to the Python 3.12 version ---
echo "Configuring 'pip3' to point to the Python 3.12 version..."
# We will create a symlink for pip3 in a high-priority PATH location.
# /usr/local/bin is typically checked before /usr/bin.
sudo ln -sf /usr/bin/pip3.12 /usr/local/bin/pip3
# If pip3.12 doesn't exist, we can install it.
if ! command -v /usr/bin/pip3.12 &> /dev/null; then
    echo "pip3.12 not found, installing it for Python 3.12..."
    sudo python3.12 -m ensurepip --upgrade
    sudo python3.12 -m pip install --upgrade pip
    sudo ln -sf /usr/local/bin/pip /usr/local/bin/pip3
fi
echo "'pip3' default has been set."


# --- Step 4: Install common packages for Python 3.12 ---
# This ensures that essential packages are available in the new default environment.
echo "Installing essential packages for Python 3.12..."
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install numpy pandas scikit-learn matplotlib seaborn jupyter ipykernel


# --- Step 5: Verification ---
echo "--- Verification Step ---"
echo "Verifying the new default Python version..."
# The 'which' command should now point to the python3.12 executable.
which python3
# The version command should report 3.12.
python3 --version

echo "Verifying the new default pip version..."
which pip3
pip3 --version

echo "--- Python 3.12 Configuration Complete ---"
echo "All new sessions in this project will now use Python 3.12 by default."
