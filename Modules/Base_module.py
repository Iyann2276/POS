from tkinter import *
from tkinter import ttk
from Modules.Database_module import getConn, clearSqlTable, SearchSql

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
        headers = ["KATEGORI", "KODE", "NAMA BARANG", "SATUAN STOK", "STOK", "SATUAN UMUM"]
        anchors = [CENTER, CENTER, W, CENTER, CENTER, CENTER]
        widths = [200, 80, 200, 200, 100, 200]
        stretch = [False, False, True, False, False, False]

        super().__init__(master, headers, anchors, widths, stretch)

    def load_data(self):
        with getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inventory ORDER BY KATEGORI")
            rows = cursor.fetchall()
            cursor.execute("SELECT * FROM cart")
            cart = cursor.fetchall()

            for i, item in enumerate(rows):
                inCart = 0
                try:
                    self.tree.insert("", END, iid=item[2], values=(item[1], item[2], item[3], item[4], item[5], item[6]))
                    for c in cart:
                        if c[0] == item[2]:
                            cursor.execute(f"SELECT SUM(QTY) FROM cart WHERE KODE_BARANG = '{c[0]}'")
                            inCart = cursor.fetchone()[0]
                            self.tree.item(item=c[0], values=(item[1], item[2], item[3], item[4], item[5]-inCart, item[6]))
                except Exception as e:
                    print(e)
                    continue
        

        conn.close()

    def clear(self):
        for it in self.tree.get_children():
            self.tree.delete(it)

    def refresh(self):
        self.clear()
        self.load_data()

    def search(self, input:str):
        self.clear()
        rows = SearchSql(input)
        with getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cart")
            cart = cursor.fetchall()

            for i, item in enumerate(rows):
                inCart = 0
                try:
                    self.tree.insert("", END, iid=item[2], values=(item[1], item[2], item[3], item[4], item[5], item[6]))
                    for c in cart:
                        if c[0] == item[2]:
                            cursor.execute(f"SELECT SUM(QTY) FROM cart WHERE KODE_BARANG = '{c[0]}'")
                            inCart = cursor.fetchone()[0]
                            self.tree.item(item=c[0], values=(item[1], item[2], item[3], item[4], item[5]-inCart, item[6]))
                except Exception as e:
                    print(e)
                    continue

class ItemList2(Table):
    def __init__(self, master):
        headers = ["KATEGORI", "ID", "NAMA BARANG", "SATUAN STOK", "STOK", "SATUAN BELI", "HARGA BELI"]
        anchors = [CENTER, CENTER, W, CENTER, CENTER, CENTER, W]
        widths = [200, 80, 200, 200, 100, 200, 200]
        stretch = [False, False, True, False, False, False, False]

        super().__init__(master, headers, anchors, widths, stretch)

    def load_data(self):
        with getConn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inventory ORDER BY KATEGORI")
            rows = cursor.fetchall()

            for item in rows:
                try:
                    self.tree.insert("", END, iid=item[2], values=(item[1], item[2], item[3], item[4], item[5], item[7], f"{item[8]:,}"))
                except Exception as e:
                    print(e)
                    continue

    def clear(self):
        for it in self.tree.get_children():
            self.tree.delete(it)

    def refresh(self):
        self.clear()
        self.load_data()

class UnitList(Table):
    def __init__(self, master):
        headers = ["SATUAN", "KONVERSI", "HARGA JUAL", "HARGA GROSIR"]
        anchors = [CENTER, CENTER, CENTER, CENTER]
        widths = [100, 100, 150, 100]
        stretch = [False, False, False, True]

        super().__init__(master, headers, anchors, widths, stretch)
        self.list = []

    def add(self, datas:dict[str, StringVar], nama:str, kode:str):
        data = {k:v.get() for k,v in datas.items()}
        try:
            self.tree.insert("", END, data["SATUAN          : "].title(),
                            values=(data["SATUAN          : "].title(),
                                    data["KONVERSI        : "],
                                    data["HARGA JUAL      : "],
                                    data["HARGA GROSIR    : "])
                            )
            self.list.append((
                            nama.title(),
                            kode.upper(),
                            data["SATUAN          : "].title(),
                            int(data["KONVERSI        : "]),
                            int(data["HARGA JUAL      : "]),
                            int(data["HARGA GROSIR    : "])
                            ))
        except Exception as e:
            print(e)
            return

    def delete(self):
        row = self.tree.selection()
        if not row:
            return
        value = self.tree.item(row[0], "values")
        for i in self.list:
            if i[2] == value[0]:
                self.tree.delete(i[2])
                self.list.remove(i)
    
    def load_data(self, nama:str):
        self.list = []
        with getConn() as conn:
            cur = conn.cursor()
            cur.execute("""SELECT NAMA_SATUAN, KONVERSI, HARGA_JUAL, HARGA_GROSIR
                        FROM konversi WHERE NAMA_BARANG = %s""", (nama,))
            rows = cur.fetchall()

            for item in rows:
                try:
                    self.tree.insert("", END, iid=item[0], values=(item[0], item[1], item[2], item[3]))
                    self.list.append((
                        nama, NONE, item[0]
                    ))
                except Exception as e:
                    print(e)
                    continue

    def clear(self):
        self.list = []
        for it in self.tree.get_children():
            self.tree.delete(it)

# ====================== CART LIST ======================

class CartList(Table):
    def __init__(self, master):
        headers = ['KODE', 'NAMA BARANG', 'SATUAN', 'Qty', 'HARGA SATUAN', 'HARGA TOTAL']
        anchors = [CENTER]*6
        widths = [80, 200, 100, 60, 200, 200]
        stretch = [False, True, False, False, False, False]

        super().__init__(master, headers, anchors, widths, stretch)
        self.cart = []

    def displayHarga(self):
        harga = []
        for item in self.cart:
            harga.append(item[2])
        totalHarga = sum(harga)
        return totalHarga

    def add(self, data, harga, satuan, qty=1):
        nama = f"{data[2]} - {satuan}"
        total = harga*qty
        for it in self.cart:
            if it[0] == nama:
                qty = it[1] + qty
                total = harga*qty
                self.tree.item(item=nama, values=(data[1], data[2], satuan, qty, harga, total))
                it[1] = qty
                it[2] = total
                return
        self.tree.insert("", END, nama, values=(data[1], data[2], satuan, qty, harga, total))
        self.cart.append([nama, qty, total, data[2], satuan])
    
    def delete(self, data, qty=1):
        nama = f"{data[1]} - {data[2]}"
        total = int(data[3])*qty
        for it in self.cart:
            if it[0] == nama and it[1] != 1:
                qty = it[1] - qty
                total = int(data[4])*qty
                self.tree.item(item=it[0], values=(data[0], data[1], data[2], qty, data[4], total))
                it[1] = qty
                it[2] = total
                return
            elif it[0] == nama and it[1] == 1:
                self.tree.delete(it[0])
                self.cart.remove(it)
                return

            
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
        self.tree.tag_configure("keluar", background="#a00000")
        self.tree.tag_configure("masuk", background="#0000a0")

        for i, item in enumerate(rows):
            try:
                if item[5] == "KELUAR":
                    self.tree.insert("", 0, values=(item[0], item[1], item[2], item[3], item[4], item[5], item[6]), tags="keluar")
                else:
                    self.tree.insert("", 0, values=(item[0], item[1], item[2], item[3], item[4], item[5], item[6]), tags="masuk")
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

