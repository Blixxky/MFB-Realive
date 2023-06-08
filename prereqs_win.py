"""
If timestamp.txt exists, if not or date is older than 30 days. Runs corresponding pip install
command for required libraries to make MFB run.
"""
from datetime import datetime, timedelta
import os
import subprocess

# Check if timestamp.txt exists
if not os.path.exists("timestamp.txt"):
    print("Timestamp file does not exist, creating a new one...")
    with open("timestamp.txt", "w", encoding="utf-8") as file:
        file.write(str(datetime.now().date()))
    # Running the pip install command
    try:
        subprocess.run(
            [
                "MFB/Scripts/python.exe",
                "-m",
                "pip",
                "install",
                "-r",
                "requirements_win.txt",
            ],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"subprocess.run exited with a non-zero exit code: {e}")

else:
    print("Timestamp file exists, checking the date...")
    # Extract the timestamp from the file
    with open("timestamp.txt", "r", encoding="utf-8") as file:
        filedate = datetime.strptime(file.read().strip(), "%Y-%m-%d").date()
    print(f"Date in file: {filedate}")

    # If it's older than 30 days, recreate the file
    if datetime.now().date() - filedate > timedelta(days=30):
        print("The file is older than 14 days, recreating it...")
        with open("timestamp.txt", "w", encoding="utf-8") as file:
            file.write(str(datetime.now().date()))
        # Running the pip install command
        try:
            subprocess.run(
                [
                    "MFB/Scripts/python.exe",
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    "requirements_win.txt",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"subprocess.run exited with a non-zero exit code: {e}")
    else:
        print("The file is not older than 30 days, no need to recreate it.")
