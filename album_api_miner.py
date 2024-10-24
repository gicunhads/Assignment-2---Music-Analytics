import requests, json, time

service = "https://dit009-spotify-assignment.vercel.app/api/v1"

def artist_id_search(name):
    try:
        
        try:
            with open('assignmenttwo.json', 'r') as file:
                data = json.load(file)  
        except FileNotFoundError:
            data = {}  

       
        if name in data:
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
                artist_name = item["name"]
                genre = item["genres"]
                popularity = item["popularity"]

            
            data[name] = {"id": id, "artist_name": artist_name, "genre": genre, "popularity": popularity}

            
            with open('assignmenttwo.json', 'w') as file:
                json.dump(data, file, indent=4)  

        
        values = [id, artist_name, genre, popularity]
        right_name = input(f"Is {artist_name} the artist you are looking for? y/n ").lower()

        if right_name == "y":
            return values
        elif right_name == "n":

            id = input("Please input the right artist id: ")

            id_search = f"{service}/artists/{id}"
            get_id = requests.get(id_search)
            id_file = get_id.json()

            values.clear()
            for item in id_file:
                artist_name = item["name"]
                genre = item["genres"]
                popularity = item["popularity"]

            values = [id, artist_name, genre, popularity]
            return values
        else:
            print("Error: invalid input")
            return None

    except KeyError:
        time.sleep(10)
        artist_id_search(name)




def artist_albums(id):
        try:
            try:
                with open('total_albums.json', 'r') as file:
                    data = json.load(file)  
            except FileNotFoundError:
                data = {}
            if id in data: 
                total_albums = data[id]
                
            else:
                album_search = f"{service}/artists/{id}/albums?limit=50&include_groups=album"
                albums = requests.get(album_search)
                album_file = albums.json()
                total_albums = album_file["total"]

                data[id] = total_albums

                with open('total_albums.json', 'w') as file:
                     json.dump(data, file, indent=4)


                

            return total_albums

                    
        except KeyError:
            time.sleep(15)
            artist_albums(id)
