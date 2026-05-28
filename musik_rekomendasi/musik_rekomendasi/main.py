# main.py
# Entry point aplikasi — inisialisasi semua data & jalankan GUI

import tkinter as tk
from tkinter import ttk

from models.lagu import Lagu
from data_structures.bst import BST
from data_structures.doubly_linked_list import DoublyLinkedList
from data_structures.stack import Stack
from data_structures.queue import Queue
from data.sample_data import SAMPLE_LAGU
from ui.halaman_katalog import HalamanKatalog
from ui.halaman_rekomendasi import HalamanRekomendasi
from ui.halaman_playlist import HalamanPlaylist


class App(tk.Tk):
    """
    Window utama aplikasi.
    Menyimpan semua state (katalog, playlist, riwayat, antrian)
    dan mengelola navigasi antar halaman via tab.
    """

    def __init__(self):
        super().__init__()

        self.title("🎵 MelodRec — Sistem Rekomendasi Musik")
        self.geometry("900x620")
        self.resizable(False, False)
        self.configure(bg="#1a1a2e")

        # ── State global (shared antar halaman) ─────────────────────────────
        self.katalog  = BST()          # semua lagu
        self.playlist = DoublyLinkedList()
        self.riwayat  = Stack()
        self.antrian  = Queue()
        self._next_id = 1              # auto-increment ID lagu baru

        # Load sample data ke BST
        for lagu in SAMPLE_LAGU:
            self.katalog.insert(lagu)
            self._next_id = max(self._next_id, lagu.id + 1)

        # ── Notebook (tab navigation) ────────────────────────────────────────
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook",          background="#1a1a2e", borderwidth=0)
        style.configure("TNotebook.Tab",      background="#16213e", foreground="#a0a0c0",
                        padding=[20, 8], font=("Consolas", 10, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", "#0f3460")],
                  foreground=[("selected", "#e94560")])

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # ── Inisialisasi tiap halaman ─────────────────────────────────────────
        self.hal_katalog      = HalamanKatalog(self.notebook, self)
        self.hal_rekomendasi  = HalamanRekomendasi(self.notebook, self)
        self.hal_playlist     = HalamanPlaylist(self.notebook, self)

        self.notebook.add(self.hal_katalog,     text="  📀 Katalog  ")
        self.notebook.add(self.hal_rekomendasi, text="  🔍 Rekomendasi  ")
        self.notebook.add(self.hal_playlist,    text="  🎵 Playlist  ")

    def get_next_id(self) -> int:
        """Generate ID unik untuk lagu baru."""
        id_baru = self._next_id
        self._next_id += 1
        return id_baru

    def refresh_semua(self):
        """Refresh tampilan semua halaman (dipanggil setelah CRUD)."""
        self.hal_katalog.refresh()
        self.hal_rekomendasi.refresh()
        self.hal_playlist.refresh()


if __name__ == "__main__":
    app = App()
    app.mainloop()
