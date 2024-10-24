
import matplotlib.pyplot as plt
import json

with open(f"./resources/country_genre.json", "r") as file:
    country_genre = json.load(file)

with open(f'./resources/country_temp.json', 'r') as file:
    country_temp = json.load(file)

countries = []
temperatures = []
number_genres = []

for country, genre in country_genre.items():
    country = country.title()
    countries.append(country)
    number_genres.append(len(genre))

for country, temp in country_temp.items():
    temperatures.append(float(temp))

combined = sorted(zip(temperatures, number_genres, countries))
temperatures, number_genres, countries = zip(*combined)

plt.figure(figsize=(10, 6))
plt.scatter(temperatures, number_genres, color="m")


for temp, num_g, country in combined:
    plt.text(temp, num_g + 0.1, country, fontsize=5)

plt.title("Average Temp. vs n. of genres per country")
plt.xlabel("Average Temperature (°C)")
plt.ylabel("Number of music genres")
plt.grid(True)
plt.show()

