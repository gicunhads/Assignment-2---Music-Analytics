
import json, re, requests, time
from geopy.geocoders import Nominatim
from requests import ReadTimeout
geolocator = Nominatim(user_agent="geoapiExercises")



playlist_id_pattern = r"[A-Za-z0-9]{22}"
word_pattern = r"[a-z]+"

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
    headers =  {
    'User-Agent': 'gigi',
    'From': 'gicunhads@gmail.com'  
}
    try:    
        location = f"https://nominatim.openstreetmap.org/reverse.php?format=json&lat={lat}&lon={long}&accept-language=en"  
        response_location = requests.get(location, headers=headers, timeout = 5) 
        data_location = response_location.json()
        country = data_location["address"]["country"]
        
        print(f"Seems you are in {country}!")
        country = country.lower()
        
        if country in country_playlist.keys():
            return country_playlist.get(country)
        else:
            return append_country_playlist(country)
    
    except ReadTimeout:
        print("Error: Timeout. in get country playlist")
    except Exception:
        print(f"Error: Location could not be found.")
        answer = input("Would you like to inform your country and playlist ID? [y] for yes: ") 
        if answer == "y":
            country = input("Insert your country: ").lower()
            if re.match(word_pattern, country):
                if country in country_playlist.keys():
                    return country_playlist.get(country)
                elif country not in country_playlist.keys():
                    return append_country_playlist(country)
        
    

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
    if country_playlist != None:
        try:
            top_tracks_week = f"{service}/playlists/{country_playlist}/tracks" # gonna get the popular tracks in the week 
            response_top_tracks = requests.get(top_tracks_week, timeout = 10)
            data_top_tracks = response_top_tracks.json()

            for item in data_top_tracks["items"]:
                track = item["track"]
                artists = track["artists"]  
                
                for artist in artists:
                    while i <= 30: # getting several artists have a limit for the API 
                        if "id" in artist.keys():
                            artist_id = artist["id"]
                            csv_artists_id += artist_id + ","
                            i += 1
                                
                    
                return csv_artists_id[:-1] # removing the last coma
        
        
        except ReadTimeout:
            retry_after = int(response_top_tracks.headers.get("Retry-After", 20))
            print(f"Rate limited. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
            
            
            response_top_tracks = requests.get(top_tracks_week, timeout=5)
            data_top_tracks = response_top_tracks.json()
        except Exception as e:
            print(f"Error: {e}")
            return None 
    else:
        return None
        

def get_top_genres(csv_artists_id):
    genres_list = []
    if csv_artists_id != None:   
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
    else:
        return None




def main():
    digit_pattern = r"-*\d+"   # confirm if it is digit
    lat = input("Insert latitude: ")
    long = input("Insert longitude: ")
    
    if re.match(digit_pattern, lat) and re.match(digit_pattern, long):
        average_temperature = get_average_temp(lat, long)
        top_genres = get_top_genres(get_top_artists((get_country_playlist(lat, long))))
        
        if top_genres != None: 
            print(f"average temperature in this week is {average_temperature}")
            print(f"the top genres were {top_genres}")
    
if __name__ == "__main__":
    main()
