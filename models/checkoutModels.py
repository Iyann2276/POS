from models.db import getConn
from models.laporanModels import addLaporanAset
from datetime import *

def penjualan(method, subtotal, payment, hargaBeli,  discount = 0.0):
    date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    total = round(subtotal - discount, 2)
    change = round(payment - total, 0)

    conn = getConn()
    cur = conn.cursor()

    cur.execute("""INSERT INTO penjualan (
                WAKTU_PEMBELIAN, SUBTOTAL, DISKON, TOTAL, DIBAYAR, KEMBALIAN, METODE
                ) VALUES (?,?,?,?,?,?,?)""", (date,subtotal,discount,total,payment,change,method.upper()))
    
    conn.commit()
    conn.close()

    data = (datetime.now().strftime("%m"), datetime.now().strftime("%d"), datetime.now().strftime("%H:%M:%S"), method, total, "MASUK", "PEMBELIAN")
    data2 = (datetime.now().strftime("%m"), datetime.now().strftime("%d"), datetime.now().strftime("%H:%M:%S"), "BARANG", hargaBeli, "KELUAR", "PEMBELIAN")

    addLaporanAset(data2)
    addLaporanAset(data)
    return total, change

def addAset(aset, jumlah):
    conn = getConn()
    cur = conn.cursor()

    cur.execute("UPDATE assets SET JUMLAH = JUMLAH + ? WHERE ASET = ?",
                (jumlah, aset))
    
    conn.commit()
    conn.close()

def subtractAset(aset:str, jumlah:int = 0):
    conn = getConn()
    cur = conn.cursor()

    cur.execute("UPDATE assets SET JUMLAH = JUMLAH - ? WHERE ASET = ?", (jumlah, aset))
    
    conn.commit()
    conn.close()