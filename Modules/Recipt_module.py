from escpos.printer import Serial

def printRecipt(items:list, change, total, tunai, method):
    p = Serial('COM6', baudrate=9600, timeout=1)

    ESC = b'\x1b'
    GS  = b'\x1d'

    LINE = b'-' * 32 + b'\n'

    def header(printer:Serial):
        printer._raw(ESC + b'@')          # reset
        printer._raw(ESC + b'a\x01')      # center
        printer._raw(GS + b'!\x11')       # double size
        printer.text("TOKO SARASA\n")

        printer._raw(GS + b'!\x00')       # normal
        printer._raw(ESC + b'a\x00')      # left

        printer.text("Gunasari Dsn. Sembir 001/009\n")
        printer.text("Kec. Sumedang Selatan\n")
        printer.text("Telp: 085947388931 [Whatsapp]\n")

        printer._raw(LINE)


    def format_item(nama, qty, harga, satuan):
        """
        32 char:
        nama 16 | qty 4 | harga 12
        """
        nama = nama[:32]
        return f"{nama:<32}\n{harga:<10,}{qty:>4}{satuan:>6}{harga*qty:>12,}\n"


    def body(printer:Serial, items):
        for full, qty, harga, nama, satuan in items:
            printer.text(format_item(nama, qty, harga, satuan))


    def footer(printer:Serial, total, tunai, change, method):
        printer._raw(LINE)

        printer._raw(ESC + b'E\x01')      # bold ON
        printer.text(f"DIBAYAR {method:>24}\n")
        printer.text(f"TOTAL {total:>26,}\n")
        printer.text(f"TUNAI {tunai:>26,}\n")
        printer.text(f"{'------------':>32}\n")
        printer.text(f"KEMBALIAN {change:>22,}\n")
        printer._raw(ESC + b'E\x00')      # bold OFF

        printer._raw(LINE)
        printer._raw(ESC + b'a\x01')      # center
        printer.text("Terima kasih\n")

        printer.cut()

    header(p)
    body(p, items)
    footer(p, int(total), int(tunai), change, method)

    p.close()
