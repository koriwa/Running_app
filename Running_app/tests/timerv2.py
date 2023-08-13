import tkinter as tk
import requests
import reverse_geocode
import datetime
from tkinter import customtkinter
import threading
import time
import subprocess
import psutil

root = tk.Tk()
root.geometry("495x595")
root.title("Timer")
root.resizable(width=False, height=False)

lon_lat = "db/database.txt"
accounts_file = "db/accounts.txt"

def format_time(elapsed_time):
    hours = elapsed_time // 3600000
    minutes = (elapsed_time // 60000) % 60
    seconds = (elapsed_time // 1000) % 60
    milliseconds = elapsed_time % 1000

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"

def start_timer():
    global elapsed_time, is_running
    is_running = True
    timer_tick()

    # Get the user's current coordinates and save to accounts.txt
    lat, lon = get_user_coordinates()
    if lat is not None and lon is not None:
        save_coordinates_to_lat_lon(lat, lon)

def stop_timer():
    global is_running
    is_running = False

    # Get the user's current coordinates and save to accounts.txt
    lat, lon = get_user_coordinates()
    if lat is not None and lon is not None:
        save_coordinates_to_lat_lon(lat, lon)

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
    if 10 <= day <= 20:
        return "th"
    else:
        suffixes = {1: "st", 2: "nd", 3: "rd"}
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

current_date = datetime.date.today()
day = current_date.day
month = current_date.strftime("%B")
year = current_date.year
ordinal_suffix = get_day_suffix(day)
formatted_date = f"{month} {day}{ordinal_suffix}, {year}"
date_to_display = tk.StringVar()
date_to_display.set(formatted_date)

background = r"assets\timer_backgroundv9.png"
background_image = tk.PhotoImage(file=background)
background_label = tk.Label(root, image=background_image)
background_label.place(x=-2, y=-2)

date_label = tk.Label(root, textvariable=date_to_display,
                       font=("Arial", 15, "bold"), background="white")
date_label.place(relx=0.5, y=67, anchor=tk.CENTER)

elapsed_time = 0
is_running = False
selected_measurement = tk.StringVar()
selected_measurement.set("kilometer")

def logout():
    global logged_in_username, elapsed_time, is_running
    logged_in_username = ""
    elapsed_time = 0
    is_running = False
    root.destroy()
    subprocess.Popen(["python", "log_in_page.py"])
    return

log_out_button = customtkinter.CTkButton(root, text="      Log out      ", text_color="white",
                                         hover_color="darkorange", width=10, fg_color="#FFBF00", command=logout)
log_out_button.place(x=10, y=25)

def change_measurement_type(button_type):
    if (selected_measurement.get() == "kilometer" and button_type == "meter_button"):
        selected_measurement.set("meter")
        meter_button.configure(fg_color="#f99009", hover_color="#f9ac06")
        kilometer_button.configure(fg_color="lightgray", hover_color="gray")
        distance_label_text.set("SET DISTANCE (CURRENT: METERS)")
        root.after(0, lambda: meter_button.place(relx=0.65, y=227, anchor=tk.CENTER))
        root.after(50, lambda: meter_button.place(relx=0.65, y=225, anchor=tk.CENTER))
    elif (selected_measurement.get() == "meter" and button_type == "kilometer_button"):
        selected_measurement.set("kilometer")
        kilometer_button.configure(fg_color="#f99009", hover_color="#f9ac06")
        meter_button.configure(fg_color="lightgray", hover_color="gray")
        distance_label_text.set("SET DISTANCE (CURRENT: KILOMETERS)")
        root.after(0, lambda: kilometer_button.place(relx=0.35, y=227, anchor=tk.CENTER))
        root.after(50, lambda: kilometer_button.place(relx=0.35, y=225, anchor=tk.CENTER))
    elif (button_type == "kilometer_button"):
        root.after(0, lambda: kilometer_button.place(relx=0.35, y=227, anchor=tk.CENTER))
        root.after(50, lambda: kilometer_button.place(relx=0.35, y=225, anchor=tk.CENTER))
    elif (button_type == "meter_button"):
        root.after(0, lambda: meter_button.place(relx=0.65, y=227, anchor=tk.CENTER))
        root.after(50, lambda: meter_button.place(relx=0.65, y=225, anchor=tk.CENTER))

current_date = datetime.date.today()
day = current_date.day
month = current_date.strftime("%B")
year = current_date.year
ordinal_suffix = get_day_suffix(day)
formatted_date = f"{month} {day}{ordinal_suffix}, {year}"
date_to_display = tk.StringVar()
date_to_display.set(formatted_date)

background = r"assets/timer_backgroundv9.png"
background_image = tk.PhotoImage(file=background)
background_label = tk.Label(root, image=background_image)
background_label.place(x=-2, y=-2)

date_label = tk.Label(root, textvariable=date_to_display,
                       font=("Arial", 15, "bold"), background="white")
date_label.place(relx=0.5, y=67, anchor=tk.CENTER)

elapsed_time = 0
is_running = False
selected_measurement = tk.StringVar()
selected_measurement.set("kilometer")

log_out_button = customtkinter.CTkButton(root, text="      Log out      ", text_color="white",
                                         hover_color="darkorange", width=10, fg_color="#FFBF00", command=logout)
log_out_button.place(x=10, y=25)

def change_measurement_type(button_type):
    if (selected_measurement.get() == "kilometer" and button_type == "meter_button"):
        selected_measurement.set("meter")
        meter_button.configure(fg_color="#f99009", hover_color="#f9ac06")
        kilometer_button.configure(fg_color="lightgray", hover_color="gray")
        distance_label_text.set("SET DISTANCE (CURRENT: METERS)")
        root.after(0, lambda: meter_button.place(relx=0.65, y=227, anchor=tk.CENTER))
        root.after(50, lambda: meter_button.place(relx=0.65, y=225, anchor=tk.CENTER))
    elif (selected_measurement.get() == "meter" and button_type == "kilometer_button"):
        selected_measurement.set("kilometer")
        kilometer_button.configure(fg_color="#f99009", hover_color="#f9ac06")
        meter_button.configure(fg_color="lightgray", hover_color="gray")
        distance_label_text.set("SET DISTANCE (CURRENT: KILOMETERS)")
        root.after(0, lambda: kilometer_button.place(relx=0.35, y=227, anchor=tk.CENTER))
        root.after(50, lambda: kilometer_button.place(relx=0.35, y=225, anchor=tk.CENTER))
    elif (button_type == "kilometer_button"):
        root.after(0, lambda: kilometer_button.place(relx=0.35, y=227, anchor=tk.CENTER))
        root.after(50, lambda: kilometer_button.place(relx=0.35, y=225, anchor=tk.CENTER))
    elif (button_type == "meter_button"):
        root.after(0, lambda: meter_button.place(relx=0.65, y=227, anchor=tk.CENTER))
        root.after(50, lambda: meter_button.place(relx=0.65, y=225, anchor=tk.CENTER))

def show_error():
    error_message.place(relx=0.5, y=465, anchor=tk.CENTER)
    root.after(2000, lambda: error_message.place_forget())

def record_progress():
    root.after(0, lambda: save_progress_button.place(relx=0.5, y=502, anchor=tk.CENTER))
    root.after(50, lambda: save_progress_button.place(relx=0.5, y=500, anchor=tk.CENTER))

    if (distance_entry.get() == ""):
        error_thread = threading.Thread(target=show_error)
        error_thread.start()
        return
    else:
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

        current_timestamp = int(time.time())

        with open(lon_lat, "a") as lon_lat:
            lon_lat.write(
                f"{logged_in_username.upper().strip()}={str(format_time(elapsed_time))}={set_distance}={current_timestamp}\n")

def distance_entry_focus(event):
    distance_entry.configure(validate="key", validatecommand=(validation, "%P")) 

def get_user_coordinates():
    try:
        response = requests.get("https://get.geojs.io/v1/ip/geo.json")
        data = response.json()
        return data["latitude"], data["longitude"]
    except:
        return None, None

def save_coordinates_to_lat_lon(lat, lon):
    with open(lon_lat, "r") as file:
        existing_data = file.read().strip()

    new_data = f"{lat},{lon}\n" if existing_data == "" else f"\n{lat},{lon}"
    with open(lon_lat, "a") as file:
        file.write(new_data)

def update_battery_percentage():
    battery = psutil.sensors_battery()
    percent = battery.percent
    battery_label.config(text=f"{percent}%")
    root.after(1000, update_battery_percentage)
        
battery_label = tk.Label(root, font=("Arial", 12))
battery_label.place(relx=0.9, y=25)

distance_label_text = tk.StringVar()
distance_label_text.set("SET DISTANCE (CURRENT: KILOMETERS)")

distance_label = tk.Label(
    root, textvariable=distance_label_text, font=("Arial", 10, "bold"))
distance_label.place(relx=0.5, y=135, anchor=tk.CENTER)

meter_button = customtkinter.CTkButton(root, text="      METER      ", text_color="white", fg_color="lightgray",
                                       hover_color="gray", corner_radius=50, width=10, command=lambda: change_measurement_type("meter_button"))
meter_button.place(relx=0.65, y=225, anchor=tk.CENTER)

kilometer_button = customtkinter.CTkButton(root, text="KILOMETER", text_color="white", fg_color="#f99009",
                                           hover_color="#f97f01", corner_radius=50, width=10, command=lambda: change_measurement_type("kilometer_button"))
kilometer_button.place(relx=0.35, y=225, anchor=tk.CENTER)

validation = root.register(allowed_inputs)  # Register the validation function
distance_entry = customtkinter.CTkEntry(root, placeholder_text="  TRAVELLED DISTANCE", bg_color="white",
                                       fg_color="white", border_color="white", text_color="black", font=("Arial", 19, "bold"), width=255)
distance_entry.place(relx=0.5, y=166.5, anchor=tk.CENTER)
distance_entry.bind("<FocusIn>", distance_entry_focus)

outer_frame = tk.Frame(root)
outer_frame.place(relx=0.5, y=400, anchor=tk.CENTER)

timer_text_label = tk.Label(
    root, text="T I M E R", font=("Arial", 15, "bold"))
timer_text_label.place(relx=0.5, y=295, anchor=tk.CENTER)

timer_label = tk.Label(root, text="00:00:00:000",
                        font=("Arial", 35), background="white")
timer_label.place(relx=0.5, y=345, anchor=tk.CENTER)

start_button = tk.Button(outer_frame, text="Start",
                          width=10, command=start_timer)
start_button.pack(side=tk.LEFT, padx=10)

stop_button = tk.Button(outer_frame, text="Stop",
                         width=10, command=stop_timer)
stop_button.pack(side=tk.LEFT)

reset_button = tk.Button(outer_frame, text="Reset",
                          width=10, command=reset_timer)
reset_button.pack(side=tk.LEFT, padx=10)

error_message = tk.Label(root, text="A DISTANCE MUST BE SET TO RECORD THE PROGRESS!", font=(
    "Arial", 11, "bold"), foreground="red")
save_progress_button = customtkinter.CTkButton(root, text="RECORD PROGRESS", text_color="white", fg_color="#f98a06",
                                               hover_color="#f9ac06", corner_radius=50, width=10, command=record_progress, font=("Arial", 20, "bold"))
save_progress_button.place(relx=0.5, y=500, anchor=tk.CENTER)


update_battery_percentage()

root.mainloop()

