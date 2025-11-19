"""Current version: v1.3.20"""

# Import the necessary modules.
import customtkinter as ctk
from tktooltip import ToolTip
from tkinter import filedialog, messagebox, PhotoImage
from PIL import Image, ImageTk
from pathlib import Path
from random import shuffle
from threading import Timer
import ast
import os, sys
import platform
from typing import Any


class App(ctk.CTk):
    def __init__(
        self,
        windows_icon: str,
        linux_icon: str,
        mac_icon: str,
        title: str = "Image References",
        geometry: tuple[int, int] = (600, 500),
        size_changer_sizes: tuple[int, int] = (600, 1000),
        min_height: int = 0,
    ) -> None:
        # setup
        super().__init__()

        # # button colors
        self.button_theme_color = {
            "normal": ("#EB6864", "#1F6AA5"),
            "hover_color": ("#ED7773", "#144770"),
            "disabled": ("#CCCCCC", "#383838"),
        }

        # dictionary for the size changer
        self.size_dict = {
            size_changer_sizes[0]: self.create_normal_layout,
            size_changer_sizes[1]: self.create_wide_layout,
        }

        # geometry settings
        self.mid_window_width = int(self.winfo_screenwidth() / 2 - geometry[0] / 2)
        self.mid_window_height = int(
            self.winfo_screenheight() / 2 - geometry[1] / 2 - 40
        )
        self.geometry(
            f"{geometry[0]}x{geometry[1]}"
            f"+{self.mid_window_width}"
            f"+{self.mid_window_height}"
        )
        self.minsize(list(self.size_dict)[0], int(min_height))

        # title and icon settings
        self.title(title)
        self.set_app_icon(
            windows_icon=windows_icon, linux_icon=linux_icon, mac_icon=mac_icon
        )

        #  widgets in the app
        # # frame declaration
        # # # everything_else_frame to make the image frame appear
        # # # properly at the top
        self.everything_else_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            bg_color="transparent",
            corner_radius=0,
            border_width=0,
        )

        # # # group_up_frame to make sure the timer frame and button
        # # # frame are centered
        self.group_up_frame = ctk.CTkFrame(
            self.everything_else_frame,
            fg_color="transparent",
            bg_color="transparent",
            corner_radius=0,
            border_width=0,
        )

        # dictionary for the default preferences
        self.default_preferences = {
            "directories": [],
            "theme": "system",
            "image_limit": 0,
            "countdown": True,
            "randomize": True,
            "loop": False,
            "alert_queue_complete": False,
            "timer_temp": 30,
            "load_timer_temp": True,
            "load_saved_directories": True,
            "wait_directory_load": 0.0,
        }

        # # save and load system
        self.save_load_system = SaveLoadSystem(
            file_name="preferences",
            extension=".txt",
            default_values=self.default_preferences,
            mutable_keys=False,
        )

        # # widgets (these have to be put after save_load_system)
        self.image_frame = ImageFrame(self)
        self.timer_frame = TimerFrame(self.group_up_frame, window=self)
        self.button_frame = ButtonFrame(
            parent=self.everything_else_frame,
            image_button_parent=self.group_up_frame,
            window=self,
        )
        self.settings_menu = SettingsMenu(self)

        self.size_notifier = SizeNotifier(self, self.size_dict)
        # reset the saved directories if load_saved_directories was
        # previously turned off
        if not self.save_load_system.values["load_saved_directories"]:
            self.save_load_system.values["directories"] = []
            self.save_load_system.save_value(
                input_value=str(self.save_load_system.values),
                file_name=self.save_load_system.file_name,
            )

        # layout that won't change
        self.everything_else_frame.pack()
        self.image_frame.pack_propagate(False)
        self.image_frame.pack(
            side="top", expand=True, fill="both", before=self.everything_else_frame
        )

        # sets the app theme to the last used theme
        ctk.set_appearance_mode(self.save_load_system.values["theme"])

        # check if a directory has been saved, and open it
        if (
            self.save_load_system.values["directories"]
            and self.save_load_system.values["load_saved_directories"]
        ):
            self.timer = Timer(
                interval=float(self.save_load_system.values["wait_directory_load"]),
                function=self.load_saved_dir,
            )
            self.timer.start()

    def set_app_icon(self, windows_icon: str, linux_icon: str, mac_icon: str):
        system = platform.system()

        try:
            if system == "Windows":
                self.iconbitmap(windows_icon)
            elif system == "Linux":
                img = PhotoImage(file=linux_icon)
                self.iconphoto(True, img)
                self._icon_ref = img
            elif system == "Darwin":  # macOS
                img = PhotoImage(file=mac_icon)
                self.iconphoto(True, img)
                self._icon_ref = img
            else:
                img = PhotoImage(file=linux_icon)
                self.iconphoto(True, img)
                self._icon_ref = img

        except Exception as e:
            print(f"Failed to load icon for {system}: {e}")

    def load_saved_dir(self):
        self.timer = None
        temp_directories = self.save_load_system.values["directories"]
        for directory in temp_directories:
            self.open_folder(predetermined_folder=directory)

    def create_normal_layout(self):
        self.button_frame.index_label.pack(side="top", fill="x")
        # repacking everything
        # group_up frame
        self.group_up_frame.pack(expand=True, fill="x")

        # timer Frame
        self.timer_frame.timers_frame.pack(expand=False, fill="both", side="top")
        self.timer_frame.buttons_frame.pack(expand=False, fill="y", side="top")

        # pack the time entry frames, entries, and labels
        # # pack the hour frames
        self.timer_frame.hour_entry.pack(
            ipadx=6, pady=2, side="top", expand=True, fill="x"
        )
        self.timer_frame.hour_label.pack(side="top")

        # # pack the minute frames
        self.timer_frame.minute_entry.pack(
            ipadx=1, pady=2, side="top", expand=True, fill="x"
        )
        self.timer_frame.minute_label.pack(side="top")

        # # pack the second frames
        self.timer_frame.second_entry.pack(
            ipadx=0, pady=2, side="top", expand=True, fill="x"
        )
        self.timer_frame.second_label.pack(side="top")

        self.timer_frame.start_button.pack(
            padx=5, side="left", before=self.timer_frame.pause_button
        )

        # rest of the stuff
        self.button_frame.left_image_control_buttons_frame.pack(
            pady=5, padx=10, side="left", before=self.timer_frame
        )
        self.button_frame.right_image_control_buttons_frame.pack(
            pady=5, padx=20, side="left"
        )

    def create_wide_layout(self):
        # group_up frame
        self.group_up_frame.pack()

        # timer Frame
        self.timer_frame.timers_frame.pack(expand=False, fill="both", side="left")
        self.timer_frame.buttons_frame.pack(expand=False, fill="y", side="left")

        # pack the time entry frames, entries, and labels
        # # pack the hour frames
        self.timer_frame.hour_entry.pack_propagate(False)
        self.timer_frame.hour_entry.pack(
            ipadx=13, pady=2, side="left", expand=True, fill="both"
        )
        self.timer_frame.hour_label.pack(side="left", padx=3)

        # # pack the minute frames
        self.timer_frame.hour_entry.pack_propagate(False)
        self.timer_frame.minute_entry.pack(
            ipadx=13, pady=2, side="left", expand=True, fill="both"
        )
        self.timer_frame.minute_label.pack(side="left", padx=3)

        # # pack the second frames
        self.timer_frame.hour_entry.pack_propagate(False)
        self.timer_frame.second_entry.pack(
            ipadx=13, pady=2, side="left", expand=True, fill="both"
        )
        self.timer_frame.second_label.pack(side="left", padx=3)

        self.timer_frame.start_button.pack(
            padx=5, side="left", before=self.timer_frame.pause_button
        )

        # rest of the stuff
        self.button_frame.left_image_control_buttons_frame.pack(
            pady=5, padx=10, side="left", before=self.timer_frame
        )
        self.button_frame.right_image_control_buttons_frame.pack(
            pady=5, padx=10, side="left"
        )

    def open_folder(self, reset_queue=False, predetermined_folder=None) -> None:
        """Opens a folder and adds all the images inside including all
        the sub-folders' images into a directory.
        """
        try:
            # close the file menu in settings_menu.
            self.settings_menu.close_menu()

            # opens a window for the user to open a folder and resets
            # the current directory if the user chooses to.
            if reset_queue:
                self.image_frame.directory_list = []
                self.save_load_system.values["directories"] = []

            folder = (
                predetermined_folder
                if predetermined_folder is not None
                else (
                    filedialog.askdirectory(
                        title="Select A Folder", initialdir="C:/Users/Pictures"
                    )
                )
            )

            # if the user does not cancel the folder selection and the
            # folder is not empty
            if folder:
                # For every single file in that path folder, check its
                # file extension (make sure to make the file suffix
                # lowercase beforehand) and if it's a '.png', '.jpg',
                # or '.jpeg', add it into the directory list.
                # (Thanks to @fashoomp from the Python discord server)
                for file in Path(folder).rglob("*.*"):
                    if file.suffix.lower() in (".png", ".jpg", ".jpeg"):
                        self.image_frame.directory_list.append(file)

                if self.image_frame.randomize_list_bool.get():
                    shuffle(self.image_frame.directory_list)

                self.image_frame.image_amount_list = list(
                    range(0, len(self.image_frame.directory_list))
                )
                self.image_frame.image_amount = len(self.image_frame.image_amount_list)
                self.image_frame.frame_index = self.image_frame.image_amount_list[0]

                # values = root.save_load_system.values
                if predetermined_folder is None:
                    self.save_load_system.values["directories"].append(str(folder))
                    self.save_load_system.save_value(
                        input_value=str(self.save_load_system.values),
                        file_name=self.save_load_system.file_name,
                    )

                # enables every button in button_frame
                self.button_frame.image_button_state("normal")

                # re-enables the image limit stuff if it was off
                self.settings_menu.image_limit_state(normal_or_disabled="normal")

                # enables the timers and buttons in timer_frame
                self.timer_frame.time_button_state(
                    start_state="normal", pause_state="disabled", reset_state="disabled"
                )
                self.timer_frame.time_entry_state("normal")

                # enables the reset queue button
                self.settings_menu.switch_folder_button.configure(
                    state="normal", fg_color=self.button_theme_color["normal"]
                )

                # binds the shortcut buttons
                self.bind(
                    "<Alt-Shift-KeyPress-O>",
                    lambda _: self.open_folder(reset_queue=True),
                )
                self.bind(
                    "<Control-Shift-KeyPress-O>",
                    lambda _: self.open_folder(reset_queue=True),
                )

                # updating image and label in button_frame
                self.button_frame.update_image_original()

                # saves the image limit that's been set before updating
                # the label
                self.image_frame.save_image_limit()
                self.button_frame.update_index_label()

                if self.timer_frame.opened_folder:
                    self.timer_frame.currently_counting_down = False
                    if predetermined_folder is None:
                        self.timer_frame.reset_time(from_folder_open=True)
                    self.timer_frame.resetted = False
                    self.timer_frame.countdown_needed = True
                self.timer_frame.opened_folder = True

        except IndexError:
            print(
                "OpenFolderWarning: Folder selection cancelled, "
                "the directory was invalid, or there were no images in the "
                "folder."
            )


class ImageFrame(ctk.CTkFrame):
    """Contains the image displayer, along with the image index, image
    ratio, list of images,
    and the directories of the image.
    """

    def __init__(self, parent):
        # setup
        self.parent = parent
        super().__init__(
            master=parent,
            fg_color="transparent",
            corner_radius=0,
            bg_color="transparent",
        )

        # needed variables for storing image files, the current image
        # index, and the image limit.
        self.frame_index = 0
        self.values = self.parent.save_load_system.values
        self.directory_list = []
        self.image_amount_list = (
            list(range(0, len(self.directory_list)))
            if list(range(0, len(self.directory_list)))
            else []
        )
        self.image_amount = len(self.image_amount_list)
        self.randomize_list_bool = ctk.BooleanVar(value=self.values["randomize"])
        self.image_limit_display = (
            self.values["image_limit"]
            if self.values["image_limit"] != "Unlimited"
            else "Unlimited"
        )
        self.image_limit_entry_var = ctk.StringVar(
            value=(
                self.image_limit_display
                if self.image_limit_display != 0
                else "Unlimited"
            )
        )

        # tells the image changer classes if it should decide the image
        # limit change based off of the image amount list or the image
        # limit that's been set.
        self.reachable_images = (
            self.image_amount_list
            if self.image_limit_display == "Unlimited"
            else list(range(0, int(self.image_limit_display)))
        )

        # image setup
        self.image_original = Image.open(
            resource_path("other_essentials/empty_placeholder.png")
        )
        self.image_ratio = self.image_original.size[0] / self.image_original.size[1]
        self.image_tk = ImageTk.PhotoImage(self.image_original)
        self.resized_tk = None

        # frame to centralize image displayer
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # image displayer, its color dictionary and event
        self.image_displayer_colors: dict = {"Light": "#EBEBEB", "Dark": "#242424"}
        self.image_displayer = ctk.CTkCanvas(
            self,
            bd=0,
            highlightthickness=0,
            relief="ridge",
            bg=self.image_displayer_colors[ctk.get_appearance_mode()],
        )
        self.image_displayer.create_image(0, 0, anchor="nw", image=self.image_tk)
        self.image_displayer.bind(
            "<Configure>",
            lambda event: self.show_full_image(
                width=int(event.width),
                height=int(event.height),
                turn_off_settings_menu=True,
            ),
        )

        # widgets layout
        self.image_displayer.pack(expand=True, fill="both", side="right")

        self.pack_propagate(flag=False)

    def show_full_image(
        self, width: int, height: int, turn_off_settings_menu=False
    ) -> None:
        """Updates the image in the image displayer."""
        # shuts off the settings menu if it's popped up
        if turn_off_settings_menu:
            self.parent.settings_menu.close_menu()

        # current ratio
        canvas_ratio = width / height

        # declare the alignment variables and set them as 0 by default.
        to_canvas_middle = 0
        to_canvas_middle_height = 0

        # get coordinates
        if canvas_ratio > self.image_ratio:
            # If canvas is wider than image
            image_width = int(height * self.image_ratio)
            image_height = int(height)
            to_canvas_middle = int((width - image_width) / 2)

        else:  # if canvas is narrower than the image
            image_width = int(width)
            image_height = int(width / self.image_ratio)
            to_canvas_middle_height = int((height - image_height) / 2)

        self.resized_tk = ImageTk.PhotoImage(
            self.image_original.resize((image_width, image_height))
        )
        self.image_displayer.create_image(
            int(image_width / 2 + to_canvas_middle),
            int(image_height / 2 + to_canvas_middle_height),
            anchor="center",
            image=self.resized_tk,
        )

    def randomize_or_not(self) -> None:
        """Changes the state of the randomize_or_not variable from on or
        off to the other one.
        """
        if self.randomize_list_bool.get():
            self.randomize_list_bool.set(True)
        else:
            self.randomize_list_bool.set(False)

        self.values["randomize"] = self.randomize_list_bool.get()
        self.parent.save_load_system.save_value(
            input_value=str(self.values),
            file_name=self.parent.save_load_system.file_name,
        )

    def save_image_limit(self) -> None:
        try:
            image_limit = (
                int(self.parent.settings_menu.image_limit_entry.get())
                if (self.parent.settings_menu.image_limit_entry.get() != "Unlimited")
                else 0
            )
            if self.image_amount_list:
                self.image_limit_display = (
                    "Unlimited"
                    if (0 >= image_limit or image_limit >= self.image_amount)
                    else str(image_limit)
                )
            else:
                self.image_limit_display = (
                    "Unlimited" if 0 >= image_limit else str(image_limit)
                )

            # Sets image_limit_display to a max num of 15mil so that the
            # program doesn't lag itself to death when it tries to
            # process a large number.
            self.image_limit_display = min(int(self.image_limit_display), 15_000_000)

        except ValueError:
            self.image_limit_display = "Unlimited"

        try:
            self.reachable_images = (
                self.image_amount_list
                if self.image_limit_display == "Unlimited"
                else list(range(0, int(self.image_limit_display)))
            )
        except MemoryError or OverflowError:
            self.reachable_images = self.image_amount_list

        # set up what the image limit entry says by deleting everything
        # there first then replacing it with what it needs to show
        self.parent.settings_menu.image_limit_entry.delete(
            first_index=0,
            last_index=len(self.parent.settings_menu.image_limit_entry.get()),
        )
        self.parent.settings_menu.image_limit_entry.insert(
            index=0, string=self.image_limit_display
        )

        # If a folder has been selected, update the image that's being
        # shown + resets the queue if the image limit is less than the
        # current frame index
        if self.image_amount_list:
            if self.image_limit_display != "Unlimited" and self.frame_index >= int(
                self.image_limit_display
            ):
                self.frame_index = self.image_amount_list[0]
                self.parent.timer_frame.reset_time()

                # update the image in self
                self.parent.button_frame.update_image_original()

            # updates the image limit displayed on the labels
            self.parent.button_frame.update_index_label()

        self.values["image_limit"] = self.image_limit_display
        self.parent.save_load_system.save_value(
            input_value=str(self.values),
            file_name=self.parent.save_load_system.file_name,
        )


class TimerFrame(ctk.CTkFrame):
    """Contains the timer, along with the buttons for the timer, and
    every function necessary for the timer.
    """

    def __init__(self, parent: Any, window: Any):
        # setup
        super().__init__(
            master=parent,
            fg_color="transparent",
            corner_radius=0,
            bg_color="transparent",
        )
        self.root = window
        self.values = self.root.save_load_system.values

        # declare timer input numbers as integer
        self.temp = 0
        self.save_temp = (
            int(self.values["timer_temp"]) if self.values["load_timer_temp"] else 0
        )
        self.countdown_temp = 0

        # declare timer string variables and setting the default value
        # as 0 except for second which is 30
        self.hour = ctk.StringVar(value="0")
        self.minute = ctk.StringVar(value="0")
        self.second = ctk.StringVar(value="30")

        if self.values["load_timer_temp"]:
            mins, secs = divmod(self.save_temp, 60)
            hours = 0
            if mins > 60:
                hours, mins = divmod(mins, 60)
            self.hour.set("{0:2d}".format(hours))
            self.minute.set("{0:2d}".format(mins))
            self.second.set("{0:2d}".format(secs))

        # images used in the countdown and colors used in the hour,
        # minute, and second labels
        self.countdown_image_dict = {
            "Light": {
                3: "app_widget_images/countdown_seconds/"
                "countdown_three_seconds_dark.png",
                2: "app_widget_images/countdown_seconds/"
                "countdown_two_seconds_dark.png",
                1: "app_widget_images/countdown_seconds/"
                "countdown_one_second_dark.png",
            },
            "Dark": {
                3: "app_widget_images/countdown_seconds/"
                "countdown_three_seconds_light.png",
                2: "app_widget_images/countdown_seconds/"
                "countdown_two_seconds_light.png",
                1: "app_widget_images/countdown_seconds/"
                "countdown_one_second_light.png",
            },
        }

        # color dictionaries
        # # colors used for the timer entries' text.
        self.entry_color_dict = {
            "Light": {
                "normal": "#000000",
                "readonly": "#6C6C6C",
                "disabled": "#D8D8D8",
            },
            "Dark": {"normal": "#FFFFFF", "readonly": "#828282", "disabled": "#545454"},
        }
        self.current_entry_color = (
            self.entry_color_dict[ctk.get_appearance_mode()]["disabled"],
            "disabled",
        )

        # # colors used for the label's normal, readonly, and disabled states
        self.label_color_dict = {
            "Dark": {"normal": "#FFFFFF", "readonly": "#888888", "disabled": "#ABABAB"},
            "Light": {
                "normal": "#000000",
                "readonly": "#ABABAB",
                "disabled": "#888888",
            },
        }

        # shortcut binds for the start, pause, and reset buttons.
        self.start_bind_dictionary = {
            "normal": "root.timer_frame.start_time(start_button_not=True, "
            "turn_off_settings_menu=True)",
            "readonly": 'print("Start Button Shortcut currently disabled.")',
            "disabled": 'print("Start Button Shortcut currently disabled.")',
        }

        self.pause_bind_dictionary = {
            "normal": "root.timer_frame.pause_time()",
            "readonly": 'print("Pause Button Shortcut currently disabled.")',
            "disabled": 'print("Pause Button Shortcut currently disabled.")',
        }

        self.reset_bind_dictionary = {
            "normal": "root.timer_frame.reset_time(" "turn_off_settings_menu=True)",
            "readonly": 'print("Reset Button Shortcut currently disabled.")',
            "disabled": 'print("Reset Button Shortcut currently disabled.")',
        }

        # image for time buttons
        self.start_time_image = ctk.CTkImage(
            light_image=Image.open(
                resource_path("app_widget_images/time_buttons/start_button.png")
            ),
            dark_image=Image.open(
                resource_path("app_widget_images/time_buttons/start_button.png")
            ),
        )
        self.pause_start_time_image = ctk.CTkImage(
            light_image=Image.open(
                resource_path("app_widget_images/time_buttons/pause_button.png")
            ),
            dark_image=Image.open(
                resource_path("app_widget_images/time_buttons/pause_button.png")
            ),
        )
        self.stop_reset_time_image = ctk.CTkImage(
            light_image=Image.open(
                resource_path(
                    "app_widget_images/time_buttons/stop_and_reset_button.png"
                )
            ),
            dark_image=Image.open(
                resource_path(
                    "app_widget_images/time_buttons/stop_and_reset_button.png"
                )
            ),
        )

        # declare the booleans and variables needed
        self.opened_folder = False
        self.paused = False
        self.resetted = False
        self.heads_up = ctk.BooleanVar(value=self.values["countdown"])
        self.next_image = bool
        self.countdown_needed = True
        self.time_start = False
        self.timer = None
        self.currently_counting_down = False
        self.from_open_folder = False
        self.folder_complete_bool = ctk.BooleanVar(
            value=self.values["alert_queue_complete"]
        )

        # frame for the timers and buttons
        self.timers_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
            border_width=0,
            bg_color="transparent",
        )
        self.buttons_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
            border_width=0,
            bg_color="transparent",
        )

        # use of entry class to take input from use
        # # hour entry
        self.hour_frame = ctk.CTkFrame(
            self.timers_frame,
            fg_color="transparent",
            corner_radius=0,
            border_width=0,
            bg_color="transparent",
        )
        self.hour_entry = ctk.CTkEntry(
            self.hour_frame,
            width=20,
            font=("Arial", 14),
            textvariable=self.hour,
            border_width=0,
            state="disabled",
            text_color=self.current_entry_color[0],
        )
        self.hour_label = ctk.CTkLabel(
            self.hour_frame,
            text="Hour",
            font=("Arial", 10),
            text_color=self.current_entry_color[0],
        )

        # # minute entry
        self.minute_frame = ctk.CTkFrame(
            self.timers_frame,
            fg_color="transparent",
            corner_radius=0,
            border_width=0,
            bg_color="transparent",
        )
        self.minute_entry = ctk.CTkEntry(
            self.minute_frame,
            width=20,
            font=("Arial", 14),
            textvariable=self.minute,
            border_width=0,
            state="disabled",
            text_color=self.current_entry_color[0],
        )
        self.minute_label = ctk.CTkLabel(
            self.minute_frame,
            text="Minute",
            font=("Arial", 10),
            text_color=self.current_entry_color[0],
        )

        # # second entry
        self.second_frame = ctk.CTkFrame(
            self.timers_frame,
            fg_color="transparent",
            corner_radius=0,
            border_width=0,
            bg_color="transparent",
        )
        self.second_entry = ctk.CTkEntry(
            self.second_frame,
            width=20,
            font=("Arial", 14),
            textvariable=self.second,
            border_width=0,
            state="disabled",
            text_color=self.current_entry_color[0],
        )
        self.second_label = ctk.CTkLabel(
            self.second_frame,
            text="Second",
            font=("Arial", 10),
            text_color=self.current_entry_color[0],
        )

        # start, pause, and reset button widget along with their tooltips
        self.start_button = ctk.CTkButton(
            self.buttons_frame,
            image=self.start_time_image,
            text="",
            width=45,
            command=lambda: self.start_time(
                start_button_not=True, turn_off_settings_menu=True
            ),
            state="disabled",
            bg_color="transparent",
            fg_color=self.root.button_theme_color["disabled"],
            hover_color=self.root.button_theme_color["hover_color"],
        )
        ToolTip(widget=self.start_button, msg="Start Timer (Ctrl+S)", delay=0.3)

        self.pause_button = ctk.CTkButton(
            self.buttons_frame,
            image=self.pause_start_time_image,
            text="",
            width=45,
            command=self.pause_time,
            state="disabled",
            bg_color="transparent",
            fg_color=self.root.button_theme_color["disabled"],
            hover_color=self.root.button_theme_color["hover_color"],
        )
        ToolTip(widget=self.pause_button, msg="Pause/Play Timer (Space)", delay=0.3)

        self.reset_button = ctk.CTkButton(
            self.buttons_frame,
            image=self.stop_reset_time_image,
            text="",
            width=45,
            command=lambda: self.reset_time(turn_off_settings_menu=True),
            state="disabled",
            bg_color="transparent",
            fg_color=self.root.button_theme_color["disabled"],
            hover_color=self.root.button_theme_color["hover_color"],
        )
        ToolTip(widget=self.reset_button, msg="Reset Timer (Ctrl+R)", delay=0.3)

        # layout
        self.pack(pady=5, padx=5, side="left")

        # # pack the time entry frames
        self.hour_frame.pack(padx=6, pady=10, side="left", expand=True, fill="both")
        self.minute_frame.pack(padx=3, pady=10, side="left", expand=True, fill="both")
        self.second_frame.pack(padx=6, pady=10, side="left", expand=True, fill="both")

        # # pack the time buttons
        self.start_button.pack(padx=5, side="left")
        self.pause_button.pack(padx=5, side="left")
        self.reset_button.pack(padx=5, side="left")

    def time_button_state(
        self, start_state: str, pause_state: str, reset_state: str
    ) -> None:
        assert (start_state, pause_state, reset_state) == "normal" or "disabled"

        # setting the time button states
        self.start_button.configure(state=start_state)
        self.pause_button.configure(state=pause_state)
        self.reset_button.configure(state=reset_state)

        # settings the colors that should be used
        self.start_button.configure(fg_color=self.root.button_theme_color[start_state])
        self.pause_button.configure(fg_color=self.root.button_theme_color[pause_state])
        self.reset_button.configure(fg_color=self.root.button_theme_color[reset_state])

        # setting the button shortcuts
        exec(
            f"self.root.bind('<Control-KeyPress-s>', "
            f"lambda _: {self.start_bind_dictionary[start_state]})"
        )
        exec(
            f"self.root.bind('<space>', "
            f"lambda _: {self.pause_bind_dictionary[pause_state]})"
        )
        exec(
            f"self.root.bind('<Control-KeyPress-r>', "
            f"lambda _: {self.reset_bind_dictionary[reset_state]})"
        )

    def time_entry_state(self, normal_or_readonly_or_disabled: str) -> None:
        # setting the time entry states
        self.hour_entry.configure(state=normal_or_readonly_or_disabled)
        self.minute_entry.configure(state=normal_or_readonly_or_disabled)
        self.second_entry.configure(state=normal_or_readonly_or_disabled)

        # setting the time entry color states
        self.current_entry_color = (
            self.entry_color_dict[ctk.get_appearance_mode()][
                normal_or_readonly_or_disabled
            ],
            normal_or_readonly_or_disabled,
        )
        self.hour_entry.configure(text_color=self.current_entry_color[0])
        self.minute_entry.configure(text_color=self.current_entry_color[0])
        self.second_entry.configure(text_color=self.current_entry_color[0])

        # setting the label state colors
        self.hour_label.configure(
            text_color=self.label_color_dict[ctk.get_appearance_mode()][
                normal_or_readonly_or_disabled
            ]
        )
        self.minute_label.configure(
            text_color=self.label_color_dict[ctk.get_appearance_mode()][
                normal_or_readonly_or_disabled
            ]
        )
        self.second_label.configure(
            text_color=self.label_color_dict[ctk.get_appearance_mode()][
                normal_or_readonly_or_disabled
            ]
        )

    def start_time(
        self,
        start_button_not=False,
        pause_button_not=False,
        turn_off_settings_menu=False,
    ) -> None:
        # Shuts off the settings menu if this function is executed
        # through the start button or shortcut bind.
        if turn_off_settings_menu:
            self.root.settings_menu.close_menu()

        try:
            if start_button_not:
                if (
                    int(self.hour.get()) * 3600
                    + int(self.minute.get()) * 60
                    + int(self.second.get())
                    <= 0
                    and not pause_button_not
                ):
                    self.save_temp = 30
                else:
                    self.save_temp = (
                        int(self.hour.get()) * 3600
                        + int(self.minute.get()) * 60
                        + int(self.second.get())
                    )
                self.values["timer_temp"] = self.save_temp
                self.root.save_load_system.save_value(
                    input_value=str(self.values),
                    file_name=self.root.save_load_system.file_name,
                )

            if (
                int(self.hour.get()) * 3600
                + int(self.minute.get()) * 60
                + int(self.second.get())
                <= 0
                and not pause_button_not
            ):
                self.hour.set("0")
                self.minute.set("0")
                self.second.set("30")

            self.temp = (
                int(self.hour.get()) * 3600
                + int(self.minute.get()) * 60
                + int(self.second.get())
            )
            self.time_entry_state("readonly")
            self.time_button_state(
                start_state="disabled", pause_state="normal", reset_state="normal"
            )
            while self.temp >= 0 and not self.paused:
                mins, secs = divmod(self.temp, 60)

                # Converting the input entered in mins or secs to hours.
                hours = 0
                if mins > 60:
                    hours, mins = divmod(mins, 60)

                self.hour.set("{0:2d}".format(hours))
                self.minute.set("{0:2d}".format(mins))
                self.second.set("{0:2d}".format(secs))

                # updating the GUI window after decrementing the self.temp
                # value every time, and turns the entries to read only to
                # prevent interruptions
                root.update()

                if not self.paused:
                    # Updates the index label incase it's paused.
                    root.button_frame.update_index_label()

                    # If self.temp value = 0, then go to the next image
                    # or start a countdown.
                    if self.temp == 0:

                        if not self.resetted:
                            if not self.from_open_folder:
                                if (
                                    self.heads_up.get()
                                    and root.image_frame.frame_index + 1
                                    in root.image_frame.reachable_images
                                    and self.countdown_needed
                                    or root.button_frame.loop_or_not.get()
                                    and self.heads_up.get()
                                    and self.countdown_needed
                                ):
                                    self.heads_up_countdown()
                                else:
                                    self.time_next_image()

                            else:
                                self.from_open_folder = False

                        else:
                            self.reset_time(disable_time_button=False)
                            self.resetted = False
                            self.from_open_folder = False
                            self.countdown_needed = True
                            self.time_entry_state("normal")
                            self.time_button_state(
                                start_state="normal",
                                pause_state="disabled",
                                reset_state="disabled",
                            )
                        break

                    else:
                        self.from_open_folder = False
                        self.time_entry_state("readonly")
                        if not self.time_start:
                            self.timer = Timer(1, self.reduce_temp_by_one_second)
                            self.timer.start()
                            self.time_start = True

                else:
                    # if it's paused, inform the user with the label
                    root.button_frame.update_index_label()

        except ValueError:
            if (
                self.hour.get() == ""
                or self.hour.get() is None
                or self.hour.get().isalpha
            ):
                self.hour.set("0")
            if (
                self.minute.get() == ""
                or self.minute.get() is None
                or self.minute.get().isalpha
            ):
                self.minute.set("0")
            if (
                self.second.get() == ""
                or self.second.get() is None
                or self.second.get().isalpha
            ):
                self.second.set("0")

            if start_button_not:
                if (
                    self.hour.get() == "0"
                    and self.minute.get() == "0"
                    and self.second.get() == "0"
                ):
                    self.second.set("30")
                self.start_time(start_button_not=True)
            else:
                self.start_time()

    def pause_time(self):
        # shuts off the settings menu if it's popped up
        self.root.settings_menu.close_menu()

        if self.paused:
            self.paused = False
            self.time_entry_state("readonly")
            self.start_time(pause_button_not=True)

        else:
            self.paused = True
            self.time_entry_state("normal")

    def reset_time(
        self,
        disable_time_button=True,
        from_folder_open=False,
        turn_off_settings_menu=False,
    ) -> None:
        """Resets the timer by setting the temp to 0, ending its process
        and setting it back  to the current save_temp if it's above 0.
        """

        # Shuts off the settings menu if this function is executed
        # through the start button or shortcut bind
        if turn_off_settings_menu:
            self.root.settings_menu.close_menu()

        self.paused = False
        self.temp = 0

        if self.save_temp <= 0:
            self.save_temp = 30

        # let the self.start_time method know that it's resetted.
        self.resetted = True

        if from_folder_open:
            self.from_open_folder = True
            self.countdown_needed = False

        # let the entry states be editable again
        self.time_entry_state("normal")

        if disable_time_button:
            self.time_button_state(
                start_state="normal", pause_state="disabled", reset_state="disabled"
            )

        mins, secs = divmod(self.save_temp, 60)
        hours = 0
        if mins > 60:
            hours, mins = divmod(mins, 60)
        self.hour.set("{0:2d}".format(hours))
        self.minute.set("{0:2d}".format(mins))
        self.second.set("{0:2d}".format(secs))

        root.button_frame.update_index_label()

    def heads_up_setting(self):
        if self.heads_up.get():
            self.heads_up.set(True)
        else:
            self.heads_up.set(False)

        self.values["countdown"] = self.heads_up.get()
        self.root.save_load_system.save_value(
            input_value=str(self.values), file_name=self.root.save_load_system.file_name
        )

    def reduce_temp_by_one_second(self):
        self.temp -= 1
        self.time_start = False

    def heads_up_countdown(self):
        """Counts down 3 seconds for the next image if self.heads_up is
        on and also sets the current image to the appropriate countdown
        image.
        """
        self.currently_counting_down = True
        self.hour.set("0")
        self.minute.set("0")
        self.second.set("3")
        self.temp = 3
        root.update()

        root.button_frame.image_button_state("disabled")
        root.settings_menu.image_limit_save_button.configure(state="disabled")
        root.settings_menu.image_limit_entry.configure(state="disabled")
        self.time_entry_state("readonly")
        self.time_button_state(
            start_state="disabled", pause_state="disabled", reset_state="disabled"
        )
        self.root.settings_menu.image_limit_state(normal_or_disabled="disabled")

        # counts down 3 seconds
        while self.temp >= 0:
            if self.temp > 0:
                root.image_frame.image_original = Image.open(
                    resource_path(
                        self.countdown_image_dict[ctk.get_appearance_mode()][self.temp]
                    )
                )
                root.image_frame.image_ratio = (
                    root.image_frame.image_original.size[0]
                    / root.image_frame.image_original.size[1]
                )
                root.image_frame.show_full_image(
                    root.image_frame.image_displayer.winfo_width(),
                    root.image_frame.image_displayer.winfo_height(),
                )

            # setting the countdown entries
            self.second.set("{0:2d}".format(self.temp))
            self.time_button_state(
                start_state="disabled", pause_state="disabled", reset_state="disabled"
            )

            root.update()

            if self.temp == 0:
                root.button_frame.image_button_state("normal")
                self.root.settings_menu.image_limit_state(normal_or_disabled="normal")
                if self.currently_counting_down:
                    self.time_next_image()
                self.currently_counting_down = False
                break

            else:
                self.time_entry_state("readonly")
                if not self.time_start:
                    self.timer = Timer(1, self.reduce_temp_by_one_second)
                    self.timer.start()
                    self.time_start = True

    def time_next_image(self):
        """Goes to the next image or resets the timer for once the timer
        ticks to 0.
        """

        # Reset the next_image bool so that the program doesn't somehow
        # go to the next image without being told to.
        self.next_image = False

        # goes to next image
        if root.image_frame.frame_index + 1 in root.image_frame.reachable_images:
            root.image_frame.frame_index += 1
            self.next_image = True

        elif root.image_frame.frame_index + 1 not in root.image_frame.reachable_images:
            if root.button_frame.loop_or_not.get():
                # set image index back to the first image's
                root.image_frame.frame_index = root.image_frame.reachable_images[0]
                self.next_image = True
            else:
                # if the alert box is enabled
                if root.timer_frame.folder_complete_bool.get():
                    messagebox.showinfo("Folder Complete", "Folder has been exhausted.")

                self.reset_time()
                self.resetted = False

        try:
            # update the image in root.image_frame
            root.button_frame.update_image_original()

            # update the index label
            root.button_frame.update_index_label()

        except IndexError:
            print("No folder has been selected yet.")

        if self.next_image:
            self.reset_time(disable_time_button=False)
            self.resetted = False
            self.start_time()

    def folder_complete_alert_not(self):
        """Changes the state of self.folder_complete_bool on and off"""
        if self.folder_complete_bool.get():
            self.folder_complete_bool.set(True)
        else:
            self.folder_complete_bool.set(False)

        self.values["alert_queue_complete"] = self.folder_complete_bool.get()
        self.root.save_load_system.save_value(
            input_value=str(self.values), file_name=self.root.save_load_system.file_name
        )


class ButtonFrame(ctk.CTkFrame):
    """Contains every button needed to change the images."""

    def __init__(self, parent: Any, image_button_parent: Any, window: Any):

        # # setup and variables needed
        super().__init__(master=parent, fg_color="transparent", corner_radius=0)
        self.image_order_index = ctk.StringVar(
            value=f"Select a folder from the file menu."
        )
        self.root = window
        self.values = self.root.save_load_system.values
        self.loop_or_not = ctk.BooleanVar(value=self.values["loop"])

        # # frames for button layout
        self.image_button_parent = image_button_parent

        # to align buttons to the left
        self.left_image_control_buttons_frame = ctk.CTkFrame(
            self.image_button_parent,
            fg_color="transparent",
            corner_radius=0,
            border_width=0,
        )

        # to align buttons to the right
        self.right_image_control_buttons_frame = ctk.CTkFrame(
            self.image_button_parent,
            fg_color="transparent",
            corner_radius=0,
            border_width=0,
        )

        # # Change image buttons (The images are the same for both dark
        # # and light mode)
        self.previous_image_png = ctk.CTkImage(
            light_image=Image.open(
                resource_path(
                    "app_widget_images/change_image_buttons/"
                    "previous_image_button.png"
                )
            ),
            dark_image=Image.open(
                resource_path(
                    "app_widget_images/change_image_buttons/"
                    "previous_image_button.png"
                )
            ),
        )
        self.next_image_png = ctk.CTkImage(
            Image.open(
                resource_path(
                    "app_widget_images/change_image_buttons/next_image_button.png"
                )
            ),
            Image.open(
                resource_path(
                    "app_widget_images/change_image_buttons/" "next_image_button.png"
                )
            ),
        )
        self.first_image_png = ctk.CTkImage(
            Image.open(
                resource_path(
                    "app_widget_images/change_image_buttons/first_image_button.png"
                )
            ),
            Image.open(
                resource_path(
                    "app_widget_images/change_image_buttons/" "first_image_button.png"
                )
            ),
        )
        self.last_image_png = ctk.CTkImage(
            Image.open(
                resource_path(
                    "app_widget_images/change_image_buttons/" "last_image_button.png"
                )
            ),
            Image.open(
                resource_path(
                    "app_widget_images/change_image_buttons/" "last_image_button.png"
                )
            ),
        )

        # # image changer buttons with their tool tips
        self.first_image_button = ctk.CTkButton(
            self.left_image_control_buttons_frame,
            image=self.first_image_png,
            text="",
            width=45,
            command=lambda: self.change_image(first_or_last=True),
            state="disabled",
            fg_color=self.root.button_theme_color["disabled"],
            hover_color=self.root.button_theme_color["hover_color"],
        )
        ToolTip(widget=self.first_image_button, msg="First Image", delay=0.3)

        self.previous_image_button = ctk.CTkButton(
            self.left_image_control_buttons_frame,
            image=self.previous_image_png,
            text="",
            width=45,
            command=lambda: self.change_image(next_or_previous=False),
            state="disabled",
            fg_color=self.root.button_theme_color["disabled"],
            hover_color=self.root.button_theme_color["hover_color"],
        )
        ToolTip(widget=self.previous_image_button, msg="Previous Image", delay=0.3)

        self.next_image_button = ctk.CTkButton(
            self.right_image_control_buttons_frame,
            image=self.next_image_png,
            text="",
            width=45,
            command=lambda: self.change_image(next_or_previous=True),
            state="disabled",
            fg_color=self.root.button_theme_color["disabled"],
            hover_color=self.root.button_theme_color["hover_color"],
        )
        ToolTip(widget=self.next_image_button, msg="Next Image", delay=0.3)

        self.last_image_button = ctk.CTkButton(
            self.right_image_control_buttons_frame,
            image=self.last_image_png,
            text="",
            width=45,
            command=lambda: self.change_image(first_or_last=False),
            state="disabled",
            fg_color=self.root.button_theme_color["disabled"],
            hover_color=self.root.button_theme_color["hover_color"],
        )
        ToolTip(widget=self.last_image_button, msg="Last Image", delay=0.3)

        # image index label
        self.index_label = ctk.CTkLabel(
            parent, text="Select an image folder from the folder menu"
        )

        # image change buttons layout
        self.first_image_button.pack(side="left")
        self.previous_image_button.pack(side="left", padx=10)

        self.next_image_button.pack(side="left", padx=10)
        self.last_image_button.pack(side="left")

    def update_index_label(self):
        """Updates the index_label inside ButtonFrame appropriately."""
        try:
            # the variable that tells the label the X it needs to show
            # in "n image out of x"
            out_of_n = (
                root.image_frame.image_amount
                if root.image_frame.image_limit_display == "Unlimited"
                else root.image_frame.image_limit_display
            )

            # the variable that may or may not be changed depending on
            # if there's anything going on right now
            end_modifier = ""

            # if it's the end of the queue and it's not paused
            if (
                root.image_frame.frame_index == root.image_frame.reachable_images[-1]
                and not root.timer_frame.paused
                and not self.loop_or_not.get()
            ):
                end_modifier = " (Queue Finished)"

            # else if it's paused (+ if it's also on loop)
            elif root.timer_frame.paused:
                end_modifier = (
                    " (Paused)" if not self.loop_or_not.get() else " (Paused, On Loop)"
                )

            # else if it's looped
            elif self.loop_or_not.get():
                end_modifier = " (On Loop)"

            # if an image limit is set up, display the total number of
            # images in parentheses
            if root.image_frame.image_limit_display != "Unlimited":
                end_modifier = f" ({root.image_frame.image_amount}) {end_modifier}"

            self.image_order_index.set(
                f"Image no. {root.image_frame.frame_index + 1}/"
                f"{out_of_n}{end_modifier}"
            )
            self.index_label.configure(textvariable=self.image_order_index)

        except IndexError:
            print(
                "IndexLabelUpdateError: No folder has been selected yet.\n"
                "\t\t\t\t\t   Nothing should go wrong, though."
            )

    def image_button_state(self, normal_or_disabled: str) -> None:
        # setting the time entry states
        for button in [
            "first_image_button",
            "previous_image_button",
            "next_image_button",
            "last_image_button",
        ]:
            exec(
                f"self.{button}.configure(state=normal_or_disabled,"
                f"fg_color=self.root.button_theme_color[normal_or_disabled])"
            )

        # setting the keyboard button shortcuts accordingly + set the
        # button colors used
        if normal_or_disabled == "normal":
            # shortcut binds
            self.root.bind(
                "<Down>", lambda _: root.button_frame.change_image(first_or_last=True)
            )
            self.root.bind(
                "<Right>",
                lambda _: root.button_frame.change_image(next_or_previous=True),
            )
            self.root.bind(
                "<Left>",
                lambda _: root.button_frame.change_image(next_or_previous=False),
            )
            self.root.bind(
                "<Up>", lambda _: root.button_frame.change_image(first_or_last=False)
            )

        else:
            # shortcut binds
            self.root.bind(
                "<Down>", lambda _: print("First Image shortcut currently disabled.")
            )
            self.root.bind(
                "<Right>",
                lambda _: print("Previous Image shortcut currently disabled."),
            )
            self.root.bind(
                "<Left>", lambda _: print("Next Image shortcut currently disabled.")
            )
            self.root.bind(
                "<Up>", lambda _: print("Last Image shortcut currently disabled.")
            )

    def update_image_original(self) -> None:
        self.root.image_frame.image_original = Image.open(
            resource_path(
                self.root.image_frame.directory_list[self.root.image_frame.frame_index]
            )
        )
        self.root.image_frame.image_ratio = (
            self.root.image_frame.image_original.size[0]
            / self.root.image_frame.image_original.size[1]
        )
        self.root.image_frame.show_full_image(
            self.root.image_frame.image_displayer.winfo_width(),
            self.root.image_frame.image_displayer.winfo_height(),
        )

    def change_image(self, next_or_previous=None, first_or_last=None) -> None:
        """Changes the image in the image displayer through the image
        change buttons. Note: Args next & first image == True, but the
        args previous & last image == False.
        """
        # closes the settings menu if it's popped up
        self.root.settings_menu.close_menu()

        try:
            if next_or_previous or first_or_last:
                # set frame index to the next image's if it's available
                if (
                    root.image_frame.frame_index + 1
                    in root.image_frame.reachable_images
                    and first_or_last is None
                ):
                    root.image_frame.frame_index += 1

                # if loop is on or if the button = first
                elif (
                    root.image_frame.frame_index + 1
                    not in root.image_frame.reachable_images
                    and self.loop_or_not.get()
                    or first_or_last
                    and next_or_previous is None
                ):

                    # re-shuffles the image directory after a loop
                    if (
                        root.image_frame.randomize_list_bool.get()
                        and first_or_last is None
                    ):
                        shuffle(root.image_frame.directory_list)

                    # set image index back to the first image's
                    root.image_frame.frame_index = root.image_frame.reachable_images[0]

            elif not next_or_previous or not first_or_last:
                # set frame index to the previous image's
                if (
                    root.image_frame.frame_index - 1
                    in root.image_frame.reachable_images
                    and first_or_last is None
                ):
                    root.image_frame.frame_index -= 1

                # if loop is on or if the button = last
                elif (
                    root.image_frame.frame_index - 1
                    not in root.image_frame.reachable_images
                    and self.loop_or_not.get()
                    or not first_or_last
                    and next_or_previous is None
                ):

                    # re-shuffles the image directory after a loop if
                    # the randomize list option is on
                    if (
                        root.image_frame.randomize_list_bool.get()
                        and first_or_last is None
                    ):
                        shuffle(root.image_frame.directory_list)

                    # set frame index to the last image's
                    root.image_frame.frame_index = root.image_frame.reachable_images[-1]

            # update the image in root.image_frame
            self.update_image_original()

            # update the label
            self.update_index_label()

        except IndexError:
            print(
                "ImageChange Error: No folder has been selected yet to be "
                "able to change image to."
            )

    def loop_not_loop(self) -> None:
        """Changes the state of loop to on or off and updates the index
        label accordingly.
        """

        if self.loop_or_not.get():
            self.loop_or_not.set(True)
        else:
            self.loop_or_not.set(False)

        self.values["loop"] = self.loop_or_not.get()
        self.root.save_load_system.save_value(
            input_value=str(self.values), file_name=self.root.save_load_system.file_name
        )

        # updates the index label accordingly
        self.update_index_label()


class SizeNotifier:
    def __init__(self, parent: Any, size_dictionary: dict):
        self.root = parent
        self.size_dict = {
            pixels: layout for pixels, layout in sorted(size_dictionary.items())
        }
        self.current_min_size: int | None = None
        self.root.bind("<Configure>", self.check_size)

        self.root.update()

    def check_size(self, event) -> None:
        if event.widget == self.root:
            window_width = event.width
            checked_size = None

            for min_size in self.size_dict:
                delta = window_width - min_size
                if delta >= 0:
                    checked_size = min_size

            if checked_size != self.current_min_size:
                self.current_min_size = checked_size
                self.size_dict[self.current_min_size]()


class SettingsMenu(ctk.CTkButton):
    def __init__(
        self,
        parent: Any,
        height: int = 41,
        width: int = 41,
        bg_color: str | tuple[str, str] = "transparent",
        fg_color: str | tuple[str, str] = "transparent",
        hover_color: str | tuple[str, str] = ("#DBDBDB", "#1F1F1F"),
    ):
        # setup
        self.parent = parent
        self.settings_icon = ctk.CTkImage(
            light_image=Image.open(
                resource_path("app_widget_images/settings_menu/settings_icon_dark.png")
            ),
            dark_image=Image.open(
                resource_path("app_widget_images/settings_menu/settings_icon_light.png")
            ),
        )
        self.save_image_limit_icon = ctk.CTkImage(
            Image.open(resource_path("app_widget_images/settings_menu/save_icon.png")),
            Image.open(resource_path("app_widget_images/settings_menu/save_icon.png")),
        )
        self.values = self.parent.save_load_system.values

        self.load_saved_temp_bool = ctk.BooleanVar(value=self.values["load_timer_temp"])
        self.load_saved_directories_bool = ctk.BooleanVar(
            value=self.values["load_saved_directories"]
        )

        super().__init__(
            master=parent,
            image=self.settings_icon,
            text="",
            height=height,
            width=width,
            bg_color=bg_color,
            fg_color=fg_color,
            corner_radius=0,
            hover_color=hover_color,
            command=self.open_menu,
        )

        self.menu_popped_up = False

        # # settings pop up menu
        self.settings_pop_up_menu = ctk.CTkFrame(parent)
        self.buttons_menu = ctk.CTkFrame(
            self.settings_pop_up_menu, border_width=1, corner_radius=0
        )
        self.checkbox_menu = ctk.CTkFrame(
            self.settings_pop_up_menu, border_width=1, corner_radius=0
        )
        self.image_limit_menu = ctk.CTkFrame(
            self.settings_pop_up_menu, border_width=1, corner_radius=0
        )
        self.image_limit_centralize_menu = ctk.CTkFrame(
            self.image_limit_menu,
            border_width=0,
            corner_radius=0,
            fg_color="transparent",
        )
        self.more_settings_menu = ctk.CTkFrame(
            self.settings_pop_up_menu, border_width=1, corner_radius=0
        )

        # button menu options
        self.add_new_folder_button = ctk.CTkButton(
            self.buttons_menu,
            text="Open Folder (Alt+O)",
            command=parent.open_folder,
            fg_color=self.parent.button_theme_color["normal"],
            hover_color=self.parent.button_theme_color["hover_color"],
        )
        self.switch_theme = ctk.CTkButton(
            self.buttons_menu,
            text="Switch Themes (Alt+S)",
            command=lambda: switch_theme(),
            fg_color=self.parent.button_theme_color["normal"],
            hover_color=self.parent.button_theme_color["hover_color"],
        )
        self.switch_folder_button = ctk.CTkButton(
            self.buttons_menu,
            text="Switch to New Folder (Alt+Shift+O)",
            command=lambda: root.open_folder(reset_queue=True),
            fg_color=self.parent.button_theme_color["disabled"],
            hover_color=self.parent.button_theme_color["hover_color"],
            state="disabled",
            text_color_disabled=("#888888", "#666666"),
        )

        # image limit menu label and entry
        self.image_limit_label = ctk.CTkLabel(
            self.image_limit_centralize_menu, text="Set Image Limit"
        )
        self.image_limit_entry = ctk.CTkEntry(
            self.image_limit_centralize_menu,
            width=68,
            textvariable=self.parent.image_frame.image_limit_entry_var,
        )
        self.image_limit_save_button = ctk.CTkButton(
            self.image_limit_centralize_menu,
            text="",
            image=self.save_image_limit_icon,
            width=25,
            height=25,
            fg_color=self.parent.button_theme_color["normal"],
            hover_color=self.parent.button_theme_color["hover_color"],
            command=self.parent.image_frame.save_image_limit,
        )
        ToolTip(self.image_limit_save_button, msg="Save Image Limit (Enter)", delay=0.3)

        # checkbox menu options
        self.countdown_checkbox = ctk.CTkCheckBox(
            self.checkbox_menu,
            text="Countdown For Next Image",
            variable=parent.timer_frame.heads_up,
            command=parent.timer_frame.heads_up_setting,
            fg_color=self.parent.button_theme_color["normal"],
            hover_color=self.parent.button_theme_color["hover_color"],
        )
        self.randomize_queue_checkbox = ctk.CTkCheckBox(
            self.checkbox_menu,
            text="Randomize Folder Queue",
            variable=parent.image_frame.randomize_list_bool,
            command=parent.image_frame.randomize_or_not,
            fg_color=self.parent.button_theme_color["normal"],
            hover_color=self.parent.button_theme_color["hover_color"],
        )
        self.loop_queue_checkbox = ctk.CTkCheckBox(
            self.checkbox_menu,
            text="Loop Folder",
            variable=parent.button_frame.loop_or_not,
            command=parent.button_frame.loop_not_loop,
            fg_color=self.parent.button_theme_color["normal"],
            hover_color=self.parent.button_theme_color["hover_color"],
        )
        self.alert_queue_complete_checkbox = ctk.CTkCheckBox(
            self.checkbox_menu,
            text="Alert When Queue is Complete",
            variable=parent.timer_frame.folder_complete_bool,
            command=parent.timer_frame.folder_complete_alert_not,
            fg_color=self.parent.button_theme_color["normal"],
            hover_color=self.parent.button_theme_color["hover_color"],
        )

        # more settings menu checkboxes
        self.load_timer_temp_checkbox = ctk.CTkCheckBox(
            self.more_settings_menu,
            text="Load Saved Timer On Launch",
            variable=self.load_saved_temp_bool,
            command=self.load_timer_temp_not,
            fg_color=self.parent.button_theme_color["normal"],
            hover_color=self.parent.button_theme_color["hover_color"],
        )
        self.load_saved_directories_checkbox = ctk.CTkCheckBox(
            self.more_settings_menu,
            text="Load Last Folders On Launch",
            variable=self.load_saved_directories_bool,
            command=self.load_saved_directories_not,
            fg_color=self.parent.button_theme_color["normal"],
            hover_color=self.parent.button_theme_color["hover_color"],
        )

        # layout
        # # buttons menu layout
        for button in [
            self.add_new_folder_button,
            self.switch_theme,
            self.switch_folder_button,
        ]:
            button.pack(expand="True", fill="x", padx=5, pady=2)

        # # image limit menu layout
        self.image_limit_label.pack(side="left", padx=5)
        self.image_limit_entry.pack(side="left", padx=2)
        self.image_limit_save_button.pack(side="left", padx=5)

        # # checkbox menu layout
        for checkbox in [
            self.countdown_checkbox,
            self.randomize_queue_checkbox,
            self.loop_queue_checkbox,
            self.alert_queue_complete_checkbox,
        ]:
            checkbox.pack(expand="True", fill="x", padx=5, pady=2)

        # # settings menu layout
        self.load_timer_temp_checkbox.pack(expand="True", fill="x", padx=5, pady=2)
        self.load_saved_directories_checkbox.pack(
            expand="True", fill="x", padx=5, pady=2
        )

        # # menu layout
        self.buttons_menu.pack(ipady=4, fill="x")
        self.image_limit_centralize_menu.pack(expand=True)
        self.image_limit_menu.pack(ipady=4, fill="x")
        self.checkbox_menu.pack(ipady=4, fill="x")
        self.more_settings_menu.pack(ipady=4, fill="x")

        # close menu by clicking right click
        self.parent.bind("<Button-3>", lambda _: self.close_menu())

        # shortcut binds
        self.parent.bind("<Alt_L>", lambda _: self.open_menu())
        self.parent.bind("<Alt_R>", lambda _: self.open_menu())
        self.parent.bind("<Alt-KeyPress-o>", lambda _: parent.open_folder())
        self.parent.bind("<Control-KeyPress-o>", lambda _: parent.open_folder())
        self.parent.bind("<Alt-KeyPress-s>", lambda _: switch_theme())
        self.image_limit_entry.bind(
            "<Return>", lambda _: self.parent.image_frame.save_image_limit()
        )

        # run self
        self.place(relx=0, rely=1, anchor="sw")

    def image_limit_state(self, normal_or_disabled: str):
        self.image_limit_entry.configure(
            state=normal_or_disabled,
            text_color=(
                ("black", "white")
                if normal_or_disabled == "normal"
                else ("#888888", "#666666")
            ),
        )
        if normal_or_disabled == "normal":
            self.image_limit_entry.bind(
                "<Return>", lambda _: self.parent.image_frame.save_image_limit()
            )
        else:
            self.image_limit_entry.unbind("<Return>")

        self.image_limit_save_button.configure(state=normal_or_disabled)
        self.image_limit_save_button.configure(
            fg_color=self.parent.button_theme_color[normal_or_disabled]
        )

    def close_menu(self):
        if self.menu_popped_up:
            self.settings_pop_up_menu.place_forget()
            self.menu_popped_up = False

    def open_menu(self):
        if not self.menu_popped_up:
            self.settings_pop_up_menu.place(relx=0, rely=0.95, anchor="sw")
            self.menu_popped_up = True
        else:
            self.settings_pop_up_menu.place_forget()
            self.menu_popped_up = False

    def load_timer_temp_not(self):
        """Changes the state of the load_timer_temp_bool variable from
        on or off to the other one.
        """
        if self.load_saved_temp_bool.get():
            self.load_saved_temp_bool.set(True)
        else:
            self.load_saved_temp_bool.set(False)

        self.values["load_timer_temp"] = self.load_saved_temp_bool.get()
        self.parent.save_load_system.save_value(
            input_value=str(self.values),
            file_name=self.parent.save_load_system.file_name,
        )

    def load_saved_directories_not(self):
        """Changes the state of the load_timer_temp_bool variable from
        on or off to the other one.
        """
        if self.load_saved_directories_bool.get():
            self.load_saved_directories_bool.set(True)
        else:
            self.load_saved_directories_bool.set(False)

        self.values["load_saved_directories"] = self.load_saved_directories_bool.get()
        self.parent.save_load_system.save_value(
            input_value=str(self.values),
            file_name=self.parent.save_load_system.file_name,
        )


class SaveLoadSystem:
    """
    A simple save and load system that uses a .txt file with a
    Python dictionary by default.
    """

    def __init__(
        self,
        file_name: str,
        default_values: dict,
        extension: str = "txt",
        mutable_keys: bool = True,
    ) -> None:
        """
        Initializes a new SaveLoadSystem object.

        :param file_name: The name of the file that must be loaded and
        saved to.
        :param extension: The file extension of that file.
        :param default_values: The default values of the file.
        :param mutable_keys: Whether the keys can be different
        from the values within default_values or not.
        """
        # Create the file name and its extension with the arguments,
        # this accounts for the use of a period before the extension of
        # the file.
        self.file_name = (
            f"{file_name}" f'.{extension[1::] if "." in extension[0] else extension}'
        )

        self.values = self.initialize_values(self.file_name, default_values)
        if not mutable_keys:
            self.values = self.validate_values(
                file_name=self.file_name,
                values=self.values,
                values_to_compare_to=default_values,
            )

    def _load_default_values(
        self,
        file_name: str,
        values_to_load: dict,
        log: str = "Default values loaded: ",
    ) -> dict:
        print(f"{log}" f"{values_to_load if values_to_load is not None else {}}")
        values = values_to_load if values_to_load is not None else {}
        self.save_value(input_value=values, file_name=file_name)
        return values

    def initialize_values(self, file_name, default_values) -> dict:
        load_default_values = lambda log: self._load_default_values(
            file_name=file_name, log=log, values_to_load=default_values
        )
        # User-friendly warning.
        show_warning_messagebox = lambda title, error: messagebox.showwarning(
            title=title,
            message=f"Default values loaded.\n"
            f"Please double-check your configuration next time.\n"
            f"Traceback: {error}",
        )

        # Tries to open the file with the file name, and makes it into a
        # new file if it's not there yet.
        try:
            values = ast.literal_eval(self.load_value(file_name))
            print(f"Loaded values: {values}")
        except FileNotFoundError:
            values = load_default_values(
                f"Creating a new {file_name} (values file)...\n" f"Default values: "
            )
        except SyntaxError as e:
            values = load_default_values(
                f"{file_name} (values file) is empty or has incorrect "
                f"syntax...\n"
                f"Default values loaded: "
            )
            show_warning_messagebox(title="SyntaxError", error=e)
        except ValueError as e:
            values = load_default_values(
                f"The values in {file_name} (values file) cannot be "
                f"parsed...\n"
                f"Default values loaded: "
            )
            show_warning_messagebox(title="ValueError", error=e)

        return values

    def validate_values(
        self, values: dict, values_to_compare_to: dict, file_name: str
    ) -> dict:
        differing_keys = set(values.keys()).difference(set(values_to_compare_to.keys()))

        if not differing_keys:
            return values

        messagebox.showwarning(
            title="Changed Keys Detected",
            message=f"Please only change the values after the keys.\n"
            f"The program is not designed to handle different "
            f"keys.\n"
            f"Differing keys: {differing_keys}",
        )
        values = self._load_default_values(
            log=f"(mutable_keys=False) Loaded values have different keys...\n"
            f"Differing keys: {differing_keys}"
            f"Default values loaded: ",
            values_to_load=values_to_compare_to,
            file_name=file_name,
        )
        return values

    # Saves the values by re-writing the values into the file.
    @staticmethod
    def save_value(input_value, file_name):
        with open(file_name, "w") as f:
            f.write(str(input_value))

    # loads the values by reading the file and returning the result
    @staticmethod
    def load_value(file_name):
        with open(file_name, "r") as f:
            read = f.read()
        return read


def resource_path(relative_path):
    """PyInstaller Helper"""
    # When running as a bundle
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)

    # When running from source
    return os.path.join(os.path.abspath("."), relative_path)


# # setup
root = App(
    windows_icon=resource_path("other_essentials/app_icon.ico"),
    linux_icon=resource_path("other_essentials/app_icon.png"),
    mac_icon=resource_path("other_essentials/app_icon.icns"),
    title="Image References",
    geometry=(550, 650),
    size_changer_sizes=(454, 788),
    min_height=346,
)


def switch_theme(switch_theme_not=True):
    """Switches the appearance of the app to dark or light mode. The
    "switch_theme" arg is to update the rest of the theme when the app
    starts up again without changing the theme.
    """
    if switch_theme_not:
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")

        root.save_load_system.values["theme"] = ctk.get_appearance_mode()
        root.save_load_system.save_value(
            input_value=str(root.save_load_system.values),
            file_name=root.save_load_system.file_name,
        )

    # update the time entry color states so that they match with the
    # theme switch
    root.timer_frame.current_entry_color = (
        root.timer_frame.entry_color_dict[ctk.get_appearance_mode()][
            root.timer_frame.current_entry_color[1]
        ],
        root.timer_frame.current_entry_color[1],
    )

    for entry in (
        root.timer_frame.hour_entry,
        root.timer_frame.minute_entry,
        root.timer_frame.second_entry,
    ):
        entry.configure(text_color=root.timer_frame.current_entry_color[0])

    # update the label state colors so that they match with the theme
    # switch
    for label in (
        root.timer_frame.hour_label,
        root.timer_frame.minute_label,
        root.timer_frame.second_label,
    ):
        label.configure(
            text_color=root.timer_frame.label_color_dict[ctk.get_appearance_mode()][
                root.timer_frame.current_entry_color[1]
            ]
        )

    # updates the background of the image displayer so that it fits with
    # the rest of the app after the theme switch
    root.image_frame.image_displayer.configure(
        bg=root.image_frame.image_displayer_colors[ctk.get_appearance_mode()]
    )


# updates the currently used theme so that the image displayer and other
# label colors match up.
switch_theme(switch_theme_not=False)

# run
root.mainloop()
