import requests


API_KEY = "key goes here"

def get_coordinates(place_name):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={place_name}&key={API_KEY}"
    response = requests.get(url).json()

    if response["status"] == "OK":
        location = response["results"][0]["geometry"]["location"]
        lat, lng = location["lat"], location["lng"]
        return lat, lng
    else:
        print("Error:", response["status"])
        return None, None

# Example Usage
place = "Eiffel Tower"

for i in range(300):
    latitude, longitude = get_coordinates(place)

    if latitude and longitude:
        print(f"{place} is located at Latitude: {latitude}, Longitude: {longitude}")
    else:
        print("Could not find location.")



