from models.db import getConn
from datetime import *

def penjualan(method, subtotal, payment, discount = 0.0):
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

    return total, change

def addAset(aset, jumlah):
    conn = getConn()
    cur = conn.cursor()

    cur.execute("UPDATE assets SET JUMLAH = JUMLAH + ? WHERE ASET = ?",
                (jumlah, aset))
    
    conn.commit()
    conn.close()