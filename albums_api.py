import json, requests, time 
from requests import ReadTimeout
from album_api_miner import artist_albums, artist_id_search


def main():
    artist_name = input("Input the first artist name: ").lower()
    artist_search = artist_id_search(artist_name)
    albums1 = artist_albums((artist_search[0]))

    if albums1 is None:
        print('An error happened')
        return None

    artist_name2 = input("Input the second artist name: ").lower()
    artist_search2 = artist_id_search(artist_name2)
    albums2 = artist_albums((artist_search2[0]))

    if albums2 is None:
        print('An error happened')
        return None

    with open(f"total_albums.json", "r") as file:
        albums = json.load(file)

    with open(f"artist_information.json", "r") as file:
        artist_information = json.load(file)

    if int(artist_information[artist_search[1].lower()]["popularity"]) > int(artist_information[artist_search2[1].lower()]["popularity"]):
        print(f"{artist_search[1]} has {albums[artist_search[0]]} albums and is more popular then {artist_search2[1]} who has {albums[artist_search2[0]]} albums.")

    elif int(artist_information[artist_search[1].lower()]["popularity"]) < int(artist_information[artist_search2[1].lower()]["popularity"]):
        print(f"{(artist_search2[1])} has {albums[artist_search2[0]]} albums and is more popular then {artist_search[1]} who has {albums[artist_search[0]]} albums.")

    elif int(artist_information[artist_search[1].lower()]["popularity"]) == int(artist_information[artist_search2[1].lower()]["popularity"]):
        print(f"{(artist_search[1])} has {albums[artist_search[0]]} albums and equally popular then {artist_search2[1]} who has {albums[artist_search2[0]]} albums.")


if __name__ == "__main__":
    main()
