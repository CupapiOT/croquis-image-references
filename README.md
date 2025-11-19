# Croquis Image References

A desktop application to help artists practice croquis (quick sketching)
using their own references offline.

## Description

![Image References App Showcase](https://github.com/user-attachments/assets/ad36978a-c101-48f2-97a4-77fb0317bda0)

A simple desktop application that anyone can use to practice croquis, using
their own files from folders within their computer. The basic functionality
&mdash; a timer and the ability to load files &mdash; are easy and intuitive to
use.

Of course, you could also simply use it to go through your images one at a
time.

This app was originally requested for the author to make by the author's
brother; this app has now helped him and a few other artists practice croquis
offline using their own set of references.

**Note**: This app offers a smooth-enough experience for regular (intended)
use, but may run into performance issues when certain buttons/commands are
spammed or when loading too many folders at once.

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

* `python 3.12` or above
* `customtkinter`
* `Pillow`
* `tkinter_tooltip`

## Installation

### For Users (Recommended)

Download the latest release for your operating system:

1. Go to the [Releases page](https://github.com/CupapiOT/croquis-image-references/releases)
2. Download the appropriate file for your platform:
   * **Windows**: `windows_build.zip`
   * **macOS**: `macos_build.zip`
   * **Linux**: `linux_build.zip`
3. Extract the zip file
4. Run the `Image References` executable

No Python installation required!

### For Developers

If you want to run from source or contribute to the project:

1. Fork the repository
2. Clone your fork locally:

```bash
   git clone https://github.com/CupapiOT/croquis-image-references.git
   cd croquis-image-references
```

3. Install Python 3.12 or higher
4. Install dependencies:

```bash
   pip install -r requirements.txt
```

5. Run the program:

```bash
   python main.py
```

## Using the Program

* **Open a folder**: Click the settings icon (bottom left corner) and select a folder containing your reference images
* **Set the timer**: Configure how long each image should display for
* **Start viewing**: Click the start button (or `ctrl + s`) to begin the slideshow; press the arrow buttons/keys to go to other images
* **Pause/Resume**: Click the pause button (or `space`) to stop the timer; you can edit the time while paused
* **Reset**: Use the reset button (or `ctrl + r`) to restart from the beginning of your session
* **Toggle appearance**: Switch between light and dark mode in the settings menu
* **Customize behavior**: Enable/disable image randomization, folder looping, maximum number of images to show, etc. in settings

## Help

Please read the [help.txt](help.txt) file for help on troubleshooting, and the full list of keyboard shortcuts.

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

See [release history](CHANGELOG.md) for full details on each version.

**Note**: Versions prior to 1.3.18 did not use Git for version control.

* 1.3.20
  * Prepared the project for release using GitHub actions.
  * These changes were made across multiple commits.
  * Skipped 1.3.19 as it was an irrelevant intermediate build.
* 1.3.18
  * Increased robustness of error-handling for users editing the `preferences.txt` file.
  * See [the commit](https://github.com/CupapiOT/croquis-image-references/commit/3e1256b80efc4659e41420ce49b84ae78fec6c37).
* 1.3.17
  * Fixed a bug related to input-handling in the timer.
* 1.3.16
  * Fixed a visual bug where the program displayed the incorrect status.
* 1.3.15
  * Added save-load system.
  * Added two settings for new save-load system.
  * Added keyboard shortcuts as alternatives to already available ones.
  * Fixed a bug where the program doesn't detect an image with a non-lowercase file extension.
* 1.29.29
  * Added dark mode.
  * Added image-limit option.
  * Added keyboard short-cut hints in settings menu.
  * Re-added previously removed feature.
* 1.0.8
  * Added an "Add New Folder to Current Queue" menu option in the folder
    menu.
  * Various bug fixes.
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

- My brother - he originally commissioned me to make this application for his professional daily use.
- My artist-friends in real life for trying the app for themselves.
