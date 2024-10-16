import json, re, requests



service = "https://dit009-spotify-assignment.vercel.app/api/v1"
genres = f"{service}/recommendations/available-genre-seeds"
response_genres = requests.get(genres)
data_genres = response_genres.json()

#after getting lat and long as inputs:
lat =57.7089 # GOING TO BE USER INPUTS
long =11.9746
date_pattern = r"\(20[0-9]{2})-(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])\b" # confirm if it is YYYY-MM-DD


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
# relating temperature to genre
'''
def get_music_data(start_date, end_date):
    # This function should fetch data from Spotify API to get popular tracks and their genres
    # For demonstration, let's simulate some data
    # You would replace this with an actual API call to Spotify
    
    # Sample data simulating genres and counts
    genre_data = {
        'genre': ['pop', 'rock', 'chill', 'indie', 'classical'],
        'play_count': [100, 80, 50, 40, 20]  # Hypothetical counts
    }'''


    #not working
def get_top_artists():
    service = "https://dit009-spotify-assignment.vercel.app/api/v1"
    top_artists = []
    try:
        top_tracks_week = f"{service}/playlists/https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=RbLHy5DwTBenI_SSakwuvQ/tracks" # gonna get the popular tracks in the week
        response_top_tracks = requests.get(top_tracks_week)
        data_top_tracks = response_top_tracks.json()
        for artist in data_top_tracks["items"]["artists"]:
            top_artists.append(artist)
        print(top_artists)
    except:
        ...

get_top_artists()
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

