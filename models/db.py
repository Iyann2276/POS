import sqlite3 as sql
from tkinter import messagebox

DB_FILE = "main_data.db"

def getConn():
    conn = sql.Connection(DB_FILE)
    conn.row_factory = sql.Row
    return conn

def init_db():
    conn = getConn()
    cur = conn.cursor()

    cur.execute("""
                CREATE TABLE IF NOT EXISTS inventory (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                KODE_PRODUK TEXT NOT NULL UNIQUE,
                KATEGORI TEXT DEFAULT '-',
                NAMA_BARANG TEXT NOT NULL UNIQUE,
                SATUAN TEXT DEFAULT '-',
                HARGA INTEGER NOT NULL,
                STOK INTEGER NOT NULL DEFAULT 0,
                HARGA_BELI INTEGER NOT NULL,
                ASET INTEGER
                )""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS penjualan (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                WAKTU_PEMBELIAN TEXT NOT NULL,
                SUBTOTAL REAL NOT NULL,
                DISKON REAL NOT NULL DEFAULT 0.0,
                TOTAL REAL NOT NULL,
                DIBAYAR REAL NOT NULL,
                KEMBALIAN REAL NOT NULL,
                METODE TEXT NOT NULL DEFAULT CASH
                )""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS laporanAset (
                BULAN INTEGER NOT NULL,
                TANGGAL INTEGER NOT NULL,
                JAM TEXT NOT NULL,
                ASET TEXT NOT NULL,
                JUMLAH INTEGER NOT NULL,
                "MASUK/KELUAR" TEXT NOT NULL,
                CATATAN TEXT
                )""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS "cart" (
                "NAMA_BARANG" TEXT NOT NULL UNIQUE,
                "QTY" INTEGER
                )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS "assets" (
                ASET TEXT NOT NULL UNIQUE,
                JUMLAH INTEGER DEFAULT 0
                )""")
    
    conn.commit()
    conn.close()

def addBarang(kode,kategori,nama,satuan,harga,stok, hargaBeli, aset):
    conn = getConn()
    cur = conn.cursor()

    try: cur.execute("INSERT INTO inventory (KODE_PRODUK, KATEGORI, NAMA_BARANG, SATUAN, HARGA, STOK, HARGA_BELI, ASET) VALUES (?,?,?,?,?,?,?,?)", (kode, kategori, nama, satuan, harga, stok, hargaBeli, aset))
    except sql.IntegrityError:
        messagebox.showerror(message='PRODUK TERSEBUT SUDAH ADA DI INVENTORY!!!')
        return    
    finally:
        conn.commit()
        conn.close()

def addQty(nama,stok):
    conn = getConn()
    cur = conn.cursor()

    try: cur.execute("INSERT INTO cart (NAMA_BARANG, QTY) VALUES (?,?)", (nama, stok))
    except sql.IntegrityError:
        cur.execute("UPDATE cart SET QTY = QTY + ? WHERE NAMA_BARANG = ?", (stok, nama))
        return    
    finally:
        conn.commit()
        conn.close()

def delQty(nama,stok):
    conn = getConn()
    cur = conn.cursor()

    cur.execute("UPDATE cart SET QTY = QTY - ? WHERE NAMA_BARANG = ?", (stok, nama))  
    conn.commit()
    conn.close()

def editBarang(kode,harga,stok):
    conn = getConn()
    cur = conn.cursor()
    cur.execute(f"UPDATE inventory SET HARGA = ?, STOK = ? WHERE KODE_PRODUK = ?", (harga, stok, kode))
    conn.commit()
    conn.close()

def hapusBarang(pid):
    conn = getConn()
    cur = conn.cursor()
    cur.execute('DELETE FROM inventory WHERE KODE_PRODUK = ?', (pid,))
    conn.commit()
    conn.close()

def addStock(code, qty):
    conn = getConn()
    cur = conn.cursor()
    cur.execute("UPDATE inventory SET STOK = STOK + ? WHERE KODE_PRODUK = ?", (qty, code))
    conn.commit()
    conn.close()

def subtractStock(code:str, qty):
    conn = getConn()
    cur = conn.cursor()
    cur.execute("UPDATE inventory SET STOK = STOK - ? WHERE KODE_PRODUK = ?", (qty, code))
    cur.execute("UPDATE inventory SET ASET = ASET - (? * HARGA_BELI) WHERE KODE_PRODUK = ?", (qty, code))
    conn.commit()
    conn.close()

def clearSqlTable(nama):
    conn = getConn()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {nama}")
    conn.commit()
    conn.close()

def getColumn(column:str)-> list:
    conn = getConn()
    cur = conn.cursor()

    cur.execute(f"SELECT {column} FROM inventory")
    datas = set(cur.fetchall())
    data = []
    for i in datas:
        data.append(i[0])
    d = sorted(data)
    conn.close()
    return d

def getCode(prefix:str)-> str:
    if len(prefix) <= 4:
        prefix = f"{prefix[0]}{prefix[2]}"
    else:
        prefix = f"{prefix[0]}{prefix[2]}{prefix[4]}"

    prefix = prefix.upper()
    conn = getConn()
    cur = conn.cursor()

    cur.execute(f"""
        SELECT KODE_PRODUK FROM inventory
        WHERE KODE_PRODUK LIKE '{prefix.upper()}%'
        ORDER BY KODE_PRODUK DESC
        LIMIT 1
    """)

    result = cur.fetchone()
    
    if result is None:
        return f"{prefix}001"
    
    lastCode = result[0]
    num = int(lastCode.replace(prefix.upper(), ""))
    num += 1

    finalCode = f"{prefix.upper()}{num:03d}"
    conn.close()
    return finalCode

def getHargaBeli(code, qty):
    conn = getConn()
    cur = conn.cursor()

    cur.execute(f"SELECT HARGA_BELI FROM inventory WHERE KODE_PRODUK LIKE '{code}'")
    hargaBeli = cur.fetchone()

    conn.close()

    return hargaBeli[0] * qty

if __name__ == "__main__": print(getHargaBeli("RKK001"))