from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox

from Modules.Base_module import CartList, ItemList, topWin
from Modules.Recipt_module import printRecipt
from Modules.Checkout_module import checkout, penjualan
from Modules.Database_module import (clearSqlTable, addQty, delQty,
                                     getKonversi, getUnit, getStokBarang,
                                     addAset)
from style import setup_style
from inventory import Inventory
from laporanAset import LaporanAset

clearSqlTable("cart")
# ======================== MAIN APPLICATION ============================

class kasir():
    def __init__(self):
        self.root = Tk()
        self.root.attributes("-fullscreen", True)
        self.root.option_add("*font", 'consolas 12')
        setup_style(self.root)

        self._build_menu()
        self._build_layout()

        self.cart = CartList(self.bodyFrame)
        self.cart.tree.bind("<Double-3>", lambda event: self.hapusBarang(self.cart.tree))

    # ---------- UI BUILDERS ---------- #

    def _build_menu(self):
        menubar = Menu(self.root)
        file = Menu(menubar, tearoff=0)

        file.add_command(label="Inventory",
                         command=lambda:self.open_Inventory()
                         if not self.cart.cart
                         else messagebox.showinfo(message="ITEM HARUS KOSONG")
                         )

        file.add_command(label="Laporan Aset",
                         command=lambda:self.open_LaporanAset()
                         if not self.cart.cart
                         else messagebox.showinfo(message="ITEM HARUS KOSONG"))
        
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

        Button(header, text="TAMBAH BARANG",
               command=self.open_add_item
               ).grid(row=0, column=0, sticky=NSEW)
        
        Button(header, text="KOSONGKAN BARANG",
               command=self.clearTable
               ).grid(row=1, column=0, sticky=NSEW)

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

        footer.columnconfigure((0,1), weight=1)
        footer.rowconfigure((0), weight=1)

        Button(footer, text="CHECKOUT",
               command=lambda: [self.open_checkout()]
               if self.cart.cart
               else messagebox.showinfo(message="ITEM KOSONG")
               ).grid(column=1, row=0, sticky=NSEW)

 # ---------- WINDOWS ---------- #

    def open_checkout(self):
        def onlyNumbers(p:str):
            if p.isdigit() or p == '':
                return True
            else:
                self.root.bell()
                return False
        
        validateNumbers = self.root.register(onlyNumbers)

        win = topWin(self.root)
        win.rowconfigure(0, weight=1)
        win.rowconfigure(1, minsize=70)
        win.columnconfigure(0, weight=1)

        frame1 = Frame(win, bg="#1a3f3a")
        frame1.grid(sticky=EW, padx=10)
        frame1.columnconfigure((0,1), weight=1)

        labels = [
            "TOTAL",
            "PEMBAYARAN"
        ]

        var_ : dict[str, IntVar] = {}

        for i, v in enumerate(labels):
            Label(frame1, font='consolas', width=10, border=5, relief=GROOVE, text=v, justify=LEFT, anchor=W)\
            .grid(column=0, row=i, sticky=NSEW)
            var_[v] = IntVar()
            e = Entry(frame1, font='consolas', width=10, border=5, relief=GROOVE, justify=CENTER, textvariable=var_[v],
                      validate="key", validatecommand=(validateNumbers, "%P"))
            e.grid(column=1, row=i, sticky=NSEW)
            e.focus_set()

        var_["TOTAL"].set(self.cart.displayHarga())
        var_["PEMBAYARAN"].set('')



        methods = ["QRIS", "CASH"]

        self.v = StringVar(value="CASH")

        for i in range(len(methods)):
            self.cash = Radiobutton(frame1, text=methods[i], variable=self.v, value=methods[i], height=3, indicatoron=0)
            self.cash.config(font='consolas')
            self.cash.grid(row=2, column=i, sticky=NSEW, pady=10)

        frame2 = Frame(win, bg="blue")
        frame2.grid(sticky=NSEW)
        frame2.rowconfigure(0, weight=1)
        frame2.columnconfigure((0, 1), weight=1)

        Button(frame2,font="consolas", text="CANCEL", command=win.destroy).grid(column=0, row=0, sticky=NSEW)
        Button(frame2,font="consolas", text="DONE", command=lambda: self.submitCheckout(var_, win)).grid(column=1, row=0, sticky=NSEW)

    def open_kembalian(self, change:int, data, total, tunai, method):
        win = topWin(self.root)
        win.rowconfigure((0,1,2), weight=1)
        win.columnconfigure(0, weight=1)

        Label(win, text=f"KEMBALIAN : {change:,}", font=("consolas", 15, "bold"), borderwidth=10, relief=RIDGE, bg="#00ADB5", foreground="black").grid(sticky=NSEW)

        Button(win, text="OK", command=win.destroy, font='consolas').grid(sticky=NSEW)
        Button(win, text="PRINT", command=lambda:printRecipt(data, change, total, tunai, method), font='consolas').grid(sticky=NSEW)

    def open_add_item(self):
        self.addWin = topWin(self.root,1200,500)
        self.addWin.rowconfigure(0, weight=1)
        self.addWin.rowconfigure(1, minsize=100)
        self.addWin.columnconfigure(0, weight=1)

        # --- Body Content ---

        frame1 = Frame(self.addWin, bg="blue")
        frame1.grid(sticky=NSEW)
        frame1.rowconfigure(0, weight=1)
        frame1.columnconfigure(0, weight=1)

        self.table = ItemList(frame1)
        self.table.load_data()
        self.table.tree.bind("<Double-3>", lambda event: self.quickAdd(self.table.tree))
        self.table.tree.bind("<KeyRelease-space>", lambda event: self.open_add_to_cart(self.table.tree))

        frame2 = Frame(self.addWin, bg="#1a3f3a", borderwidth=5, relief=RAISED)
        frame2.grid(sticky=NSEW)
        frame2.rowconfigure((0, 1, 2), weight=1, uniform="1")
        frame2.columnconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform="1")

        # --- Footer Content ---

        # Function #

        def clearSearchBar(event):
            self.searchBar.delete(0, END)
            self.searchBar.config(foreground='black', justify=LEFT)

        def addSearchBar(event):
            if self.searchBar.get() == "":
                self.searchBar.delete(0, END)
                self.searchBar.config(foreground='grey', justify=CENTER)
                self.searchBar.insert(0, "CARI NAMA BARANG")

        def submitSearchBar(event):
            namaBarang = self.searchBar.get().title()
            self.table.search(namaBarang)
        
        # Content #

        self.searchBar = Entry(frame2, font=('consolas', 17), foreground='grey', justify=CENTER, borderwidth=5, relief=GROOVE)
        self.searchBar.grid(column=0, row=0, columnspan=2, sticky=NSEW)
        self.searchBar.insert(0, "CARI NAMA BARANG")
        self.searchBar.bind('<FocusIn>', clearSearchBar)
        self.searchBar.bind('<FocusOut>', addSearchBar)
        self.searchBar.bind('<Return>', submitSearchBar)

        Button(frame2, text="Cari", command=lambda:submitSearchBar(None)).grid(column=2, row=0, rowspan=1, sticky=NSEW)
        Button(frame2, text="RELOAD", command=self.table.refresh).grid(column=4, row=0, rowspan=3, sticky=NSEW)
        Button(frame2, text="DONE", command=self.addWin.destroy).grid(column=5, row=0, rowspan=3, sticky=NSEW)

    def open_add_to_cart(self, item_table):
        row = item_table.selection()
        if not row:
            return
        produk = item_table.item(row[0], "values")[2]
        stokDasar = int(item_table.item(row[0], "values")[4])
        self.win = topWin(self.addWin, h=400)
        self.win.rowconfigure(0, weight=1)
        self.win.rowconfigure(1, minsize=70)
        self.win.columnconfigure(0, weight=1)

        frame = Frame(self.win, borderwidth=5, relief=RIDGE)
        frame.grid(sticky=EW, padx=10)
        frame.columnconfigure((0,1), weight=1, uniform='1')
        frame.rowconfigure((0,1,2,3), weight=1, uniform='1')

        konversi = getUnit(produk)
        satuan = [key for key in konversi]
        qty, hargaJual = getKonversi(produk, satuan[0])
        stok = getStokBarang(produk, stokDasar-qty)

        def onSelect(event):
            selectedValue = self.satuan.get()
            qty, hargaJual = getKonversi(produk, selectedValue, int(self.qty.get()))
            self.hargaJual.config(text=f" Rp {hargaJual*int(self.qty.get()):18} ")
            self.stok.config(text=getStokBarang(produk, stokDasar-qty))

        def qtyAdd(qty):
            ref = int(self.qty.get())
            QTY = ref + qty
            self.qty.delete(0, END)
            self.qty.insert(0, QTY)
            ref = int(self.qty.get())
            if ref <= 0:
                self.qty.delete(0, END)
                self.qty.insert(0, "1")
            onSelect(None)
            
        Label(frame, text="SATUAN :").grid(column=0, row=0, sticky=NSEW)
        self.satuan = Combobox(frame, values=satuan, state='readonly')
        self.satuan.set(satuan[0])
        self.satuan.grid(column=1, row=0, sticky=NSEW)

        self.satuan.bind("<<ComboboxSelected>>", onSelect)

        self.hargaJual = Label(frame, text=f" Rp {hargaJual:18} ", font=("Consolas", 20), anchor=W, relief=SUNKEN, borderwidth=5)
        self.hargaJual.grid(row=1, columnspan=2, column=0, sticky=EW)

        frame1 = Frame(frame, bg="blue", relief=RAISED, borderwidth=5)
        frame1.grid(row=2, columnspan=2, sticky=EW)
        frame1.columnconfigure((0,1,3,4), min=50)
        frame1.columnconfigure(2, weight=1)

        self.qty = Entry(frame1, font='consolas', width=10, border=5, relief=GROOVE, justify=CENTER)
        self.qty.grid(column=2, row=0, sticky=NSEW)
        self.qty.insert(0, '1')
        Button(frame1,command=lambda: qtyAdd(-10), font='consolas', text="-10").grid(column=0,row=0,sticky=NSEW)
        Button(frame1,command=lambda: qtyAdd(-1), font='consolas', text="-1").grid(column=1,row=0,sticky=NSEW)
        Button(frame1,command=lambda: qtyAdd(1), font='consolas', text="+1").grid(column=3,row=0,sticky=NSEW)
        Button(frame1,command=lambda: qtyAdd(10), font='consolas', text="+10").grid(column=4,row=0,sticky=NSEW)

        self.stok = Label(frame, text=f"{stok}", font=("Consolas", 14), anchor=CENTER, relief=SUNKEN, borderwidth=5)
        self.stok.grid(row=3, columnspan=2, column=0, sticky=NSEW)

        frame2 = Frame(self.win, bg="blue")
        frame2.grid(sticky=NSEW)
        frame2.rowconfigure(0, weight=1)
        frame2.columnconfigure((0, 1), weight=1)

        Button(frame2,font="consolas", text="CANCEL", command=lambda: [self.win.destroy(), self.addWin.grab_set()]).grid(column=0, row=0, sticky=NSEW)
        Button(frame2,font="consolas", text="DONE", command=lambda: [self.tambahBanyakBarang(self.table.tree), self.win.destroy(), self.addWin.grab_set()]).grid(column=1, row=0, sticky=NSEW)

    # ---------- ACTIONS ---------- #         

    def quickAdd(self, item_table):
        row = item_table.selection()
        if not row:
            return
        value = item_table.item(row[0], "values")
        try: qty, hargaJual = getKonversi(value[2], value[5])
        except ValueError: messagebox.showinfo(message=("SATUAN UMUM BELUM DICANTUMKAN")); return
        if qty < int(value[4]):
            addQty(value[1], f"{value[2]} - {value[5]}", value[5], qty)
            self.table.tree.item(item=value[1], values=(value[0], value[1], value[2], value[3], int(value[4])-qty, value[5]))
            self.cart.add(value, hargaJual, value[5])
            self.updateHarga()
        else: messagebox.showinfo(message=("STOK TIDAK CUKUP"))

    def tambahBanyakBarang(self, item_table):
        row = item_table.selection()
        if not row:
            return
        value = item_table.item(row[0], "values")
        qty1 = int(self.qty.get())
        satuan = self.satuan.get()
        qty, hargaJual = getKonversi(value[2], satuan, qty1)
        if qty <= int(value[4]):
            addQty(value[1], f"{value[2]} - {satuan}", satuan, qty)
            self.table.tree.item(item=value[1], values=(value[0], value[1], value[2], value[3], int(value[4])-qty, value[5]))
            self.cart.add(value, hargaJual, satuan, qty1)
            self.updateHarga()
        else:
            messagebox.showinfo(message=("STOK TIDAK CUKUP"))

    def hapusBarang(self, item_table):
        row = item_table.selection()
        if not row:
            return
        values = item_table.item(row[0], "values")
        qty = getKonversi(values[1],values[2])[0]
        delQty(f"{values[1]} - {values[2]}", qty)
        self.cart.delete(values)
        self.updateHarga()

    def clearTable(self):
        self.cart.clear()
        self.totalHarga.config(text=f"Rp {0:15,}")

    def updateHarga(self):
        self.totalHarga.config(text=f"Rp {self.cart.displayHarga():15,}")

    def submitCheckout(self, info:dict[str, StringVar], root:Toplevel):
        try: data = [v.get() for v in info.values()]
        except Exception as e: messagebox.showinfo(message=f"MASUKAN PEMBAYARAN\nError : {e}"); return
        method = self.v.get()
        if not method: return
        if data[1] >= data[0]:
            hargaBeli = checkout(self.cart.cart)
            total, change = penjualan(method, data[0], data[1], hargaBeli)
            addAset(method, total)

            self.totalHarga.config(text=f"Rp {0:15,}")
            root.destroy()
            self.open_kembalian(int(change), self.cart.cart, total, data[1], method)
            self.cart.clear()

        else: messagebox.showinfo(message="PEMBAYARAN KURANG")

    def open_Inventory(self):
        self.Inventory = Inventory()
        self.Inventory.root.mainloop()

    def open_LaporanAset(self):
        self.LaporanAset = LaporanAset()
        self.LaporanAset.root.mainloop()

# ====================== RUN PROGRAM ======================

if __name__ == "__main__":
    app = kasir()
    app.root.mainloop()