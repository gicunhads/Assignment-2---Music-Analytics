import requests
import json


def get_lyrics_top50():

    lyrics = {}

    service = "https://dit009-spotify-assignment.vercel.app/api/v1"
    url = f"{service}/playlists/37i9dQZEVXbMDoHDwVN2tF"
    response = requests.get(url)
    data = response.json()

    for i in range(len(data['tracks']['items'])):

        song_name = data['tracks']['items'][i]['track']['name']
        artist_name = data['tracks']['items'][i]['track']['artists'][0]['name']

        url_lyrics = f'https://api.lyrics.ovh/v1/{artist_name}/{song_name}'
        response = requests.get(url_lyrics)
        lyric_data = response.json()

        lyrics[song_name] = lyric_data

    with open('./resources/songs.json', 'w') as file:
        json.dump(lyrics, file)

    with open('./resources/spotify.json', 'w') as file1:
        json.dump(data, file1)


def main():
    get_lyrics_top50()


if __name__ == '__main__':
    main()
