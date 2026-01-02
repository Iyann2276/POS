import psycopg

# ======================= GET_CONN ===========================

def getConn():
    conn = psycopg.connect(
        host="localhost",
        dbname="POS",
        user="postgres",
        password="IYANN2276",
        port=5432
    )
    return conn
# ======================== ACTION ============================

# --- TABLE ---

def clearSqlTable(nama):
    with getConn() as conn:
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {nama}")

def SearchSql(input:str, table:str = 'inventory', column:str = 'NAMA') -> list[tuple]:
    with getConn() as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table} WHERE {column} LIKE '%{input}%'")
        return cur.fetchall()
# --- GET RAW DATA ---

def fetchKonversi(namaBarang: str) -> list[tuple]:
    with getConn() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT NAMA_SATUAN, KONVERSI, HARGA_JUAL
            FROM konversi
            WHERE NAMA_BARANG = %s
        """, (namaBarang,))
        return cur.fetchall()

# --- GET DATA ---

def getUnit(namaBarang: str) -> dict:
    rows = fetchKonversi(namaBarang)
    return {satuan: konversi for satuan, konversi, _ in rows}

def getStokBarang(namaBarang: str, stokDasar: int) -> dict:
    rows = fetchKonversi(namaBarang)

    rows = sorted(rows, key=lambda x: x[1], reverse=True)

    hasil = {}
    sisa = stokDasar

    for satuan, konversi, _ in rows:
        hasil[satuan] = sisa // konversi
        sisa %= konversi

    return hasil

def getKonversi(namaBarang: str, satuan: str, jumlah: int = 1) -> int:
    rows = fetchKonversi(namaBarang)
    for nama_satuan, konversi, harga in rows:
        if nama_satuan == satuan:
            return konversi * int(jumlah), harga
    raise ValueError(f"Satuan '{satuan}' tidak ditemukan")

def getColumn(column: str, table: str = "inventory") -> list:
    with getConn() as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT {column} FROM {table}")
        return sorted({row[0] for row in cur.fetchall()})
    
def dataForCheckout(nama:str, satuan:str, qty:int = 1):
    units = getUnit(nama.title())
    with getConn() as conn:
        cur = conn.cursor()
        cur.execute(f"""
            SELECT HARGA_BELI, SATUAN_HARGA_BELI
            FROM inventory
            WHERE NAMA = '{nama.title()}'
            ORDER BY KODE DESC
            LIMIT 1
        """)

        result = cur.fetchone()
        unit1 = units[satuan.title()]
        unit2 = units[result[1].title()]

        hargaBeli = int((result[0] * (unit1/unit2)) * qty)

        return hargaBeli
        
    
def getCode(kategori:str)-> str:
    with getConn() as conn:
        cur = conn.cursor()

        cur.execute(f"""
            SELECT KODE FROM inventory
            WHERE KATEGORI = '{kategori.upper()}'
            ORDER BY KODE DESC
            LIMIT 1
        """)

        result = cur.fetchone()
    
    if result is None:
        return ""
    
    lastCode:str = result[0]
    prefix = "".join(char for char in lastCode if char.isalpha())
    num = int(lastCode.replace(prefix, ""))
    num += 1

    finalCode = f"{prefix.upper()}{num:03d}"
    return finalCode

# --- CRUD ---

def addProduct(barang:list, units:list):
    with getConn() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO inventory (KATEGORI, KODE, NAMA, SATUAN_STOK)
            VALUES (%s,%s,%s,%s)
        """, tuple(barang))
        cur.executemany("""
            INSERT INTO konversi (NAMA_BARANG, ID_BARANG, NAMA_SATUAN, KONVERSI, HARGA_JUAL, HARGA_GROSIR)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, units)

def delProduct(kode):
    with getConn() as conn:
        cur= conn.cursor()
        cur.execute('DELETE FROM inventory WHERE KODE = %s', (kode,))
        cur.execute('DELETE FROM konversi WHERE ID_BARANG = %s', (kode,))

def editProduct(kode:str, satuan:str):
    with getConn() as conn:
        cur= conn.cursor()
        cur.execute('UPDATE inventory SET SATUAN_UMUM = %s WHERE KODE = %s', (satuan, kode,))

def restockProduct(kode:str, satuan:str, harga:int, qty:int, aset:int):
    with getConn() as conn:
        cur= conn.cursor()
        cur.execute('''UPDATE inventory SET
                    STOK = STOK + %s,
                    SATUAN_HARGA_BELI = %s,
                    HARGA_BELI = %s,
                    ASET = %s
                    WHERE KODE = %s''', (qty, satuan, harga, aset, kode,))

def subtractProduct(kode:str, qty:int, aset:int):
    with getConn() as conn:
        cur= conn.cursor()
        cur.execute('''UPDATE inventory SET
                    STOK = STOK - %s,
                    ASET = %s
                    WHERE KODE = %s''', (qty, aset, kode,))

def sellProduct(items:list):
    with getConn() as conn:
        cur= conn.cursor()
        cur.executemany('''UPDATE inventory SET
                    STOK = STOK - %s,
                    ASET = ASET - %s
                    WHERE NAMA = %s''', items)

def addUnit(units:tuple):
    with getConn() as conn:
        cur= conn.cursor()
        cur.execute("""
            INSERT INTO konversi (NAMA_BARANG, ID_BARANG, NAMA_SATUAN, KONVERSI, HARGA_JUAL, HARGA_GROSIR)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, units)

def deleteUnit(nama:str, satuan:str):
    with getConn() as conn:
        cur= conn.cursor()
        cur.execute('DELETE FROM konversi WHERE NAMA_BARANG = %s AND NAMA_SATUAN = %s', (nama, satuan))

def addQty(kode: str, nama: str, satuan: str, stok: int = 1):
    with getConn() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO cart (KODE_BARANG, NAMA_BARANG, SATUAN_BARANG, QTY)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT(NAMA_BARANG)
            DO UPDATE SET QTY = cart.QTY + excluded.QTY
        """, (kode, nama, satuan, stok))

def delQty(nama,stok):
    with getConn() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE cart SET QTY = QTY - %s WHERE NAMA_BARANG = %s", (stok, nama))

# --- LAPORAN ---

def addPenjualan(data:tuple):
    with getConn() as conn:
        cur = conn.cursor()
        cur.execute("""INSERT INTO penjualan (
                WAKTU_PEMBELIAN, SUBTOTAL, DISKON, TOTAL, DIBAYAR, KEMBALIAN, METODE
                ) VALUES (%s,%s,%s,%s,%s,%s,%s)""", data)
        
def addAset(aset:str, amount:int):
    with getConn() as conn:
        cur = conn.cursor()
        cur.execute('UPDATE assets SET JUMLAH = JUMLAH + %s WHERE ASET = %s', (amount, aset.upper()))

def addLaporanAset(data):
    with getConn() as conn:
        cur = conn.cursor()

        cur.executemany("""INSERT INTO laporanAset (
                    BULAN, TANGGAL, JAM, ASET, JUMLAH, "MASUK/KELUAR", CATATAN
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)""", data)
        
def getAset()->int:
    with getConn() as conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM assets ORDER BY ASET")
        data = cur.fetchall()

        total = []

        for i in data:
            total.append(i[1])

        barang = total[0]
        aset = total[1]
        qris = total[2]

        total = sum(total)
        return total, aset, qris, barang

def getProfit():
    pendapatan = []
    pengeluaran = []
    with getConn() as conn:
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
        return pendapatan, pengeluaran


if __name__ == "__main__":
    pass