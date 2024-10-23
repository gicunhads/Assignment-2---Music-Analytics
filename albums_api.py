import json, requests, time

service = "https://dit009-spotify-assignment.vercel.app/api/v1"

def artist_id_search(name):
    try:
            artist_search = f"{service}/search?q={name}&type=artist&limit=1"
    
            result = requests.get(artist_search)
            result_data = result.json()


            values_dict = {}
            


    


            for item in result_data["artists"]["items"]:
               id = item["id"]
               artist_name = item["name"]
               genre = item["genres"]
               popularity = item["popularity"]

               values_dict[id] = [artist_name, genre, popularity]

               
            right_name = input("Is " + artist_name + " the artist you are looking for? y/n").lower()
            if right_name == "y":
               return values_dict
            elif right_name =="n":
            
                id = input("Please input the right artist id: ")

                   
                id_search = f"{service}/artists/{id}"
                get_id = requests.get(id_search)
                id_file = get_id.json()

                values_dict.clear()

                for item in id_file:
                   artist_name = item["name"]
                   genre = item["genres"]
                   popularity = item["popularity"]

                   values_dict[id] = [artist_name, genre, popularity]

               

            else:
                print("Error: invalid input")
                return(None)
               
    except KeyError:
        time.sleep(5)
        artist_id_search(name)



def artist_albums(id):
    try:
        album_search = f"{service}/artists/{id}/albums?limit=50&include_groups=album"
        albums = requests.get(album_search)
        album_file = albums.json()
        total_albums = album_file["total"]
        print(total_albums)
        return total_albums
    except KeyError:
        time.sleep(10)
        artist_albums(id)
     


def main():
    artist_name1 = input("Input the first artist name: ")
    artist_id1 = artist_id_search(artist_name1)
    album_amount1 = artist_albums(artist_id1)
    


    artist_name2 = input("Input the second artist name: ")
    artist_id2 = artist_id_search(artist_name2)
    album_amount2 = artist_albums(artist_id2)
    


if __name__ == "__main__":
    main()
