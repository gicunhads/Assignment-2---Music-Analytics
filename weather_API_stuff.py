import json, re, requests, time
from geopy.geocoders import Nominatim
from requests import ReadTimeout
geolocator = Nominatim(user_agent="geoapiExercises")

with open(f"./resources/country_genre.json", "r") as file:
    country_genre = json.load(file)

with open(f'./resources/country_temp.json', 'r') as file:
    country_temp = json.load(file)


playlist_id_pattern = r"[A-Za-z0-9]{22}"
word_pattern = r"[a-z]+"


def get_country_playlist(country):
    answer = input (f"Seems that {country} is not in our system. Would you like to add it? [y] for yes: ")
    if answer == "y":
        playlist_id = input(f"Insert playlist ID for {country}: ")

        if re.match(playlist_id_pattern, playlist_id):
            return playlist_id

        else:
            print("Invalid arguments.")
            return get_country_playlist(country)

    else:
        print("ending program...")
        return None

def get_country(lat,long):
    headers =  {
    'User-Agent': 'gigi',
    'From': 'gicunhads@gmail.com' }
    try:    
        location = f"https://nominatim.openstreetmap.org/reverse.php?format=json&lat={lat}&lon={long}&accept-language=en"  
        response_location = requests.get(location, headers=headers, timeout = 5) 
        data_location = response_location.json()
        country = data_location["address"]["country"]
        return country
    except:
        print(f"Error: Location could not be found.")
        
def get_country_genre(country):   
    global country_genre
    try:    
        
        print(f"Seems you are in {country}!")
        country = country.lower()
        
        if country in country_genre.keys():
            return country_genre[country]
        else:
            return get_top_genres(get_top_artists(get_country_playlist(country)))
    
    except ReadTimeout:
        print("Error: Timeout. in get country playlist")
    
    except Exception:
        print(f"Error: Location could not be found.")
        answer = input("Would you like to inform your country and playlist ID? [y] for yes: ") 
        if answer == "y":
            country = input("Insert your country: ").lower()
            if re.match(word_pattern, country):
                if country in country_genre.keys():
                    return country_genre[country]
                elif country not in country_genre.keys():
                    return get_country_playlist(country)
        
    

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
    names_list = []
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
                    if genres not in genres_list and genres != []:
                        genres_list.append(genres)  
                if "name" in artist:
                    name = artist["name"]
                    if name not in names_list and name != "":
                        names_list.append(name) 

            if genres_list != []:
                return genres_list
            
            else:
                print(f"No genres found.")
                print(f"top artists: {names_list}")
        except ReadTimeout:
            print("Error in get top genres: Timeout")
        
    else:
        return None




def main():
    digit_pattern = r"-*\d+"   
    lat = input("Insert latitude: ")
    long = input("Insert longitude: ") 
    
    if re.match(digit_pattern, lat) and re.match(digit_pattern, long):
        average_temperature = get_average_temp(lat, long)
        
        country = get_country(lat,long)
        country = country.lower()
        top_genres = get_country_genre(country)
        if top_genres != None: 
            print(f"average temperature in this week is {average_temperature}°C")
            if top_genres != []:
                country_genre[country] = top_genres
                country_temp[country] = average_temperature
                with open(f'./resources/country_genre.json', 'w') as file:
                    json.dump(country_genre, file)
                with open(f'./resources/country_temp.json', 'w') as file:
                    json.dump(country_temp, file)
                print(f"the top genres were {top_genres}")
            
    
if __name__ == "__main__":
    main()
            



