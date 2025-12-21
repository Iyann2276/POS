from models.db import getConn

def addLaporanAset(data):
    conn = getConn()
    cur = conn.cursor()

    cur.execute("""INSERT INTO laporanAset (
                BULAN, TANGGAL, JAM, ASET, JUMLAH, "MASUK/KELUAR", CATATAN
                ) VALUES (?, ?, ?, ?, ?, ?, ?)""", data)
    
    conn.commit()
    conn.close()

def getAset()->int:
    conn = getConn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM assets")
    data = cur.fetchall()

    total = []

    for i in data:
        total.append(i[1])

    aset = total[0]
    qris = total[1]
    barang = total[2]

    total = sum(total)
    conn.close()
    return total, aset, qris, barang

def getProfit():
    pendapatan = []
    pengeluaran = []
    conn = getConn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM laporanAset")
    result = cur.fetchall()

    for data in result:
        if data[5] == "MASUK":
            pendapatan.append(data[4])
        elif data[5] == "KELUAR":
            pengeluaran.append(data[4])
        else: pass

    pendapatan = sum(pendapatan)
    pengeluaran = sum(pengeluaran)

    conn.close
    return pendapatan, pengeluaran