import tkinter as tk
import requests
from geopy.geocoders import Nominatim

lat_lon = "db\database.txt"


def format_time(elapsed_time):
    hours = elapsed_time // 3600000
    minutes = (elapsed_time // 60000) % 60
    seconds = (elapsed_time // 1000) % 60
    milliseconds = elapsed_time % 1000

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"


def start_timer():
    global elapsed_time, is_running, start_time
    is_running = True
    start_time = elapsed_time
    save_start_coordinates()  # Save the start coordinates
    timer_tick()


def stop_timer():
    global is_running, stop_time
    is_running = False
    stop_time = elapsed_time
    save_coordinates_to_database()


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


def get_weather(lat, lon):
    url = 'https://api.openweathermap.org/data/2.5/weather?q=Auckland&appid='
    params = {
        'lat': lat,
        'lon': lon,
        'appid': 'c6165bbc9ba64babc84b5557d1c160483'
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'weather' in data:
        weather = data['weather'][0]['description']
        return weather
    else:
        return 'Unknown'


def save_start_coordinates():
    lat, lon = get_location()
    if lat is not None and lon is not None:
        geolocator = Nominatim(user_agent="timer_app")
        location = geolocator.reverse((lat, lon), exactly_one=True)
        city = location.address.split(",")[-3] if location else 'Unknown'

        with open(lat_lon, "a") as file:
            file.write(
                f"Start - Latitude: {lat}, Longitude: {lon}, City: {city}\n")


def save_start_coordinates():
    lat, lon = get_location()
    if lat is not None and lon is not None:
        geolocator = Nominatim(user_agent="timer_app")
        location = geolocator.reverse((lat, lon), exactly_one=True)
        city = location.address.split(",")[-3] if location else 'Unknown'

        with open(lat_lon, "a") as file:
            file.write(
                f"Start - Latitude: {lat}, Longitude: {lon}, City: {city}, Timer: {format_time(start_time)}\n")


def save_coordinates_to_database():
    lat, lon = get_location()
    if lat is not None and lon is not None:
        geolocator = Nominatim(user_agent="timer_app")
        location = geolocator.reverse((lat, lon), exactly_one=True)
        city = location.address.split(",")[-3] if location else 'Unknown'

        with open(lat_lon, "a") as file:
            file.write(
                f"Stop - Latitude: {lat}, Longitude: {lon}, City: {city}, Timer: {format_time(start_time)} - {format_time(stop_time)}\n")


elapsed_time = 0
is_running = False
start_time = 0
stop_time = 0

root = tk.Tk()
root.title("Timer App")

outer_frame = tk.Frame(root, bd=2)
outer_frame.pack(padx=10, pady=10)

timer_frame = tk.Frame(outer_frame, bd=2)
timer_frame.pack()

canvas = tk.Canvas(timer_frame, width=280, height=80)
canvas.pack()

timer_label = tk.Label(canvas, text="00:00:00:000", font=("Arial", 20))
timer_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

start_button = tk.Button(outer_frame, text="Start", width=10, command=start_timer)
start_button.pack(side=tk.LEFT, padx=10)

stop_button = tk.Button(outer_frame, text="Stop", width=10, command=stop_timer)
stop_button.pack(side=tk.LEFT)

reset_button = tk.Button(outer_frame, text="Reset", width=10, command=reset_timer)
reset_button.pack(side=tk.LEFT, padx=10)

root.mainloop()
