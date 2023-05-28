import configparser
import os.path
import shutil
import tkinter as tk
from tkinter import font, messagebox, filedialog, ttk
from ttkthemes import ThemedStyle

# Initialize variables
settings_ini_created = False
combo_ini_created = False
game_dir_set = False
logfile_created = False
logfile_appended = False
hearthstone_dir = os.path.join(os.getenv("LocalAppData"), "Blizzard", "Hearthstone")
log_config_file = os.path.join(hearthstone_dir, "log.config")

if not os.path.isfile("settings.ini"):
    settings_ini_created = True
    print("settings.ini was not found and created with default values.")
    # Create the settings.ini file with default content
    with open("settings.ini", "w") as configfile:
        configfile.write(
            """[BotSettings]
monitor = 1
resolution = 1920x1080
logs = True
location =
mode =
level =
preferelite = False
notificationurl =
MouseSpeed = 0.2
GameDir =
preferbooncaster = False
preferboonfighter = False
preferboonprotector = False
preferprotector = False
preferfighter = False
prefercaster = False
waitForEXP = False
quitBeforeBossFight = False
stopAtBossFight = False
preferPassiveTreasures = True
"""
        )
    # Set game_dir_set to False since settings.ini was just created
    game_dir_set = False

else:
    # settings.ini was found, so game_dir_set is not applicable
    game_dir_set = None

# Check if GameDir is set only if settings.ini was not found
if game_dir_set is None:
    default_game_dir = r"C:\Program Files (x86)\Hearthstone"
    if os.path.isfile(os.path.join(default_game_dir, "hearthstone.exe")):
        game_dir = default_game_dir
        game_dir_set = True
        print("hearthstone.exe was found")
    else:
        game_dir = ""
        game_dir_set = False

# Update the value of GameDir in settings.ini
if game_dir_set:
    with open("settings.ini", "r+") as configfile:
        lines = configfile.readlines()
        configfile.seek(0)
        for line in lines:
            if line.startswith("GameDir"):
                configfile.write(f"GameDir = {game_dir}\n")
            else:
                configfile.write(line)
        configfile.truncate()

# Check if the directory exists
if os.path.isdir(hearthstone_dir):
    # Check if the log.config file exists
    if not os.path.isfile(log_config_file):
        logfile_created = True
        # Write the default log.config content to the file
        with open(log_config_file, "w") as configfile:
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
    if not logfile_created:
        # Read the contents of log.config file
        with open(log_config_file, "r") as configfile:
            log_config_content = configfile.read()

        # Check if "[Zone]" section exists in the log.config content
        if "[Zone]" not in log_config_content:
            logfile_appended = True
            # Append the "[Zone]" section to the end of the file
            with open(log_config_file, "a") as configfile:
                configfile.write(
                    """\n[Zone]
LogLevel=1
FilePrinting=true
ConsolePrinting=false
ScreenPrinting=false"""
                )

# Check if combo.ini file exists
if not os.path.isfile("combo.ini"):
    print("combo.ini was not found and was created with default values.")
    combo_ini_created = True
    # Create the combo.ini file with default content
    with open("combo.ini", "w") as configfile:
        configfile.write(
            """[Mercenary]
Alexstrasza=1,3
Anduin Wrynn=1,2
Antonidas=1
Aranna Starseeker=2,3,1
Baine Bloodhoof=1
Balinda Stonehearth=1,2,3:chooseone=2
Baron Geddon=2
Blademaster Samuro=1,3
Blink Fox=1,1,2
Brann Bronzebeard=1,2,3
Brightwing=1
Bru'kan=1,1,3
C'Thun=1,2
Cairne Bloodhoof=1
Captain Galvangar=1,3,2
Captain Hooktusk=1,2,3
Cariel Roame=2,1
Chi-Ji=1,1,3
Cookie, the Cook=1
Cornelius Roame=1,2,2
Deathwing=1,2,3
Diablo=1,2,3,2,3,2,3
Edwin, Defias Kingpin=1,2,3
Elise Starseeker=1,2,3
Eudora=1,2
Fathom-Lord Karathress=1,2
Kazakus, golem shaper=1
Garona Halforcen=1,2,3
Garrosh Hellscream=1,3
Genn Greymane=2,3,1
Gruul=1,2,3
Grommash Hellscream=2,3
Guff Runetotem=2
Illidan Stormrage=1,3,2
Jaina Proudmoore=1,3,2
King Krush=1,2,3
King Mukla=1,3
Kurtrus Ashfallen=1,3,2,3,2
Lady Anacondra=1
Lady Vashj=1,2,3
Leeroy Jenkins=1,2,3
Lokholar the Ice Lord=1
Long'xin=1
Lord Jaraxxus=3,2,1
Lord Slitherspear=1,2,3
Lorewalker Cho=1,2,3
Malfurion=1
Mannoroth=1,3
Millhouse Manastorm=1,1,2
Morgl the Oracle=1,2
Mr. Smite=1
Murky=1,3
Mutanus=1,2,2,2,2,2,2,2
Natalie Seline=1,3
Neeru Fireblade=1,1,3
Nefarian=1,3
Nemsy Necrofizzle=1,3,2
Niuzao=1,3
Patches the Pirate=1,2,3
Prince Malchezaar=1,2,3
Old Murk-Eye=1,2,3,2,3,2,3
Onyxia=1,3
Prophet Velen=1,3
Queen Azshara=1,2,3
Ragnaros=2
Rathorian=1,2,2,3
Rattlegore=1,2,3
Rokara=1,3
Scabbs Cutterbutter=1,2:chooseone=2
Sir Finley=1,3,2
Sinestra=1,3,2
Sky Admiral Rogers=1,3
Sneed=1,2
Sylvanas Windrunner=1,1,3
Tamsin Roame=1
Tavish Stormpike=1
Tess Greymane=1,2,3
The lich king=1,2
Thrall=1
Tidemistress Athissa=1,1,3,3
Trigore the Lasher=2
Tyrael=1,3,2
Tyrande Whisperwind=1,2
Valeera Sanguinar=1,2,3
Vanessa VanCleef=1
Vanndar Stormpike=1,1,3
Varden Dawngrasp=1
Varian Wrynn=3
Varok Saurfang=1,2
Vol'jin=1,2
War Master Voone=1,2,3
Wrathion=1,2,3
Yogg-Saron=1,2
Yu'lon=1,2
Xuen=1,3
Xyrella=1,3
Yrel=1,2,3
Ysera=1,2,3
Y'Shaarj=1,2
Uther Lightbringer=1,3,2
Zar'jira, the Sea Witch=1,3,2

[Neutral]
Bladehand Berserker=1
Boggy=1
Devilsaur=1
Dragonmaw Poacher=1
Drakonid=1
Eudora's Cannon=1
Elementium Terror=1
Fathom Guard=1
Fel Infernal=1
Felfin Navigator=1
Giantfin=1
Greater Golem=1
Grounding Totem=1
Hozen Troublemaker=1
Huffer=1
Hulking Overfiend=1
Hungry Naga=1
Imp Familiar=2
Jade Golem=1
Lesser Fire Elemental=2
Lesser Water Elemental=1
Marching Murlocs=1
Misha=1
Mogu Conqueror=1
Mukla's big brother=1
Nightmare Viper=1
Patchling=1
Pufferfisher=1
Saurok Raider=1
Spawn of N'Zoth=1
Spud M.E.=1
Stonemaul Banner=2
Superior Golem=1
Void Consumer=1
Water Elemental=1
Warlord Parjesh=1
Wavethrasher=1

# below, specific boss fight (ex: Air Elemental)
#[Air Elemental]
#_handselection=Balinda Stonehearth+Baron Geddon+Ragnaros
#Balinda Stonehearth=1
#Baron Geddon=2
#Ragnaros=2
"""
        )


# Create backups of the settings.ini file
backup_filenames = ["settings.bak.ini"]

for i in range(len(backup_filenames) - 1, 0, -1):
    if os.path.isfile(backup_filenames[i]):
        # Move the existing backup to the next backup file
        shutil.copy(backup_filenames[i], backup_filenames[i - 1])

# Move the original settings.ini to settings.bak.ini
if os.path.isfile("settings.ini"):
    shutil.copy("settings.ini", backup_filenames[0])


# Function to update the settings.ini file
def update_settings():
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read("settings.ini")

    # Update the ini_settings_loaded variable
    global ini_settings_loaded
    ini_settings_loaded = True

    # Get the selected location, mode, and level from the dropdown menus
    location = location_var.get()
    mode = mode_var.get()
    level = level_var.get()

    # Update or add the location entry
    if "BotSettings" in config:
        config["BotSettings"]["location"] = location
        config["BotSettings"]["mode"] = mode
        config["BotSettings"]["level"] = level
    else:
        config["BotSettings"] = {"location": location, "mode": mode, "level": level}

    # Update the MouseSpeed value
    config["BotSettings"]["MouseSpeed"] = mouse_speed_var.get()

    # Update the GameDir value
    config["BotSettings"]["GameDir"] = game_dir

    # Update the checkbox values
    config["BotSettings"]["preferbooncaster"] = str(preferbooncaster_var.get())
    config["BotSettings"]["preferboonfighter"] = str(preferboonfighter_var.get())
    config["BotSettings"]["preferboonprotector"] = str(preferboonprotector_var.get())
    config["BotSettings"]["preferprotector"] = str(preferprotector_var.get())
    config["BotSettings"]["preferfighter"] = str(preferfighter_var.get())
    config["BotSettings"]["prefercaster"] = str(prefercaster_var.get())
    config["BotSettings"]["waitForEXP"] = str(wait_for_exp_var.get())
    config["BotSettings"]["quitBeforeBossFight"] = str(quit_before_boss_var.get())
    config["BotSettings"]["stopAtBossFight"] = str(stop_at_boss_var.get())
    config["BotSettings"]["preferelite"] = str(preferelite_var.get())
    config["BotSettings"]["preferPassiveTreasures"] = str(
        prefer_passive_treasures_var.get()
    )

    # Save the changes to the settings.ini file
    with open("settings.ini", "w") as configfile:
        config.write(configfile)

    messagebox.showinfo("Success", "Settings updated successfully.")


# Function to browse and select the game directory
def browse_game_dir():
    game_dir = filedialog.askdirectory()
    if game_dir:
        game_dir_var.set(game_dir)


# Create the main window
window = tk.Tk()
window.title("MFB Config Engine")
window.geometry("420x700")
window.configure(padx=0, pady=15)

style = ThemedStyle(window)
style.theme_use("plastik")
style.configure("Header.TLabel", foreground="#392B58", font=("Tahoma", 12))

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
style.configure("TLabel", font=("Tahoma", 9))
style.configure("TCombobox", font=("Tahoma", 11), relief="sunken")
style.configure("TEntry", font=("Tahoma", 9))
style.configure("TButton", font=("Tahoma", 9))
style.configure("TCheckbutton", font=("Tahoma", 9))
label_font = font.Font(family="Tahoma", size=11)

# Create the location dropdown
location_label = tk.Label(window, text="Zone:", font=label_font, fg="#454545")
location_label.pack()
location_var = tk.StringVar()
location_dropdown = ttk.Combobox(window, textvariable=location_var)
location_dropdown["values"] = list(level_ranges.keys())
location_dropdown.pack()

# Create the mode dropdown
mode_label = tk.Label(window, text="Mode:", font=label_font, fg="#454545")
mode_label.pack()
mode_var = tk.StringVar()
mode_dropdown = ttk.Combobox(window, textvariable=mode_var)
mode_dropdown["values"] = ["Normal", "Heroic"]
mode_dropdown.pack()

# Create the level dropdown
level_label = tk.Label(window, text="Level:", font=label_font, fg="#454545")
level_label.pack()
level_var = tk.StringVar()
level_dropdown = ttk.Combobox(window, textvariable=level_var)
level_dropdown.pack()


def update_level_dropdown(*args):
    selected_location = location_var.get()
    selected_mode = mode_var.get()

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


# Create the MouseSpeed dropdown
mouse_speed_label = tk.Label(window, text="Mouse Speed:", font=label_font)
mouse_speed_label.pack()
mouse_speed_var = tk.StringVar()
mouse_speed_dropdown = ttk.Combobox(window, textvariable=mouse_speed_var)
mouse_speed_dropdown["values"] = ["0.1", "0.2", "0.3", "0.4"]
mouse_speed_dropdown.pack()

# Create the GameDir entry
game_dir_label = tk.Label(window, text="Game Directory:", font=label_font)
game_dir_label.pack()
game_dir_var = tk.StringVar()
game_dir_entry = ttk.Entry(
    window, textvariable=game_dir_var, width=40
)  # Increase the width to 40
game_dir_entry.pack()


# Create the Browse button
browse_button = ttk.Button(window, text="Browse", command=browse_game_dir)
browse_button.pack()

header_label = ttk.Label(
    window, text="Bonus Preferences", style="Header.TLabel", anchor="center"
)
header_label.pack(padx=(85, 70), pady=(20, 5))

# Create the checkbox for preferbooncaster
preferbooncaster_var = tk.BooleanVar()
preferbooncaster_checkbox = ttk.Checkbutton(
    window,
    text="Prefer Caster Boon",
    variable=preferbooncaster_var,
    command=lambda: handle_preferbooncaster(preferbooncaster_var),
)
preferbooncaster_checkbox.pack(anchor="w", padx=(150, 0))

# Create the checkbox for preferboonfighter
preferboonfighter_var = tk.BooleanVar()
preferboonfighter_checkbox = ttk.Checkbutton(
    window,
    text="Prefer Fighter Boon",
    variable=preferboonfighter_var,
    command=lambda: handle_preferboonfighter(preferboonfighter_var),
)
preferboonfighter_checkbox.pack(anchor="w", padx=(150, 0))

# Create the checkbox for preferboonprotector
preferboonprotector_var = tk.BooleanVar()
preferboonprotector_checkbox = ttk.Checkbutton(
    window,
    text="Prefer Protector Boon",
    variable=preferboonprotector_var,
    command=lambda: handle_preferboonprotector(preferboonprotector_var),
)
preferboonprotector_checkbox.pack(anchor="w", padx=(150, 0))


# Function to handle preferbooncaster checkbox
def handle_preferbooncaster(var):
    if var.get():
        preferboonfighter_var.set(False)
        preferboonprotector_var.set(False)


# Function to handle preferboonfighter checkbox
def handle_preferboonfighter(var):
    if var.get():
        preferbooncaster_var.set(False)
        preferboonprotector_var.set(False)


# Function to handle preferboonprotector checkbox
def handle_preferboonprotector(var):
    if var.get():
        preferbooncaster_var.set(False)
        preferboonfighter_var.set(False)


header_label = ttk.Label(
    window, text="Fight Preference", style="Header.TLabel", anchor="center"
)
header_label.pack(padx=(70, 70), pady=(10, 5))

# Create the checkbox for prefercaster
prefercaster_var = tk.BooleanVar()
prefercaster_checkbox = ttk.Checkbutton(
    window,
    text="Prefer Caster",
    variable=prefercaster_var,
    command=lambda: handle_prefercaster(prefercaster_var),
)
prefercaster_checkbox.pack(anchor="w", padx=(150, 0))

# Create the checkbox for preferfighter
preferfighter_var = tk.BooleanVar()
preferfighter_checkbox = ttk.Checkbutton(
    window,
    text="Prefer Fighter",
    variable=preferfighter_var,
    command=lambda: handle_preferfighter(preferfighter_var),
)
preferfighter_checkbox.pack(anchor="w", padx=(150, 0))

# Create the checkbox for preferprotector
preferprotector_var = tk.BooleanVar()
preferprotector_checkbox = ttk.Checkbutton(
    window,
    text="Prefer Protector",
    variable=preferprotector_var,
    command=lambda: handle_preferprotector(preferprotector_var),
)
preferprotector_checkbox.pack(anchor="w", padx=(150, 0))


# Function to handle prefercaster checkbox
def handle_prefercaster(var):
    if var.get():
        preferfighter_var.set(False)
        preferprotector_var.set(False)


# Function to handle preferfighter checkbox
def handle_preferfighter(var):
    if var.get():
        prefercaster_var.set(False)
        preferprotector_var.set(False)


# Function to handle preferprotector checkbox
def handle_preferprotector(var):
    if var.get():
        prefercaster_var.set(False)
        preferfighter_var.set(False)


header_label = ttk.Label(
    window, text="Miscellaneous", style="Header.TLabel", anchor="center"
)
header_label.pack(padx=(70, 85), pady=(10, 5))

# Create the checkbox for waitForEXP
wait_for_exp_var = tk.BooleanVar(value=True)
wait_for_exp_checkbox = ttk.Checkbutton(
    window, text="Wait for EXP (longer runs, more track exp)", variable=wait_for_exp_var
)
wait_for_exp_checkbox.pack(anchor="w", padx=(150, 0))


# Create the checkbox for quitBeforeBossFight
quit_before_boss_var = tk.BooleanVar()
quit_before_boss_checkbox = ttk.Checkbutton(
    window,
    text="Quit Before Boss Fight",
    variable=quit_before_boss_var,
    command=lambda: handle_checkbox_selection(quit_before_boss_var, stop_at_boss_var),
)
quit_before_boss_checkbox.pack(anchor="w", padx=(150, 0))

# Create the checkbox for stopAtBossFight
stop_at_boss_var = tk.BooleanVar()
stop_at_boss_checkbox = ttk.Checkbutton(
    window,
    text="Stop At Boss Fight",
    variable=stop_at_boss_var,
    command=lambda: handle_checkbox_selection(stop_at_boss_var, quit_before_boss_var),
)
stop_at_boss_checkbox.pack(anchor="w", padx=(150, 0))


# Callback function to handle checkbox selection
def handle_checkbox_selection(selected_var, other_var):
    if selected_var.get():
        other_var.set(False)


# Create the checkbox for preferelite
preferelite_var = tk.BooleanVar(value=True)
preferelite_checkbox = ttk.Checkbutton(
    window, text="Prefer Elite Fights", variable=preferelite_var
)
preferelite_checkbox.pack(anchor="w", padx=(150, 0))

# Create the checkbox for preferPassiveTreasures
prefer_passive_treasures_var = tk.BooleanVar(value=True)
prefer_passive_treasures_checkbox = ttk.Checkbutton(
    window, text="Prefer Passive Treasures", variable=prefer_passive_treasures_var
)
prefer_passive_treasures_checkbox.pack(anchor="w", padx=(150, 0), pady=(0, 25))

# Create a label to display the tracking information
tracking_label = tk.Label(window, text="")
tracking_label.pack()

# Update the tracking label text before updating the settings
tracking_text = ""


if settings_ini_created:
    tracking_text += "Settings.ini created with defaults.\n"
else:
    tracking_text += "Settings.ini loaded from existing file.\n"

if combo_ini_created:
    tracking_text += "Combo.ini created with defaults.\n"

if game_dir_set:
    tracking_text += "hearthstone.exe was found.\n"

if logfile_created:
    tracking_text += "log.config was not found, but able to be created."

if logfile_appended:
    tracking_text += "log.config was found, and had to be appended."
tracking_label["text"] = tracking_text


# Create the Update button
update_button = ttk.Button(window, text="Update Settings", command=update_settings)
update_button.pack()

# Read the settings from the settings.ini file
config = configparser.ConfigParser()
config.optionxform = str
config.read("settings.ini")

# Populate the GUI elements with the values from the settings.ini file
if "BotSettings" in config:
    location_var.set(config["BotSettings"].get("location", ""))
    mode_var.set(config["BotSettings"].get("mode", ""))
    level_var.set(config["BotSettings"].get("level", ""))
    mouse_speed_var.set(config["BotSettings"].get("MouseSpeed", ""))
    game_dir_var.set(config["BotSettings"].get("GameDir", ""))
    preferbooncaster_var.set(
        config["BotSettings"].getboolean("preferbooncaster", False)
    )
    preferboonfighter_var.set(
        config["BotSettings"].getboolean("preferboonfighter", False)
    )
    preferboonprotector_var.set(
        config["BotSettings"].getboolean("preferboonprotector", False)
    )
    preferprotector_var.set(config["BotSettings"].getboolean("preferprotector", False))
    preferfighter_var.set(config["BotSettings"].getboolean("preferfighter", False))
    prefercaster_var.set(config["BotSettings"].getboolean("prefercaster", False))
    wait_for_exp_var.set(config["BotSettings"].getboolean("waitForEXP", False))
    quit_before_boss_var.set(
        config["BotSettings"].getboolean("quitBeforeBossFight", False)
    )
    stop_at_boss_var.set(config["BotSettings"].getboolean("stopAtBossFight", False))
    preferelite_var.set(config["BotSettings"].getboolean("preferelite", False))
    prefer_passive_treasures_var.set(
        config["BotSettings"].getboolean("preferPassiveTreasures", True)
    )


# Run the GUI
window.mainloop()
