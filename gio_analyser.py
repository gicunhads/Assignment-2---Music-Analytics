import json, re, requests, time
from geopy.geocoders import Nominatim
from requests import ReadTimeout
geolocator = Nominatim(user_agent="geoapiExercises")
from spotify_api_miner import get_top_artists, get_top_genres, get_average_temp, get_country_genre, get_country

digit_pattern = r"-*\d+"   
playlist_id_pattern = r"[A-Za-z0-9]{22}"
word_pattern = r"[a-z]+"


with open(f"./resources/country_genre.json", "r") as file:
    country_genre = json.load(file)

with open(f'./resources/country_temp.json', 'r') as file:
    country_temp = json.load(file)

def main():  
    digit_pattern = r"-*\d+"   
    lat = input("Insert latitude: ")
    long = input("Insert longitude: ") 
    
    if re.match(digit_pattern, lat) and re.match(digit_pattern, long):
        average_temperature = get_average_temp(lat, long)
        
        country = get_country(lat,long)
        country = country.lower()
        top_genres = get_country_genre(country)
        if top_genres != None: 
            print(f"average temperature in this week is {average_temperature}°C")
            if top_genres != []:
                top_genres = [genre for sublist in top_genres for genre in sublist]
                country_genre[country] = []
                country_genre[country].extend(top_genres)
                country_temp[country] = average_temperature
                with open(f'./resources/country_genre.json', 'w') as file:
                    json.dump(country_genre, file)
                with open(f'./resources/country_temp.json', 'w') as file:
                    json.dump(country_temp, file)
                print(f"the top genres were {top_genres}")
    
if __name__ == "__main__":
    main()
            
            


