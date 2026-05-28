# algorithms/linear_search.py
# Digunakan untuk: Fitur rekomendasi — filter lagu by genre, mood, atau keduanya

from models.lagu import Lagu


def linear_search(katalog: list, genre: str = None, mood: str = None) -> list:
    """
    Mencari lagu yang cocok dengan kriteria genre dan/atau mood.
    Menggunakan Linear Search — scan semua elemen satu per satu.
    
    Parameter:
        katalog : list semua Lagu yang tersedia
        genre   : filter berdasarkan genre (None = abaikan filter ini)
        mood    : filter berdasarkan mood  (None = abaikan filter ini)
    
    Return: list Lagu yang cocok dengan kriteria
    """
    hasil = []

    for lagu in katalog:                       # O(n) — cek semua elemen
        cocok_genre = (genre is None) or (lagu.genre == genre.lower())
        cocok_mood  = (mood  is None) or (lagu.mood  == mood.lower())

        if cocok_genre and cocok_mood:
            hasil.append(lagu)

    return hasil


def cari_by_judul(katalog: list, query: str) -> list:
    """
    Cari lagu berdasarkan kata kunci di judul atau nama artis.
    Case-insensitive, partial match.
    
    Return: list Lagu yang judulnya/artistnya mengandung query.
    """
    hasil = []
    query = query.lower()

    for lagu in katalog:
        if query in lagu.judul.lower() or query in lagu.artis.lower():
            hasil.append(lagu)

    return hasil
