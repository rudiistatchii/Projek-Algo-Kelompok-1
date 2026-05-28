# ui/halaman_katalog.py
# Halaman CRUD Lagu — menggunakan BST untuk penyimpanan, Quick Sort untuk sorting

import tkinter as tk
from tkinter import ttk, messagebox

from models.lagu import Lagu
from algorithms.quick_sort import quick_sort


WARNA = {
    "bg":       "#1a1a2e",
    "panel":    "#16213e",
    "card":     "#0f3460",
    "aksen":    "#e94560",
    "teks":     "#eaeaea",
    "teks2":    "#a0a0c0",
    "hijau":    "#4ecca3",
    "kuning":   "#f5a623",
}

GENRE_LIST = ["pop", "rock", "jazz", "hiphop", "indie", "r&b", "electronic"]
MOOD_LIST  = ["happy", "sad", "chill", "energetic"]


class HalamanKatalog(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg=WARNA["bg"])
        self.app = app
        self._sort_key = "id"
        self._sort_asc = True
        self._bangun_ui()
        self.refresh()

    # ── BUILD UI ─────────────────────────────────────────────────────────────

    def _bangun_ui(self):
        # ── Header ──
        header = tk.Frame(self, bg=WARNA["bg"])
        header.pack(fill="x", padx=15, pady=(12, 5))

        tk.Label(header, text="📀  Katalog Lagu", bg=WARNA["bg"],
                fg=WARNA["aksen"], font=("Consolas", 16, "bold")).pack(side="left")

        # Tombol sort
        sort_frame = tk.Frame(header, bg=WARNA["bg"])
        sort_frame.pack(side="right")
        tk.Label(sort_frame, text="Sort:", bg=WARNA["bg"],
                fg=WARNA["teks2"], font=("Consolas", 9)).pack(side="left", padx=4)
        for label, key in [("ID","id"),("Judul","judul"),("Pop.","popularitas"),("Durasi","durasi")]:
            tk.Button(sort_frame, text=label, bg=WARNA["card"], fg=WARNA["teks"],
                    font=("Consolas", 8), relief="flat", padx=6,
                    command=lambda k=key: self._toggle_sort(k)).pack(side="left", padx=2)

        # ── Tabel ──
        tabel_frame = tk.Frame(self, bg=WARNA["bg"])
        tabel_frame.pack(fill="both", expand=True, padx=15, pady=5)

        cols = ("ID", "Judul", "Artis", "Genre", "Mood", "Durasi", "Pop.")
        self.tabel = ttk.Treeview(tabel_frame, columns=cols, show="headings",
            height=13, selectmode="browse")

        lebar = {"ID": 40, "Judul": 180, "Artis": 130, "Genre": 70,
                "Mood": 80, "Durasi": 60, "Pop.": 50}
        for col in cols:
            self.tabel.heading(col, text=col)
            self.tabel.column(col, width=lebar[col], anchor="center")

        style = ttk.Style()
        style.configure("Treeview",        background=WARNA["panel"],
                        foreground=WARNA["teks"],  fieldbackground=WARNA["panel"],
                        rowheight=24, font=("Consolas", 9))
        style.configure("Treeview.Heading", background=WARNA["card"],
                        foreground=WARNA["aksen"],  font=("Consolas", 9, "bold"))
        style.map("Treeview", background=[("selected", WARNA["card"])])

        scrollbar = ttk.Scrollbar(tabel_frame, orient="vertical",
                                command=self.tabel.yview)
        self.tabel.configure(yscrollcommand=scrollbar.set)

        self.tabel.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tabel.bind("<<TreeviewSelect>>", self._on_pilih_baris)

        # ── Form CRUD ──
        form_frame = tk.Frame(self, bg=WARNA["panel"], padx=15, pady=10)
        form_frame.pack(fill="x", padx=15, pady=(0, 10))

        fields_kiri = [("Judul", "judul"), ("Artis", "artis"), ("Durasi (detik)", "durasi")]
        fields_kanan = [("Genre", "genre"), ("Mood", "mood"), ("Popularitas (1-100)", "pop")]

        self.entry = {}

        kiri = tk.Frame(form_frame, bg=WARNA["panel"])
        kiri.pack(side="left", fill="x", expand=True)
        kanan = tk.Frame(form_frame, bg=WARNA["panel"])
        kanan.pack(side="left", fill="x", expand=True, padx=(20, 0))

        for label, key in fields_kiri:
            tk.Label(kiri, text=label, bg=WARNA["panel"], fg=WARNA["teks2"],
                    font=("Consolas", 9)).pack(anchor="w")
            e = tk.Entry(kiri, bg=WARNA["card"], fg=WARNA["teks"], insertbackground="white",
                        font=("Consolas", 9), relief="flat", width=28)
            e.pack(anchor="w", pady=(0, 4))
            self.entry[key] = e

        for label, key in fields_kanan:
            tk.Label(kanan, text=label, bg=WARNA["panel"], fg=WARNA["teks2"],
                    font=("Consolas", 9)).pack(anchor="w")
            if key == "genre":
                cb = ttk.Combobox(kanan, values=GENRE_LIST, state="readonly",
                                font=("Consolas", 9), width=26)
                cb.pack(anchor="w", pady=(0, 4))
                self.entry[key] = cb
            elif key == "mood":
                cb = ttk.Combobox(kanan, values=MOOD_LIST, state="readonly",
                                font=("Consolas", 9), width=26)
                cb.pack(anchor="w", pady=(0, 4))
                self.entry[key] = cb
            else:
                e = tk.Entry(kanan, bg=WARNA["card"], fg=WARNA["teks"], insertbackground="white",
                            font=("Consolas", 9), relief="flat", width=28)
                e.pack(anchor="w", pady=(0, 4))
                self.entry[key] = e

        # Tombol aksi
        btn_frame = tk.Frame(form_frame, bg=WARNA["panel"])
        btn_frame.pack(side="right", padx=(20, 0), anchor="s")

        for teks, fn, warna in [
            ("➕ Tambah",  self._tambah,  WARNA["hijau"]),
            ("✏️  Edit",    self._edit,    WARNA["kuning"]),
            ("🗑️  Hapus",  self._hapus,   WARNA["aksen"]),
            ("🔄 Reset",   self._reset_form, WARNA["teks2"]),
        ]:
            tk.Button(btn_frame, text=teks, bg=warna, fg="#111",
                    font=("Consolas", 9, "bold"), relief="flat", width=12,
                    command=fn).pack(pady=3)

        self._id_dipilih = None

    # ── REFRESH ──────────────────────────────────────────────────────────────

    def refresh(self):
        """Reload tabel dari BST, dengan sort yang aktif."""
        semua = self.app.katalog.semua_lagu()
        if self._sort_key != "id":
            semua = quick_sort(semua, key=self._sort_key, ascending=self._sort_asc)
        elif not self._sort_asc:
            semua = list(reversed(semua))

        self.tabel.delete(*self.tabel.get_children())
        for l in semua:
            self.tabel.insert("", "end", iid=str(l.id),
                            values=(l.id, l.judul, l.artis,
                                    l.genre, l.mood, l.durasi_format(), l.popularitas))

    def _toggle_sort(self, key: str):
        if self._sort_key == key:
            self._sort_asc = not self._sort_asc
        else:
            self._sort_key = key
            self._sort_asc = True
        self.refresh()

    # ── EVENT ────────────────────────────────────────────────────────────────

    def _on_pilih_baris(self, _event):
        sel = self.tabel.selection()
        if not sel:
            return
        id_lagu = int(sel[0])
        lagu = self.app.katalog.search(id_lagu)
        if lagu:
            self._id_dipilih = id_lagu
            self.entry["judul"].delete(0, tk.END);  self.entry["judul"].insert(0, lagu.judul)
            self.entry["artis"].delete(0, tk.END);  self.entry["artis"].insert(0, lagu.artis)
            self.entry["durasi"].delete(0, tk.END); self.entry["durasi"].insert(0, lagu.durasi)
            self.entry["pop"].delete(0, tk.END);    self.entry["pop"].insert(0, lagu.popularitas)
            self.entry["genre"].set(lagu.genre)
            self.entry["mood"].set(lagu.mood)

    # ── CRUD ─────────────────────────────────────────────────────────────────

    def _ambil_form(self):
        """Ambil & validasi input form. Return dict atau None jika invalid."""
        judul  = self.entry["judul"].get().strip()
        artis  = self.entry["artis"].get().strip()
        genre  = self.entry["genre"].get().strip()
        mood   = self.entry["mood"].get().strip()

        if not all([judul, artis, genre, mood]):
            messagebox.showwarning("Input kosong", "Harap isi semua field!")
            return None

        try:
            durasi = int(self.entry["durasi"].get())
            pop    = int(self.entry["pop"].get())
            if not (1 <= pop <= 100):
                raise ValueError
        except ValueError:
            messagebox.showwarning("Input salah",
                                "Durasi & Popularitas harus angka (Pop: 1-100)!")
            return None

        return {"judul": judul, "artis": artis, "genre": genre,
                "mood": mood, "durasi": durasi, "pop": pop}

    def _tambah(self):
        data = self._ambil_form()
        if not data:
            return
        id_baru = self.app.get_next_id()
        lagu = Lagu(id_baru, data["judul"], data["artis"],
                    data["genre"], data["mood"], data["durasi"], data["pop"])
        self.app.katalog.insert(lagu)
        self._reset_form()
        self.app.refresh_semua()
        messagebox.showinfo("Berhasil", f"Lagu '{lagu.judul}' ditambahkan! (ID: {id_baru})")

    def _edit(self):
        if not self._id_dipilih:
            messagebox.showwarning("Pilih lagu", "Klik baris lagu yang ingin diedit dulu!")
            return
        data = self._ambil_form()
        if not data:
            return
        lagu_lama = self.app.katalog.search(self._id_dipilih)
        lagu_baru = Lagu(self._id_dipilih, data["judul"], data["artis"],
                        data["genre"], data["mood"], data["durasi"], data["pop"])
        self.app.katalog.delete(self._id_dipilih)
        self.app.katalog.insert(lagu_baru)
        self._reset_form()
        self.app.refresh_semua()
        messagebox.showinfo("Berhasil", f"Lagu ID {self._id_dipilih} diperbarui!")

    def _hapus(self):
        if not self._id_dipilih:
            messagebox.showwarning("Pilih lagu", "Klik baris lagu yang ingin dihapus dulu!")
            return
        lagu = self.app.katalog.search(self._id_dipilih)
        if not messagebox.askyesno("Konfirmasi", f"Hapus '{lagu.judul}'?"):
            return
        self.app.katalog.delete(self._id_dipilih)
        self._reset_form()
        self.app.refresh_semua()

    def _reset_form(self):
        self._id_dipilih = None
        for key, widget in self.entry.items():
            if isinstance(widget, ttk.Combobox):
                widget.set("")
            else:
                widget.delete(0, tk.END)
        self.tabel.selection_remove(*self.tabel.selection())
