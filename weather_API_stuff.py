
import json, re, requests, time
from geopy.geocoders import Nominatim
from requests import ReadTimeout
geolocator = Nominatim(user_agent="geoapiExercises")
'''
my idea is:
ask for user input of lat and long
identify which country the person is in
then, depending on the country, cross the data with the most played song in that week in that country
find the genre (for that, need to relate the songs to the artists and then find the genre)
--see the most popular genre (regex maybe? or create a counter)
and then see if there is a relation to genre and the average tempertaure in that region in that week!
i also want to use regex for error handling when dealing with inputs'''

playlist_id_pattern = r"[A-Za-z0-9]{22}"
word_pattern = r"\w+"

country_playlist = {
    "sweden": "37i9dQZEVXbKVvfnL1Us06",
    "united states": "37i9dQZEVXbLRQDuF5jeBp",
    "brazil": "37i9dQZEVXbKzoK95AbRy9",
    "canada": "37i9dQZEVXbMda2apknTqH",
    "italy": "37i9dQZEVXbIQnj7RRhdSX",
    "france": "37i9dQZEVXbKQ1ogMOyW9N",
    "denmark": "37i9dQZEVXbL3J0k32lWnN",
    }


def append_country_playlist(country):
    global country_playlist
    answer = input (f"Seems that {country} is not in our system. Would you like to add it? [y] for yes: ")
    if answer == "y":
        playlist_id = input(f"Insert playlist ID for {country}: ")

        if re.match(playlist_id_pattern, playlist_id):
            country_playlist[country] = playlist_id
            return playlist_id

        else:
            print("Invalid arguments.")
            return append_country_playlist(country)

    else:
        print("ending program...")
        return None

def get_country_playlist(lat, long):   
    global country_playlist
    try:    
        location = f"https://nominatim.openstreetmap.org/reverse.php?format=json&lat={lat}&lon={long}&accept-language=en"  
        response_location = requests.get(location, timeout = 5) 

        if response_location.status_code == 403:
            print(f"Error: Received 403 Forbidden. The location API request was blocked.")
            answer = input("Would you like to inform your country and playlist ID? [y] for yes: ")
            if answer == "y":
                country = input("Insert your country: ")
                if re.match(word_pattern, country):
                    return append_country_playlist(country)
        
        elif response_location.status_code != 200:
            print(f"Error: Received {response_location.status_code} from location API.")
            return None
       
        data_location = response_location.json()
        country = data_location["address"]["country"]
        
        print(f"Seems you are in {country}!")
        country = country.lower()
        if country in country_playlist.keys():
            return country_playlist.get(country)
        elif country not in country_playlist.keys():
            return append_country_playlist(country)
    except ReadTimeout:
        print("Error in get country playlist")
    

def get_average_temp(lat, long):
    try:   
        weather = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&past_days=7&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
         
        response_weather = requests.get(weather)
        data_weather = response_weather.json()
        
        sum_temp = 0
        for temperature in data_weather["hourly"]["temperature_2m"]:
            sum_temp += temperature
        average_temp = sum_temp/(len(data_weather["hourly"]["temperature_2m"]))
        return f"{average_temp:.2f}"
    
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_top_artists(country_playlist):
    service = "https://dit009-spotify-assignment.vercel.app/api/v1"
    csv_artists_id = ""
    i = 0
    try:
        top_tracks_week = f"{service}/playlists/{country_playlist}/tracks"  
        response_top_tracks = requests.get(top_tracks_week, timeout = 10)
        if response_top_tracks == 429:
            
            retry_after = int(response_top_tracks.headers.get("Retry-After", 20))
            print(f"Rate limited. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
            
            
            response_top_tracks = requests.get(top_tracks_week, timeout=5)

        data_top_tracks = response_top_tracks.json()
       
        for item in data_top_tracks["items"]:
            track = item["track"]
            artists = track["artists"]  
            
            for artist in artists:
                while i < 20:
                    if "id" in artist.keys():
                        artist_id = artist["id"]
                        csv_artists_id += artist_id + ","
                        i += 1
                            
                
            return csv_artists_id[:-1] # removing the last coma
    
    
    except ReadTimeout:
        print("error in get top artists")

def get_top_genres(csv_artists_id):
    genres_list = []
    try:    
        service = "https://dit009-spotify-assignment.vercel.app/api/v1" 
        
        artists_data = f"{service}/artists?ids={csv_artists_id}"
        response_artist = requests.get(artists_data, timeout = 15)
        artist_data_json = response_artist.json()
        list_of_dicts = artist_data_json["artists"] 
        
        for artist in list_of_dicts:   
            if "genres" in artist:
                genres = artist["genres"]
                if genres not in genres_list:
                    genres_list.append(genres)  

        return genres_list
    
    except ReadTimeout:
        print("error in get top genres")


"""
Italy (Rome): ("41.9028", "12.4964")
France (Paris): ("48.8566", "2.3522")
Canada (Toronto): ("43.651070", "-79.347015")
United States (New York City): ("40.7128", "-74.0060")
Sweden (Stockholm): ("59.3293", "18.0686")
"""


def main():
    digit_pattern = r"-*\d+"   
    lat = input("Insert latitude: ")
    long = input("Insert longiude: ")
    if re.match(digit_pattern, lat) and re.match(digit_pattern, long):
        average_temperature = get_average_temp(lat, long)
        top_genres = get_top_genres(get_top_artists((get_country_playlist(lat, long))))
        print(f"average temperature in this week is {average_temperature}")
        print(f"the top genres were {top_genres}")

if __name__ == "__main__":
    main()

