import tkinter as tk
import requests
from tkinter import ttk
from PIL import ImageTk, Image
import datetime
import sys
import time
import subprocess
from math import radians, sin, cos, sqrt, atan2
import reverse_geocode

import tkinter as tk
import requests
from tkinter import ttk
from PIL import ImageTk, Image
import datetime
import sys
import time
import subprocess
from math import radians, sin, cos, sqrt, atan2
import gpsd

lat_lon = "db/database.txt"

def format_time(elapsed_time):
    hours = elapsed_time // 3600000
    minutes = (elapsed_time // 60000) % 60
    seconds = (elapsed_time // 1000) % 60
    milliseconds = elapsed_time % 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"

def get_location():
    url = 'http://api.ipstack.com/check'
    access_key = 'd9fd00991e116ca7b01b8cd957b2fcf1'
    params = {
        'access_key': access_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'latitude' in data and 'longitude' in data:
        return data['latitude'], data['longitude']
    else:
        return None, None

start_latitude, start_longitude = None, None

def save_start_coordinates():
    global start_latitude, start_longitude
    lat, lon = get_location()
    
    if lat is not None and lon is not None:
        start_latitude, start_longitude = lat, lon
        
        with open(lat_lon, "a", encoding="utf-8") as file:
            file.write(f"Start - Latitude: {lat}, Longitude: {lon}\n")

def save_stop_coordinates(start_time, stop_time):
    global start_latitude, start_longitude
    lat, lon = get_location()
    
    if lat is not None and lon is not None:
        stop_latitude, stop_longitude = lat, lon
        
        with open(lat_lon, "a", encoding="utf-8") as file:
            file.write(f"Stop - Latitude: {lat}, Longitude: {lon}, Timer: {format_time(start_time)} - {format_time(stop_time)}\n")
        
        distance = calculate_distance(start_latitude, start_longitude, stop_latitude, stop_longitude)
        distance_label.config(text=f"Distance: {distance:.2f} km")

def calculate_distance(start_lat, start_lon, stop_lat, stop_lon):
    # Radius of the Earth in kilometers
    R = 6371.0

    lat1 = radians(start_lat)
    lon1 = radians(start_lon)
    lat2 = radians(stop_lat)
    lon2 = radians(stop_lon)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def start_timer():
    global elapsed_time, is_running, start_time
    is_running = True
    start_time = elapsed_time
    save_start_coordinates()
    timer_tick()

def stop_timer():
    global is_running, stop_time
    is_running = False
    stop_time = elapsed_time
    save_stop_coordinates(start_time, stop_time)

def reset_timer():
    global elapsed_time, is_running
    if not is_running:
        elapsed_time = 0
        is_running = False
        timer_label.config(text=format_time(elapsed_time))

def timer_tick():
    global elapsed_time, is_running
    if is_running:
        elapsed_time += 10
        timer_label.config(text=format_time(elapsed_time))
    timer_label.after(10, timer_tick)


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


def allowed_inputs(input_text):
    if input_text.isdigit():
        return True
    elif input_text == "":
        return True
    elif input_text.count('.') == 1 and input_text.replace('.', '').isdigit():
        return True
    else:
        return False


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def logout():
    global logged_in_username, elapsed_time, is_running
    logged_in_username = ""
    elapsed_time = 0
    is_running = False
    root.destroy()
    subprocess.Popen(["python", "log_in_page.py"])
    return


# Create the main root window
root = tk.Tk()
root.geometry("495x595")
root.title("Timer")
root.resizable(width=False, height=False)


# Initialize the username variable with a default value "Guest"
logged_in_username = ""

# Check if a username is provided as a command-line argument, if not, set it as "Guest"
if (len(sys.argv) > 1):
    logged_in_username = sys.argv[1]

if (logged_in_username == ""):
    logged_in_username = "Guest"

# Print the logged-in username for debugging purposes
print(logged_in_username)

background = r"assets\timer_backgroundv10.png"
background_image = ImageTk.PhotoImage(Image.open(background))

background_label = ttk.Label(root, image=background_image)
background_label.place(x=-2, y=-2)

# Define the StringVar for displaying the formatted date
date_to_display = tk.StringVar()

date_label = ttk.Label(root, textvariable=date_to_display,
                       font=("Arial", 15, "bold"), background="white")
date_label.place(relx=0.5, y=67, anchor=tk.CENTER)

# Get the current date
current_date = datetime.date.today()

# Extract the day, month, and year from the current date
day = current_date.day
month = current_date.strftime("%B")
year = current_date.year

ordinal_suffix = get_day_suffix(day)
formatted_date = f"{month} {day}{ordinal_suffix}, {year}"

date_to_display.set(formatted_date)  # Set the initial value of the StringVar

elapsed_time = 0
is_running = False

outer_frame = tk.Frame(root)
outer_frame.place(relx=0.5, y=400, anchor=tk.CENTER)

timer_text_label = ttk.Label(
    root, text="T I M E R", font=("Arial", 15, "bold"))
timer_text_label.place(relx=0.5, y=295, anchor=tk.CENTER)

timer_label = ttk.Label(root, text="00:00:00:000",
                        font=("Arial", 35), background="white")
timer_label.place(relx=0.5, y=345, anchor=tk.CENTER)

distance_label = ttk.Label(root, text="Distance: 0.00 km", font=("Arial", 12))
distance_label.place(relx=0.5, y=240, anchor=tk.CENTER)

start_button = ttk.Button(outer_frame, text="Start",
                          width=10, command=start_timer)
start_button.pack(side=tk.LEFT, padx=10)

stop_button = ttk.Button(outer_frame, text="Stop",
                         width=10, command=stop_timer)
stop_button.pack(side=tk.LEFT)

reset_button = ttk.Button(outer_frame, text="Reset",
                          width=10, command=reset_timer)
reset_button.pack(side=tk.LEFT, padx=10)

root.mainloop()
