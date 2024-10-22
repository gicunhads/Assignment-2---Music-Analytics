import json, requests, datetime
from datetime import datetime
from datetime import *






def artist_id_search(name):
    service = "https://dit009-spotify-assignment.vercel.app/api/v1"
    id_search = f"{service}/search?q={name}&type=artist&limit=1"
    result = requests.get(id_search)
    result_data = result.json()


    for item in result_data["artists"]["items"]:
        id = item["id"]
        artist_name = item["name"]

    right_name = input("Is " + artist_name + " the artist you are looking for? y/n").lower()
    if right_name == "y":
        return id
    else:
        id = input("Please input the right artist id: ")
        return id




        

def artist_albums(id):
    service = "https://dit009-spotify-assignment.vercel.app/api/v1"
    album_search = f"{service}/artists/{id}/albums"
    albums = requests.get(album_search)
    album_file = albums.json()
    d1 = datetime.today().date()
    for item in album_file["items"]:
        dicto = {}
        name = item["name"]
        release_date = item["release_date"]
        release_date1 = datetime.strptime(release_date,'%Y-%m-%d').date()
        if d1 > release_date1:
            d1 = release_date1

        dicto[name] = release_date
    year = d1.year()
    if len(dicto) == 20:
         album_search2 = #will make another album search that only searches thru the years it hasnt searched yet
         albums2 = requests.get(album_search)
         

       


def main():
    artist_name = input("Input artist name: ")
    artist_id = artist_id_search(artist_name)
    albums = artist_albums(artist_id)

   


if __name__ == "__main__":
    main()
