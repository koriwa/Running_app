import tkinter as tk
import tkinter.ttk as ttk
import subprocess
import sys
from PIL import ImageTk, Image
import customtkinter

# Create the main log window
log = tk.Tk()
log.geometry("800x600")
log.title("Recorded Progress")
log.resizable(width=False, height=False)

# function to center the window
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


# Center the log window on the screen
center_window(log)

# Load the background image
background = Image.open("assets/log_background.png")
background_image = ImageTk.PhotoImage(background)

# Create a Label to display the background image
background_label = tk.Label(log, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Get the logged-in username from command-line argument or set a default
LOGGED_IN_USERNAME = sys.argv[1] if len(sys.argv) > 1 else "Guest"

try:
    # Read recorded data from the user_timer_data.txt file
    with open("db/user_timer_data.txt", "r", encoding='utf-8') as data_file:
        recorded_data = data_file.readlines()

    # Filter the data to display only the records for the logged-in user
    user_data = [entry.strip() for entry in recorded_data if entry.split('=')
                 [0] == LOGGED_IN_USERNAME]

    # Create a Treeview widget for displaying the table
    table_frame = tk.Frame(log, bg="orange")
    table_frame.pack(pady=10)

    # Create a vertical scrollbar for the table
    scrollbar = ttk.Scrollbar(table_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create the Treeview widget with a scrollbar
    table = ttk.Treeview(
        table_frame,
        columns=("Date", "Time", "Distance"),
        show="headings",
        height=20,
        yscrollcommand=scrollbar.set)
    table.heading("Date", text="Date")
    table.heading("Time", text="Time")
    table.heading("Distance", text="Distance (km)")
    table.pack()

    # Configure the scrollbar to work with the table
    scrollbar.config(command=table.yview)

    # Bind mouse events to simulate the hover effect
    table.tag_configure("hover")

    # Insert data into the table
    if user_data:
        for entry in user_data:
            entry_parts = entry.split("=")
            if len(entry_parts) == 5:
                _, elapsed_time, set_distance, current_timestamp, current_date = entry_parts
                # Convert the distance from meters to kilometers
                set_distance_km = float(set_distance) / 1000
                table.insert(
                    "", "end", values=(
                        current_date, elapsed_time, f"{set_distance_km:.2f} km"), tags=(
                        "normal",))
    else:
        # Handle the case when no recorded data is found for the user
        record_label = tk.Label(
            log, text="No recorded data found for this user.", font=(
                "Arial", 12), fg="orange")
        record_label.pack(pady=10)

    # Function to handle mouse enter event (hover)
    def on_enter(event):
        """
        Handles the mouse enter event for the Treeview table rows. (basically the hover)
        """
        item = table.identify_row(event.y)
        if item:
            table.item(item, tags=("hover",))

    # Function to handle mouse leave event (hover exit)
    def on_leave(event):
        """
        Handles the mouse leave event for the Treeview table rows. (basically the hover again)
        """
        item = table.identify_row(event.y)
        if item:
            table.item(item, tags=("normal",))

    # Bind mouse enter and leave events
    table.bind("<Enter>", on_enter)
    table.bind("<Leave>", on_leave)

except FileNotFoundError:
    # Handle the case when the file is not found
    record_label = tk.Label(
        log, text="No recorded data found.", font=("Arial", 12), fg="black")
    record_label.pack(pady=10)

# Function to navigate back to the timer page


def back_button_function():
    """
    Destroys the current log window and navigates back to the timer page.
    """
    log.destroy()
    subprocess.Popen(["python", "timer.py", LOGGED_IN_USERNAME])


# Create a custom "Back" button
back_button = customtkinter.CTkButton(
    master=log,
    width=100,
    text="Back",
    bg_color="white",
    command=back_button_function,
    corner_radius=100,
    fg_color="#FFBF00",
    hover_color="dark orange")
back_button.place(x=30, y=475)

# Start the main GUI loop
log.mainloop()
