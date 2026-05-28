# ui/halaman_playlist.py
# Halaman Playlist — menggunakan DLL (prev/next), Stack (riwayat), Queue (antrian)

import tkinter as tk
from tkinter import ttk, messagebox


WARNA = {
    "bg":     "#1a1a2e", "panel": "#16213e",
    "card":   "#0f3460", "aksen": "#e94560",
    "teks":   "#eaeaea", "teks2": "#a0a0c0",
    "hijau":  "#4ecca3", "kuning": "#f5a623",
}


class HalamanPlaylist(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg=WARNA["bg"])
        self.app = app
        self._bangun_ui()

    def _bangun_ui(self):
        # ── Header ──
        tk.Label(self, text="🎵  Playlist & Player", bg=WARNA["bg"],
                 fg=WARNA["aksen"], font=("Consolas", 16, "bold")).pack(
                 anchor="w", padx=15, pady=(12, 5))

        # ── Player card ──
        player = tk.Frame(self, bg=WARNA["card"], padx=20, pady=12)
        player.pack(fill="x", padx=15, pady=5)

        tk.Label(player, text="▶  Sedang Diputar", bg=WARNA["card"],
                 fg=WARNA["teks2"], font=("Consolas", 9)).pack(anchor="w")
        self.label_now = tk.Label(player, text="— Belum ada lagu —",
                                  bg=WARNA["card"], fg=WARNA["hijau"],
                                  font=("Consolas", 13, "bold"), wraplength=700)
        self.label_now.pack(anchor="w", pady=3)

        self.label_detail = tk.Label(player, text="",
                                     bg=WARNA["card"], fg=WARNA["teks2"],
                                     font=("Consolas", 9))
        self.label_detail.pack(anchor="w")

        # Tombol prev/next/antrian
        ctrl = tk.Frame(player, bg=WARNA["card"])
        ctrl.pack(anchor="w", pady=(8, 0))

        for teks, fn, warna in [
            ("⏮ Prev",      self._prev,           WARNA["panel"]),
            ("▶ Play",       self._play_sekarang,  WARNA["aksen"]),
            ("⏭ Next",      self._next,            WARNA["panel"]),
            ("⏭+ Dari Antrian", self._play_antrian, WARNA["kuning"]),
        ]:
            tk.Button(ctrl, text=teks, bg=warna, fg=WARNA["teks"],
                      font=("Consolas", 9, "bold"), relief="flat", padx=10, pady=5,
                      command=fn).pack(side="left", padx=3)

        # ── 3 kolom: Playlist / Riwayat / Antrian ──
        kolom_frame = tk.Frame(self, bg=WARNA["bg"])
        kolom_frame.pack(fill="both", expand=True, padx=15, pady=5)

        # Playlist
        self._kolom_playlist(kolom_frame)
        # Riwayat
        self._kolom_riwayat(kolom_frame)
        # Antrian
        self._kolom_antrian(kolom_frame)

    def _kolom_playlist(self, parent):
        frame = tk.Frame(parent, bg=WARNA["panel"], padx=8, pady=8)
        frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        tk.Label(frame, text="📋 Playlist", bg=WARNA["panel"],
                 fg=WARNA["aksen"], font=("Consolas", 10, "bold")).pack(anchor="w")

        self.list_playlist = tk.Listbox(frame, bg=WARNA["card"], fg=WARNA["teks"],
                                         selectbackground=WARNA["aksen"],
                                         font=("Consolas", 8), relief="flat",
                                         activestyle="none", height=10)
        self.list_playlist.pack(fill="both", expand=True, pady=5)

        btn_f = tk.Frame(frame, bg=WARNA["panel"])
        btn_f.pack(fill="x")
        tk.Button(btn_f, text="▶ Putar ini", bg=WARNA["hijau"], fg="#111",
                  font=("Consolas", 8, "bold"), relief="flat",
                  command=self._putar_pilihan).pack(side="left", padx=(0, 4))
        tk.Button(btn_f, text="➕ ke Antrian", bg=WARNA["card"], fg=WARNA["teks"],
                  font=("Consolas", 8), relief="flat",
                  command=self._tambah_antrian).pack(side="left", padx=(0, 4))
        tk.Button(btn_f, text="🗑", bg=WARNA["aksen"], fg="white",
                  font=("Consolas", 8), relief="flat",
                  command=self._hapus_dari_playlist).pack(side="left")

    def _kolom_riwayat(self, parent):
        frame = tk.Frame(parent, bg=WARNA["panel"], padx=8, pady=8)
        frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        tk.Label(frame, text="🕐 Riwayat", bg=WARNA["panel"],
                 fg=WARNA["kuning"], font=("Consolas", 10, "bold")).pack(anchor="w")

        self.list_riwayat = tk.Listbox(frame, bg=WARNA["card"], fg=WARNA["teks"],
                                        font=("Consolas", 8), relief="flat",
                                        activestyle="none", height=10,
                                        selectbackground=WARNA["kuning"])
        self.list_riwayat.pack(fill="both", expand=True, pady=5)

        tk.Label(frame, text="(Stack — terbaru di atas)", bg=WARNA["panel"],
                 fg=WARNA["teks2"], font=("Consolas", 7)).pack(anchor="w")

    def _kolom_antrian(self, parent):
        frame = tk.Frame(parent, bg=WARNA["panel"], padx=8, pady=8)
        frame.pack(side="left", fill="both", expand=True)

        tk.Label(frame, text="⏭ Antrian", bg=WARNA["panel"],
                 fg=WARNA["hijau"], font=("Consolas", 10, "bold")).pack(anchor="w")

        self.list_antrian = tk.Listbox(frame, bg=WARNA["card"], fg=WARNA["teks"],
                                        font=("Consolas", 8), relief="flat",
                                        activestyle="none", height=10,
                                        selectbackground=WARNA["hijau"])
        self.list_antrian.pack(fill="both", expand=True, pady=5)

        btn_f = tk.Frame(frame, bg=WARNA["panel"])
        btn_f.pack(fill="x")
        tk.Button(btn_f, text="🗑 Hapus", bg=WARNA["aksen"], fg="white",
                  font=("Consolas", 8), relief="flat",
                  command=self._hapus_dari_antrian).pack(side="left")
        tk.Label(frame, text="(Queue — FIFO)", bg=WARNA["panel"],
                 fg=WARNA["teks2"], font=("Consolas", 7)).pack(anchor="w")

    # ── PLAYER CONTROLS ──────────────────────────────────────────────────────

    def _update_now_playing(self, lagu):
        if lagu:
            self.label_now.config(
                text=f"♪  {lagu.judul}  —  {lagu.artis}")
            self.label_detail.config(
                text=f"{lagu.genre} | {lagu.mood} | {lagu.durasi_format()} | ⭐{lagu.popularitas}")
            self.app.riwayat.push(lagu)   # push ke Stack riwayat
            self._refresh_riwayat()
        else:
            self.label_now.config(text="— Belum ada lagu —")
            self.label_detail.config(text="")

    def _play_sekarang(self):
        lagu = self.app.playlist.lagu_sekarang()
        if lagu:
            self._update_now_playing(lagu)
        else:
            messagebox.showinfo("Info", "Playlist kosong!")

    def _next(self):
        lagu = self.app.playlist.next_lagu()
        if lagu:
            self._update_now_playing(lagu)
            self._highlight_current()
        else:
            messagebox.showinfo("Info", "Sudah lagu terakhir!")

    def _prev(self):
        lagu = self.app.playlist.prev_lagu()
        if lagu:
            self._update_now_playing(lagu)
            self._highlight_current()
        else:
            messagebox.showinfo("Info", "Sudah lagu pertama!")

    def _play_antrian(self):
        """Dequeue dari Queue, putar lagunya."""
        lagu = self.app.antrian.dequeue()
        if lagu:
            self._update_now_playing(lagu)
            self._refresh_antrian()
        else:
            messagebox.showinfo("Info", "Antrian kosong!")

    def _putar_pilihan(self):
        sel = self.list_playlist.curselection()
        if not sel:
            return
        idx   = sel[0]
        semua = self.app.playlist.tampilkan()
        if idx < len(semua):
            lagu = semua[idx]
            self.app.playlist.set_current(lagu.id)
            self._update_now_playing(lagu)
            self._highlight_current()

    def _tambah_antrian(self):
        sel = self.list_playlist.curselection()
        if not sel:
            return
        semua = self.app.playlist.tampilkan()
        idx   = sel[0]
        if idx < len(semua):
            lagu = semua[idx]
            self.app.antrian.enqueue(lagu)
            self._refresh_antrian()
            messagebox.showinfo("Info", f"'{lagu.judul}' ditambahkan ke antrian!")

    def _hapus_dari_playlist(self):
        sel = self.list_playlist.curselection()
        if not sel:
            return
        semua = self.app.playlist.tampilkan()
        idx   = sel[0]
        if idx < len(semua):
            lagu = semua[idx]
            self.app.playlist.hapus(lagu.id)
            self._refresh_playlist()
            self._update_now_playing(self.app.playlist.lagu_sekarang())

    def _hapus_dari_antrian(self):
        sel = self.list_antrian.curselection()
        if not sel:
            return
        antrian_list = self.app.antrian.tampilkan()
        idx = sel[0]
        if idx < len(antrian_list):
            lagu = antrian_list[idx]
            self.app.antrian.hapus(lagu.id)
            self._refresh_antrian()

    # ── REFRESH ──────────────────────────────────────────────────────────────

    def _refresh_playlist(self):
        self.list_playlist.delete(0, tk.END)
        for l in self.app.playlist.tampilkan():
            self.list_playlist.insert(tk.END, f"  {l.judul} — {l.artis}")
        self._highlight_current()

    def _refresh_riwayat(self):
        self.list_riwayat.delete(0, tk.END)
        for l in self.app.riwayat.tampilkan():
            self.list_riwayat.insert(tk.END, f"  {l.judul} — {l.artis}")

    def _refresh_antrian(self):
        self.list_antrian.delete(0, tk.END)
        for i, l in enumerate(self.app.antrian.tampilkan(), 1):
            self.list_antrian.insert(tk.END, f"  {i}. {l.judul} — {l.artis}")

    def _highlight_current(self):
        """Highlight lagu yang sedang diputar di listbox playlist."""
        current = self.app.playlist.lagu_sekarang()
        if not current:
            return
        semua = self.app.playlist.tampilkan()
        for i, l in enumerate(semua):
            if l.id == current.id:
                self.list_playlist.selection_clear(0, tk.END)
                self.list_playlist.selection_set(i)
                self.list_playlist.see(i)
                break

    def refresh(self):
        """Dipanggil setelah ada perubahan dari halaman lain."""
        self._refresh_playlist()
        self._refresh_riwayat()
        self._refresh_antrian()
