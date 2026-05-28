# data_structures/doubly_linked_list.py
# Digunakan untuk: Playlist (navigasi next & previous lagu)

from models.lagu import Lagu


class Node:
    """Satu kotak dalam rantai DLL — menyimpan lagu + pointer ke dua arah."""

    def __init__(self, lagu: Lagu):
        self.lagu = lagu
        self.prev = None   # pointer ke node SEBELUMNYA
        self.next = None   # pointer ke node BERIKUTNYA


class DoublyLinkedList:
    """
    Doubly Linked List untuk menyimpan playlist lagu.
    
    Operasi:
        tambah(lagu)          - tambah lagu ke akhir playlist
        hapus(id_lagu)        - hapus lagu berdasarkan ID
        next_lagu()           - pindah ke lagu berikutnya
        prev_lagu()           - pindah ke lagu sebelumnya
        lagu_sekarang()       - return lagu yang sedang aktif
        tampilkan()           - return semua lagu sebagai list
        kosong()              - cek apakah playlist kosong
    """

    def __init__(self):
        self.head    = None   # node pertama
        self.tail    = None   # node terakhir
        self.current = None   # node yang sedang diputar
        self.ukuran  = 0

    def kosong(self) -> bool:
        return self.head is None

    def tambah(self, lagu: Lagu):
        """Tambah lagu baru di akhir playlist."""
        node_baru = Node(lagu)

        if self.kosong():
            self.head    = node_baru
            self.tail    = node_baru
            self.current = node_baru
        else:
            # sambungkan ke tail lama
            node_baru.prev = self.tail
            self.tail.next = node_baru
            self.tail      = node_baru

        self.ukuran += 1

    def hapus(self, id_lagu: int) -> bool:
        """
        Hapus node berdasarkan ID lagu.
        Return True jika berhasil, False jika tidak ditemukan.
        """
        temp = self.head

        while temp:
            if temp.lagu.id == id_lagu:
                # update current jika node ini yang sedang diputar
                if temp == self.current:
                    self.current = temp.next or temp.prev

                # sambung ulang pointer tetangga
                if temp.prev:
                    temp.prev.next = temp.next
                else:
                    self.head = temp.next   # hapus head

                if temp.next:
                    temp.next.prev = temp.prev
                else:
                    self.tail = temp.prev   # hapus tail

                # putus pointer node ini
                temp.prev = None
                temp.next = None

                self.ukuran -= 1
                return True

            temp = temp.next

        return False   # ID tidak ditemukan

    def next_lagu(self) -> Lagu | None:
        """Pindah ke lagu berikutnya. Return lagu baru atau None jika sudah akhir."""
        if self.current and self.current.next:
            self.current = self.current.next
            return self.current.lagu
        return None

    def prev_lagu(self) -> Lagu | None:
        """Pindah ke lagu sebelumnya. Return lagu baru atau None jika sudah awal."""
        if self.current and self.current.prev:
            self.current = self.current.prev
            return self.current.lagu
        return None

    def lagu_sekarang(self) -> Lagu | None:
        """Return objek Lagu yang sedang aktif."""
        if self.current:
            return self.current.lagu
        return None

    def set_current(self, id_lagu: int) -> bool:
        """Set lagu aktif berdasarkan ID. Return True jika ditemukan."""
        temp = self.head
        while temp:
            if temp.lagu.id == id_lagu:
                self.current = temp
                return True
            temp = temp.next
        return False

    def tampilkan(self) -> list:
        """Return list semua objek Lagu dalam playlist (urut dari head)."""
        hasil = []
        temp  = self.head
        while temp:
            hasil.append(temp.lagu)
            temp = temp.next
        return hasil

    def __len__(self) -> int:
        return self.ukuran
