import requests
import json
import re
import matplotlib.pyplot as plt

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

lyrics = {}
ratios = {}



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

    with open('spotify.json', 'w') as file1:
        json.dump(data, file1)


def main():

    with open('songs.json', 'r') as file:
        lyric = json.load(file)
    for key in lyric:
        if 'error' not in lyric[key]:

            amount_happy_word = 0
            amount_sad_word = 0

            for word in happy_song_words:
                text = lyric[key]['lyrics']
                word = word.lower()
                cases = re.findall( word , text.lower())
                amount_happy_word += len(cases)

            for word in sad_song_words:
                text = lyric[key]['lyrics']
                word = word.lower()
                cases = re.findall( word , text.lower())
                amount_sad_word += len(cases)

            if amount_sad_word != 0:
                ratio = amount_happy_word/amount_sad_word
            else:
                ratio = amount_happy_word/1

            ratios[key] = ratio

        else:
            continue

    song_names = []
    song_ratio = []
    for key in ratios:
        song_names.append(key)
        song_ratio.append(ratios[key])

    fig, ax = plt.subplots()
    ax.bar(song_names, song_ratio)
    plt.show()
    avg = sum(song_ratio)/len(song_ratio)
    print(avg)

    # finding teh median of the ratios to determine when a song is happy or sad.
    # the median in the first testcase of spotify top 50 was 1.25
    # so this will be the value used to determine when it is sad or happy

    song_ratio.sort()
    mid = len(song_ratio) // 2
    res = (song_ratio[mid] + song_ratio[~mid]) / 2
    print(res)
    popularity_of_song = []

    with open('spotify.json', 'r') as file:
        spotify = json.load(file)

    for i in range(len(song_names)):
        popularity = spotify['tracks']['items'][i]['track']['popularity']
        popularity_of_song.append(popularity)
        #print(f'{song_names[i]} is this popular: {popularity}')

    fig = plt.figure()

    sad_average = []
    happy_average = []

    for i in range(len(popularity_of_song)):
        if song_ratio[i] < 1.25:
            plt.plot(song_ratio[i], popularity_of_song[i], 'bo')
            sad_average.append(popularity_of_song[i])
        else:
            plt.plot(song_ratio[i], popularity_of_song[i], 'ro')
            happy_average.append(popularity_of_song[i])

    avg_happy = sum(happy_average)/len(happy_average)
    avg_sad = sum(sad_average)/len(sad_average)

    print(f'the average of happy songs: {avg_happy}, and the average of the sad songs: {avg_sad}')



    plt.show()





if __name__ == "__main__":
    main()

