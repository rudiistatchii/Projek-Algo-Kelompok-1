# data_structures/bst.py
# Digunakan untuk: Katalog lagu — insert, search, delete by ID

from models.lagu import Lagu


class NodeBST:
    """Satu node dalam BST — menyimpan lagu dan pointer kiri/kanan."""

    def __init__(self, lagu: Lagu):
        self.lagu  = lagu
        self.left  = None   # child kiri  (ID lebih kecil)
        self.right = None   # child kanan (ID lebih besar)


class BST:
    """
    Binary Search Tree untuk menyimpan katalog lagu berdasarkan ID.
    
    Aturan BST:
        - child kiri  → ID lebih KECIL dari parent
        - child kanan → ID lebih BESAR dari parent
    
    Operasi:
        insert(lagu)         - tambah lagu ke katalog
        search(id)           - cari lagu berdasarkan ID → O(log n)
        delete(id)           - hapus lagu dari katalog
        inorder()            - return semua lagu terurut by ID (ascending)
        semua_lagu()         - alias inorder(), return list Lagu
    """

    def __init__(self):
        self.root   = None
        self._ukuran = 0

    # ── INSERT ──────────────────────────────────────────────────────────────

    def insert(self, lagu: Lagu):
        """Tambah lagu ke BST. ID harus unik."""
        self.root    = self._insert(self.root, lagu)
        self._ukuran += 1

    def _insert(self, node: NodeBST, lagu: Lagu) -> NodeBST:
        if node is None:
            return NodeBST(lagu)

        if lagu.id < node.lagu.id:
            node.left  = self._insert(node.left, lagu)
        elif lagu.id > node.lagu.id:
            node.right = self._insert(node.right, lagu)
        # jika ID sama, abaikan (tidak boleh duplikat)

        return node

    # ── SEARCH ──────────────────────────────────────────────────────────────

    def search(self, id_lagu: int) -> Lagu | None:
        """Cari lagu berdasarkan ID. Return objek Lagu atau None."""
        node = self._search(self.root, id_lagu)
        return node.lagu if node else None

    def _search(self, node: NodeBST, id_lagu: int) -> NodeBST | None:
        if node is None or node.lagu.id == id_lagu:
            return node

        if id_lagu < node.lagu.id:
            return self._search(node.left, id_lagu)
        return self._search(node.right, id_lagu)

    # ── DELETE ──────────────────────────────────────────────────────────────

    def delete(self, id_lagu: int) -> bool:
        """Hapus lagu berdasarkan ID. Return True jika berhasil."""
        if not self.search(id_lagu):
            return False
        self.root    = self._delete(self.root, id_lagu)
        self._ukuran -= 1
        return True

    def _delete(self, node: NodeBST, id_lagu: int) -> NodeBST | None:
        if node is None:
            return None

        if id_lagu < node.lagu.id:
            node.left  = self._delete(node.left, id_lagu)
        elif id_lagu > node.lagu.id:
            node.right = self._delete(node.right, id_lagu)
        else:
            # Node ditemukan — 3 kasus:
            if node.left is None:       # kasus 1 & 2: 0 atau 1 child
                return node.right
            if node.right is None:
                return node.left

            # kasus 3: punya 2 child → ganti dengan successor terkecil (inorder)
            successor      = self._min_node(node.right)
            node.lagu      = successor.lagu
            node.right     = self._delete(node.right, successor.lagu.id)

        return node

    def _min_node(self, node: NodeBST) -> NodeBST:
        """Cari node dengan ID terkecil (paling kiri)."""
        while node.left:
            node = node.left
        return node

    # ── TRAVERSAL ───────────────────────────────────────────────────────────

    def inorder(self) -> list:
        """Return list Lagu terurut ascending by ID."""
        hasil = []
        self._inorder(self.root, hasil)
        return hasil

    def _inorder(self, node: NodeBST, hasil: list):
        if node:
            self._inorder(node.left, hasil)
            hasil.append(node.lagu)
            self._inorder(node.right, hasil)

    def semua_lagu(self) -> list:
        """Alias inorder() — return semua lagu sebagai list."""
        return self.inorder()

    def __len__(self) -> int:
        return self._ukuran
