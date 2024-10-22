import json
import re
import matplotlib.pyplot as plt


def determine_sad_or_happy():

    ratios = {}

    with open('./resources/songs.json', 'r') as file:
        lyric = json.load(file)

    # Used chatgpt to get the 50 most used words in sad songs and happy songs.
    # Then I created a json file containing the words.
    with open('./resources/happy_and_sad_words.json', 'r') as file1:
        words = json.load(file1)

    for key in lyric:
        if 'error' not in lyric[key]:

            amount_happy_word = 0
            amount_sad_word = 0

            for word in words['happy_song_words']:
                text = lyric[key]['lyrics']
                word = word.lower()
                cases = re.findall( word , text.lower())
                amount_happy_word += len(cases)

            for word in words['sad_song_words']:
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
            ratios[key] = None

    return ratios


def get_average(list_of_nums):
    avg = sum(list_of_nums)/len(list_of_nums)
    return avg


def plot_happy_or_sad():
    pass


def happy_or_sad_popular():
    ratios = determine_sad_or_happy()

    song_names = []
    song_ratio = []
    for key in ratios:
        song_names.append(key)
        song_ratio.append(ratios[key])

    with open('./resources/spotify.json', 'r') as file:
        spotify = json.load(file)

    popularity_of_song = []

    for i in range(len(song_names)):
        popularity = spotify['tracks']['items'][i]['track']['popularity']
        popularity_of_song.append(popularity)

    sad_popularity = []
    happy_popularity = []
    songs_missing_lyrics = []

    for i in range(len(popularity_of_song)):
        try:
            if song_ratio[i] < 1:
                sad_popularity.append(popularity_of_song[i])
            else:
                happy_popularity.append(popularity_of_song[i])
        except TypeError:
            songs_missing_lyrics.append(song_names[i])

    avg_happy = get_average(happy_popularity)
    avg_sad = get_average(sad_popularity)

    num_of_happy = len(happy_popularity)
    num_of_sad = len(sad_popularity)

    print(f'The average popularity of happy songs: {avg_happy}, and the average of the sad songs: {avg_sad}')

    if avg_happy > avg_sad:
        print('Therefore it can be concluded that currently happy songs are more popular than sad songs')
    elif avg_sad > avg_happy:
        print('Therefore it can be concluded that currently sad songs are more popular than happy songs')
    else:
        print('People like sad and happy songs equally')

    if avg_happy > avg_sad and num_of_happy > num_of_sad:
        print('And there are also more happy songs than sad songs in the top 50')
    elif avg_happy > avg_sad and num_of_happy < num_of_sad:
        print('Even though there are more sad songs than happy songs in the top 50')
    elif avg_happy < avg_sad and num_of_happy > num_of_sad:
        print('Even though there are more happy songs than sad songs in the top 50')
    elif avg_happy < avg_sad and num_of_happy < num_of_sad:
        print('And there are also more sad songs than happy songs in the top 50')
    else:
        print('And there are equally many sad and happy songs in the top 50')

    print(f'There were {num_of_happy} happy songs and {num_of_sad} sad songs in the world top 50 \n')

    print(f'Was unable to find lyrics for the following {len(songs_missing_lyrics)} songs: {songs_missing_lyrics}. \nAnd therefore they have been excluded from the data')


def main():
    happy_or_sad_popular()


if __name__ == "__main__":
    main()
