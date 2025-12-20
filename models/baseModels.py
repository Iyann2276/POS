from tkinter import *
from tkinter import ttk
from models.db import getConn, clearSqlTable

# ====================== BASE TREEVIEW CLASS ======================

class Table():
    def __init__(self, master, headers, anchors, widths, stretch_flags):
        self.tree = ttk.Treeview(master, columns=headers, show="headings")

        for name, anchor, width, stretch in zip(headers, anchors, widths, stretch_flags):
            self.tree.column(name, anchor=anchor, width=width, minwidth=width, stretch=stretch)
            self.tree.heading(name, text=name, anchor=anchor)

        self.tree.grid(row=0, column=0, sticky=NSEW)


# ====================== INVENTORY LIST ======================

class ItemList(Table):
    def __init__(self, master):
        headers = ["KATEGORI", "ID", "NAMA BARANG", "SATUAN", "STOK", "HARGA SATUAN"]
        anchors = [CENTER, CENTER, W, CENTER, CENTER, CENTER]
        widths = [200, 80, 200, 100, 60, 200]
        stretch = [False, False, True, False, False, False]

        super().__init__(master, headers, anchors, widths, stretch)

    def load_data(self):
        conn = getConn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory ORDER BY KATEGORI")
        rows = cursor.fetchall()
        cursor.execute("SELECT * FROM cart")
        cart = cursor.fetchall()

        for i, item in enumerate(rows):
            inCart = 0
            try:
                self.tree.insert("", END, iid=item[1], values=(item[2], item[1], item[3], item[4], item[6], item[5]))
                for c in cart:
                    if c[0] == item[1]:
                        inCart = c[1]
                        self.tree.item(item=c[0], values=(item[2], item[1], item[3], item[4], item[6]-inCart, item[5]))
            except Exception:
                continue
        

        conn.close()

    def clear(self):
        for it in self.tree.get_children():
            self.tree.delete(it)

    def refresh(self):
        self.clear()
        self.load_data()

class ItemList2(Table):
    def __init__(self, master):
        headers = ["KATEGORI", "ID", "NAMA BARANG", "SATUAN", "STOK", "HARGA SATUAN", "HARGA BELI"]
        anchors = [CENTER, CENTER, W, CENTER, CENTER, CENTER, CENTER]
        widths = [200, 80, 200, 100, 60, 200, 200]
        stretch = [False, False, True, False, False, False, False]

        super().__init__(master, headers, anchors, widths, stretch)

    def load_data(self):
        conn = getConn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory ORDER BY KATEGORI")
        rows = cursor.fetchall()
        cursor.execute("SELECT * FROM cart")
        cart = cursor.fetchall()

        for i, item in enumerate(rows):
            inCart = 0
            try:
                self.tree.insert("", END, iid=item[1], values=(item[2], item[1], item[3], item[4], item[6], item[5], item[7]))
                for c in cart:
                    if c[0] == item[1]:
                        inCart = c[1]
                        self.tree.item(item=c[0], values=(item[2], item[1], item[3], item[4], item[6]-inCart, item[5], item[7]))
            except Exception:
                continue
        

        conn.close()

    def clear(self):
        for it in self.tree.get_children():
            self.tree.delete(it)

    def refresh(self):
        self.clear()
        self.load_data()

# ====================== CART LIST ======================

class CartList(Table):
    def __init__(self, master):
        headers = ['ID', 'NAMA BARANG', 'Qty', 'HARGA SATUAN', 'HARGA TOTAL']
        anchors = [CENTER]*5
        widths = [80, 200, 60, 200, 200]
        stretch = [False, True, False, False, False]

        super().__init__(master, headers, anchors, widths, stretch)
        self.cart = []

    def displayHarga(self):
        harga = []
        for item in self.cart:
            harga.append(item[2])
        totalHarga = sum(harga)
        return totalHarga

    def add(self, data, qty=1):
        total = int(data[5])*qty
        for it in self.cart:
            if it[0] == data[1]:
                qty = it[1] + qty
                total = int(data[5])*qty
                self.tree.item(item=data[1], values=(data[1], data[2], qty, data[5], total))
                it[1] = qty
                it[2] = total
                return
        self.tree.insert("", END, data[1], values=(data[1], data[2], qty, data[5], total))
        self.cart.append([data[1], qty, total])
    
    def delete(self, data, qty=1):
        total = int(data[3])*qty
        for it in self.cart:
            if it[0] == data[0] and it[1] != 1:
                qty = it[1] - qty
                total = int(data[3])*qty
                self.tree.item(item=it[0], values=(data[0], data[1], qty, data[3], total))
                it[1] = qty
                it[2] = total
                return
            if it[0] == data[0] and it[1] == 1:
                self.tree.delete(it[0])
                self.cart.remove(it)
            
    def clear(self):
        clearSqlTable("cart")
        self.cart = []
        for it in self.tree.get_children():
            self.tree.delete(it)

# ====================== LAPORAN ======================

class Laporan(Table):
    def __init__(self, master):
        headers = ["BULAN", "TANGGAL", "PADA", "ASET", "JUMLAH", "KELUAR / MASUK", "CATATAN"]
        anchors = [CENTER, CENTER, CENTER, CENTER, CENTER, CENTER, CENTER]
        widths = [200, 200, 200, 200, 200, 200, 200]
        stretch = [False, False, False, False, False, False, True]

        super().__init__(master, headers, anchors, widths, stretch)

    def load_data(self):
        conn = getConn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM laporanAset ORDER BY BULAN")
        rows = cursor.fetchall()

        for i, item in enumerate(rows):
            try:
                self.tree.insert("", 0, values=(item[0], item[1], item[2], item[3], item[4], item[5], item[6]))
            except Exception:
                continue
        
        conn.close

# ====================== WINDOW ======================

def topWin(master, w = 400, h = 300):
    root = Toplevel(master, relief=RIDGE, borderwidth=10, bg='#1a3f3a')
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()
    x = (screen_width/2) - (w/2)
    y = (screen_height/2) - (h/2)
    root.geometry("%dx%d+%d+%d" % (w, h, x, y))
    root.overrideredirect(True)
    root.attributes("-topmost", False)
    root.grab_set()
    return root
