#!/bin/bash
# CDSW Python 3.12 Switch Script
# Source this script to switch to Python 3.12: source switch_to_python312.sh

echo "Switching to Python 3.12..."

# Find python3.12
PYTHON312_PATH=$(which python3.12 2>/dev/null)

if [ -z "$PYTHON312_PATH" ]; then
    echo "Error: python3.12 not found in PATH"
    return 1
fi

echo "Found python3.12 at: $PYTHON312_PATH"

# Get the directory containing python3.12
PYTHON312_DIR=$(dirname "$PYTHON312_PATH")
echo "Python 3.12 directory: $PYTHON312_DIR"

# Save the original PATH
export ORIGINAL_PATH="$PATH"

# Update PATH to prioritize Python 3.12
export PATH="$PYTHON312_DIR:$PATH"

# Set Python version environment variables
export PY_PYTHON=3.12
export PYTHON_VERSION=3.12

# Also create aliases for convenience
alias python312='python3.12'
alias pip312='python3.12 -m pip'

# Verify the switch
echo ""
echo "Switch completed!"
echo "=================="
echo "Python executable: $(which python3)"
echo "Python version: $(python3 --version 2>&1)"
echo "Python 3.12 path: $PYTHON312_PATH"
echo ""
echo "You can now use:"
echo "  python3     - for Python 3.12"
echo "  python312   - for Python 3.12 (alias)"
echo "  pip312      - for pip with Python 3.12 (alias)"
echo ""
echo "To verify Python 3.12 features:"
echo "  python3 -c 'import zoneinfo; print(\"zoneinfo module available\")'"
echo ""
echo "To revert to original PATH:"
echo "  export PATH=\$ORIGINAL_PATH"
