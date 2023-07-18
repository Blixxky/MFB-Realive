#!python3
"""
MFB GUI

This module provides a graphical user interface for MFB settings configuration and starting/stopping the bot.
"""
import configparser
import logging
import os.path
import platform
import subprocess
import sys
import tkinter as tk
from tkinter import font, messagebox, filedialog, ttk
from typing import List
from ttkthemes import ThemedStyle

log = logging.getLogger(__name__)
venv_path = os.path.join('MFB')
activate_script = os.path.join(venv_path, 'Scripts', 'activate' if platform.system( ) == 'Windows' else 'activate')

if os.path.exists(activate_script):
    try:
        subprocess.run(activate_script, shell=True, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while activating virtual environment: {e}")
        sys.exit(1)
else:
    # Create venv
    if platform.system( ) == 'Windows':
        subprocess.run(["py", "-3.11", "-m", "venv", "MFB"], check=True)
    elif platform.system( ) == 'Linux':
        subprocess.run(["python3.11", "-m", "venv", "MFB"], check=True)
    else:
        print("Unsupported platform.")
        sys.exit(1)

# Initialize variables
SETTINGS_INI_CREATED = False
COMBO_INI_CREATED = False
GAME_DIR_SET = False
LOGFILE_CREATED = False
LOGFILE_APPENDED = False
local_app_data = os.getenv("LocalAppData")
hearthstone_dir = os.path.join(
    os.path.expanduser(local_app_data) if local_app_data else "",
    "Blizzard",
    "Hearthstone",
)

log_config_file = os.path.join(hearthstone_dir, "log.config")

# Check if the directory exists
if os.path.isdir(hearthstone_dir):
    # Check if the log.config file exists
    if not os.path.isfile(log_config_file):
        LOGFILE_CREATED = True
        # Write the default log.config content to the file
        with open(log_config_file, "w", encoding="utf-8") as configfile:
            configfile.write(
                """[Power]
LogLevel=1
FilePrinting=True
ConsolePrinting=False
ScreenPrinting=False
Verbose=True
[Achievements]
LogLevel=1
FilePrinting=True
ConsolePrinting=False
ScreenPrinting=False
Verbose=False
[Arena]
LogLevel=1
FilePrinting=True
ConsolePrinting=False
ScreenPrinting=False
Verbose=False
[FullScreenFX]
LogLevel=1
FilePrinting=True
ConsolePrinting=False
ScreenPrinting=False
Verbose=False
[LoadingScreen]
LogLevel=1
FilePrinting=True
ConsolePrinting=False
ScreenPrinting=False
Verbose=False
[Gameplay]
LogLevel=1
FilePrinting=True
ConsolePrinting=False
ScreenPrinting=False
Verbose=False
[Zone]
LogLevel=1
FilePrinting=true
ConsolePrinting=false
ScreenPrinting=false
"""
            )

    # If log.config file was not just created, check and append the [Zone] section
    if not LOGFILE_CREATED:
        # Read the contents of log.config file
        with open(log_config_file, "r", encoding="utf-8") as configfile:
            log_config_content = configfile.read( )

        # Check if "[Zone]" section exists in the log.config content
        if "[Zone]" not in log_config_content:
            LOGFILE_APPENDED = True
            # Append the "[Zone]" section to the end of the file
            with open(log_config_file, "a", encoding="utf-8") as configfile:
                configfile.write(
                    """\n[Zone]
LogLevel=1
FilePrinting=true
ConsolePrinting=false
ScreenPrinting=false"""
                )

settings_ini_path = os.path.join('conf', 'user', 'settings.ini')


def update_settings():
    """
    Read the settings and update the settings file
    """
    custom_config = configparser.ConfigParser( )
    custom_config.optionxform = str
    custom_config.read(settings_ini_path, encoding="utf-8")

    # Define the settings dictionary
    settings = {
        "location": str(location_var.get( )),
        "mode": str(mode_var.get( )),
        "level": str(level_var.get( )),
        "preferbooncaster": str(preferbooncaster_var.get( )),
        "preferboonfighter": str(preferboonfighter_var.get( )),
        "preferboonprotector": str(preferboonprotector_var.get( )),
        "preferprotector": str(preferprotector_var.get( )),
        "preferfighter": str(preferfighter_var.get( )),
        "prefercaster": str(prefercaster_var.get( )),
        "waitforexp": str(wait_for_exp_var.get( )),
        "quitbeforebossfight": str(quit_before_boss_var.get( )),
        "stopatbossfight": str(stop_at_boss_var.get( )),
        "preferelite": str(preferelite_var.get( )),
        "preferpassivetreasures": str(prefer_passive_treasures_var.get( )),
    }

    # Update the settings in the configuration file
    if "BotSettings" not in custom_config:
        custom_config["BotSettings"] = {}
    custom_config["BotSettings"].update(settings)

    # Write the updated settings to the settings.ini file
    with open(settings_ini_path, "w", encoding="utf-8") as config_file:
        custom_config.write(config_file)

    messagebox.showinfo("Success", "Settings updated successfully.")


def browse_and_write_game_dir():
    """
    Browse for hearthstone.exe and write the game directory to settings.ini
    """
    hs_dir = filedialog.askdirectory( )
    if hs_dir:
        # Write the game directory to settings.ini
        setdir = configparser.ConfigParser( )
        setdir.read(settings_ini_path, encoding="utf-8")

        # Check if the "[BotSettings]" section exists
        if not setdir.has_section("BotSettings"):
            # Create the "[BotSettings]" section if it doesn't exist
            setdir.add_section("BotSettings")

        # Update the existing or create a new "gamedir" entry under the "[BotSettings]" section
        setdir.set("BotSettings", "gamedir", hs_dir)

        with open(settings_ini_path, "w", encoding="utf-8") as config_file:
            setdir.write(config_file)

        # Update the game directory value in the GUI
        game_dir_var.set(
            hs_dir
        )  # Assuming game_dir_var is the variable for displaying the game directory


# Create the main window
window = tk.Tk( )
window.title("MFB Config Engine")
window.geometry("420x735")
window.configure(padx=0, pady=10)

style = ThemedStyle(window)
style.theme_use("arc")
style.configure("Header.TLabel", font=("Helvetica", 10))

# Define the acceptable level ranges for each location and mode
level_ranges = {
    "Barrens": {
        "Normal": ["4", "6", "7", "8", "10", "13", "15", "17", "18", "20"],
        "Heroic": ["5", "8", "10", "15", "15b", "20", "20b", "25", "25b", "30"],
    },
    "Felwood": {
        "Normal": [
            "20",
            "21",
            "23",
            "25",
            "27",
            "28",
            "30",
            "30b",
            "30c",
            "30d",
            "30e",
        ],
        "Heroic": [
            "26",
            "27",
            "28",
            "29",
            "29b",
            "29c",
            "30",
            "30b",
            "30c",
            "30d",
            "30e",
        ],
    },
    "Winterspring": {
        "Normal": ["30", "30b", "30c", "30d", "30e", "30f"],
        "Heroic": ["30", "30b", "30c", "30d", "30e", "30f"],
    },
    "Darkmoon": {  # Insert "Darkmoon" after "Winterspring"
        "Normal": [
            "30",
            "30b",
            "30c",
            "30d",
            "30e",
            "30f",
            "30g",
            "30h",
            "30i",
            "30j",
            "30k",
        ],
        "Heroic": [
            "30",
            "30b",
            "30c",
            "30d",
            "30e",
            "30f",
            "30g",
            "30h",
            "30i",
            "30j",
            "30k",
        ],
    },
    "Blackrock": {
        "Normal": [
            "30",
            "30b",
            "30c",
            "30d",
            "30e",
            "30f",
            "30g",
            "30h",
            "30i",
            "30j",
            "30k",
            "30l",
            "30m",
            "30n",
            "30o",
            "30p",
        ],
        "Heroic": [
            "30",
            "30b",
            "30c",
            "30d",
            "30e",
            "30f",
            "30g",
            "30h",
            "30i",
            "30j",
            "30k",
            "30l",
            "30m",
            "30n",
            "30o",
            "30p",
        ],
    },
    "Alterac": {
        "Normal": [
            "30",
            "30b",
            "30c",
            "30d",
            "30e",
            "30f",
            "30g",
            "30h",
            "30i",
            "30j",
            "30k",
            "30l",
        ],
        "Heroic": [
            "30",
            "30b",
            "30c",
            "30d",
            "30e",
            "30f",
            "30f",
            "30g",
            "30h",
            "30i",
            "30j",
            "30k",
            "30l",
        ],
    },
    "Blackrock Mountain": {
        "Normal": [
            "31",
            "31b",
            "31c",
            "31d",
            "31e",
            "31f",
            "31g",
            "31h",
            "31i",
            "31j",
            "31k",
            "31l",
        ],
        "Heroic": [
            "31",
            "31b",
            "31c",
            "31d",
            "31e",
            "31f",
            "31g",
            "31h",
            "31i",
            "31j",
            "31k",
            "31l",
        ],
    },
}

# Apply the themed style to the existing ttk widgets
style.configure("TLabel", font=("Georgia", 8))
style.configure("TCombobox", font=("Georgia", 9))
style.configure("TEntry", font=("Georgia", 8))
style.configure("TButton", font=("Georgia", 8, "bold"))
style.configure("TCheckbutton", font=("Georgia", 8))
label_font = font.Font(family="Helvetica", size=9)

# Define script status variables
script_running = False
main_process = None  # Process that will be initiated by subprocess.Popen

# Create a label to display the script status
status_var = tk.StringVar( )
status_var.set("Start")


def toggle_start_stop():
    global script_running
    global main_process
    global status_var

    if script_running:
        # If script is already running, stop it
        main_process.kill( )
        script_running = False
        status_var.set("Start")
    else:
        # If script is not running, start it
        script_running = True
        status_var.set("Stop")

        # Define the commands based on the system platform
        if platform.system( ) == "Windows":
            # This is a Windows machine
            python_command = ["py", "-3.11", "-m", "venv", "MFB"]
            python_interpreter = os.path.join("MFB", "Scripts", "python.exe")
            main_command = [python_interpreter, "main.py"]
        elif platform.system( ) == "Linux":
            # This is a Linux machine
            python_command = ["python3.11", "-m", "venv", "MFB"]
            python_interpreter = os.path.join("MFB", "bin", "python")
            main_command = [python_interpreter, "main.py"]
        else:
            print(f"Unsupported platform: {platform.system( )}")
            return

        # Run the Python command to create/activate the venv if needed
        subprocess.run(python_command)

        # Start the main script within the activated venv and keep track of the process
        main_process = subprocess.Popen(main_command)


# Create the button that will run toggle_start_stop when pressed
start_button = ttk.Button(window, textvariable=status_var, command=toggle_start_stop)
start_button.pack( )

# Create the zone dropdown
location_label = tk.Label(window, text="Zone:", font=label_font, fg="#454545")
location_label.pack( )
location_var = tk.StringVar( )
location_dropdown = ttk.Combobox(window, textvariable=location_var)
location_dropdown["values"] = list(level_ranges.keys( ))
location_dropdown.pack( )

# Create the mode dropdown
mode_label = tk.Label(window, text="Mode:", font=label_font, fg="#454545")
mode_label.pack( )
mode_var = tk.StringVar( )
mode_dropdown = ttk.Combobox(window, textvariable=mode_var)
mode_dropdown["values"] = ["Normal", "Heroic"]
mode_dropdown.pack( )

# Create the level dropdown
level_label = tk.Label(window, text="Level:", font=label_font, fg="#454545")
level_label.pack( )
level_var = tk.StringVar( )
level_dropdown = ttk.Combobox(window, textvariable=level_var)
level_dropdown.pack( )


def update_level_dropdown(*args):
    """
    Write the correct available levels for each Location/Zone
    """
    selected_location = location_var.get( )
    selected_mode = mode_var.get( )

    # Clear the current options in the level dropdown
    level_dropdown["values"] = []

    # Check if the selected location and mode exist in the level_ranges dictionary
    if (
            selected_location in level_ranges
            and selected_mode in level_ranges[selected_location]
    ):
        level_options = level_ranges[selected_location][selected_mode]
        level_dropdown["values"] = level_options


# Bind the update_level_dropdown function to the changes in location and mode dropdowns
location_var.trace("w", update_level_dropdown)
mode_var.trace("w", update_level_dropdown)

# Create the gamedir entry
game_dir_label = tk.Label(window, text="Game Directory:", font=label_font)
game_dir_label.pack( )
game_dir_var = tk.StringVar( )
game_dir_entry = ttk.Entry(window, textvariable=game_dir_var, width=40)
game_dir_entry.pack( )

# Create the Browse button
browse_button = ttk.Button(window, text="Browse", command=browse_and_write_game_dir)
browse_button.pack( )

header_label = ttk.Label(
    window, text="Bonus Preferences", style="Header.TLabel", anchor="center"
)
header_label.pack(padx=(85, 70), pady=(5, 5))

# Create a list to store the checkbox variables
boon_checkboxes: List[tk.BooleanVar] = []


# Function to handle checkbox changes for boons
def handle_boon_checkbox(var: tk.BooleanVar):
    """
    Max of 2 checkboxes at a time
    """
    checked_count = sum(var.get( ) for var in boon_checkboxes)
    if checked_count > 2:
        var.set(False)  # Reset the checkbox if the maximum is reached


def initialize_config_parser():
    class CustomConfigParser(configparser.ConfigParser):
        def __init__(self):
            super( ).__init__( )

        def optionxform(self, optionstr):
            return optionstr

    config = CustomConfigParser( )
    config.read(settings_ini_path)

    return config


# Call the function to initialize the config parser
config = initialize_config_parser( )

# Create the BooleanVar variables
preferbooncaster_var = tk.BooleanVar( )
preferboonfighter_var = tk.BooleanVar( )
preferboonprotector_var = tk.BooleanVar( )

if "BotSettings" in config:
    preferbooncaster_var.set(config["BotSettings"].getboolean("preferbooncaster", False))
    preferboonfighter_var.set(config["BotSettings"].getboolean("preferboonfighter", False))
    preferboonprotector_var.set(config["BotSettings"].getboolean("preferboonprotector", False))

# Create the checkbox for preferbooncaster
preferbooncaster_checkbox = ttk.Checkbutton(
    window, text="Prefer Caster Boon", variable=preferbooncaster_var,
    command=lambda: handle_boon_checkbox(preferbooncaster_var)
)
preferbooncaster_checkbox.pack(anchor="w", padx=(150, 0))
boon_checkboxes.append(preferbooncaster_var)

# Create the checkbox for preferboonfighter
preferboonfighter_checkbox = ttk.Checkbutton(
    window, text="Prefer Fighter Boon", variable=preferboonfighter_var,
    command=lambda: handle_boon_checkbox(preferboonfighter_var)
)
preferboonfighter_checkbox.pack(anchor="w", padx=(150, 0))
boon_checkboxes.append(preferboonfighter_var)

# Create the checkbox for preferboonprotector
preferboonprotector_checkbox = ttk.Checkbutton(
    window, text="Prefer Protector Boon", variable=preferboonprotector_var,
    command=lambda: handle_boon_checkbox(preferboonprotector_var)
)
preferboonprotector_checkbox.pack(anchor="w", padx=(150, 0))
boon_checkboxes.append(preferboonprotector_var)

# Force a redraw of the window to ensure the checkboxes reflect their BooleanVar values
window.update_idletasks( )

header_label = ttk.Label(
    window, text="Fight Preference", style="Header.TLabel", anchor="center"
)
header_label.pack(padx=(70, 70), pady=(10, 5))

# Create a list to store the checkbox variables
fight_checkboxes: List[tk.BooleanVar] = []


# Function to handle checkbox changes for fights
def handle_fight_checkbox(var: tk.BooleanVar):
    """
    Maximum of 2 checkboxes ticked
    """
    checked_count = sum(var.get( ) for var in fight_checkboxes)
    if checked_count > 2:
        var.set(False)  # Reset the checkbox if the maximum is reached


# Create the checkbox for prefercaster
prefercaster_var = tk.BooleanVar( )
prefercaster_var.set(config["BotSettings"].getboolean("prefercaster", False))
prefercaster_checkbox = ttk.Checkbutton(
    window,
    text="Prefer Caster",
    variable=prefercaster_var,
    command=lambda: handle_fight_checkbox(prefercaster_var),
)
prefercaster_checkbox.pack(anchor="w", padx=(150, 0))
fight_checkboxes.append(prefercaster_var)

# Create the checkbox for preferfighter
preferfighter_var = tk.BooleanVar( )
preferfighter_var.set(config["BotSettings"].getboolean("preferfighter", False))
preferfighter_checkbox = ttk.Checkbutton(
    window,
    text="Prefer Fighter",
    variable=preferfighter_var,
    command=lambda: handle_fight_checkbox(preferfighter_var),
)
preferfighter_checkbox.pack(anchor="w", padx=(150, 0))
fight_checkboxes.append(preferfighter_var)

# Create the checkbox for preferprotector
preferprotector_var = tk.BooleanVar( )
preferprotector_var.set(config["BotSettings"].getboolean("preferprotector", False))
preferprotector_checkbox = ttk.Checkbutton(
    window,
    text="Prefer Protector",
    variable=preferprotector_var,
    command=lambda: handle_fight_checkbox(preferprotector_var),
)
preferprotector_checkbox.pack(anchor="w", padx=(150, 0))
fight_checkboxes.append(preferprotector_var)

header_label = ttk.Label(
    window, text="Miscellaneous", style="Header.TLabel", anchor="center"
)

header_label.pack(padx=(70, 70), pady=(10, 5))
wait_for_exp_label = ttk.Label(window, text="Wait For Exp in seconds")
wait_for_exp_label.pack(anchor="w", padx=(150, 0), pady=(0, 0))
wait_for_exp_var = tk.IntVar( )
wait_for_exp_entry = ttk.Entry(window, textvariable=wait_for_exp_var, width=1)
wait_for_exp_entry.pack(anchor="w", padx=(205, 0), pady=(1, 1))

stop_at_boss_var: tk.BooleanVar = tk.BooleanVar( )
# Create the checkbox for quitbeforebossfight
quit_before_boss_var = tk.BooleanVar( )
quit_before_boss_checkbox = ttk.Checkbutton(
    window,
    text="Quit Before Boss Fight",
    variable=quit_before_boss_var,
    command=lambda: handle_checkbox_selection(quit_before_boss_var, stop_at_boss_var),
)
quit_before_boss_checkbox.pack(anchor="w", padx=(150, 0))

# Create the checkbox for stopatbossfight
stop_at_boss_checkbox = ttk.Checkbutton(
    window,
    text="Stop At Boss Fight",
    variable=stop_at_boss_var,
    command=lambda: handle_checkbox_selection(stop_at_boss_var, quit_before_boss_var),
)
stop_at_boss_checkbox.pack(anchor="w", padx=(150, 0))


def handle_checkbox_selection(selected_var, other_var):
    """
    Callback function to handle checkbox selection
    """
    if selected_var.get( ):
        other_var.set(False)


# Create the checkbox for preferelite
preferelite_var = tk.BooleanVar(value=True)
preferelite_checkbox = ttk.Checkbutton(
    window, text="Prefer Elite Fights", variable=preferelite_var
)
preferelite_checkbox.pack(anchor="w", padx=(150, 0))

# Create the checkbox for preferpassivetreasures
prefer_passive_treasures_var = tk.BooleanVar(value=True)
prefer_passive_treasures_checkbox = ttk.Checkbutton(
    window, text="Prefer Passive Treasures", variable=prefer_passive_treasures_var
)
prefer_passive_treasures_checkbox.pack(anchor="w", padx=(150, 0), pady=(0, 25))

# Create a label to display the tracking information
tracking_label = tk.Label(window, text="")
tracking_label.pack( )

# Update the tracking label text before updating the settings
TRACKING_TEXT = ""

if SETTINGS_INI_CREATED:
    TRACKING_TEXT += "Settings.ini created with defaults.\n"
else:
    TRACKING_TEXT += "Settings.ini loaded from existing file.\n"

if COMBO_INI_CREATED:
    TRACKING_TEXT += "Combo.ini created with defaults.\n"

if LOGFILE_CREATED:
    TRACKING_TEXT += "log.config was not found, but able to be created."

if LOGFILE_APPENDED:
    TRACKING_TEXT += "log.config was found, and had to be appended."
tracking_label["text"] = TRACKING_TEXT

# Call the function to initialize the config parser
config = initialize_config_parser( )

# Populate the GUI elements with the values from the settings.ini file
if "BotSettings" in config:
    location_var.set(config["BotSettings"].get("location", ""))
    mode_var.set(config["BotSettings"].get("mode", ""))
    level_var.set(config["BotSettings"].get("level", ""))
    game_dir_var.set(config["BotSettings"].get("gamedir", ""))
    wait_for_exp_var.set(int(config["BotSettings"].get("waitforexp", "0")))
    quit_before_boss_var.set(
        config["BotSettings"].getboolean("quitbeforebossfight", False)
    )
    stop_at_boss_var.set(config["BotSettings"].getboolean("stopatbossfight", False))
    preferelite_var.set(config["BotSettings"].getboolean("preferelite", False))
    prefer_passive_treasures_var.set(
        config["BotSettings"].getboolean("preferpassivetreasures", True)
    )

update_button = ttk.Button(window, text="Update Settings", command=update_settings)
update_button.pack(anchor="center")

# Run the GUI
window.mainloop( )
