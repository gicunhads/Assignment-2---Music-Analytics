import json, requests, time 
from requests import ReadTimeout

service = "https://dit009-spotify-assignment.vercel.app/api/v1"



def artist_id_search(name):

    try:
            with open('assignmenttwo.json', 'r') as file:
                 data = json.load(file)
                 for item in data:
                     if item == name:
                             id = data[name]["id"]
                             artist_name = data[name]["artist_name"]
                             genre = data[name]["genre"]
                             popularity = data[name]["popularity"]
                     else: 
                        artist_search = f"{service}/search?q={name}&type=artist&limit=1"
    
                        result = requests.get(artist_search)
                        result_data = result.json()
                        for item in result_data["artists"]["items"]:
                             id = item["id"]
                             print(id)
                             artist_name = item["name"]
                             print(artist_name)
                             genre = item["genres"]
                             print(genre)
                             popularity = item["popularity"]
                             print(popularity)
                             
                        new_artist_name = {name : {"id" : id, "artist_name" : artist_name,"genre" : genre, "popularity" : popularity }}
                        out_file = open('assignmenttwo.json', "w")
                        json.dump(new_artist_name)
                        out_file.close()


            values = []
            values.append(id)
            values.append(artist_name)
            values.append(genre)
            values.append(popularity)
               

               

               
            right_name = input("Is " + artist_name + " the artist you are looking for? y/n").lower()
            if right_name == "y":
               return values
            elif right_name =="n":
                
            
                    id = input("Please input the right artist id: ")

                   
                    id_search = f"{service}/artists/{id}"
                    get_id = requests.get(id_search)
                    id_file = get_id.json()

                    values.clear()
                    
                    for item in id_file:
                       artist_name = item["name"]
                       genre = item["genres"]
                       popularity = item["popularity"]

                    values.append(id)
                    values.append(artist_name)
                    values.append(genre)
                    values.append(popularity)
                    return values


               

            else:
                print("Error: invalid input")
                return(None)
               
    except KeyError:
        time.sleep(10)
        artist_id_search(name)



def artist_albums(id):

    try:
        

        album_search = f"{service}/artists/{id}/albums?limit=50&include_groups=album"
        albums = requests.get(album_search)
        album_file = albums.json()
        
        
        total_albums = []

        for item in album_file["items"]:
            album_name = item["name"]
            total_albums.append(album_name)
        print(len(total_albums))


    except KeyError:
        time.sleep(10)
        artist_albums2(id)

def artist_albums2(id):

    try:
        time.sleep(30)

        album_search = f"{service}/artists/{id}/albums?limit=50&include_groups=album"
        albums = requests.get(album_search)
        album_file = albums.json()
        
        
        total_albums = []

        for item in album_file["items"]:
            album_name = item["name"]
            total_albums.append(album_name)
        print(len(total_albums))


    except KeyError:
        time.sleep(10)
        artist_albums(id)
     


def main():
    artist_name = input("Input the first artist name: ").lower()
    artist_search = artist_id_search(artist_name)
    albums = artist_albums((artist_search[0]))

    artist_name2 = input("Input the second artist name: ")
    artist_search2 = artist_id_search(artist_name2)
    albums2 = artist_albums((artist_search2))

    if artist_search[3] > artist_search2[3]: 
        print(f"{(artist_search[1])} has {albums} albums and is more popular then {artist_search2[1]} who has {albums2} albums.")

    elif artist_search[3] < artist_search2[3]: 
        print(f"{(artist_search2[1])} has {albums2} albums and is more popular then {artist_search[1]} who has {albums} albums.")

    elif artist_search[3] == artist_search2[3]: 
        print(f"{(artist_search[1])} has {albums} albums and equally popular then {artist_search2[1]} who has {albums2} albums.")


   



if __name__ == "__main__":
    main()
