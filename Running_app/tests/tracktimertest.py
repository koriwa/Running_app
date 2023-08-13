import tkinter as tk
import requests
import reverse_geocode

lat_lon = "db/database.txt"

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

def stop_timer():
    global is_running
    is_running = False
    save_coordinates_to_database()

def reset_timer():
    global elapsed_time, is_running
    if not is_running:
        elapsed_time = 0
        is_running = False
        timer_label.config(text=format_time(elapsed_time))

def timer_tick(): #
    global elapsed_time, is_running
    if is_running:
        elapsed_time += 10
        timer_label.config(text=format_time(elapsed_time))
    timer_label.after(10, timer_tick)

def get_user_coordinates():
    try:
        with open("database.txt", "r", encoding= "cp1252") as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip()
                lat_lon_city = last_line.split(", ")
                latitude = float(lat_lon_city[0].split(": ")[1])
                longitude = float(lat_lon_city[1].split(": ")[1])
                return latitude, longitude
            else:
                return None, None
    except FileNotFoundError:
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

def save_coordinates_to_database():
    lat, lon = get_user_coordinates()
    if lat is not None and lon is not None:
        try:
            # Use reverse_geocode library to get location name (city) based on latitude and longitude
            location_data = reverse_geocode.search((lat, lon))
            city = location_data[0]['city'] if location_data else 'Unknown'

            # Save the coordinates and city to the lat_lon file with UTF-8 encoding
            with open(lat_lon, "a", encoding="utf-8") as file:
                file.write(f"Latitude: {lat}, Longitude: {lon}, City: {city}\n")
            
            print("Coordinates saved successfully.")
        except Exception as e:
            print(f"Error saving coordinates: {e}")
    else:
        print("Coordinates not available.")



elapsed_time = 0
is_running = False

root = tk.Tk()
root.title("Timer App")

# Create the outer frame
outer_frame = tk.Frame(root, bd=2)
outer_frame.pack(padx=10, pady=10)

# Create the inner frame to hold the timer
timer_frame = tk.Frame(outer_frame, bd=2)
timer_frame.pack()

# Create a canvas to place the timer label
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

