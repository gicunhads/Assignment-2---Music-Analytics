import json, requests, time 
from requests import ReadTimeout
from album_api_miner import artist_albums, artist_id_search




def main():
    artist_name = input("Input the first artist name: ").lower()
    artist_search = artist_id_search(artist_name)
    albums = artist_albums((artist_search[0]))

    if albums == None:
        albums = artist_albums((artist_search[0]))

    artist_name2 = input("Input the second artist name: ").lower()
    artist_search2 = artist_id_search(artist_name2)
    albums2 = artist_albums((artist_search2[0]))

    if albums2 == None:
        albums2 = artist_albums((artist_search2[0]))



    if artist_search[3] > artist_search2[3]: 
        print(f"{(artist_search[1])} has {albums} albums and is more popular then {artist_search2[1]} who has {albums2} albums.")

    elif artist_search[3] < artist_search2[3]: 
        print(f"{(artist_search2[1])} has {albums2} albums and is more popular then {artist_search[1]} who has {albums} albums.")

    elif artist_search[3] == artist_search2[3]: 
        print(f"{(artist_search[1])} has {albums} albums and equally popular then {artist_search2[1]} who has {albums2} albums.")



    
    


if __name__ == "__main__":
    main()
