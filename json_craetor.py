import json
song_words_combined = {
    "happy": [
        # English happy words
        "Love", "Smile", "Dance", "Sunshine", "Joy", "Happy", "Sing", "Dream", "Celebrate",
        "Heart", "Light", "Free", "Shine", "Fly", "Life", "Beautiful", "Together", "Laughter",
        "Sky", "Sweet", "Summer", "Fun", "Baby", "Forever", "Bright", "Magic", "Perfect",
        "Party", "Golden", "Peace", "Rainbow", "Rise", "Run", "Cheer", "Breeze", "Glow",
        "Bliss", "Hug", "Feel", "Kiss", "Sun", "Rhythm", "Wonderful", "Dancefloor",
        "Shining", "Fire", "Groove", "Wind", "Paradise",
        # Swedish happy words
        "Kärlek", "Leende", "Dans", "Sol", "Glädje", "Lycka", "Sjunga", "Dröm", "Fira",
        "Hjärta", "Ljus", "Fri", "Stråla", "Flyga", "Liv", "Vacker", "Tillsammans", "Skratt",
        "Himmel", "Söt", "Sommar", "Skoj", "Älskling", "För evigt", "Magi", "Perfekt",
        "Fest", "Gyllene", "Fred", "Regnbåge", "Stiga", "Springa", "Hurra", "Bris", "Glöd",
        "Kram", "Känna", "Kyss", "Rytm", "Underbar", "Dansgolv", "Strålande", "Eld", "Vind",
        "Paradis",
        # Danish happy words
        "Kærlighed", "Smil", "Dans", "Solskin", "Glæde", "Lykkelig", "Synge", "Drøm", "Fejre",
        "Lys", "Fri", "Skinne", "Flyve", "Smuk", "Sammen", "Latter", "Sød", "Sjov",
        "Skat", "For evigt", "Magi", "Gylden", "Fred", "Regnbue", "Stig", "Løbe", "Jubel",
        "Brise", "Glød", "Kram", "Føle", "Kys", "Rytme", "Vidunderlig", "Dansegulv",
        "Skinnende", "Ild", "Groove", "Paradis"
    ],
    "sad": [
        # English sad words
        "Tears", "Broken", "Lonely", "Heart", "Cry", "Pain", "Goodbye", "Lost", "Alone",
        "Sad", "Gone", "Miss", "Hurt", "Dark", "Empty", "Fading", "Memories", "Cold",
        "Silence", "Sorrow", "Regret", "Fallen", "Blue", "Distance", "Shattered", "Time",
        "Rain", "Longing", "Night", "Fear", "Wounds", "Grief", "Shadows", "Apart",
        "Despair", "Farewell", "Anguish", "Bleeding", "Forgotten", "Wasted", "Hope",
        "Goodnight", "Solitude", "Heartache", "Brokenness", "Whisper", "End",
        "Betray", "Fading",
        # Swedish sad words
        "Tårar", "Brustet", "Ensam", "Hjärta", "Gråt", "Smärta", "Farväl", "Förlorad", "Ensamt",
        "Ledsen", "Borta", "Saknar", "Sårad", "Mörk", "Tom", "Bleknar", "Minnen", "Kall",
        "Tystnad", "Sorg", "Ånger", "Föll", "Blå", "Avstånd", "Krossad", "Tid",
        "Regn", "Längtan", "Natt", "Rädsla", "Sår", "Sorg", "Skuggor", "Isär",
        "Förtvivlan", "Ångest", "Blödande", "Glömd", "Bortkastad", "Hopp",
        "Godnatt", "Ensamhet", "Hjärtesorg", "Viskning", "Slut",
        "Förråda", "Bleknar",
        # Danish sad words
        "Tårer", "Knust", "Ensom", "Hjerte", "Græde", "Smerte", "Farvel", "Tabt", "Alene",
        "Trist", "Væk", "Savner", "Såret", "Mørk", "Tom", "Falmer", "Minder", "Kold",
        "Tavshed", "Sorg", "Fortrydelse", "Faldet", "Blå", "Afstand", "Knust", "Tid",
        "Regn", "Længsel", "Nat", "Frygt", "Sår", "Skygger", "Adskilt",
        "Fortvivlelse", "Angst", "Blødende", "Glemt", "Spildt", "Håb",
        "Godnat", "Ensomhed", "Hjertesorg", "Knusthed", "Hvisken", "Slut",
        "Forråde", "Falmer"
    ]
}

with open(f'./resources/happy_and_sad_words.json', 'w') as file:
    json.dump(song_words_combined, file)
