#!/bin/bash

# Create virtual environment
python3.11 -m venv MFB

# Activate virtual environment
source MFB/bin/activate

# Install requirements
pip install -r requirements_linux.txt
