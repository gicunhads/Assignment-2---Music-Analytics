import json, re, requests, time
from geopy.geocoders import Nominatim
from requests import ReadTimeout
geolocator = Nominatim(user_agent="geoapiExercises")
from spotify_api_miner import get_top_artists, get_top_genres, get_average_temp, get_country_genre, get_country

digit_pattern = r"-*\d+"   
playlist_id_pattern = r"[A-Za-z0-9]{22}"
word_pattern = r"[a-z]+"


country_genre =  {
    "sweden": ["Swedish gangsta rap", "swedish hip hop", "swedish trap", "swedish trap pop"],
    "united states": ["k-pop"],
    "brazil": ["Agronejo", "arrocha", "musica tocantinense", "sertanejo", "sertanejo universitario"],
    "canada": ["modern country pop", "pop rap"],
    "italy": ["Italian pop", "pop virale italiano", "rap genovese"],
    "france": ["modern country pop", "pop rap"],
    "netherlands": ["Art pop", "dance pop", "pop"],
    "india": ["Desi pop", "hindi indie", "indian indie", "indian singer-songwriter"]
    }

country_temp = { "sweden":9.44,
    "united states": 28.50,
    "brazil":27.32,
    "canada": 10.94,
    "italy": 28.08,
    "france": 24.45,
    "netherlands": 12.15,
    "india": 28.50

}

def main():
    digit_pattern = r"-*\d+"   
    lat = input("Insert latitude: ")
    long = input("Insert longitude: ") 
    
    if re.match(digit_pattern, lat) and re.match(digit_pattern, long):
        average_temperature = get_average_temp(lat, long)
        
        country = get_country(lat,long)
        top_genres = get_country_genre(country)
        if top_genres != None: 
            print(f"average temperature in this week is {average_temperature}°C")
            if top_genres != []:
                country_genre[country] = top_genres
                country_temp[country] = average_temperature
                with open(f'./resources/country_genre.json', 'w') as file:
                    json.dump(country_genre, file)
                with open(f'./resources/country_temp.json', 'w') as file:
                    json.dump(country_temp, file)
                print(f"the top genres were {top_genres}")
            
    
if __name__ == "__main__":
    main()
            


