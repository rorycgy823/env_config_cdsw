#!/bin/bash

# =================================================================
# CDSW Session Setup Script for Python 3.12
# =================================================================
# This script is designed to be run at the start of every CDSW
# session to configure it for Python 3.12.
# It handles cases where project-level builds are not permitted.
# =================================================================

echo "--- Configuring Session for Python 3.12 ---"

# --- Step 1: Verify Python 3.12 is available ---
if ! command -v python3.12 &> /dev/null; then
    echo "ERROR: python3.12 is not installed in this environment. Cannot proceed."
    exit 1
fi
PYTHON312_EXECUTABLE=$(which python3.12)
echo "Found Python 3.12 at: $PYTHON312_EXECUTABLE"


# --- Step 2: Create a dedicated Python 3.12 Virtual Environment ---
# This is the most robust way to ensure a clean and isolated environment.
# We'll create it in the user's home directory to persist it between sessions.
VENV_DIR="$HOME/.py312-venv"
echo "Setting up Python 3.12 virtual environment in: $VENV_DIR"

if [ ! -f "$VENV_DIR/bin/python" ]; then
    echo "Virtual environment not found. Creating it now..."
    # Create the virtual environment using the python3.12 executable
    $PYTHON312_EXECUTABLE -m venv $VENV_DIR
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi


# --- Step 3: Activate the Virtual Environment for the current session ---
# Activating the venv is the most reliable way to switch the session's context.
echo "Activating the virtual environment for this session..."
# The 'source' command modifies the current shell's environment.
source $VENV_DIR/bin/activate


# --- Step 4: Install or Upgrade Essential Packages ---
# This ensures the virtual environment has the necessary tools.
echo "Upgrading pip and installing essential packages in the virtual environment..."
pip install --upgrade pip setuptools wheel
pip install numpy pandas scikit-learn matplotlib seaborn jupyter ipykernel


# --- Step 5: Verification ---
echo "--- Verification ---"
echo "The following commands should now report Python 3.12."

echo -n "which python3 -> "
which python3

echo -n "python3 --version -> "
python3 --version

echo -n "which pip3 -> "
which pip3

echo -n "pip3 --version -> "
pip3 --version | head -n 1

echo "------------------------------------------------"
echo "✅ SUCCESS: Your session is now running on Python 3.12."
echo "All subsequent commands in this session will use this environment."
echo "To make this permanent for all new sessions, add the following"
echo "line to your project's startup script in the settings:"
echo "source $HOME/workspace/setup_py312_session.sh"
echo "------------------------------------------------"
