# data_structures/stack.py
# Digunakan untuk: Riwayat lagu yang pernah diputar (LIFO)

from models.lagu import Lagu


class Stack:
    """
    Stack berbasis list Python — prinsip LIFO.
    
    Operasi:
        push(lagu)    - tambah lagu ke atas tumpukan (lagu baru diputar)
        pop()         - ambil & hapus lagu paling atas
        peek()        - lihat lagu paling atas tanpa menghapus
        kosong()      - cek apakah stack kosong
        tampilkan()   - return semua lagu (terbaru di index 0)
    """

    def __init__(self, kapasitas: int = 50):
        self._items    : list[Lagu] = []
        self.kapasitas : int        = kapasitas   # batas riwayat

    def kosong(self) -> bool:
        return len(self._items) == 0

    def penuh(self) -> bool:
        return len(self._items) >= self.kapasitas

    def push(self, lagu: Lagu):
        """Tambah lagu ke riwayat. Jika penuh, buang yang paling lama."""
        if self.penuh():
            # buang elemen paling bawah (terlama)
            self._items.pop(0)
        self._items.append(lagu)

    def pop(self) -> Lagu | None:
        """Ambil & hapus lagu paling atas (paling baru). Return None jika kosong."""
        if self.kosong():
            return None
        return self._items.pop()

    def peek(self) -> Lagu | None:
        """Lihat lagu paling atas TANPA menghapus."""
        if self.kosong():
            return None
        return self._items[-1]

    def tampilkan(self) -> list:
        """Return list lagu — index 0 = paling baru (top of stack)."""
        return list(reversed(self._items))

    def __len__(self) -> int:
        return len(self._items)
