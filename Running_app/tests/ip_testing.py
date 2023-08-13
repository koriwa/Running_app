import requests

def get_ip_address(api_key):
    # Replace 'YOUR_API_KEY' with your actual ipstack.com API key
    url = f"http://api.ipstack.com/check?access_key={api_key}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            ip_address = data.get("ip")
            if ip_address:
                callback_url = f"http://{ip_address}/callback"
            else:
                print("Unable to get IP address from the API response.")
        else:
            print("Failed to get IP address:", response.text)
    except requests.RequestException as e:
        print("Error occurred:", e)

# Replace 'YOUR_API_KEY' with your actual ipstack.com API key
api_key = "d9fd00991e116ca7b01b8cd957b2fcf1"
get_ip_address(api_key)