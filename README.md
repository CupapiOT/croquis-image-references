# DIY Croquis - Image References

A desktop application to help artists practice croquis (quick sketching) 
using their own references offline.

## Description

![Image References App Showcase](https://github.com/user-attachments/assets/ad36978a-c101-48f2-97a4-77fb0317bda0)

A simple desktop application that anyone can use to practice croquis, using their own files from folders within their computer. The basic functionality &mdash; a timer and the ability to load files &mdash; are easy and intuitive to use.
Of course, you could also simply use it to go through your images one at a time.

This app was originally requested for the author to make by the author's brother; this app has now helped him and a few other artists practice croquis offline using their own set of references.

**Note**: This app offers a smooth-enough experience for regular (intended) use, but may run into performance issues when certain buttons/commands are spammed or when loading too many folders at once.

### Features

* ⏱️ A complete timer with hour, minute, and seconds settings, with a play, pause, and reset timer buttons.
* 🔃 Arrow-buttons to move to the next, previous, first, and last image in the queue.
* 🌗 Light and dark mode themes.
* ♾️ Supports uploading a large number of folders (As many as your PC can handle).
* ↔️ An option to switch to a new folder, discarding the previous loaded folders.
* 🖼️ Supports `.jpg`, `.jpeg` and `.png` files.
* ⌨️ Convenient keyboard shortcuts for all the UI elements.
* 🔝 An option to set a limit on how many images you'd like to go through.
* 💪 A responsive layout.
* ⚙️ Multiple toggle-able settings:
  * Countdown between images,
  * Randomizing folder queue,
  * Folder looping,
  * Alert when folder is complete,
  * Load last-used timer settings,
  * Load last-loaded folders.

## Getting Started

### Dependencies

All dependencies are listed in the [requirements.txt](requirements.txt) file.

Note: You may not need the newest versions of these modules, as this project was originally created in July 2023.
* `python 3.11` or above
* `customtkinter`
* `Pillow`
* `tkinter_tooltip` 

### Installing

* Fork the repository.
* Clone your fork locally.
* Run `pip install -r requirements.txt` to install dependencies.

### Executing and using the program

* Run the `main.py` file.
* To use the program, simply open a folder from your computer from the settings icon inside the program and set the timer up as you please, then click the start button. 
* You can change the time while it's going by pressing the pause button and editing the time, or you can reset the timer to when you started it via the reset timer button.
* You can toggle between light and dark mode by clicking the settings icon and pressing the button to switch between them.
* Adjust other settings, such as image queue randomization or folder looping, by toggling the options in the settings menu.

## Help

Please read the [help.txt](help.txt) file for help on troubleshooting and a copy of the above guide on how to get started, and for a full list of keyboard shortcuts.

If you're facing other issues not present within the file, feel free to [open an issue](https://github.com/CupapiOT/croquis-image-references/issues) on GitHub.

## Contributions

Contributions are welcome! If you’d like to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-XYZ`).
3. Make your changes and test thoroughly.
4. Submit a pull request.

**Refactors and clean-ups** are especially appreciated, as the code could use some improvements in readability and structure (especially around the `if` statements!). Please make sure to document your changes and adhere to the existing code style as much as possible. 

If you’re unsure about something or want to suggest a feature, feel free to [open an issue](https://github.com/CupapiOT/ImageReferences/issues), and we can discuss it!

## Author

[@CupapiOT](https://github.com/CupapiOT)

## Version History

**Note**: Versions prior to 1.3.17 did not use Git for version control.

* 1.3.17
    * Fixed a bug related to input-handling in the timer.
    * See [release history](CHANGELOG.md?plain=1#L8) for full details.
* 1.3.16
    * Fixed a visual bug where the program displayed the incorrect status.
    * See [release history](CHANGELOG.md?plain=1#L18) for full details.
* 1.3.15
    * Added save-load system.
    * Added two settings for new save-load system.
    * Added keyboard shortcuts as alternatives to already available ones.
    * Fixed a bug where the program doesn't detect an image with a non-lowercase file extension.
    * See [release history](CHANGELOG.md?plain=1#L22) for full details.
* 1.29.29
    * Added dark mode.
    * Added image-limit option.
    * Added keyboard short-cut hints in settings menu.
    * Re-added previously removed feature.
    * See [release history](CHANGELOG.md?plain=1#L39) for full details.
* 1.0.8
    * Added an "Add New Folder to Current Queue" menu option in the folder 
      menu.
    * Various bug fixes, see [release history](CHANGELOG.md?plain=1#L56) for full details.
* 1.0.0
    * Improvements and bug-fixes (Not Documented).
* 0.9.13
    * Add support for uploading files in multiple directories.
    * Other improvements and bugfixes (Not Documented).
* 0.9.11
    * Initial release.

## License

This project is licensed under the GNU GPL v3 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

### Beta Tester
My brother.

### Special Thanks
My brother &mdash; it was originally him that asked me to make this application for him to use.
