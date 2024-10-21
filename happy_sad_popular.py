import requests
import json
import re

#Used chatgpt to get the words for happy and sad songs
happy_song_words = [
    "Love", "Smile", "Dance", "Sunshine", "Joy", "Happy", "Sing", "Dream", "Celebrate",
    "Heart", "Light", "Free", "Shine", "Fly", "Life", "Beautiful", "Together", "Laughter",
    "Sky", "Sweet", "Summer", "Fun", "Baby", "Forever", "Bright", "Magic", "Perfect",
    "Party", "Golden", "Peace", "Rainbow", "Rise", "Run", "Cheer", "Breeze", "Glow",
    "Smile", "Bliss", "Hug", "Feel", "Kiss", "Sun", "Rhythm", "Wonderful", "Dancefloor",
    "Shining", "Fire", "Groove", "Wind", "Paradise"
]
sad_song_words = [
    "Tears", "Broken", "Lonely", "Heart", "Cry", "Pain", "Goodbye", "Lost", "Alone",
    "Sad", "Gone", "Miss", "Hurt", "Dark", "Empty", "Fading", "Memories", "Cold",
    "Silence", "Sorrow", "Regret", "Fallen", "Blue", "Distance", "Shattered", "Time",
    "Rain", "Longing", "Night", "Fear", "Wounds", "Grief", "Shadows", "Apart",
    "Despair", "Farewell", "Anguish", "Bleeding", "Forgotten", "Wasted", "Hope",
    "Goodnight", "Solitude", "Heartache", "Alone", "Brokenness", "Whisper", "End",
    "Betray", "Fading"
]

lyrics = {

}



def apicall():
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

    with open('songs.json', 'w') as file:
        json.dump(lyrics, file)

    print(lyrics['Die With A Smile']['lyrics'])


def main():
    with open('songs.json', 'r') as file:
        lyric = json.load(file)
    for key in lyric:
        if 'error' not in lyric[key]:
            print(key, lyric[key]['lyrics'])
        else:
            continue



if __name__ == "__main__":
    main()

