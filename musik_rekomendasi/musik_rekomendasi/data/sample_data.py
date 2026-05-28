# data/sample_data.py
# Data awal — diload saat aplikasi pertama kali dibuka

from models.lagu import Lagu

SAMPLE_LAGU = [
    Lagu(1,  "Blinding Lights",     "The Weeknd",     "pop",     "energetic", 200, 98),
    Lagu(2,  "Bohemian Rhapsody",   "Queen",           "rock",    "happy",     354, 97),
    Lagu(3,  "Someone Like You",    "Adele",           "pop",     "sad",       285, 95),
    Lagu(4,  "Shape of You",        "Ed Sheeran",      "pop",     "happy",     234, 94),
    Lagu(5,  "Smells Like Teen",    "Nirvana",         "rock",    "energetic", 301, 93),
    Lagu(6,  "Fly Me to the Moon",  "Frank Sinatra",   "jazz",    "chill",     147, 90),
    Lagu(7,  "Lose Yourself",       "Eminem",          "hiphop",  "energetic", 326, 92),
    Lagu(8,  "Hotline Bling",       "Drake",           "hiphop",  "chill",     267, 88),
    Lagu(9,  "Gravity",             "John Mayer",      "pop",     "sad",       246, 85),
    Lagu(10, "Take Five",           "Dave Brubeck",    "jazz",    "chill",     324, 87),
    Lagu(11, "Yellow",              "Coldplay",        "pop",     "happy",     269, 91),
    Lagu(12, "Hotel California",    "Eagles",          "rock",    "chill",     391, 96),
    Lagu(13, "Peaches",             "Justin Bieber",   "pop",     "happy",     198, 83),
    Lagu(14, "HUMBLE.",             "Kendrick Lamar",  "hiphop",  "energetic", 177, 89),
    Lagu(15, "The Night We Met",    "Lord Huron",      "indie",   "sad",       213, 82),
]
