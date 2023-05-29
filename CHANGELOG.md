
2023-05-28
----------
New:
-  Added MFB Config Engine. A GUI for settings.ini configuration. Run conf/user/config.py or config.pyw (no console)
		1. Loads settings.ini file if it exists, creates it with defaults if it does not.
		2. If combo.ini doesn't exist, it's created with defaults.
		3. If it can locate hearthstone.exe at the default game directory for Windows (C:\Program Files (x86)\Hearthstone), it will use it as the Game Dir automatically.
		4. If it locates the "%LocalAppData%/Blizzard/Hearthstone" directory, it checks for log.config and creates one if it does not exist. 
		5. It will only show the appropriate levels for each Zone and Mode, and uses the same naming convention as MFB. i.e. Winterspring Heroic 30, 30b, 30c, ...
		6. If you are missing all the files, it may not create all of them and configure all of the settings first launch, launch it a second time (known).

Bug Fixes/Misc:
- Fixed some typos and case issues (bounty.py, encounter.py)
- Fixed some typos (image_utils.py, game.py, bounty.py, campfire.py, travelpoint.py, treasure.py, encounter.py, gameloop.py, battlenetloop.py)
- Removed tests/unit directory.
- Changed setup.cfg to max line length of 100 for flake8, since some comments triggered it with 88.

2023-03-15
----------

New:
- Battle.net support for 1920x1080 screen resolution

Bug Fixes:
- Board is well detected during first battle; it was broken after last Hearthstone update
- scroll function updated, for Bounty Level selection, as workaround for Windows users
- a font/name change in english prevents bounties.png from working in darkmoon, this cropped version fixes it


2023-02-22
----------

New:
- dedicated environment to install python dependencies
- feature to pause the bot (move mouse in a corner of the screen)

Changes:
- use Python 3.11 (instead of 3.10) - users need to upgrade Python
- output details improved. Users will see less useless logs
- enemies detection improved (useful in Felwood)

Bug Fixes:
- second ability for Lord Godfrey fixed
- second ability for Jandice and Lilian fixed


2023-02-15
----------

New:
- new Travel Point menu (with Boss Rush) support added
- support for new portal (travel point skin) added
- support for faction added
- all types updated
- 6 new mercenaries add
- support for dual-type minion support added
- Arcane Ward, Healing Totem and Stoneclaw Totem added and won't attack

Bug Fixes:
- security update


2023-02-09
----------

New:
- to be able to target a friendly mercenary/minion selected by name (in combo.ini)
- click on reconnect button when Hearthstone shows the pop-in 


2022-12-12
----------

New:
- you can configure combos for a specific enemy/battle (usefull for Boss Battle)
- feature added to select mercenaries from cards in hand (usefull for Boss Battle)


2022-11-28
----------

New:
- select a passive treasure (when MFB doesn't find a known/configured treasure)
- new Mercenary 'Chromie' added
- user can choose (in combo.ini) which cards to pick to put on board
- boon priorization available

Changes:
- Raven Familiar will use second ability and Blue Portal won't attack

Bug Fixes:
- SPUD leaving your side of the board should be well detected. Fixes #21
- Darkmoon zone added
- thresholds updated to improve battles detection on Encounter Map


2022-11-14
----------

New:
- new bounties added (Darkmoon and missing Blackrock)
- trying to support "Bonus loot" button at end of bounty
- Rattlegore (protector) added

Bug Fixes:
- image bounty for Neeru Fireblade wasn't correct
- new images for better battles (encounter map) detection
- update for Jaraxxus (Fel Infernal doesn't have Charge)
- images updated for battle on encounter map (to avoid to click on a disabled battle)


2022-11-07
----------

New:
- new Campfire screen (from 24.6 HS patch) is supported
