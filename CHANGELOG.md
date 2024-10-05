# Release History

## 1.3.18 - 2024-10-05

### Additions
 - Increased robustness of error-handling for users editing the `preferences.txt` file for a more user-friendly experience. See [the commit](https://github.com/CupapiOT/croquis-image-references/commit/3e1256b80efc4659e41420ce49b84ae78fec6c37).

**Note**: Versions prior to 1.3.18 did not use Git for version control. The changes you see below are taken from `README.txt` files from their respective versions (not available on GitHub).

## 1.3.17 - 2024-04-14

### Fixes
 - Fixed the timers not recovering wrongly inputted values in the hour, minute, and second timers. It used to only pay attention to the hour timers.

### Codebase Refactors
 - Manually reformatted every line of code to follow PEP8's 79-character limit for code and 72-character limit for comment/docstring lines.



## 1.3.16 - 2024-04-07

### Fixes
 - Fixed a bug where the text at the bottom of the image displayer incorrectly displayed "loop" when the program did not have the "Loop Folder" setting turned on, and vice versa. 



## 1.3.15 - 2023-11-17

### Additions
 - Added a save load system. The program now saves your settings, from your directories*, the image limit you set, all the way to the timer's time that you set up**.
 - With the new save load system, there are now two extra settings options at the bottom of the settings menu to choose whether you save your last used directory or not, and an option to choose whether you save your last used timer time or not.
 - Added two new shortcuts: Ctrl + O and Ctrl + Shift + O. They're both just alternatives to the shortcuts Alt + O (Open Folder) and Alt + Shift + O (Switch to New Folder) respectively.

### Fixes
 - Fixed an issue where the program didn't detect image files that ended in an extension with non-lowercase capitalization.

### Notes
*The way the program saves your current directories isn't done perfectly, it only opens/loads the directories you last opened in the same order you did the last time you opened the program. This WILL reshuffle the directories that the program loads as the program loads them if you have the "Randomize Folder Queue" setting turned on.

**To save the amount of time you inputted into the timer, you have to start the timer in order for it to save it.



## 1.2.29 - 2023-09-25

### Additions
 - Re-added the "Open Folder" menu option in the folder menu in the form of a "Switch to New Folder" button that's disabled on first launch.
 - Added a dark mode along with a button that switches between light and dark mode in the settings menu. The starting theme on launch will be your system's current theme.
 - Added an option to set an image limit. This image limit is a number you can set in the new settings menu that determines how many images the program will go through in the queue. The default image limit is 'Unlimited'.
 - Added keyboard short-cut hints next to the options in the settings menu, as well as keyboard short-cut hints for the time buttons.

### Changes
 - Moved everything in the folder menu to a settings menu in the bottom left corner of the screen.
 - Changed the (in simplified terms) "foundation" that the program runs on, which took ages but also decreased the file size somehow. In development terms, changed from using `tkinter` and `ttkbootstrap` to `customtkinter`.

### Fixes
 - Fixed a bug where the timer sometimes counts down multiple seconds at once.



## 1.0.8 - 2023-08-21

### Additions
 - Added a "Add New Folder to Current Queue" menu option in the folder menu.

### Fixes
 - Fixed an issue where the timer lags the entire program while counting down.
 - Fixed a bug where cancelling a folder selection selects the image folders within the  project itself.
 - Fixed a bug where the image-change shortcut hotkeys weren't being disabled when the program was counting down for the next image.
 - Fixed several bugs related to selecting a new folder while time is paused, counting down, and while it's counting down 3 seconds for the next image.



## Earlier Versions (Undocumented)

**Note**: The dates beside the version numbers are likely to be false. They were taken from the "modified" property of their respective `Image References.exe` files.

### 1.0.0 - 2023-08-18
 - Improvements and bug-fixes (Not Documented).

### 0.9.13 - 2023-08-17
 - Add support for uploading files in multiple directories.
 - Other improvements and bugfixes (Not Documented).

### 0.9.11 - 2023-08-16
 - Initial release.
