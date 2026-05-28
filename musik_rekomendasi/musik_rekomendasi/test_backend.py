# test_backend.py
# Jalankan file ini untuk verifikasi semua struktur data & algoritma benar
# python test_backend.py

import sys
sys.path.insert(0, '.')

from models.lagu import Lagu
from data_structures.bst import BST
from data_structures.doubly_linked_list import DoublyLinkedList
from data_structures.stack import Stack
from data_structures.queue import Queue
from algorithms.quick_sort import quick_sort
from algorithms.linear_search import linear_search, cari_by_judul
from data.sample_data import SAMPLE_LAGU


def separator(judul):
    print(f"\n{'='*50}")
    print(f"  {judul}")
    print('='*50)


# ── TEST BST ─────────────────────────────────────────────────────────────────
separator("TEST BST — Katalog Lagu")

katalog = BST()
for lagu in SAMPLE_LAGU:
    katalog.insert(lagu)

print(f"Total lagu di katalog: {len(katalog)}")

# search
hasil = katalog.search(7)
print(f"Search ID 7: {hasil}")

# inorder (harusnya terurut by ID)
print("Inorder traversal (by ID):")
for l in katalog.semua_lagu():
    print(f"  {l}")

# delete
katalog.delete(13)
print(f"\nSetelah hapus ID 13, total: {len(katalog)}")
print(f"Search ID 13 (harusnya None): {katalog.search(13)}")


# ── TEST DOUBLY LINKED LIST ───────────────────────────────────────────────────
separator("TEST DOUBLY LINKED LIST — Playlist")

playlist = DoublyLinkedList()
for lagu in SAMPLE_LAGU[:5]:
    playlist.tambah(lagu)

print(f"Playlist ({len(playlist)} lagu):")
for l in playlist.tampilkan():
    print(f"  {l}")

print(f"\nLagu sekarang : {playlist.lagu_sekarang()}")
print(f"Next          : {playlist.next_lagu()}")
print(f"Next lagi     : {playlist.next_lagu()}")
print(f"Prev          : {playlist.prev_lagu()}")

playlist.hapus(2)
print(f"\nSetelah hapus ID 2: {[str(l) for l in playlist.tampilkan()]}")


# ── TEST STACK ────────────────────────────────────────────────────────────────
separator("TEST STACK — Riwayat")

riwayat = Stack()
for lagu in SAMPLE_LAGU[:4]:
    riwayat.push(lagu)
    print(f"  Push: {lagu.judul}")

print(f"\nTop (peek): {riwayat.peek()}")
print(f"Pop       : {riwayat.pop()}")
print(f"Pop       : {riwayat.pop()}")
print(f"Sisa      : {len(riwayat)}")


# ── TEST QUEUE ────────────────────────────────────────────────────────────────
separator("TEST QUEUE — Antrian Berikutnya")

antrian = Queue()
for lagu in SAMPLE_LAGU[5:9]:
    antrian.enqueue(lagu)
    print(f"  Enqueue: {lagu.judul}")

print(f"\nPeek (depan): {antrian.peek()}")
print(f"Dequeue     : {antrian.dequeue()}")
print(f"Dequeue     : {antrian.dequeue()}")
print(f"Sisa        : {len(antrian)}")


# ── TEST QUICK SORT ───────────────────────────────────────────────────────────
separator("TEST QUICK SORT — Sort by Popularitas")

semua = SAMPLE_LAGU.copy()
terurut = quick_sort(semua, key="popularitas", ascending=False)
print("Top 5 by popularitas (descending):")
for l in terurut[:5]:
    print(f"  {l.popularitas:3d} | {l.judul}")

terurut_judul = quick_sort(semua, key="judul", ascending=True)
print("\nTop 5 by judul (ascending):")
for l in terurut_judul[:5]:
    print(f"  {l.judul}")


# ── TEST LINEAR SEARCH ────────────────────────────────────────────────────────
separator("TEST LINEAR SEARCH — Rekomendasi")

semua_lagu_list = SAMPLE_LAGU

hasil_pop = linear_search(semua_lagu_list, genre="pop")
print(f"Lagu genre POP ({len(hasil_pop)} hasil):")
for l in hasil_pop:
    print(f"  {l}")

hasil_chill = linear_search(semua_lagu_list, mood="chill")
print(f"\nLagu mood CHILL ({len(hasil_chill)} hasil):")
for l in hasil_chill:
    print(f"  {l}")

hasil_combo = linear_search(semua_lagu_list, genre="pop", mood="happy")
print(f"\nLagu POP + HAPPY ({len(hasil_combo)} hasil):")
for l in hasil_combo:
    print(f"  {l}")

hasil_judul = cari_by_judul(semua_lagu_list, "the")
print(f"\nCari keyword 'the' ({len(hasil_judul)} hasil):")
for l in hasil_judul:
    print(f"  {l}")

print("\n✅ Semua test selesai!")
