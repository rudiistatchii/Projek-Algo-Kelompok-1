# ui/halaman_rekomendasi.py
# Halaman Rekomendasi — filter lagu by genre & mood menggunakan Linear Search

import tkinter as tk
from tkinter import ttk, messagebox

from algorithms.linear_search import linear_search, cari_by_judul
from algorithms.quick_sort import quick_sort


WARNA = {
    "bg":    "#1a1a2e", "panel": "#16213e",
    "card":  "#0f3460", "aksen": "#e94560",
    "teks":  "#eaeaea", "teks2": "#a0a0c0",
    "hijau": "#4ecca3",
}

GENRE_LIST = ["(semua)", "pop", "rock", "jazz", "hiphop", "indie", "r&b", "electronic"]
MOOD_LIST  = ["(semua)", "happy", "sad", "chill", "energetic"]


class HalamanRekomendasi(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg=WARNA["bg"])
        self.app = app
        self._bangun_ui()

    def _bangun_ui(self):
        # ── Header ──
        tk.Label(self, text="🔍  Rekomendasi Lagu", bg=WARNA["bg"],
                 fg=WARNA["aksen"], font=("Consolas", 16, "bold")).pack(
                 anchor="w", padx=15, pady=(12, 5))

        # ── Filter panel ──
        filter_frame = tk.Frame(self, bg=WARNA["panel"], padx=15, pady=12)
        filter_frame.pack(fill="x", padx=15, pady=5)

        # Baris 1: genre & mood
        baris1 = tk.Frame(filter_frame, bg=WARNA["panel"])
        baris1.pack(fill="x")

        tk.Label(baris1, text="Genre:", bg=WARNA["panel"], fg=WARNA["teks2"],
                 font=("Consolas", 10)).pack(side="left", padx=(0, 6))
        self.cb_genre = ttk.Combobox(baris1, values=GENRE_LIST, state="readonly",
                                     font=("Consolas", 10), width=14)
        self.cb_genre.current(0)
        self.cb_genre.pack(side="left", padx=(0, 20))

        tk.Label(baris1, text="Mood:", bg=WARNA["panel"], fg=WARNA["teks2"],
                 font=("Consolas", 10)).pack(side="left", padx=(0, 6))
        self.cb_mood = ttk.Combobox(baris1, values=MOOD_LIST, state="readonly",
                                    font=("Consolas", 10), width=14)
        self.cb_mood.current(0)
        self.cb_mood.pack(side="left", padx=(0, 20))

        # Baris 2: search by keyword
        baris2 = tk.Frame(filter_frame, bg=WARNA["panel"])
        baris2.pack(fill="x", pady=(8, 0))

        tk.Label(baris2, text="Cari:", bg=WARNA["panel"], fg=WARNA["teks2"],
                 font=("Consolas", 10)).pack(side="left", padx=(0, 6))
        self.entry_cari = tk.Entry(baris2, bg=WARNA["card"], fg=WARNA["teks"],
                                   insertbackground="white", font=("Consolas", 10),
                                   relief="flat", width=30)
        self.entry_cari.pack(side="left", padx=(0, 10))

        tk.Button(baris2, text="🔎 Cari", bg=WARNA["aksen"], fg="white",
                  font=("Consolas", 9, "bold"), relief="flat", padx=12,
                  command=self._cari).pack(side="left", padx=4)
        tk.Button(baris2, text="Rekomendasi", bg=WARNA["hijau"], fg="#111",
                  font=("Consolas", 9, "bold"), relief="flat", padx=12,
                  command=self._rekomendasikan).pack(side="left", padx=4)
        tk.Button(baris2, text="Reset", bg=WARNA["card"], fg=WARNA["teks2"],
                  font=("Consolas", 9), relief="flat", padx=8,
                  command=self._reset).pack(side="left", padx=4)

        # ── Label info hasil ──
        self.label_info = tk.Label(self, text="", bg=WARNA["bg"],
                                   fg=WARNA["teks2"], font=("Consolas", 9))
        self.label_info.pack(anchor="w", padx=15)

        # ── Tabel hasil ──
        tabel_frame = tk.Frame(self, bg=WARNA["bg"])
        tabel_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        cols = ("ID", "Judul", "Artis", "Genre", "Mood", "Durasi", "Pop.")
        self.tabel = ttk.Treeview(tabel_frame, columns=cols, show="headings",
                                  height=14, selectmode="browse")

        lebar = {"ID": 40, "Judul": 200, "Artis": 140, "Genre": 70,
                 "Mood": 80, "Durasi": 60, "Pop.": 50}
        for col in cols:
            self.tabel.heading(col, text=col)
            self.tabel.column(col, width=lebar[col], anchor="center")

        scrollbar = ttk.Scrollbar(tabel_frame, orient="vertical",
                                  command=self.tabel.yview)
        self.tabel.configure(yscrollcommand=scrollbar.set)
        self.tabel.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Tombol "Tambah ke Playlist"
        tk.Button(self, text="➕ Tambah ke Playlist", bg=WARNA["hijau"], fg="#111",
                  font=("Consolas", 10, "bold"), relief="flat", pady=6,
                  command=self._ke_playlist).pack(pady=(0, 10))

        # Load semua lagu default
        self._tampilkan(self.app.katalog.semua_lagu())

    # ── AKSI ─────────────────────────────────────────────────────────────────

    def _rekomendasikan(self):
        """Filter by genre & mood menggunakan Linear Search."""
        genre = self.cb_genre.get()
        mood  = self.cb_mood.get()

        semua = self.app.katalog.semua_lagu()
        hasil = linear_search(
            semua,
            genre=None if genre == "(semua)" else genre,
            mood=None  if mood  == "(semua)" else mood,
        )
        # sort hasil by popularitas descending
        hasil = quick_sort(hasil, key="popularitas", ascending=False)
        self._tampilkan(hasil)
        self.label_info.config(
            text=f"Linear Search selesai — {len(hasil)} lagu ditemukan "
                 f"(genre: {genre}, mood: {mood}), diurutkan by popularitas"
        )

    def _cari(self):
        """Cari by keyword di judul/artis."""
        keyword = self.entry_cari.get().strip()
        if not keyword:
            self._rekomendasikan()
            return
        semua = self.app.katalog.semua_lagu()
        hasil = cari_by_judul(semua, keyword)
        self._tampilkan(hasil)
        self.label_info.config(text=f"Ditemukan {len(hasil)} lagu dengan keyword '{keyword}'")

    def _reset(self):
        self.cb_genre.current(0)
        self.cb_mood.current(0)
        self.entry_cari.delete(0, tk.END)
        self._tampilkan(self.app.katalog.semua_lagu())
        self.label_info.config(text="")

    def _tampilkan(self, daftar_lagu: list):
        self.tabel.delete(*self.tabel.get_children())
        for l in daftar_lagu:
            self.tabel.insert("", "end", iid=str(l.id),
                              values=(l.id, l.judul, l.artis,
                                      l.genre, l.mood, l.durasi_format(), l.popularitas))

    def _ke_playlist(self):
        sel = self.tabel.selection()
        if not sel:
            messagebox.showwarning("Pilih lagu", "Klik lagu yang ingin ditambahkan ke playlist!")
            return
        id_lagu = int(sel[0])
        lagu = self.app.katalog.search(id_lagu)
        if lagu:
            self.app.playlist.tambah(lagu)
            self.app.hal_playlist.refresh()
            messagebox.showinfo("Berhasil", f"'{lagu.judul}' ditambahkan ke playlist!")

    def refresh(self):
        """Dipanggil setelah CRUD di katalog."""
        self._tampilkan(self.app.katalog.semua_lagu())
        self.label_info.config(text="")
