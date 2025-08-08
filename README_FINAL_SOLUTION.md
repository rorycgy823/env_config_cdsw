# FINAL SOLUTION: Setting up Python 3.12 in CDSW Sessions

This guide provides the most reliable method for using Python 3.12 in your CDSW project, especially when you cannot build or modify the project's base Engine.

## The Problem
Your project's default Python version is 3.6, and you want to use 3.12 for all your work within the project's sessions. Since you cannot "Build" a new engine, the change must be applied every time a new session starts.

## The Solution: Automated Session Setup
We will use the `setup_py312_session.sh` script to automatically configure every new session for Python 3.12. This script creates a persistent virtual environment, ensuring your packages and configuration are saved between sessions.

---

### Step 1: Make the Script Executable
First, you only need to do this once. Open a CDSW terminal and run:
```bash
chmod +x setup_py312_session.sh
```

---

### Step 2: Add the Script to Your Project's Startup Settings
This is the most important step. It will make the Python 3.12 switch automatic for every new session.

1.  In the CDSW UI, go to your **Project Settings**.
2.  Look for a section named **"Session Startup Script"**, **"Environment Variables"**, or a similar "Startup" section.
3.  Add the following single line to the script/configuration box:

    ```bash
    source $HOME/workspace/setup_py312_session.sh
    ```
    *Note: `$HOME/workspace/` is the typical path to your project files in CDSW. If your project is in a different location, adjust the path accordingly.*

---

### Step 3: Stop and Start Your Session
Stop your current CDSW session and start a new one. The startup script will now run automatically.

---

### Step 4: Verification
Once the new session starts, you can verify that you are using Python 3.12.

1.  **Check the session log**: You should see the output from the `setup_py312_session.sh` script, ending with "✅ SUCCESS: Your session is now running on Python 3.12."

2.  **Run commands in the terminal**:
    ```bash
    python3 --version
    # Expected output: Python 3.12.x

    which python3
    # Expected output: /home/cdsw/.py312-venv/bin/python3
    ```

3.  **Check in a Python script or notebook**:
    ```python
    import sys
    print(sys.version)
    # Expected output: Should show Python 3.12.x

    import pandas
    print(pandas.__version__)
    # This should work, as pandas is installed by the setup script.
    ```

## How It Works
The `setup_py312_session.sh` script:
1.  Checks if a Python 3.12 virtual environment exists in your home directory (`~/.py312-venv`).
2.  If it doesn't, it creates one using the `python3.12` executable from your base Engine.
3.  It then `sources` the virtual environment's `activate` script, which correctly modifies your session's `PATH` and other environment variables.
4.  Finally, it installs a set of common data science packages into this virtual environment.

This is the industry-standard way to manage different Python versions and dependencies within a project.
