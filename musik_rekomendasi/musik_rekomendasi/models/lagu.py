# models/lagu.py
# Blueprint (class) untuk satu objek Lagu

class Lagu:
    """
    Merepresentasikan satu lagu dalam sistem.
    
    Atribut:
        id          : int   - nomor unik tiap lagu
        judul       : str   - judul lagu
        artis       : str   - nama artis/band
        genre       : str   - genre (pop, rock, jazz, dll)
        mood        : str   - suasana (happy, sad, chill, energetic)
        durasi      : int   - durasi dalam detik
        popularitas : int   - nilai 1-100
    """

    def __init__(self, id: int, judul: str, artis: str,
                genre: str, mood: str, durasi: int, popularitas: int):
        self.id          = id
        self.judul       = judul
        self.artis       = artis
        self.genre       = genre.lower()
        self.mood        = mood.lower()
        self.durasi      = durasi       # dalam detik
        self.popularitas = popularitas  # 1 - 100

    def durasi_format(self) -> str:
        """Mengubah durasi detik menjadi format mm:ss."""
        menit  = self.durasi // 60
        detik  = self.durasi % 60
        return f"{menit}:{detik:02d}"

    def __str__(self) -> str:
        return (f"[{self.id}] {self.judul} - {self.artis} "
                f"| {self.genre} | {self.mood} "
                f"| {self.durasi_format()} | ⭐{self.popularitas}")

    def __repr__(self) -> str:
        return f"Lagu(id={self.id}, judul='{self.judul}')"
