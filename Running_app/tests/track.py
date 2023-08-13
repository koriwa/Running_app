import requests
import reverse_geocode


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


def save_coordinates_to_txt(lat, lon):
    with open("database.txt", "w") as file:
        file.write(f"Latitude: {lat}, Longitude: {lon}")


# Example usage:
lat, lon = get_location()

if lat is not None and lon is not None:
    print(f"Latitude: {lat}, Longitude: {lon}")
    weather = get_weather(lat, lon)
    print(f"Current weather: {weather}")

    save_coordinates_to_txt(lat, lon)  # Save the coordinates to a text file
else:
    print("Location not found.")
