from tkinter import *
import tkinter as tk
from tkinter import ttk
import datetime
import threading
import sys
import time
import subprocess
from PIL import ImageTk, Image
import customtkinter


# Create the main root window
root = Tk()
root.geometry("495x595")
root.title("Timer")
root.resizable(width=False, height=False)

# Initialize the username variable with a default value "Guest"
# Global Variables
Logged_in_username = ""
elapsed_time = 0
is_running = False
selected_measurement = StringVar()
recorded_entries = set()

# Check if a username is provided as a command-line argument, if not, set
# it as "Guest"
if (len(sys.argv) > 1):
    Logged_in_username = sys.argv[1]
    print(Logged_in_username)

if (Logged_in_username == ""):
    Logged_in_username = "Guest"

# Print the logged-in username for debugging purposes
print(Logged_in_username)

# Define the file name for storing user timer data
user_timer_data_file = "db/user_timer_data.txt"

# battery = psutil.sensors_battery()
# percent = battery.percent

# Function to center a window on the screen


def center_window(window):
    """
    Centers the specified window on the screen.

    Args:
        window: The tkinter window to be centered.
    """
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    center_x = (screen_width - width) // 2
    center_y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{center_x}+{center_y}")


center_window(root)


# Formats the time
def format_time(elapsed_time):
    hours = elapsed_time // 3600000
    minutes = (elapsed_time // 60000) % 60
    seconds = (elapsed_time // 1000) % 60
    milliseconds = elapsed_time % 1000

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"


def start_timer():
    global elapsed_time, is_running
    is_running = True
    # Disable the "Start" button
    start_button.config(state=tk.DISABLED)
    # Enable the "Stop" button
    stop_button.config(state=tk.NORMAL)
    timer_tick()

# Function to stop the timer
def stop_timer():
    global is_running
    is_running = False
    # Re-enable the "Start" button
    start_button.config(state=tk.NORMAL)
    # Disable the "Stop" button
    stop_button.config(state=tk.DISABLED)
    # Enable the "Reset" button if the timer isn't at 00:00:000
    if elapsed_time != 0:
        reset_button.config(state=tk.NORMAL)

# Function to reset the timer
def reset_timer():
    global elapsed_time, is_running
    if not is_running:
        elapsed_time = 0
        # Re-enable the "Start" button
        start_button.config(state=tk.NORMAL)
        # Disable the "Stop" button
        stop_button.config(state=tk.DISABLED)
        # Disable the "Reset" button if the timer is already at 00:00:000
        if elapsed_time == 0:
            reset_button.config(state=tk.DISABLED)
        else:
            reset_button.config(state=tk.NORMAL)
        timer_label.config(text=format_time(elapsed_time))


# Handles each tick of the timer
def timer_tick():
    global elapsed_time, is_running
    if is_running:
        elapsed_time += 10
        timer_label.config(text=format_time(elapsed_time))
    timer_label.after(10, timer_tick)


# Function to get the suffix for a day number (e.g., 1st, 2nd, 3rd, 4th, ...)
def get_day_suffix(day):
    if (10 <= day <= 20):
        return "th"
    else:
        suffixes = {
            1: "st",
            2: "nd",
            3: "rd"
        }
        suffix = suffixes.get(day % 10, "th")
        return suffix

# Function to validate allowed inputs (digits, empty input, or a single
# decimal number)


def allowed_inputs(input_text):
    if input_text.isdigit():  # Check if the input consists only of digits
        return True
    elif input_text == "":  # Allow an empty input
        return True
    elif input_text.count('.') == 1 and input_text.replace('.', '').isdigit():
        return True
    else:
        return False


# Get the current date
current_date = datetime.date.today()

# Extract the day, month, and year from the current date
day = current_date.day
month = current_date.strftime("%B")
year = current_date.year

# Get the ordinal suffix for the day (e.g., 1st, 2nd, 3rd, 4th, ...)
ordinal_suffix = get_day_suffix(day)

# Format the date with the day, month, year, and the ordinal suffix
formatted_date = f"{month} {day}{ordinal_suffix}, {year}"

# Create a StringVar to hold the formatted date, and set it as the value
# for date_to_display
date_to_display = StringVar()
date_to_display.set(formatted_date)

# Load the background image for the timer
background = r"assets/timer_backgroundv9.png"
background_image = ImageTk.PhotoImage(Image.open(background))

# Create a label to display the background image
background_label = ttk.Label(root, image=background_image)
background_label.place(x=-2, y=-2)

# Create a label to display the formatted date
date_label = ttk.Label(root, textvariable=date_to_display,
                       font=("Arial", 15, "bold"), background="white")
date_label.place(relx=0.5, y=67, anchor=tk.CENTER)

# Initialize the timer to zero and set its running status to False
elapsed_time = 0
is_running = False

# Create a StringVar to keep track of the selected measurement
# (kilometer/meter)
selected_measurement = StringVar()
selected_measurement.set("kilometer")

# Define a set to keep track of recorded entries
recorded_entries = set()

# Function to log out the user and reset timer-related variables
def logout():
    global Logged_in_username, elapsed_time, is_running
    Logged_in_username = ""  # Clear the Logged_in_username
    elapsed_time = 0  # Reset the elapsed_time to 0
    is_running = False  # Set the timer to not running
    root.destroy()  # Close the window or perform any other desired actions
    # Open log_in_page.py using subprocess
    subprocess.Popen(["python", "log_in_page.py"])
    return


def log():
    global Logged_in_username, elapsed_time, is_running
    root.destroy()  # Close the window or perform any other desired actions
    # Open log.py using subprocess
    subprocess.Popen(["python", "log.py", Logged_in_username])
    return

# Create a custom button for logging out
log_out_button = customtkinter.CTkButton(
    root,
    text="      Log out      ",
    text_color="white",
    hover_color="darkorange",
    width=10,
    fg_color="#FFBF00",
    command=logout,
    bg_color="orange")
log_out_button.place(x=10, y=25)  # Place the log_out_button on the window

log_button = customtkinter.CTkButton(
    root,
    text="      Log      ",
    text_color="white",
    hover_color="darkorange",
    width=10,
    fg_color="#FFBF00",
    command=log,
    bg_color="orange")
log_button.place(x=415, y=25)  # Place the log_out_button on the window

# Function to change the measurement type (kilometer/meter) for distance
def change_measurement_type(button_type):
    # Check the currently selected measurement type and the button_type
    # parameter to determine the action
    if (selected_measurement.get() ==
            "kilometer" and button_type == "meter_button"):
        # If the current measurement is kilometers and the meter button is clicked:
        # Set the selected_measurement to "meter"
        selected_measurement.set("meter")
        # Configure the appearance of the meter_button to indicate it's
        # selected
        meter_button.configure(fg_color="#f99009", hover_color="#f9ac06")
        # Configure the appearance of the kilometer_button to indicate it's
        # unselected
        kilometer_button.configure(fg_color="lightgray", hover_color="gray")
        # Update the distance label to reflect the change in measurement
        distance_label_text.set("SET DISTANCE (CURRENT: METERS)")
        # Place the meter_button with a slight delay to give a smooth visual
        # transition
        root.after(0, lambda: meter_button.place(
            relx=0.65, y=227, anchor=tk.CENTER))
        root.after(50, lambda: meter_button.place(
            relx=0.65, y=225, anchor=tk.CENTER))

    elif (selected_measurement.get() == "meter" and button_type == "kilometer_button"):
        # If the current measurement is meters and the kilometer button is clicked:
        # Set the selected_measurement to "kilometer"
        selected_measurement.set("kilometer")
        # Configure the appearance of the kilometer_button to indicate it's
        # selected
        kilometer_button.configure(fg_color="#f99009", hover_color="#f9ac06")
        # Configure the appearance of the meter_button to indicate it's
        # unselected
        meter_button.configure(fg_color="lightgray", hover_color="gray")
        # Update the distance label to reflect the change in measurement
        distance_label_text.set("SET DISTANCE (CURRENT: KILOMETERS)")
        # Place the kilometer_button with a slight delay to give a smooth
        # visual transition
        root.after(0, lambda: kilometer_button.place(
            relx=0.35, y=227, anchor=tk.CENTER))
        root.after(50, lambda: kilometer_button.place(
            relx=0.35, y=225, anchor=tk.CENTER))

    elif (button_type == "kilometer_button"):
        # If the button_type is "kilometer_button" (but the current measurement is not changing):
        # Place the kilometer_button with a slight delay to give a smooth
        # visual transition
        root.after(0, lambda: kilometer_button.place(
            relx=0.35, y=227, anchor=tk.CENTER))
        root.after(50, lambda: kilometer_button.place(
            relx=0.35, y=225, anchor=tk.CENTER))

    elif (button_type == "meter_button"):
        # If the button_type is "meter_button" (but the current measurement is not changing):
        # Place the meter_button with a slight delay to give a smooth visual
        # transition
        root.after(0, lambda: meter_button.place(
            relx=0.65, y=227, anchor=tk.CENTER))
        root.after(50, lambda: meter_button.place(
            relx=0.65, y=225, anchor=tk.CENTER))


# Function to show the error message and hide it after 2000ms
def show_error():
    error_message.place(relx=0.5, y=465, anchor=tk.CENTER)
    root.after(2000, lambda: error_message.place_forget())


def record_progress():
    # Show the save_progress_button on the window
    root.after(0, lambda: save_progress_button.place(
        relx=0.5, y=502, anchor=tk.CENTER))
    root.after(50, lambda: save_progress_button.place(
        relx=0.5, y=500, anchor=tk.CENTER))

    # Check if a distance is provided
    if (distance_entry.get() == ""):
        # If distance is not provided, show an error message in a new thread
        error_thread = threading.Thread(target=show_error)
        error_thread.start()
        return
    else:
        # Convert the distance to a numeric value
        distance_string = str(distance_entry.get())
        set_distance = 0

        if selected_measurement.get() == "kilometer":
            if distance_string.endswith('.'):
                distance_string = distance_string[:-1]
            set_distance = float(distance_string) * 1000
        elif selected_measurement.get() == "meter":
            if distance_string.endswith('.'):
                distance_string = distance_string[:-1]
            set_distance = float(distance_string)

        # Get the current timestamp in seconds
        current_timestamp = int(time.time())

        # Get the current date in the format "Month Day, Year"
        current_date = datetime.datetime.now().strftime("%B %d, %Y")

        # Create a unique identifier for this entry
        entry_id = f"{Logged_in_username.strip()}_{set_distance}_{current_date}"

        # Check if the entry is already recorded
        if entry_id in recorded_entries:
            # Display an error message label if the same entry is found
            error_label.config(
                text="Duplicate entry detected. Please record a different progress.")
            error_label.place(relx=0.5, y=530, anchor=tk.CENTER)
            root.after(3000, lambda: error_label.place_forget())
            return
        else:
            # Add the entry_id to the recorded_entries set
            recorded_entries.add(entry_id)

        # Open the user_timer_data_file in append mode to add new data
        with open(user_timer_data_file, "a", encoding='utf-8') as user_timer_data:
            # Write the data in the format:
            # "username=elapsed_time=set_distance=current_timestamp=date"
            user_timer_data.write(
                f"{Logged_in_username.strip()}={str(format_time(elapsed_time))}={set_distance}={current_timestamp}={current_date}\n")

# Function to handle focus event on distance entry
def distance_entry_focus():
    distance_entry.configure(
        validate="key", validatecommand=(validation, "%P"))

distance_label_text = StringVar()
distance_label_text.set("SET DISTANCE (CURRENT: KILOMETERS)")

distance_label = ttk.Label(
    root, textvariable=distance_label_text, font=("Arial", 10, "bold"))
distance_label.place(relx=0.5, y=135, anchor=tk.CENTER)

error_label = ttk.Label(root, text="", font=(
    "Arial", 11, "bold"), foreground="red")

meter_button = customtkinter.CTkButton(
    root,
    text="      METER      ",
    text_color="white",
    fg_color="lightgray",
    hover_color="gray",
    corner_radius=50,
    width=10,
    command=lambda: change_measurement_type("meter_button"))
meter_button.place(relx=0.65, y=225, anchor=tk.CENTER)

kilometer_button = customtkinter.CTkButton(
    root,
    text="KILOMETER",
    text_color="white",
    fg_color="#f99009",
    hover_color="#f97f01",
    corner_radius=50,
    width=10,
    command=lambda: change_measurement_type("kilometer_button"))
kilometer_button.place(relx=0.35, y=225, anchor=tk.CENTER)

validation = root.register(allowed_inputs)  # Register the validation function
distance_entry = customtkinter.CTkEntry(
    root,
    placeholder_text="  TRAVELLED DISTANCE",
    bg_color="white",
    fg_color="white",
    border_color="white",
    text_color="black",
    font=(
        "Arial",
        19,
        "bold"),
    width=255)
distance_entry.place(relx=0.5, y=166.5, anchor=tk.CENTER)
distance_entry.bind("<FocusIn>", distance_entry_focus)

outer_frame = Frame(root)
outer_frame.place(relx=0.5, y=400, anchor=tk.CENTER)

timer_text_label = ttk.Label(
    root, text="T I M E R", font=("Arial", 15, "bold"))
timer_text_label.place(relx=0.5, y=295, anchor=tk.CENTER)

timer_label = ttk.Label(root, text="00:00:00:000",
                        font=("Arial", 35), background="white")
timer_label.place(relx=0.5, y=345, anchor=tk.CENTER)

start_button = ttk.Button(outer_frame, text="Start",
                          width=10, command=start_timer)
start_button.pack(side=tk.LEFT, padx=10)

stop_button = ttk.Button(outer_frame, text="Stop",
                         width=10, command=stop_timer)
stop_button.pack(side=tk.LEFT)

reset_button = ttk.Button(outer_frame, text="Reset",
                          width=10, command=reset_timer,
                          state=tk.DISABLED)
reset_button.pack(side=tk.LEFT, padx=10)

error_message = ttk.Label(
    root,
    text="A DISTANCE MUST BE SET TO RECORD THE PROGRESS!",
    font=(
        "Arial",
        11,
        "bold"),
    foreground="red")
save_progress_button = customtkinter.CTkButton(
    root,
    text="RECORD PROGRESS",
    text_color="white",
    fg_color="#f98a06",
    hover_color="#f9ac06",
    corner_radius=50,
    width=10,
    command=record_progress,
    font=(
        "Arial",
        20,
         "bold"))
save_progress_button.place(relx=0.5, y=500, anchor=tk.CENTER)


root.mainloop()
