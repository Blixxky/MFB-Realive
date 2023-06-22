"""
If timestamp.txt exists, if not or date is older than 30 days. Runs corresponding pip install
command for required libraries to make MFB run.
"""

import os
import subprocess
from datetime import datetime, timedelta

current_dir = os.path.dirname(os.path.abspath(__file__))

# Define file paths
timestamp_path = os.path.join(current_dir, "timestamp.txt")
requirements_path = os.path.join(current_dir, "requirements_win.txt")


# Check if timestamp.txt exists
if not os.path.exists(timestamp_path):
    print("Timestamp file does not exist, creating a new one...")
    with open(timestamp_path, "w", encoding="utf-8") as file:
        file.write(str(datetime.now().date()))

else:
    print("Timestamp file exists, checking the date...")
    # Extract the timestamp from the file
    with open(timestamp_path, "r", encoding="utf-8") as file:
        filedate = datetime.strptime(file.read().strip(), "%Y-%m-%d").date()
    print(f"Date in file: {filedate}")

    # If it's older than 30 days, recreate the file
    if datetime.now().date() - filedate > timedelta(days=30):
        print("The file is older than 30 days, recreating it...")
        with open(timestamp_path, "w", encoding="utf-8") as file:
            file.write(str(datetime.now().date()))
    else:
        print("The file is not older than 30 days, no need to recreate it.")
        exit()

# Running the pip install command
try:
    result = subprocess.run(
        [
            "MFB/Scripts/python.exe",
            "-m",
            "pip",
            "install",
            "-r",
            requirements_path,
        ],
        check=True,
        capture_output=True,
        text=True
    )
    print(result.stdout)  # Print output from subprocess
except subprocess.CalledProcessError as e:
    print(f"subprocess.run exited with a non-zero exit code: {e}")
    print(e.stderr)  # Print error output from subprocess
