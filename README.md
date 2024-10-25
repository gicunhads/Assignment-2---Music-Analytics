# Assignment-2---Music-Analytics

Task devision: \
Tobias: \
Made the question about happy and sad songs popularity, 
connected all the different python files from the group into the two python files in the end, 
debugging others code.

Tyra: \
Did the question about the correlation inbetween album amount and popularity. 

Giovana:
I have used three APIs: Spotify API, Open Weather API and Nominatim API. My program gets the user input as latitude and longitude, and gets the country the person is located in (Nominatim API), the average temperature in that location that week(Open weather API), and the playlist ID of that country (Spotify API). Then, with the playlist ID, Spotify API gets the artists on that playlist, and gets their ID, which with them, will get the list of the popular genres that week. Moreover, I have done error handling for my tasks, such as cases as playlist ID is invalid, no genres found, invalid latitude and longitude, invalid country, blocked API requests and time outs.


files: \
json_creator.py : creates a json file with the top 50 most used words in happy and sad songs in danish, english and swedish. \
artist_information.json: stores general information like name, id, genre and popularity about an artist
total_albums.json: stores information about the total amout of album that is connected to a certain artist id. 
music_data_analyser.py : analysis the data we get from the api calls  \
spotify_api_miner.py : retrieves all the information from the api's

