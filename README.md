# Mercenaries Farm Bot Realive
MFB-Realive : https://github.com/Blixxky/MFB-Realive

![Image](rejoice.jpg)

# Built on the back of [Mercenaries Farm Bot by @Efemache](https://github.com/Efemache/Mercenaries-Farm-bot)

## Supported Resolutions

- For fullscreen mode, both the Hearthstone resolution and your screen resolution must match. For example, use **1920x1080** for both.
- **1920x1080** in fullscreen mode ✔️✔️
- **1920x1080** in windowed mode ✔️✔️

- To play in windowed mode, ensure that your monitor has a higher resolution than Hearthstone in both width ad height.
- **Any 16:9** aspect ratio with a minimum of 960x540, such as 960x540, 1024x576, 1280x720, 1600x900, and so on, in fullscreen mode ✔️
- **Any 16:9** aspect ratio, including higher resolutions like 2560x1440, in windowed mode ✔️

<sub>✔️✔️ tested and working</sub>

<sub>✔️ reported as working</sub>

## Installation

### Windows
1. Install [Python 3.11](https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64-webinstall.exe) (⚠️ select the "Add Python 3.11 to PATH" during installation) 
2. Download the project
   - [MFB-Realive](https://github.com/Blixxky/MFB-Realive)
4. Open *`conf/user/config.py`* or *`conf/user/config.pyw`* and set your preferred '*settings*' using the GUI. 
   - Set **GameDir** by browsing in the GUI or putting the path in '*settings.ini*' under "GameDir". This is where '*hearthstone.exe*' is
   - Create your Hearthstone *`log.config`* file
6. Start Hearthstone with same resolution as set in *`settings.ini`*, Config Engine creates settings with default 1920x1080.
7. Create a group of mercenaries named "Botwork"
8. Run HSbotRunner.bat 
   - The bat file now checks the last time dependencies were installed. If never or greater than 30 days, it will pip install all reqs.

### Linux
1. Install python3-venv *`sudo apt install python3.11-venv`*
2. Install gir1.2-wnck-3.0 *`sudo apt install gir1.2-wnck-3.0`*
3. Install - if needed - libharfbuzz-gobject0 *`sudo apt install libharfbuzz-gobject0`*
4. Download the project
   - [MFB-Realive](https://github.com/Blixxky/MFB-Realive)
5. Run *`conf/user/config.py`* or *`conf/user/config.pyw`* and set your preferences
6. Set **GameDir** to your Hearthstone directory using the Browse button.
6. Create/Edit your Hearthstone [log.config file](https://github.com/Efemache/Mercenaries-Farm-bot/wiki/Settings#logconfig)
7. Start Hearthstone with same resolution as set in *`settings.ini`*, Config Engine creates settings with default 1920x1080.
8. Create a group of mercenaries named "Botwork" 
9. Run HSbotRunner.sh

### While the bot is running...
- Don't move the Hearthstone window
- Don't put another window in front of Hearthstone
- Don't touch your mouse unless you want to bypass the bot (drag it to the top left corner until you get the resume alert)
- Don't resize the Hearthstone window or change the resolution
- Eat popcorn..

## Features: 

* Starts from Battle.net with a screen resolution of 1080.
* Supports Up to "March of the Lich King" expansion and Returns to Naxxramas mini-set release.
* Completes a lot of campfire tasks and some bounties.
* Transitions to Travel point selection.
* Transitions to Level/Bounty selection.
* Smooth transitions between encounters.
* Prioritizes the spirit healer.
* Prioritizes the mysterious node.
* Allows placement of mercenaries on the board.
* Searches for suitable opponents.
* Ability selection for each mercenary using combo.ini file.
* Defaults to the first abilities if no configuration exists.
* Ability targeting of friendly minions by Type, Faction, or Name.
* Performs attacks against opponents when abilities require it.
* Allows the choice of a treasure after passing a level.
* Collects rewards for reaching the last level.
* Claims packs, coins, and equipment from completed tasks.
* Battle uses a simple AI which utilizes the Hearthstone RPS system <sup>(Protector > Fighter > Caster > Protector)</sup>
* It doesn't know about taunt, divine shield, stealth, attack, health, ... yet

## Configuration

There are two ways to configure MFB now:
1. You can use *`conf/user/config.py`*, the new Config Engine GUI. This will create *`settings.ini`* if it does not exist, *`combo.ini`* if it does not exist. 
2. You can edit the *`conf/user/settings.ini`* file, the *'conf/user/combo.ini'* file, and the *'log.config'* file (WINE - *`USER\AppData\Local\Blizzard\Hearthstone\`* or Windows - *`%LocalAppData%/Blizzard/Hearthstone`*) in a text editor.


* "settings.ini" handles most of the bots settings and preferences. 
<details><summary><i>Click here for a default settings.ini file</i></summary>
[BotSettings]<br>
monitor = 1<br>
resolution = 1920x1080<br>
logs = True<br>
location = Felwood<br>
mode = Normal<br>
level = 25<br>
preferelite = False<br>
notificationurl =<br>
MouseSpeed = 0.2<br>
GameDir = C:\Program Files (x86)\Hearthstone<br>
preferbooncaster = False<br>
preferboonfighter = False<br>
preferboonprotector = False<br>
preferprotector = False<br>
preferfighter = False<br>
prefercaster = False<br>
waitForEXP = True<br>
quitBeforeBossFight = False<br>
stopAtBossFight = False<br>
preferPassiveTreasures = True<br>
</details>

* "combo.ini" is to configure Mercenary attack rotations.
<details><summary><i>Click here for a default combo.ini file</i></summary>
[Mercenary]<br>
Alexstrasza=1,3<br>
Anduin Wrynn=1,2<br>
Antonidas=1<br>
Aranna Starseeker=2,3,1<br>
Baine Bloodhoof=1<br>
Balinda Stonehearth=1,2,3:chooseone=2<br>
Baron Geddon=2<br>
Blademaster Samuro=1,3<br>
Blink Fox=1,1,2<br>
Brann Bronzebeard=1,2,3<br>
Brightwing=1<br>
Bru'kan=1,1,3<br>
C'Thun=1,2<br>
Cairne Bloodhoof=1<br>
Captain Galvangar=1,3,2<br>
Captain Hooktusk=1,2,3<br>
Cariel Roame=2,1<br>
Chi-Ji=1,1,3<br>
Cookie, the Cook=1<br>
Cornelius Roame=1,2,2<br>
Deathwing=1,2,3<br>
Diablo=1,2,3,2,3,2,3<br>
Edwin, Defias Kingpin=1,2,3<br>
Elise Starseeker=1,2,3<br>
Eudora=1,2<br>
Fathom-Lord Karathress=1,2<br>
Kazakus, golem shaper=1<br>
Garona Halforcen=1,2,3<br>
Garrosh Hellscream=1,3<br>
Genn Greymane=2,3,1<br>
Gruul=1,2,3<br>
Grommash Hellscream=2,3<br>
Guff Runetotem=2<br>
Illidan Stormrage=1,3,2<br>
Jaina Proudmoore=1,3,2<br>
King Krush=1,2,3<br>
King Mukla=1,3<br>
Kurtrus Ashfallen=1,3,2,3,2<br>
Lady Anacondra=1<br>
Lady Vashj=1,2,3<br>
Leeroy Jenkins=1,2,3<br>
Lokholar the Ice Lord=1<br>
Long'xin=1<br>
Lord Jaraxxus=3,2,1<br>
Lord Slitherspear=1,2,3<br>
Lorewalker Cho=1,2,3<br>
Malfurion=1<br>
Mannoroth=1,3<br>
Millhouse Manastorm=1,1,2<br>
Morgl the Oracle=1,2<br>
Mr. Smite=1<br>
Murky=1,3<br>
Mutanus=1,2,2,2,2,2,2,2<br>
Natalie Seline=1,3<br>
Neeru Fireblade=1,1,3<br>
Nefarian=1,3<br>
Nemsy Necrofizzle=1,3,2<br>
Niuzao=1,3<br>
Patches the Pirate=1,2,3<br>
Prince Malchezaar=1,2,3<br>
Old Murk-Eye=1,2,3,2,3,2,3<br>
Onyxia=1,3<br>
Prophet Velen=1,3<br>
Queen Azshara=1,2,3<br>
Ragnaros=2<br>
Rathorian=1,2,2,3<br>
Rattlegore=1,2,3<br>
Rokara=1,3<br>
Scabbs Cutterbutter=1,2:chooseone=2<br>
Sir Finley=1,3,2<br>
Sinestra=1,3,2<br>
Sky Admiral Rogers=1,3<br>
Sneed=1,2<br>
Sylvanas Windrunner=1,1,3<br>
Tamsin Roame=1<br>
Tavish Stormpike=1<br>
Tess Greymane=1,2,3<br>
The lich king=1,2<br>
Thrall=1<br>
Tidemistress Athissa=1,1,3,3<br>
Trigore the Lasher=2<br>
Tyrael=1,3,2<br>
Tyrande Whisperwind=1,2<br>
Valeera Sanguinar=1,2,3<br>
Vanessa VanCleef=1<br>
Vanndar Stormpike=1,1,3<br>
Varden Dawngrasp=1<br>
Varian Wrynn=3<br>
Varok Saurfang=1,2<br>
Vol'jin=1,2<br>
War Master Voone=1,2,3<br>
Wrathion=1,2,3<br>
Yogg-Saron=1,2<br>
Yu'lon=1,2<br>
Xuen=1,3<br>
Xyrella=1,3<br>
Yrel=1,2,3<br>
Ysera=1,2,3<br>
Y'Shaarj=1,2<br>
Uther Lightbringer=1,3,2<br>
Zar'jira, the Sea Witch=1,3,2<br>

[Neutral]<br>
Bladehand Berserker=1<br>
Boggy=1<br>
Devilsaur=1<br>
Dragonmaw Poacher=1<br>
Drakonid=1<br>
Eudora's Cannon=1<br>
Elementium Terror=1<br>
Fathom Guard=1<br>
Fel Infernal=1<br>
Felfin Navigator=1<br>
Giantfin=1<br>
Greater Golem=1<br>
Grounding Totem=1<br>
Hozen Troublemaker=1<br>
Huffer=1<br>
Hulking Overfiend=1<br>
Hungry Naga=1<br>
Imp Familiar=2<br>
Jade Golem=1<br>
Lesser Fire Elemental=2<br>
Lesser Water Elemental=1<br>
Marching Murlocs=1<br>
Misha=1<br>
Mogu Conqueror=1<br>
Mukla's big brother=1<br>
Nightmare Viper=1<br>
Patchling=1<br>
Pufferfisher=1<br>
Saurok Raider=1<br>
Spawn of N'Zoth=1<br>
Spud M.E.=1<br>
Stonemaul Banner=2<br>
Superior Golem=1<br>
Void Consumer=1<br>
Water Elemental=1<br>
Warlord Parjesh=1<br>
Wavethrasher=1<br>

\# below, specific boss fight (ex: Air Elemental)
\#[Air Elemental]<br>
\#_handselection=Balinda Stonehearth+Baron Geddon+Ragnaros<br>
\#Balinda Stonehearth=1<br>
\#Baron Geddon=2<br>
\#Ragnaros=2<br>

</details>

* "log.config" helps us track what's on the board.
<details><summary><i>Click here for a default log.config file</i></summary>
[Power]<br>
LogLevel=1<br>
FilePrinting=True<br>
ConsolePrinting=False<br>
ScreenPrinting=False<br>
Verbose=True<br>
[Achievements]<br>
LogLevel=1<br>
FilePrinting=True<br>
ConsolePrinting=False<br>
ScreenPrinting=False<br>
Verbose=False<br>
[Arena]<br>
LogLevel=1<br>
FilePrinting=True<br>
ConsolePrinting=False<br>
ScreenPrinting=False<br>
Verbose=False<br>
[FullScreenFX]<br>
LogLevel=1<br>
FilePrinting=True<br>
ConsolePrinting=False<br>
ScreenPrinting=False<br>
Verbose=False<br>
[LoadingScreen]<br>
LogLevel=1<br>
FilePrinting=True<br>
ConsolePrinting=False<br>
ScreenPrinting=False<br>
Verbose=False<br>
[Gameplay]<br>
LogLevel=1<br>
FilePrinting=True<br>
ConsolePrinting=False<br>
ScreenPrinting=False<br>
Verbose=False<br>
[Zone]<br>
LogLevel=1<br>
FilePrinting=true<br>
ConsolePrinting=false<br>
ScreenPrinting=false<br>
</details>

To change the group's name (default: Botwork), follow these steps:
1. Create a screenshot in-game on the "Choose a Party" screen.
2. Put the screenshot in the MFB directory: `conf/user/<resolution>/buttons/group_name.png`
3. The file should be similar to `files/1920x1080/buttons/group_name.png`.

## Starting the bot

If you encounter the following errors:

- "SetForegroundWindow error": It means there is another foreground window from another process. This can occur when using the "windows" key on the keyboard to open the Window Menu. Close the other window to resolve the issue.

- "cp949 error": This error is likely to occur if you are using a Korean version of Windows. Refer to issue #154 for a solution.

- "AHK Not Installed": This error is not a problem. Previous versions of MFB used AHK, but now it installs win32gui for new Windows users.

- "'pip' is not recognized as an internal or external command, operable program or batch file.": During Python installation, make sure to select "Add Python [...] to PATH" option. Additionally, it's recommended to disable the long path limitation.

- "Settings file is missing section 'BotSettings'": Run conf/user/config.py or edit a conf/user/settings.ini file  the `conf/user/settings.sample.ini` file to `conf/user/settings.ini` to resolve this error. Read the settings wiki page for configuring user parameters and ensure to set the mandatory settings.

- "The mouse pointer doesn't move at all (Windows)": Starting the .bat file as an administrator might resolve this issue for some users. If you encounter an error like "No such file or directory," refer to the solution below:
<details><summary><i>Run as Admin</i></summary>
To start the bot as an administrator, follow these steps:<br>
1. Start CMD as an Admin.<br>
2. In the Command Prompt, type `C:` if MFB is installed in the "C:" drive. Adjust the drive letter accordingly if it's installed in a different location.<br>
3. If you are in *`C:\WINDOWS\system32`*, type *`cd ..\..`* to navigate to the root of your drive ("C:" or "D:" or "E:" etc.)<br>
4. Go to the MFB directory by typing *`cd \my\path\to\Mercenaries-Farm-Bot\`*<br>
5. Start the *`HSbotRunner.bat`* file from there.
</details>
- "No such file or directory":

  - For installing requirements: If you see an error like `ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements_win.txt'`, make sure you are running the command from the correct directory.

  - For running *`main.py`*: If you see an error like *`C:\Users\user\AppData\Local\Programs\Python\Python310\python.exe`*: can't open file *`C:\Windows\system32\main.py`*: [Errno 2] No such file or directory`, try running the bot as a regular user. If it still doesn't work, refer to solution below.

<details><summary><i>Run as Admin</i></summary>
To start the bot as an administrator, follow these steps:<br>
1. Start CMD as an Admin.<br>
2. In the Command Prompt, type `C:` if MFB is installed in the "C:" drive. Adjust the drive letter accordingly if it's installed in a different location.<br>
3. If you are in *`C:\WINDOWS\system32`*, type *`cd ..\..`* to navigate to the root of your drive ("C:" or "D:" or "E:" etc.)<br>
4. Go to the MFB directory by typing *`cd \my\path\to\Mercenaries-Farm-Bot\`*<br>
5. Start the *`HSbotRunner.bat`* file from there.
</details>

# If you would like to support [@Efemache](https://github.com/Efemache) for their great work:

## Send a quick tip
You can give them a quick tip at their [Ko-Fi](https://ko-fi.com/mercenariesfarm) page.

## Send Crypto:
If you prefer to support using crypto, you can send your contribution to the following addresses:

|    Platform           | Address | QR Code | 
| :------------         | :-------------:|  :-------------:|  
| Bitcoin (BTC)         | 3L4MJh6JVrnHyDDrvrkZQNtUytYNjop18f | ![BTC](https://user-images.githubusercontent.com/56414438/162740117-eeebb1ef-2971-40d3-8e8f-a39fa51e8c6e.png) |
| Ethereum (ETH) or Binance Smart Chain (BNB/BUSD) (*)| 0x6Db162daDe8385608867A3B19CF1465e0ed7c0e2 | ![ETH-BSC](https://user-images.githubusercontent.com/56414438/162740147-39c72409-94f3-4871-b9e5-a782ab9c2522.png) |

 (\*) Note: Ethereum (ETH) and Binance Smart Chain (BNB/BUSD) share the same address.
 
 (\*) If you send your contribution in a different ERC-20 token on the Ethereum blockchain or a different BEP-20 token on the Binance Smart Chain, please inform us accordingly.

### Roadmap
1. Write better logic for catching where MFB is in it's routine to better assist with reconnects and sustaining productivity.
2. Create a more intuitive pause/resume system.
3. Create better logging and exception handling for troubleshooting.
4. Build upon the Treasure preference system, and get more data and screenshots for treasures.
5. Implement a Convolutional Neural Networks (Alex + Keras + TensorFlow) to have it learn off of recorded play data.
6. More to come...


