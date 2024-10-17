import json, re, requests
from geopy.geocoders import Nominatim
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
date_pattern = r"\(20[0-9]{2})-(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])\b" # confirm if it is YYYY-MM-DD
digit_pattern = r"\bd+\b"   # confirm if it is digit

country_playlist = {
"sverige": "37i9dQZEVXbKVvfnL1Us06",
"usa": "37i9dQZEVXbLRQDuF5jeBp",
"brasil": "37i9dQZEVXbKzoK95AbRy9",
"canada": "37i9dQZEVXbMda2apknTqH",
"italia": "37i9dQZEVXbIQnj7RRhdSX",
"france": "37i9dQZEVXbKQ1ogMOyW9N",
}




def get_country_playlist(lat, long):   
    location = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={long}"  
    response_location = requests.get(location) 
    data_location = response_location.json()
    country = data_location["address"]["country"]
    print(f"Seems you are in {country}!")
    country = country.lower()
    if country in country_playlist.keys():
        return country_playlist.get(country)
        


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
        ...
# relating temperature to genre (AND REGION?)


    #testing for sweden
def get_top_artists(country_playlist):
    service = "https://dit009-spotify-assignment.vercel.app/api/v1"
    top_artists = []
    
    try:
        top_tracks_week = f"{service}/playlists/{country_playlist}/tracks" # gonna get the popular tracks in the week 
        response_top_tracks = requests.get(top_tracks_week)
        data_top_tracks = response_top_tracks.json()
        
        for item in data_top_tracks["items"]:
            track = item["track"]
            artists = track["artists"]  
            
            for artist in artists:
                if "id" in artist.keys():
                    artist_id = artist["id"]
                    top_artists.append(artist_id)
                    
                
        return top_artists
    
    except:
        print("boo")

def get_top_genres(list_artists_id):
    service = "https://dit009-spotify-assignment.vercel.app/api/v1"
    top_genres = []
    for artist_id in list_artists_id:
        artist_url = f"{service}/artists/{artist_id}"
        response_artist = requests.get(artist_url)
        artist_data = response_artist.json()
        
        genres = artist_data.get("genres", [])
        if genres != []:   
            top_genres.append(genres)
    print(top_genres)
    return top_genres



get_country_playlist("41.8933", "12.4828")
get_top_artists(get_country_playlist("48.8575", "2.3514"))




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

