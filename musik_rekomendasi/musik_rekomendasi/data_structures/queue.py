# data_structures/queue.py
# Digunakan untuk: Antrian lagu berikutnya / Play Queue (FIFO)

from models.lagu import Lagu


class Queue:
    """
    Queue berbasis list Python — prinsip FIFO.
    
    Operasi:
        enqueue(lagu)  - tambah lagu ke belakang antrian
        dequeue()      - ambil & hapus lagu paling depan (diputar berikutnya)
        peek()         - lihat lagu paling depan tanpa menghapus
        kosong()       - cek apakah antrian kosong
        tampilkan()    - return semua lagu dalam antrian
    """

    def __init__(self):
        self._items: list[Lagu] = []

    def kosong(self) -> bool:
        return len(self._items) == 0

    def enqueue(self, lagu: Lagu):
        """Tambah lagu ke belakang antrian."""
        self._items.append(lagu)

    def dequeue(self) -> Lagu | None:
        """Ambil & hapus lagu paling depan antrian. Return None jika kosong."""
        if self.kosong():
            return None
        return self._items.pop(0)

    def peek(self) -> Lagu | None:
        """Lihat lagu paling depan TANPA menghapusnya."""
        if self.kosong():
            return None
        return self._items[0]

    def hapus(self, id_lagu: int) -> bool:
        """Hapus lagu dari antrian berdasarkan ID."""
        for i, lagu in enumerate(self._items):
            if lagu.id == id_lagu:
                self._items.pop(i)
                return True
        return False

    def tampilkan(self) -> list:
        """Return list semua lagu dalam antrian (index 0 = paling depan)."""
        return list(self._items)

    def __len__(self) -> int:
        return len(self._items)
