#!/bin/bash

# Function to check if we're in a virtual environment
check_venv() {
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        deactivate
    fi
}

# Function to find requirements file
find_requirements() {
    if [ -f "requirements.txt" ]; then
        echo "requirements.txt"
    elif [ -f "requirements/dev.txt" ]; then
        echo "requirements/dev.txt"
    elif [ -f "requirements/base.txt" ]; then
        echo "requirements/base.txt"
    else
        echo ""
    fi
}

# Check if we're in a virtual environment and deactivate if so
check_venv

# Remove existing venv directory if it exists
if [ -d "venv" ]; then
    echo "Removing existing venv..."
    rm -rf venv
fi

# Create new virtual environment
echo "Creating new virtual environment..."
python3 -m venv venv

# Activate the new environment
echo "Activating new virtual environment..."
source venv/bin/activate

# Check for and install requirements
REQ_FILE=$(find_requirements)
if [ ! -z "$REQ_FILE" ]; then
    echo "Installing dependencies from $REQ_FILE..."
    pip install -r "$REQ_FILE"
else
    echo "No requirements file found. Skipping dependency installation."
fi

echo "Virtual environment has been reset and dependencies installed (if found)."