import json, requests, datetime
from datetime import datetime





def artist_id_search(name):
    service = "https://dit009-spotify-assignment.vercel.app/api/v1"
    id_search = f"{service}/search?q={name}&type=artist&limit=1"
    result = requests.get(id_search)
    result_data = result.json()
    for item in result_data["artists"]["items"]:
        id = item["id"]
    
#must add error handling in case wrong artist where user can choose to enter id on their own

    return(id)
        

def artist_albums(id):
    service = "https://dit009-spotify-assignment.vercel.app/api/v1"
    album_search = f"{service}/artists/{id}/albums"
    albums = requests.get(album_search)
    album_file = albums.json()
    for item in album_file["items"]:
        dicto = {}
        name = item["name"]
        release_date = item["release_date"]
        dicto[name] = release_date
        print(dicto)
#must add error handling in case total album amout is greater then 20. The spotify thing that gets album can only get 20 at a time
        if len(dicto) == 20:
            
    
       


def main():
    artist_name = input("Input artist name: ")
    artist_id = artist_id_search(artist_name)
    albums = artist_albums(artist_id)
    
   


if __name__ == "__main__":
    main()
