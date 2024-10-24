import requests
import json
import re
from requests import ReadTimeout
import time


def get_lyrics_top50():

    top50_lists = {
        'denmark': '37i9dQZEVXbL3J0k32lWnN',
        'global': '37i9dQZEVXbMDoHDwVN2tF',
        'sweden': '37i9dQZEVXbLoATJ81JYXz',
    }

    service = "https://dit009-spotify-assignment.vercel.app/api/v1"

    for key in top50_lists:
        lyrics = {}
        url = f"{service}/playlists/{top50_lists[key]}"
        response = requests.get(url)
        data = response.json()

        for i in range(len(data['tracks']['items'])):
            song_name = data['tracks']['items'][i]['track']['name']
            artist_name = data['tracks']['items'][i]['track']['artists'][0]['name']
            url_lyrics = f'https://api.lyrics.ovh/v1/{artist_name}/{song_name}'
            response = requests.get(url_lyrics)
            lyric_data = response.json()
            lyrics[song_name] = lyric_data

        with open(f'./resources/{key}_songs.json', 'w') as file:
            json.dump(lyrics, file)

        with open(f'./resources/{key}_spotify.json', 'w') as file1:
            json.dump(data, file1)


def get_country_playlist(country):

    playlist_id_pattern = r"[A-Za-z0-9]{22}"

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

    word_pattern = r"[a-z]+"

    with open(f"./resources/all_coutries_genre.json", "r") as file:
        country_genre = json.load(file)

    try:

        print(f"Fetching data from {country}!")
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
    if csv_artists_id is not None:
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

            if genres_list is not []:
                return genres_list

            else:
                print(f"No genres found.")
                print(f"top artists: {names_list}")
        except ReadTimeout:
            print("Error in get top genres: Timeout")

    else:
        return None


def artist_id_search(name):

    service = "https://dit009-spotify-assignment.vercel.app/api/v1"

    try:

        try:
            with open('resources/artist_information.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        if name in data:
            id = data[name]["id"]
            artist_name = data[name]["artist_name"]
            genre = data[name]["genre"]
            popularity = data[name]["popularity"]
        else:
            artist_search = f"{service}/search?q={name}&type=artist&limit=1"
            result = requests.get(artist_search)
            result_data = result.json()

            for item in result_data["artists"]["items"]:
                id = item["id"]
                artist_name = item["name"]
                genre = item["genres"]
                popularity = item["popularity"]

            data[name] = {"id": id, "artist_name": artist_name, "genre": genre, "popularity": popularity}

            with open('resources/artist_information.json', 'w') as file:
                json.dump(data, file, indent=4)

        values = [id, artist_name, genre, popularity]
        right_name = input(f"Is {artist_name} the artist you are looking for? y/n ").lower()

        if right_name == "y":
            return values

        elif right_name == "n":

            id = input("Please input the right artist id: ")

            id_search = f"{service}/artists/{id}"
            get_id = requests.get(id_search)
            id_file = get_id.json()

            values.clear()
            for item in id_file:
                artist_name = item["name"]
                genre = item["genres"]
                popularity = item["popularity"]

            values = [id, artist_name, genre, popularity]
            return True
        else:
            print("Error: invalid input")
            return None

    except KeyError:
        time.sleep(10)
        artist_id_search(name)


def artist_albums(id):

    service = "https://dit009-spotify-assignment.vercel.app/api/v1"

    try:
        try:
            with open('resources/total_albums.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        if id in data:
            total_albums = data[id]

        else:
            album_search = f"{service}/artists/{id}/albums?limit=50&include_groups=album"
            albums = requests.get(album_search)
            album_file = albums.json()
            total_albums = album_file["total"]

            data[id] = total_albums

            with open('resources/total_albums.json', 'w') as file:
                json.dump(data, file, indent=4)
        return True

    except KeyError:
        time.sleep(15)
        artist_albums(id)


def get_country_genre_temp(lat, long):

    digit_pattern = r"-*\d+"
    country_genre = {}
    country_temp = {}

    if re.match(digit_pattern, lat) and re.match(digit_pattern, long):
        average_temperature = get_average_temp(lat, long)

        country = get_country(lat,long)
        country = country.lower()
        top_genres = get_country_genre(country) # returns [[]]
        country = country.title()
        if top_genres is not None:
            if top_genres is not []:
                country_genre[country] = []

                country_genre[country].extend(top_genres)
                country_temp[country] = average_temperature

                with open(f'./resources/country_genre.json', 'w') as file:
                    json.dump(country_genre, file)

                with open(f'./resources/country_temp.json', 'w') as file:
                    json.dump(country_temp, file)
                return True



def artist_id_search(name):
    service = "https://dit009-spotify-assignment.vercel.app/api/v1"
    try:
        
        try:
            with open('assignmenttwo.json', 'r') as file:
                data = json.load(file)  
        except FileNotFoundError:
            data = {}  

       
        if name in data:
            id = data[name]["id"]
            artist_name = data[name]["artist_name"]
            genre = data[name]["genre"]
            popularity = data[name]["popularity"]
        else:
           
            artist_search = f"{service}/search?q={name}&type=artist&limit=1"
            result = requests.get(artist_search)
            result_data = result.json()

            for item in result_data["artists"]["items"]:
                id = item["id"]
                artist_name = item["name"]
                genre = item["genres"]
                popularity = item["popularity"]

            
            data[name] = {"id": id, "artist_name": artist_name, "genre": genre, "popularity": popularity}

            
            with open('assignmenttwo.json', 'w') as file:
                json.dump(data, file, indent=4)  

        
        values = [id, artist_name, genre, popularity]
        right_name = input(f"Is {artist_name} the artist you are looking for? y/n ").lower()

        if right_name == "y":
            return values
        elif right_name == "n":

            id = input("Please input the right artist id: ")

            id_search = f"{service}/artists/{id}"
            get_id = requests.get(id_search)
            id_file = get_id.json()

            values.clear()
            for item in id_file:
                artist_name = item["name"]
                genre = item["genres"]
                popularity = item["popularity"]

            values = [id, artist_name, genre, popularity]
            return values
        else:
            print("Error: invalid input")
            return None

    except KeyError:
        time.sleep(10)
        artist_id_search(name)




def artist_albums(id):
    service = "https://dit009-spotify-assignment.vercel.app/api/v1"
        try:
            try:
                with open('total_albums.json', 'r') as file:
                    data = json.load(file)  
            except FileNotFoundError:
                data = {}
            if id in data: 
                total_albums = data[id]
                
            else:
                album_search = f"{service}/artists/{id}/albums?limit=50&include_groups=album"
                albums = requests.get(album_search)
                album_file = albums.json()
                total_albums = album_file["total"]

                data[id] = total_albums

                with open('total_albums.json', 'w') as file:
                     json.dump(data, file, indent=4)


                

            return total_albums

                    
        except KeyError:
            time.sleep(15)
            artist_albums(id)

def main():
    menu = '''
    Here you can update data from the api's necessary for the analysis.
    chose which data you want to fetch/update:
    1. Data for whether sad or happy songs are more popular.
    2. Exit
    '''
    print(menu)
    choice = input('What do you choose? (choose between 1-4): ')

    match choice:
        case '1':
            get_lyrics_top50()
        case '2':
            print('thanks for using the program')
        case _:
            print('please choose a valid option')
            main()


if __name__ == '__main__':
    main()
