
import json, re, requests

service = "https://dit009-spotify-assignment.vercel.app/api/v1"
genres = f"{service}/recommendations/available-genre-seeds"
response_genres = requests.get(genres)
data_genres = response_genres.json()

#after getting lat and long as inputs:
lat =57.7089 # GOING TO BE USER INPUTS, my idea is to create a dict with some regions and the user inputs the region and then we get the lat? maybe? or just define it as sweden?
long =11.9746
date_pattern = r"\(20[0-9]{2})-(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])\b" # confirm if it is YYYY-MM-DD

# working:
def get_average_temp():
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
# relating temperature to genre later on, seeing like if temp < x or y (AND REGION?)


    #not working ;testing for sweden
def get_top_artists():
    service = "https://dit009-spotify-assignment.vercel.app/api/v1"
    top_artists = []
    try:
        top_tracks_week = f"{service}/playlist/37i9dQZEVXbLoATJ81JYXz?si=_O8CFC5mQ3mEEoUmGRUk0Q/tracks" # gonna get the popular tracks in the week in sweden
        response_top_tracks = requests.get(top_tracks_week)
        data_top_tracks = response_top_tracks.json()
        for artist_id in data_top_tracks["items"]["artists"]["id"]:
            top_artists.append(artist_id)
        print(top_artists)
    except:
        print("boo")

get_top_artists()
