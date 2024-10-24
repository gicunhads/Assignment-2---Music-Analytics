import matplotlib.pyplot as plt
import numpy as np
import json

with open('assignmenttwo.json', 'r') as file:
    data = json.load(file) 
with open('total_albums.json', 'r') as file1:
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
print(sd)

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
