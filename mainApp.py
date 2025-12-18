from tkinter import *
from tkinter import messagebox

from models.db import getConn, addQty, clearSqlTable, delQty, init_db, subtractStock
from style import setup_style
from models.baseModels import ItemList, CartList, topWin
from models.checkoutModels import penjualan, addAset
from inventory import Inventory

init_db()
clearSqlTable("cart")
# ====================== MAIN APPLICATION ======================

class Application:
    def __init__(self):
        self.root = Tk()
        self.root.attributes("-fullscreen", True)
        setup_style(self.root)

        self._build_menu()
        self._build_layout()

        self.cart = CartList(self.bodyFrame)
        self.cart.tree.bind("<Double-1>", lambda event: self.hapusBarang(self.cart.tree))
    # ---------- UI BUILDERS ---------- #

    def _build_menu(self):
        menubar = Menu(self.root)
        file = Menu(menubar, tearoff=0)
        file.add_command(label="Inventory", command=lambda:Inventory() if not self.cart.cart else messagebox.showinfo(message="ITEM HARUS KOSONG"))
        file.add_separator()
        file.add_command(label="Quit", command=quit)
        menubar.add_cascade(label="File", menu=file)
        self.root.config(menu=menubar)

    def _build_layout(self):
        main = Frame(self.root, bg="#faabdd")
        main.pack(fill=BOTH, expand=True)

        # Grid setup
        main.columnconfigure(0, weight=1)
        main.rowconfigure(0, minsize=200)
        main.rowconfigure(1, minsize=500)
        main.rowconfigure(2, weight=1)

        # Header
        header = Frame(main, bg="#1a3f3a", relief=RAISED, borderwidth=5)
        header.grid(row=0, column=0, sticky=NSEW)

        Button(header, text="TAMBAH BARANG", command=self.open_add_item).grid(row=0, column=0, sticky=NSEW)
        Button(header, text="KOSONGKAN BARANG", command=self.clearTable).grid(row=1, column=0, sticky=NSEW)

        self.totalHarga = Label(header, text=f"Rp {0:15}", font=("Consolas", 20), anchor=E)
        self.totalHarga.grid(row=0, rowspan=2, column=1, sticky=NSEW)

        # Body
        self.bodyFrame = Frame(main, bg="#faabdd", relief=SUNKEN, borderwidth=5)
        self.bodyFrame.grid(row=1, column=0, sticky=NSEW)
        self.bodyFrame.columnconfigure(0, weight=1)
        self.bodyFrame.rowconfigure(0, weight=1)

        # Footer
        footer = Frame(main, bg="#1a3f3a")
        footer.grid(row=2, column=0, sticky=NSEW)

        self.footerFrame = Frame(footer)
        #self.footerFrame.grid(sticky=NSEW)
        footer.columnconfigure((0,1), weight=1)
        footer.rowconfigure((0), weight=1)

        Button(footer, text="CHECKOUT", command=lambda: [self.open_checkout()] if self.cart.cart else messagebox.showinfo(message="ITEM KOSONG")).grid(column=1, row=0, sticky=NSEW)

    # ---------- WINDOWS ---------- #

    def open_checkout(self):
        self.win = topWin(self.root)
        self.win.rowconfigure(0, weight=1)
        self.win.rowconfigure(1, minsize=70)
        self.win.columnconfigure(0, weight=1)

        frame1 = Frame(self.win, bg="#1a3f3a")
        frame1.grid(sticky=EW, padx=10)
        frame1.columnconfigure((0,1), weight=1)
        #frame1.rowconfigure((0,1), weight=1)

        totalHarga = Label(frame1, font='consolas', width=10, border=5, relief=GROOVE, text="TOTAL", justify=LEFT, anchor=W)
        totalHarga.grid(column=0, row=0, sticky=NSEW)
        pembayaran = Label(frame1, font='consolas', width=10, border=5, relief=GROOVE, text="PEMBAYARAN", justify=LEFT, anchor=W)
        pembayaran.grid(column=0, row=1, sticky=NSEW)

        self.total = Entry(frame1, font='consolas', width=10, border=5, relief=GROOVE, justify=CENTER)
        self.total.grid(column=1, row=0, sticky=NSEW)
        self.total.insert(0, self.cart.displayHarga())
        self.pembayaran = Entry(frame1, font='consolas', width=10, border=5, relief=GROOVE, justify=CENTER)
        self.pembayaran.grid(column=1, row=1, sticky=NSEW)

        methods = ["QRIS", "CASH"]

        self.v = StringVar(value="CASH")

        for i in range(len(methods)):
            self.cash = Radiobutton(frame1, text=methods[i], variable=self.v, value=methods[i], height=3, indicatoron=0)
            self.cash.config(font='consolas')
            self.cash.grid(row=2, column=i, sticky=NSEW, pady=10)

        frame2 = Frame(self.win, bg="blue")
        frame2.grid(sticky=NSEW)
        frame2.rowconfigure(0, weight=1)
        frame2.columnconfigure((0, 1), weight=1)

        Button(frame2,font="consolas", text="CANCEL", command=self.win.destroy).grid(column=0, row=0, sticky=NSEW)
        Button(frame2,font="consolas", text="DONE", command=lambda: [self.submitCheckout(), self.win.destroy()]).grid(column=1, row=0, sticky=NSEW)

    def submitCheckout(self):
        method = self.v.get()
        if not method: return
        total = self.total.get()
        bayar = self.pembayaran.get()
        if bayar == '': messagebox.showinfo(message="MASUKAN PEMBAYARAN")
        total = int(self.total.get())
        bayar = int(self.pembayaran.get())
        if bayar >= total:
            conn = getConn()
            cur = conn.cursor()

            cur.execute("SELECT * FROM cart")
            items = cur.fetchall()

            for item in items:
                subtractStock(item[0], item[1])

            t, c = penjualan(method, total, bayar)
            
            addAset(method, t)
            self.open_kembalian(int(c))
            
            self.cart.clear()
            clearSqlTable("cart")
        else: messagebox.showinfo(message="PEMBAYARAN KURANG")

    def open_kembalian(self, change):
        win = topWin(self.root)
        win.rowconfigure((0,1), weight=1)
        win.columnconfigure(0, weight=1)

        Label(win, text=f"KEMBALIAN : {change}", font=("consolas", 15, "bold"), borderwidth=10, relief=RIDGE, bg="#00ADB5", foreground="black").grid(sticky=NSEW)

        Button(win, text="OK", command=win.destroy, font='consolas').grid(sticky=NSEW)

    def open_add_item(self):
        self.addWin = topWin(self.root,1200,500)
        self.addWin.rowconfigure(0, weight=1)
        self.addWin.rowconfigure(1, minsize=100)
        self.addWin.columnconfigure(0, weight=1)

        frame1 = Frame(self.addWin, bg="blue")
        frame1.grid(sticky=NSEW)
        frame1.rowconfigure(0, weight=1)
        frame1.columnconfigure(0, weight=1)

        self.table = ItemList(frame1)
        self.table.load_data()
        self.table.tree.bind("<Double-1>", lambda event: self.tambahBarang(self.table.tree))
        self.table.tree.bind("<Double-3>", lambda event: self.open_quantity())

        frame2 = Frame(self.addWin, bg="blue")
        frame2.grid(sticky=NSEW)

        Button(frame2, text="DONE", command=self.addWin.destroy).grid(column=0, row=0, sticky=NSEW)

    def open_quantity(self):
        self.win = topWin(self.addWin)
        self.win.rowconfigure(0, weight=1)
        self.win.rowconfigure(1, minsize=70)
        self.win.columnconfigure(0, weight=1)

        frame1 = Frame(self.win, bg="blue")
        frame1.grid(sticky=EW, padx=10)
        frame1.columnconfigure((0,1,3,4), min=50)
        frame1.columnconfigure(2, weight=1)

        self.qty = Entry(frame1, font='consolas', width=10, border=5, relief=GROOVE, justify=CENTER)
        self.qty.grid(column=2, row=0, sticky=NSEW)
        self.qty.insert(0, '1')
        Button(frame1,command=lambda: self.qtyAdd(-10), font='consolas', text="-10").grid(column=0,row=0,sticky=NSEW)
        Button(frame1,command=lambda: self.qtyAdd(-1), font='consolas', text="-1").grid(column=1,row=0,sticky=NSEW)
        Button(frame1,command=lambda: self.qtyAdd(1), font='consolas', text="+1").grid(column=3,row=0,sticky=NSEW)
        Button(frame1,command=lambda: self.qtyAdd(10), font='consolas', text="+10").grid(column=4,row=0,sticky=NSEW)

        frame2 = Frame(self.win, bg="blue")
        frame2.grid(sticky=NSEW)
        frame2.rowconfigure(0, weight=1)
        frame2.columnconfigure((0, 1), weight=1)

        Button(frame2,font="consolas", text="CANCEL", command=self.win.destroy).grid(column=0, row=0, sticky=NSEW)
        Button(frame2,font="consolas", text="DONE", command=lambda: [self.tambahBanyakBarang(self.table.tree), self.win.destroy()]).grid(column=1, row=0, sticky=NSEW)

    # ---------- ACTIONS ---------- #

    def qtyAdd(self, qty):
        ref = int(self.qty.get())
        QTY = ref + qty
        self.qty.delete(0, END)
        self.qty.insert(0, QTY)
        ref = int(self.qty.get())
        if ref <= 0:
            self.qty.delete(0, END)
            self.qty.insert(0, "1")            

    def tambahBarang(self, item_table):
        row = item_table.selection()
        if not row:
            messagebox.showinfo(message="BARANG BELUM DISELECT")
            return
        value = item_table.item(row[0], "values")
        if int(value[4]) > 0:
            addQty(value[1], 1)
            self.table.tree.item(item=value[1], values=(value[0], value[1], value[2], value[3], int(value[4])-1, value[5]))
            self.cart.add(value)
            self.updateHarga()
        else: messagebox.showinfo(message=("STOK TIDAK CUKUP"))

    def tambahBanyakBarang(self, item_table):
        qty = int(self.qty.get())
        row = item_table.selection()
        if not row:
            messagebox.showinfo(message="BARANG BELUM DISELECT")
            self.open_add_item()
            return
        value = item_table.item(row[0], "values")
        if qty < int(value[4]):
            addQty(value[1], qty)
            self.table.tree.item(item=value[1], values=(value[0], value[1], value[2], value[3], int(value[4])-qty, value[5]))
            self.cart.add(value, qty)
            self.updateHarga()
        else:
            messagebox.showinfo(message=("STOK TIDAK CUKUP"))
            self.open_add_item()

    def hapusBarang(self, item_table):
        row = item_table.selection()
        if not row:
            return
        values = item_table.item(row[0], "values")
        delQty(values[0], 1)
        self.cart.delete(values)
        self.updateHarga()

    def clearTable(self):
        self.cart.clear()
        self.totalHarga.config(text=f"Rp {0:15,}")

    def updateHarga(self):
        self.totalHarga.config(text=f"Rp {self.cart.displayHarga():15,}")

# ====================== RUN PROGRAM ======================

if __name__ == "__main__":
    #app = Inventory()
    app = Application()
    app.root.mainloop()