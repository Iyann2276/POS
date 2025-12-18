from models.db import getConn

def addLaporanAset(data):
    conn = getConn()
    cur = conn.cursor()

    cur.execute("""INSERT INTO laporanAset (
                BULAN, TANGGAL, JAM, ASET, JUMLAH, "MASUK/KELUAR"
                ) VALUES (?, ?, ?, ?, ?, ?)""", data)
    
    conn.commit()
    conn.close()