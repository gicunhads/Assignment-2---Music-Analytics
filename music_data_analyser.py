import json
import re
import matplotlib.pyplot as plt
from spotify_api_miner import get_country_genre_temp
from spotify_api_miner import artist_albums, artist_id_search
import numpy as np


def determine_sad_or_happy(choice):

    ratios = {}

    with open(f'./resources/{choice}_songs.json', 'r') as file:
        lyric = json.load(file)

    # Used chatgpt to get the 50 most used words in sad songs and happy songs.
    # Then I created a json file containing the words.
    with open('./resources/happy_and_sad_words.json', 'r') as file1:
        words = json.load(file1)

    for key in lyric:
        if 'error' not in lyric[key]:

            amount_happy_word = 0
            amount_sad_word = 0

            for word in words['happy']:
                text = lyric[key]['lyrics']
                word = word.lower()
                cases = re.findall(r'\b' + word + r'\b', text.lower())
                amount_happy_word += len(cases)

            for word in words['sad']:
                text = lyric[key]['lyrics']
                word = word.lower()
                cases = re.findall(r'\b' + word + r'\b', text.lower())
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


def plot_happy_or_sad(happy, sad, choice):
    data = {
        'happy': happy,
        'sad': sad
    }
    names = list(data.keys())
    values = list(data.values())

    plt.bar(names, values)
    plt.ylabel('Average popularity')
    plt.title('Song popularity based on happy or sad lyrics')
    plt.savefig(f'./resources/plot_happy_or_sad_in_{choice}.png')
    plt.show()


def happy_or_sad_popular():

    print('Choose which country you want to see the happy/sad correlation with popularity in, you can chose between Denmark, Sweden or the global top50: ')
    choice = input('(Write: Denmark, Sweden or global): ')
    choice.lower()

    ratios = determine_sad_or_happy(choice)

    song_names = []
    song_ratio = []
    for key in ratios:
        song_names.append(key)
        song_ratio.append(ratios[key])

    with open(f'./resources/{choice}_spotify.json', 'r') as file:
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

    print('\n')
    print(f'The average popularity of happy songs: {avg_happy:.2f}, and the average of the sad songs: {avg_sad:.2f}')

    if avg_happy > avg_sad:
        print(f'Therefore it can be concluded that currently happy songs are more popular than sad songs in {choice.capitalize()}')
    elif avg_sad > avg_happy:
        print(f'Therefore it can be concluded that currently sad songs are more popular than happy songs in {choice.capitalize()}')
    else:
        print(f'People like sad and happy songs equally in {choice.capitalize()}')

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

    print(f'There were {num_of_happy} happy songs and {num_of_sad} sad songs in {choice.capitalize()}s top 50 \n')

    print(f'Was unable to find lyrics for the following {len(songs_missing_lyrics)} songs: {songs_missing_lyrics}. \nAnd therefore they have been excluded from the data')

    plot_happy_or_sad(avg_happy, avg_sad, choice)


def compare_genre_temperature():
    lat = input("Insert latitude: ")
    long = input("Insert longitude: ")

    valid = get_country_genre_temp(lat, long)
    if valid is not None:
        with open('./resources/country_genre.json', 'r') as file:
            country_genre = json.load(file)

        with open(f'./resources/all_country_temp.json', 'r') as file:
            country_temp = json.load(file)

        country = list(country_genre.keys())[0]

        string_of_genres = ''

        try:
            for value in country_genre[country]:
                if value == country_genre[country][-2]:
                    string_of_genres += value + 'and '
                elif value == country_genre[country][-1]:
                    string_of_genres += value
                else:
                    string_of_genres += value + ', '
        except IndexError:
            string_of_genres += country_genre[country][0]

        print(f"the top genres were {string_of_genres}")
        print(f"average temperature in this week is {country_temp[country.lower()]}°C")
        plot_genre_temperature()


def plot_genre_temperature():

    with open(f"./resources/all_coutries_genre.json", "r") as file:
        country_genre = json.load(file)

    with open(f'./resources/all_country_temp.json', 'r') as file:
        country_temp = json.load(file)

    countries = []
    temperatures = []
    number_genres = []

    for country, genre in country_genre.items():
        countries.append(country)
        number_genres.append(len(genre))

    for country, temp in country_temp.items():
        temperatures.append(float(temp))

    combined = sorted(zip(temperatures, number_genres, countries))
    temperatures, number_genres, countries = zip(*combined)

    plt.figure(figsize=(10, 6))
    plt.scatter(temperatures, number_genres, color="m")

    for temp, num_g, country in combined:
        plt.text(temp, num_g + 0.1, country, fontsize=9)

    plt.title("Average Temp. vs n. of genres per country")
    plt.xlabel("Average Temperature (°C)")
    plt.ylabel("Number of music genres")
    plt.grid(True)
    plt.savefig('./resources/averagetemp_vs_number_genre.png')
    plt.show()


def option3():

    artist_name = input("Input the first artist name: ").lower()
    artist_search = artist_id_search(artist_name)
    albums1 = artist_albums(artist_search[0])

    if albums1 is None:
        print('An error happened')
        return None

    artist_name2 = input("Input the second artist name: ").lower()
    artist_search2 = artist_id_search(artist_name2)
    albums2 = artist_albums(artist_search2[0])

    if albums2 is None:
        print('An error happened')
        return None

    with open(f"./resources/total_albums.json", "r") as file:
        albums = json.load(file)

    with open(f"./resources/artist_information.json", "r") as file:
        artist_information = json.load(file)

    if artist_search[3] > artist_search2[3]:
        print(f"{artist_search[1]} has {albums[artist_search[0]]} albums and is more popular then {artist_search2[1]} who has {albums[artist_search2[0]]} albums.")

    elif artist_search[3] < artist_search2[3]:
        print(f"{(artist_search2[1])} has {albums[artist_search2[0]]} albums and is more popular then {artist_search[1]} who has {albums[artist_search[0]]} albums.")

    elif artist_search[3] == artist_search2[3]:
        print(f"{(artist_search[1])} has {albums[artist_search[0]]} albums and equally popular then {artist_search2[1]} who has {albums[artist_search2[0]]} albums.")

    plot_albums_popularity()


def plot_albums_popularity():

    with open('resources/artist_information.json', 'r') as file:
        data = json.load(file)
    with open('resources/total_albums.json', 'r') as file1:
        data1 = json.load(file1)

    popularity = []
    album_amount = []
    id_list = []
    unsorted_list = {}

    for item in data1:
        id_list.append(item)

    for item in data:
         name = item
         artist_popularity = data[name]["popularity"]
         id = data[name]["id"]
         if id in id_list:
             albums = data1.get(id)
             unsorted_list[albums] = artist_popularity

    myKeys = list(unsorted_list.keys())
    myKeys.sort()

    sd = {i: unsorted_list[i] for i in myKeys}

    for item in sd:
        albums = item
        album_amount.append(albums)

    for item in sd.values():
        artist_popularity = item
        popularity.append(artist_popularity)

    xpoints = np.array(album_amount)
    ypoints = np.array(popularity)

    plt.xlabel("amount of albums")
    plt.ylabel("popularity")

    plt.plot(xpoints, ypoints)
    plt.show()


def main():

    menu = '''
    Have you ever wondered...

    Do positive lyrics tend to lead to more popular songs? 
    How does the weather influence the genre of music people listen to? 
    Does having more albums make an artist more popular?
    
    Welcome to our music analysis!
    Here you can choose between three different analysis.
    1. The correlation between popularity and happy or sad songs.
    2. The correlation between temperature and top genres.
    3. The correlation between popularity and number of albums.
    4. Exit
    '''
    print(menu)
    choice = input('Enter your choice (number between 1-4): ')

    match choice:
        case '1':
            happy_or_sad_popular()
        case '2':
            compare_genre_temperature()
        case '3':
            option3()
        case '4':
            print('Thanks for using our music analyzer')
        case _:
            print('Please write a valid choice \n')
            main()


if __name__ == "__main__":
    main()
