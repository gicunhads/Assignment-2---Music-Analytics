
import json, re, requests
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="geoapiExercises")

service = "https://dit009-spotify-assignment.vercel.app/api/v1"
genres = f"{service}/recommendations/available-genre-seeds"
response_genres = requests.get(genres)
data_genres = response_genres.json()




#after getting lat and long as inputs:
lat = 57.7089 # GOING TO BE USER INPUTS
long =11.9746
sweden = "37i9dQZEVXbKVvfnL1Us06" # going to make a dict for this later
date_pattern = r"\(20[0-9]{2})-(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])\b" # confirm if it is YYYY-MM-DD
digit_pattern = r"\bd+\b"   


def get_country(lat, long):   
    location = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={long}"  
    response_location = requests.get(location) 
    data_location = response_location.json()
    country = data_location["address"]["country"]
    print(f"Seems you are in {country}!")
    return country


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
def get_top_artists(country):
    service = "https://dit009-spotify-assignment.vercel.app/api/v1"
    top_artists = []
    
    try:
        top_tracks_week = f"{service}/playlists/{country}/tracks" # gonna get the popular tracks in the week in sweden
        response_top_tracks = requests.get(top_tracks_week)
        data_top_tracks = response_top_tracks.json()
        
        for item in data_top_tracks["items"]:
            track = item["track"]
            artists = track["artists"]  
            
            for artist in artists:
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


get_country(lat,long)
get_top_artists(sweden)
get_top_genres(get_top_artists(sweden))
