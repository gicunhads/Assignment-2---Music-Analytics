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
    countries.append(country)
    number_genres.append(len(genre))

for country, temp in country_temp.items():
    temperatures.append(temp)


plt.figure(figsize=(10, 6))
plt.scatter(temp, number_genres, color="m")


for i, country in enumerate(countries):
    plt.text(temperatures[i], number_genres[i] + 0.1, country, fontsize=9)

plt.title("Average Temp. vs n. of genres per country")
plt.xlabel("Average Temperature (°C)")
plt.ylabel("Number of music genres")
plt.grid(True)
plt.show()
