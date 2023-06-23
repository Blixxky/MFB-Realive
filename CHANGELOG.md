2023-06-23
----------
1. Changed `HSbotRunner.bat` and `HSbotRunner.sh` to force a Python 3.11 venv.
2. Fixed `/conf/user/config.py` read issues from settings, and adjusting checkboxes appropriately.
3. Configured `/conf/user/config.py` to use the MFB venv and prereqs scripts.

2023-06-22 v1.0.5
-----------------
1. Rewrote `HSbotRunner.bat` and `HSbotRunner.sh` to use prereqs script.
2. Removed all links to AHK since it's deprecated and no longer used.
3. Defined `modules/platforms/window_managers/windows/win32gui_manager.py` left, top, width, height at the module level.
4. Removed `modules/platforms/window_managers/windows/factory.py` unnecessary else statement.
5. Cleaned `modules/platforms/window_managers/windows/factory.py` `_find_window` function.
6. Created `modules/__init__.py` empty list for root handlers, as it was required later in the module.
7. Commented out Zone changes in `/modules/log_board.py` and `/modules/encounter.py` as it was game-breaking for some users.
8. Changed `conf\system\attacks.json` Archmage Khadgar 2nd ability to choose target. Changed #2 bool to true.
9. Changed `conf\system\combo.ini` Prince Malchezaar=1,3,2 from Prince Malchezaar=1,2,3.
10. Changed `conf\user\config.py` combo.ini info upon creation.
11. Rewrote `modules/bounty.py` `goToEncounter` into multiple helper functions.
12. Rewrote `modules/encounter.py` `parse_ability_setting` function.
13. Rewrote `modules/file_utils.py` `readINI` to not use `_sections`.
14. Removed `modules/file_utils.py` orphan expression `os.path.exists(dstdir) or os.mkdir(dstdir)`.
15. Added `modules/image_utils.py` better exception handling.
16. Removed `modules/image_utils.py` `find_element` unnecessary `elif`.
17. Removed `modules/image_utils.py` `partscreen` `resolution=None`.
18. Rewrote `modules/log_board.py` `LogHSMercs` class into multiple functions.
19. Added `modules/log_board.py` some `__init__` declarations.
20. Added `modules/notification.py` better exception handling.
21. Added `modules/notification.py` `request.urlopen(req)` with statement to properly release resources.
22. Added `modules/travelpoint.py` better exception handling.
23. Added `modules/bounty.py` missing docstrings.
24. Added `modules/encounter.py` missing docstrings.

2023-06-12 v1.0.4 hotfix
-----------------
1. Converted all relative imports to absolute.
2. Organized all imports to be properly sorted unless to do so would break them (config.py)

2023-06-11 v1.0.4
-----------------
1. Updated `conf\user\combo.ini` to add Archimonde, rescued student, drakonid 3 to ability rotations.
2. Updated `conf\system\mercs.json` to add rescued student and drakonid 3.
3. Changed `modules/init.py` `_sections` to `has_section` for `configparser`.
4. Changed `modules/platforms/factory.py` `elif` Linux statement to `if`.
5. Replaced `modules/platforms/factory.py` `Exception` with a more specific `ValueError` exception on line 13.
6. Changed `modules/platforms/factory.py` unnecessary `else` to `elif` on line 8 to address the `no-else-return` linting issue.
7. Changed `modules/platforms/window_managers/windows/win32gui_manager.py` relative imports to absolute.
8. Defined `modules/platforms/window_managers/windows/win32gui_manager.py` global variables 'left', 'top', 'width', and 'height' at the module level.
9. Removed `modules/platforms/window_managers/windows/win32gui_manager.py` unnecessary `else` statement after the return statement.
10. Addressed `modules/platforms/window_managers/windows/win32gui_manager.py` inconsistency in return statements by having all of them return an expression.
11. Moved `modules/platforms/window_managers/windows/win32gui_manager.py` attribute `_handles` definition inside the `__init__` method.
12. Added `modules/__init__.py` module docstring.
13. Added `modules/platforms/__init__.py` module docstring.
14. Added `modules/platforms/window_managers/base.py` function docstrings.
15. Changed `modules/platforms/window_managers/linux.py` relative imports to absolute.
16. Removed `modules/platforms/window_managers/linux.py` unused argument `BNCount` on line 44.
17. Resolved `modules/platforms/window_managers/linux.py` unnecessary `else` statement on line 86.
18. Defined `modules/platforms/window_managers/linux.py` "win" within the `__init__` method.
19. Removed `modules/settings/conf/conf.py` unused `setting_name`.
20. Removed `modules/settings/conf/settings.py` unnecessary `else` after `raise`.
21. Changed `modules/settings/conf/settings.py` `raise` to use f-string.
22. Added `modules/battlenetloop.py` `found_element` variable.
23. Fixed `modules/battlenetloop.py` import order.
24. Cleaned `modules/bounty.py` import statements.
25. Simplified `modules/bounty.py` function by reducing the number of branches and statements (Line 106).
26. Simplified `modules/bounty.py` the chained comparison in `searchForEncounter()` by removing unnecessary parentheses (Line 200).
27. Changed `modules/bounty.py` string concatenation in `travelToLevel()` to use explicit concatenation instead of implicit concatenation (Line 286).
28. Changed `modules/bounty.py` string formatting in `send_slack_notification()` to use an f-string instead of formatting a regular string (Line 333).
29. Removed `modules/bounty.py` unnecessary return statement at the end of the `quitBounty()` function (Line 356).
30. Removed `modules/campfire.py` `toggle_campfire_screen()` removed unnecessary `elif` and `else`.
31. Removed `modules/campfire.py` `look_at_campfire_completed_tasks()` removed unnecessary `else` after `break`.
32. Modified `modules/encounter.py` the `__init__` method to take any number of keyword arguments.
33. Rewrote `modules/encounter.py` class `Enemies` to use a `namedtuple`.
34. Rewrote `modules/encounter.py` class `Board` to use a `namedtuple`.
35. Changed `modules/encounter.py` `log.debug` to use lazy `%` formatting (Line 783).
36. Moved `modules/encounter.py` `self.coord_y` to inside `__init__`.
37. Cleaned `modules/encounter.py` import list.
38. Added `modules/encounter.py` `selectCardsInHand` docstring.
39. Added `modules/encounter.py` `cardsInHand` docstring.
40. Added `modules/encounter.py` `execute_action_sequence` docstring.
41. Added `modules/encounter.py` `find_enemies` docstring.
42. Added `modules/exceptions.py` module docstring and class docstrings.
43. Changed `modules/file_utils.py` `elif` to use raw string on lines 32 and 34.
44. Added `modules/file_utils.py` encoding types to open functions.
45. Added `modules/file_utils.py` `copy_dir_and_func_files` docstring.
46. Converted `modules/game.py` lines 22 and 24 to f-strings.


2023-06-09 v1.0.3
-----------------
1. Changed `log.info` string to use lazy `%` formatting.
2. Changed `modules/platforms/platforms.py` `log.info` string to use lazy `%` formatting.
3. Changed `modules/conf/conf.py` `log.info` string to use lazy `%` formatting.
4. Changed `modules/conf/settings.py` `log.error` string to use lazy `%` formatting.
5. Changed `modules/conf/settings.py` `log.info` string to use lazy `%` formatting.
6. Changed `modules/conf/settings.py` raise `SettingsError` string to use lazy `%` formatting.
7. Changed `modules/conf/settings.py` raise `MissingGameDirectory` string to use lazy `%` formatting.
8. Modified `modules/conf/settings.py` the `Zone.log` path builder. Line 79.
9. Changed `modules/bounty.py` `log.info` strings to use lazy `%` formatting (line 82, 253).
10. Changed `modules/bounty.py` `log.debug` strings to use lazy `%` formatting (line 197, 211).
11. Changed `modules/bounty.py` `json.dumps` string to use lazy `%` formatting.
12. Changed `modules/encounter.py` `log.debug` strings to use lazy `%` formatting (line 90, 115, 171, 172, 249, 366, 368, 783, 832).
13. Changed `modules/encounter.py` `log.warning` string to use lazy `%` formatting.
14. Changed `modules/encounter.py` `log.info` strings to use lazy `%` formatting (line 283, 515, 573, 667, 670, 767, 774, 787).
15. Changed `modules/encounter.py` `log.error` string to use lazy `%` formatting.
16. Changed `modules/game.py` `log.info` string to use lazy `%` formatting.
17. Changed `modules/gameloop.py` `log.error` string to use lazy `%` formatting.
18. Removed `modules/gameloop.py` commented `time.sleep` commands and a disabled function.
19. Changed `modules/image_utils.py` `log.error` string to use lazy `%` formatting (line 60, 100, 102).
20. Changed `modules/image_utils.py` `log.info` string to use lazy `%` formatting (line 201).
21. Changed `modules/image_utils.py` `print` string to use lazy `%` formatting (line 204).
22. Changed `modules/image_utils.py` `log.debug` string to use lazy `%` formatting.
23. Changed `modules/notification.py` `log.info` strings to use lazy `%` formatting (line 44, 76).
24. Changed `modules/notification.py` `log.error` strings to use lazy `%` formatting (line 46, 48, 50, 78, 80, 82).
25. Changed `modules/resolution.py` `log.error` string to use lazy `%` formatting.
26. Changed `modules/resolution.py` `log.debug` string to use lazy `%` formatting.
27. Changed `modules/travelpoint.py` `log.error` string to use lazy `%` formatting.
28. Changed `modules/treasure.py` `log.debug` string to use lazy `%` formatting.
29. Changed `main.py` `log.info` strings to use lazy `%` formatting (line 22, 41).
30. Changed `main.py` `log.error` string to use lazy `%` formatting.


2023-06-08 v1.0.2
-----------------
1. Added module docstring to main.py
2. Added module docstring to /modules/bounty.py
3. Added function docstring to /modules/bounty.py searchForEncounter
4. Added module docstring to /modules/campfire.py
5. Added function docstring to /modules/campfire.py toggle_campfire_screen
6. Added function docstring to /modules/campfire.py check_party_tasks
7. Added function docstring to /modules/campfire.py check_visitor_tasks
8. Added function docstring to /modules/campfire.py claim_task_reward
9. Added module docstring to /modules/encounter.py
10. Added class docstring to /modules/encounter.py Enemies
11. Added class docstring to /modules/encounter.py Board
12. Added function docstring to /modules/encounter.py select_enemy_to_attack
13. Edited function docstring to /modules/encounter.py select_random_enemy_to_attack
14. Edited function docstring to /modules/encounter.py priorityMercByRole
15. Edited function docstring to /modules/encounter.py pickBestAllyToBuff
16. Edited function docstring to /modules/encounter.py get_ability_for_this_turn
17. Added function docstring to /modules/encounter.py parse_ability_setting
18. Added function docstring to /modules/encounter.py didnt_find_a_name_for_this_one
19. Edited function docstring to /modules/encounter.py select_ability
20. Edited function docstring to /modules/file_utils.py readjson
21. Edited function docstring to /modules/file_utils.py read_ini_to_dict
22. Edited function docstring to /modules/file_utils.py parseINI
23. Edited function docstring to /modules/file_utils.py readINI
24. Edited function docstring to /modules/file_utils.py writeINI
25. Added module docstring to /modules/game.py
26. Edited function docstring to /modules/game.py defaultCase
27. Added module docstring to /modules/gameloop.py
28. Added module docstring to /modules/image_utils.py
29. Edited function docstring to /modules/image_utils.py get_resolution
30. Edited function docstring to /modules/image_utils.py resize
31. Edited function docstring to /modules/image_utils.py get_gray_image
32. Edited function docstring to /modules/image_utils.py find_element_from_file
33. Edited function docstring to /modules/image_utils.py partscreen
34. Edited function docstring to /modules/image_utils.py find_element_center_on_screen
35. Added module docstring to /modules/log_board.py
36. Edited function docstring to /modules/log_board.py LogHSMercs
37. Added function docstring to /modules/log_board.py find_battle_start_log
38. Added function docstring to /modules/log_board.py follow
39. Added function docstring to /modules/log_board.py get_zonechanged
40. Added function docstring to /modules/log_board.py start
41. Added function docstring to /modules/log_board.py stop
42. Added function docstring to /modules/log_board.py cleanHand
43. Added function docstring to /modules/log_board.py getHand
44. Added function docstring to /modules/log_board.py cleanBoard
45. Added function docstring to /modules/log_board.py getMyBoard
46. Added function docstring to /modules/log_board.py getEnemyBoard
47. Added module docstring to /modules/mouse_utils.py
48. Added function docstring to /modules/mouse_utils.py mouse_click
49. Added function docstring to /modules/mouse_utils.py mouse_scroll
50. Added function docstring to /modules/mouse_utils.py mouse_position
51. Added function docstring to /modules/mouse_utils.py move_mouse_and_click
52. Added function docstring to /modules/mouse_utils.py move_mouse
53. Edited function docstring to /modules/mouse_utils.py mouse_random_movement
54. Added module docstring to /modules/notification.py
55. Edited function docstring to /modules/notification.py send_notification
56. Edited function docstring to /modules/notification.py send_slack_notification
57. Added module docstring to /modules/resolution.py
58. Edited function docstring to /modules/resolution.py resize_image
59. Added function docstring to /modules/resolution.py gen_images_new_resolution
60. Added module docstring to /modules/travelpoint.py
61. Added function docstring to /modules/travelpoint.py get_travelpoints_list
62. Edited function docstring to /modules/travelpoint.py travelpointSelection
63. Added module docstring to /modules/treasure.py
64. Edited function docstring to /modules/treasure.py chooseTreasure
65. Added module docstring to /modules/utils.py
66. Added module docstring to /modules/platforms/factory.py
67. Added function docstring to /modules/platforms/factory.py get_window_manager
68. Added module docstring to /modules/platforms/platforms.py
69. Added function docstring to /modules/platforms/platforms.py find_os
70. Added module docstring to /modules/platforms/window_managers/base.py
71. Added function docstring to /modules/platforms/window_managers/base.py WindowMgr
72. Added module docstring to /modules/platforms/window_managers/linux.py get_window_geometry
73. Edited function docstring to /modules/platforms/window_managers/linux.py WindowMgrLinux
74. Edited function docstring to /modules/platforms/window_managers/linux.py find_game
75. Added module docstring to /modules/platforms/window_managers/windows/factory.py 
76. Added function docstring to /modules/platforms/window_managers/windows/factory.py get_window_mgr_on_windows
77. Added module docstring to /modules/platforms/window_managers/windows/win32gui_manager.py
78. Edited function docstring to /modules/platforms/window_managers/windows/win32gui_manager.py WindowMgrWindowsWin32Gui
79. Added function docstring to /modules/platforms/window_managers/windows/win32gui_manager.py __init__
80. Edited function docstring to /modules/platforms/window_managers/windows/win32gui_manager.py find_game
81. Added function docstring to /modules/platforms/window_managers/windows/win32gui_manager.py get_window_geometry
82. Edited function docstring to /modules/platforms/window_managers/windows/win32gui_manager.py _window_enum_callback
83. Added function docstring to /modules/platforms/window_managers/windows/win32gui_manager.py _find_window
84. Added function docstring to /modules/platforms/window_managers/windows/win32gui_manager.py _show_window
85. Edited function docstring to /modules/platforms/window_managers/windows/win32gui_manager.py _set_foreground
86. Added module docstring to /modules/settings/conf/conf.py
87. Added function docstring to /modules/settings/conf/conf.py set_settings
88. Added function docstring to /modules/settings/conf/conf.py initusersettings
89. Added function docstring to /modules/settings/conf/conf.py get_config
90. Added function docstring to /modules/settings/conf/conf.py update_settings_with_file
91. Added function docstring to /modules/settings/conf/conf.py log_settings_dict
92. Added function docstring to /modules/settings/conf/conf.py log_setting_dict_helper
93. Added module docstring to /modules/settings/conf/settings.py
94. Added function docstring to /modules/settings/conf/settings.py add_bot_settings
95. Added function docstring to /modules/settings/conf/settings.py get_system_user_settings
96. Edited function docstring to /modules/settings/conf/settings.py get_settings
97. Edited function docstring to /modules/settings/conf/settings.py copy_config_from_sample_if_not_exists
98. Removed references to bot_speed in multiple files as it's deprecated. Remove bot_speed from your settings.ini if it exists.




2023-05-31
----------
Bug fix:
- Blizzard updated the way zone.log is generated, it's now in it's own timestamped directory.  Fix by [@spxtctre](https://github.com/spxctreofficial)

2023-05-28
----------
New:
-  Added MFB Config Engine. A GUI for settings.ini configuration. Run conf/user/config.py or config.pyw (no console)
		1. Loads settings.ini file if it exists, creates it with defaults if it does not.
		2. If combo.ini doesn't exist, it's created with defaults.
		3. It checks for log.config and creates one if it does not exist, or appends the necessary section if not found in an existing file.
		4. It will only show the appropriate levels for each Zone and Mode, and uses the same naming convention as MFB. i.e. Winterspring Heroic 30, 30b, 30c, ...
		5. If you are missing all the files, it may not create all of them and configure all of the settings first launch, launch it a second time (known).

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
