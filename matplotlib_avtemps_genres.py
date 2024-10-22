import matplotlib.pyplot as plt

countries = ["Canada", "Italy", "France", "United States", "India", "Brazil", "Sweden"]
temperatures = [10.94, 28.08, 24.45, 28.50, 25.27, 27.32, 9.44]
genres = [2, 3, 3, 1, 4, 5, 4]


plt.figure(figsize=(10, 6))
plt.scatter(temperatures, genres, color="m")


for i, country in enumerate(countries):
    plt.text(temperatures[i], genres[i] + 0.1, country, fontsize=9)

plt.title("Average Temp. vs n. of genres per country")
plt.xlabel("Average Temperature (°C)")
plt.ylabel("Number of music genres")
plt.grid(True)
plt.show()
