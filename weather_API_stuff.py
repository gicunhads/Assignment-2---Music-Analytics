
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


#after getting lat and long as inputs in the main:
# testing
 # going to make a dict for this later, going to get the country with the Nominatim API
digit_pattern = r"\bd+\b"   # confirm if it is digit


def get_country_playlist(lat, long):   
    country_playlist = {
    "sweden": "37i9dQZEVXbKVvfnL1Us06",
    "united states": "37i9dQZEVXbLRQDuF5jeBp",
    "brazil": "37i9dQZEVXbKzoK95AbRy9",
    "canada": "37i9dQZEVXbMda2apknTqH",
    "italy": "37i9dQZEVXbIQnj7RRhdSX",
    "france": "37i9dQZEVXbKQ1ogMOyW9N",
    }
    try:    
        location = f"https://nominatim.openstreetmap.org/reverse.php?format=json&lat={lat}&lon={long}&accept-language=en"  
        response_location = requests.get(location, timeout = 5) 
       
        if response_location.status_code != 200:
            print(f"Error: Received {response_location.status_code} from location API.")
            return None
       
        data_location = response_location.json()
        country = data_location["address"]["country"]
        
        print(f"Seems you are in {country}!")
        country = country.lower()
        if country in country_playlist.keys():
            return country_playlist.get(country)
        elif country not in country_playlist.keys():
            print("Error: country not in playlist") #deal with this later so user can use playlist ID
            return None
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
    
    except: 
        print("error in get average temperature")
# relating temperature to genre (AND REGION?)


def get_top_artists(country_playlist):
    service = "https://dit009-spotify-assignment.vercel.app/api/v1"
    top_artists = []
   
    try:
        top_tracks_week = f"{service}/playlists/{country_playlist}/tracks" # gonna get the popular tracks in the week 
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
                if "id" in artist.keys():
                    artist_id = artist["id"]
                    top_artists.append(artist_id)
                    
               
        return top_artists
    
    except ReadTimeout:
        print("error in get top artists")

def get_top_genres(list_artists_id):
    try:    
        service = "https://dit009-spotify-assignment.vercel.app/api/v1"
        top_genres = []
        for artist_id in list_artists_id:
            artist_url = f"{service}/artists/{artist_id}"
            response_artist = requests.get(artist_url, timeout = 15)

            if response_artist == 429:  
                retry_after = int(response_artist.headers.get("Retry-After", 20))
                print(f"Rate limited. Retrying after {retry_after} seconds...")
                time.sleep(retry_after)
                
                
                response_artist = requests.get(artist_url, timeout=5)
                artist_data = response_artist.json()
            
            
            artist_data = response_artist.json()
            
            genres = artist_data.get("genres", timeout = 10)
            
            if artist_data == 429:  
                retry_after = int(artist_data.headers.get("Retry-After", 20))
                print(f"Rate limited. Retrying after {retry_after} seconds...")
                time.sleep(retry_after)
                
                
                response_artist = artist_data.get("genres", timeout = 15)
                artist_data = response_artist.json()

            if genres != []:   
                for item in genres:
                    if item not in top_genres:
                        top_genres.append(item)
        return top_genres
    except ReadTimeout:
        print("error in get top genres")


"""
Italy (Rome): ("41.9028", "12.4964")
France (Paris): ("48.8566", "2.3522")
Canada (Toronto): ("43.651070", "-79.347015")
United States (New York City): ("40.7128", "-74.0060")
Sweden (Stockholm): ("59.3293", "18.0686")
"""


'''
{'genres': ['acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'anime', 'black-metal', 'bluegrass', 'blues', 
'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-house', 'children', 'chill', 'classical', 'club', 'comedy', 
'country', 'dance', 'dancehall', 'death-metal', 'deep-house', 'detroit-techno', 'disco', 'disney', 'drum-and-bass', 'dub', 'dubstep', 
'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove', 
'grunge', 'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop', 'holidays', 'honky-tonk', 'house', 'idm', 
'indian', 'indie', 'indie-pop', 'industrial', 'iranian', 'j-dance', 'j-idol', 'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 
'latino', 'malay', 'mandopop', 'metal', 'metal-misc', 'metalcore', 'minimal-techno', 'movies', 'mpb', 'new-age', 'new-release', 
'opera', 'pagode', 'party', 'philippines-opm', 'piano', 'pop', 'pop-film', 'post-dubstep', 'power-pop', 'progressive-house', 
'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'rainy-day', 'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-roll', 'rockabilly',
 'romance', 'sad', 'salsa', 'samba', 'sertanejo', 'show-tunes', 'singer-songwriter', 'ska', 'sleep', 'songwriter', 'soul', 'soundtracks', 
 'spanish', 'study', 'summer', 'swedish', 'synth-pop', 'tango', 'techno', 'trance', 'trip-hop', 'turkish', 'work-out', 'world-music']}'''


"""canada['3y2cIKLjiOlp1Np37WiUdH', '1HY2Jd0NmPuamShAr6KMms', '0du5cEVh5yTK9QJze8zA0C', '74KM79TiuVKeVCqs8QtB0B', '6qqNVTkY8uBg9cP3Jd7DAH', '1Xyo4u8uXC1ZmMpatF05PJ', '699OTQXzgjhIYAHMy9RyPD', '246dkjvS1zLTtiykXe5h60', '4oUHIQIBe0LHzYfvXNW4QM', '7GlBOeep6PqTfFi59PTUUN', '1iCnM8foFssWlPRLfAbIwo', '74KM79TiuVKeVCqs8QtB0B', '22wbnEMDvgVIAGdFeek6ET', '74KM79TiuVKeVCqs8QtB0B', '4tuJ0bMpJh08umKkEXKUI5', '40ZNYROS4zLfyyBSs2PGe2', '70kkdajctXSbqSMJbQO424', '2RQXRUsr4IW1f3mKyKsy4B', '33qOK5uJ8AR2xuQQAhHump', '74KM79TiuVKeVCqs8QtB0B', '7Ez6lTtSMjMf2YSYpukP1I', '40ZNYROS4zLfyyBSs2PGe2', '40ZNYROS4zLfyyBSs2PGe2', '2FXC3k01G6Gw61bmprjgqS', '718COspgdWOnwOFpJHRZHS', '7GlBOeep6PqTfFi59PTUUN', '6qqNVTkY8uBg9cP3Jd7DAH', '1oSPZhvZMIrWW5I41kPkkY', '0Y5tJX1MQlPlqiwlOH1tJY', '699OTQXzgjhIYAHMy9RyPD', '4oUHIQIBe0LHzYfvXNW4QM', '3bO19AOone0ubCsfDXDtYt', '2YZyLoL8N0Wb9xBt1NhZWg', '4gvjmrtzydbMpyJaXUtwvP', '22wbnEMDvgVIAGdFeek6ET', '4j96cMcT8GRi11qbvo1cLQ', '1WaFQSHVGZQJTbf0BdxdNo', '10exVja0key0uqUkk6LJRT', '77SW9BnxLY8rJ0RciFqkHh', '25uiPmTg16RbhZWAqwLBy5', '6qqNVTkY8uBg9cP3Jd7DAH', '4oUHIQIBe0LHzYfvXNW4QM', '4GGfAshSkqoxpZdoaHm7ky', '2tIP7SsRs7vjIcLrU85W8J', '5HK6QtizXJzCmoYTkvFRik', '64KEffDW9EtZ1y2vBYgq8T', '3oSJ7TBVCWMDMiYjXNiCKE', '40ZNYROS4zLfyyBSs2PGe2', '1nzgtKYFckznkcVMR3Gg4z', '6Xgp2XMz1fhVYe7i6yNAax', '74KM79TiuVKeVCqs8QtB0B', '4Gso3d4CscCijv0lmajZWs', '25uiPmTg16RbhZWAqwLBy5', '66CXWjxzNUsdJxJ2JdwvnR', '4oUHIQIBe0LHzYfvXNW4QM', '7GlBOeep6PqTfFi59PTUUN', '45dkTj5sMRSjrmBSBeiHym', '0rvjqX7ttXeg3mTy8Xscbt', '2hlmm7s2ICUX0LVIhVFlZQ', ...]; ['modern country pop', 'pop rap', 'art pop', 'dance pop', 'pop', 'indie pop', 'bedroom pop', 'classic oklahoma country', 'atl hip hop', 'plugg', 'pluggnb', 'rage rap', 'rap', 'contemporary country', 'singer-songwriter pop', 'candy pop', 'metropopolis', 'uk pop', 'melodic rap', 'trap', 'country']"""
"""us:['1HY2Jd0NmPuamShAr6KMms', '0du5cEVh5yTK9QJze8zA0C', '6qqNVTkY8uBg9cP3Jd7DAH', '74KM79TiuVKeVCqs8QtB0B', '7GlBOeep6PqTfFi59PTUUN', '1Xyo4u8uXC1ZmMpatF05PJ', '699OTQXzgjhIYAHMy9RyPD', '1iCnM8foFssWlPRLfAbIwo', '1oSPZhvZMIrWW5I41kPkkY', '74KM79TiuVKeVCqs8QtB0B', '246dkjvS1zLTtiykXe5h60', '4oUHIQIBe0LHzYfvXNW4QM', '4tuJ0bMpJh08umKkEXKUI5', '3y2cIKLjiOlp1Np37WiUdH', '74KM79TiuVKeVCqs8QtB0B', '74KM79TiuVKeVCqs8QtB0B', '7GlBOeep6PqTfFi59PTUUN', '6qqNVTkY8uBg9cP3Jd7DAH', '4AK6F7OLvEQ5QYCBNiQWHq', '7GlBOeep6PqTfFi59PTUUN', '22wbnEMDvgVIAGdFeek6ET', '40ZNYROS4zLfyyBSs2PGe2', '70kkdajctXSbqSMJbQO424', '2YZyLoL8N0Wb9xBt1NhZWg', '33qOK5uJ8AR2xuQQAhHump', '2RQXRUsr4IW1f3mKyKsy4B', '77SW9BnxLY8rJ0RciFqkHh', '4AK6F7OLvEQ5QYCBNiQWHq', '2tIP7SsRs7vjIcLrU85W8J', '4V8LLVI7PbaPR0K2TGSxFF', '1U1el3k54VvEUzo3ybLPlM', '1WaFQSHVGZQJTbf0BdxdNo', '40ZNYROS4zLfyyBSs2PGe2', '2sSGPbdZJkaSE2AbcGOACx', '40ZNYROS4zLfyyBSs2PGe2', '2hlmm7s2ICUX0LVIhVFlZQ', '74KM79TiuVKeVCqs8QtB0B', '2FXC3k01G6Gw61bmprjgqS', '22wbnEMDvgVIAGdFeek6ET', '6qxpnaukVayrQn6ViNvu9I', '4oUHIQIBe0LHzYfvXNW4QM', '4GGfAshSkqoxpZdoaHm7ky', '12GqGscKJx3aE4t07u7eVZ', '6pV5zH2LzjOUHaAvENdMMa', '718COspgdWOnwOFpJHRZHS', '74KM79TiuVKeVCqs8QtB0B', '4oUHIQIBe0LHzYfvXNW4QM', '0Y5tJX1MQlPlqiwlOH1tJY', '699OTQXzgjhIYAHMy9RyPD', '7GlBOeep6PqTfFi59PTUUN', '0ErzCpIMyLcjPiwT4elrtZ', '0yknvLWQZxwsMjhUhwWZQ8', '0hF6lbAjRsq4svrQUr5sgU', '4gvjmrtzydbMpyJaXUtwvP', '25uiPmTg16RbhZWAqwLBy5', '6qqNVTkY8uBg9cP3Jd7DAH', '2h93pZq0e7k5yf4dywlkpM', '40ZNYROS4zLfyyBSs2PGe2', '7Ez6lTtSMjMf2YSYpukP1I', ...]"""
def main():
    digit_pattern = r"-*\d+"   # confirm if it is digit
    lat = input("Insert latitude: ")
    long = input("Insert longiude: ")
    if re.match(digit_pattern, lat) and re.match(digit_pattern, long):
        average_temperature = get_average_temp(lat, long)
        top_genres = get_top_genres(get_top_artists((get_country_playlist(lat, long))))
        print(f"average temperature in this week is {average_temperature}")
        print(f"the top genres were {top_genres}")

if __name__ == "__main__":
    main()

