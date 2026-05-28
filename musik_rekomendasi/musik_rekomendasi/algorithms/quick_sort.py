# algorithms/quick_sort.py
# Digunakan untuk: Mengurutkan lagu by popularitas / durasi / judul

from models.lagu import Lagu


def quick_sort(arr: list, key: str = "popularitas", ascending: bool = False) -> list:
    """
    Mengurutkan list Lagu menggunakan algoritma Quick Sort.
    
    Parameter:
        arr       : list Lagu yang akan diurutkan
        key       : atribut yang jadi acuan sort
                    ("popularitas", "durasi", "judul", "artis")
        ascending : True = kecil ke besar, False = besar ke kecil
    
    Return: list Lagu yang sudah terurut (list baru, tidak mengubah asli)
    """
    if len(arr) <= 1:
        return arr

    arr = list(arr)   # salin agar tidak mengubah list asli
    _quick_sort(arr, 0, len(arr) - 1, key)

    if not ascending:
        arr.reverse()

    return arr


def _quick_sort(arr: list, low: int, high: int, key: str):
    """Fungsi rekursif Quick Sort (in-place)."""
    if low < high:
        pi = _partition(arr, low, high, key)
        _quick_sort(arr, low, pi - 1, key)
        _quick_sort(arr, pi + 1, high, key)


def _partition(arr: list, low: int, high: int, key: str) -> int:
    """Pilih pivot (elemen terakhir), atur ulang elemen di sekitarnya."""
    pivot = _get_value(arr[high], key)
    i     = low - 1

    for j in range(low, high):
        if _get_value(arr[j], key) <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]   # swap

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def _get_value(lagu: Lagu, key: str):
    """Ambil nilai atribut lagu untuk dibandingkan."""
    nilai = getattr(lagu, key)
    # untuk string (judul/artis), ubah ke lowercase agar sort tidak case-sensitive
    if isinstance(nilai, str):
        return nilai.lower()
    return nilai
