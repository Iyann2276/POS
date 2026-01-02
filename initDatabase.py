from Modules.Database_module import getConn

def init_db():
    with getConn() as conn:
        cur = conn.cursor()

        # --- TABLE ---

        cur.execute("""CREATE TABLE IF NOT EXISTS inventory (
                    ID_BARANG INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    KATEGORI TEXT NOT NULL,
                    KODE TEXT NOT NULL UNIQUE,
                    NAMA TEXT NOT NULL UNIQUE,
                    SATUAN_STOK TEXT NOT NULL,
                    STOK INTEGER DEFAULT 0,
                    SATUAN_UMUM TEXT DEFAULT 'None',
                    SATUAN_HARGA_BELI TEXT DEFAULT 'None',
                    HARGA_BELI INTEGER DEFAULT 0,
                    ASET BIGINT DEFAULT 0
                    )""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS konversi (
                    ID_SATUAN INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    ID_BARANG TEXT,
                    NAMA_BARANG TEXT,
                    NAMA_SATUAN TEXT,
                    KONVERSI INTEGER,
                    HARGA_JUAL INTEGER,
                    HARGA_GROSIR INTEGER,
                    FOREIGN KEY (ID_BARANG) REFERENCES inventory(KODE),
                    FOREIGN KEY (NAMA_BARANG) REFERENCES inventory(NAMA)
                    )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS penjualan (
                    ID_PENJUALAN INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    WAKTU_PEMBELIAN TEXT NOT NULL,
                    SUBTOTAL REAL NOT NULL,
                    DISKON REAL NOT NULL DEFAULT 0.0,
                    TOTAL REAL NOT NULL,
                    DIBAYAR REAL NOT NULL,
                    KEMBALIAN REAL NOT NULL,
                    METODE TEXT
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
        
        cur.execute("""CREATE TABLE IF NOT EXISTS cart (
                    KODE_BARANG TEXT,
                    NAMA_BARANG TEXT UNIQUE,
                    SATUAN_BARANG TEXT,
                    QTY INTEGER,
                    HARGA_BELI INTEGER,
                    HARGA_JUAL INTEGER
                    )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS assets (
                    ASET TEXT NOT NULL UNIQUE,
                    JUMLAH BIGINT DEFAULT 0
                    )""")
                    
        cur.execute("""INSERT INTO assets
                    VALUES ('CASH', 0), ('QRIS', 0), ('BARANG', 0)
                    ON CONFLICT DO NOTHING;""")
        
        # --- TRIGGER ---

        cur.execute("""CREATE OR REPLACE FUNCTION delete_cart_if_zero_fn()
                    RETURNS trigger AS $$
                    BEGIN
                        IF NEW.QTY <= 0 THEN
                            DELETE FROM cart WHERE NEW.QTY <= 0;
                            RETURN NULL;
                        END IF;

                        RETURN NEW;
                    END;
                    $$ LANGUAGE plpgsql;
                    """)

        cur.execute("""DROP TRIGGER IF EXISTS delete_cart_if_zero ON cart;

                    CREATE TRIGGER delete_cart_if_zero
                    AFTER UPDATE OF QTY ON cart
                    FOR EACH ROW
                    EXECUTE FUNCTION delete_cart_if_zero_fn();
                    """)
        
        cur.execute("""CREATE OR REPLACE FUNCTION update_assets_fn()
                    RETURNS trigger AS $$
                    BEGIN
                        UPDATE assets
                        SET JUMLAH = (SELECT SUM(ASET) FROM inventory)
                        WHERE ASET = 'BARANG';

                        RETURN NEW;
                    END;
                    $$ LANGUAGE plpgsql;
                    """)

        cur.execute("""DROP TRIGGER IF EXISTS update_asset ON inventory;
                    CREATE TRIGGER update_asset
                    AFTER UPDATE OF ASET ON inventory
                    FOR EACH ROW
                    EXECUTE FUNCTION update_assets_fn();
                    """)

if __name__ == "__main__":
    init_db()