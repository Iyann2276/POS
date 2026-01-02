from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox

from style import setup_style
from initDatabase import init_db
from Modules.Base_module import ItemList2, UnitList, topWin
from Modules.Database_module import (getColumn, getKonversi, getCode, getUnit,
                                     delProduct, addProduct, editProduct,
                                     addUnit, deleteUnit, restockProduct,
                                     subtractProduct)

init_db()

class Inventory:
    def __init__(self):
        if __name__ == "__main__": self.root = Tk()
        else: self.root = Toplevel()
        self.root.attributes('-fullscreen', True)
        setup_style(self.root)

    # ---------- UI ---------- #
        main = Frame(self.root, bg="#faadbb")
        main.pack(side=TOP, expand=True, fill=BOTH)
        main.columnconfigure(0, weight=1)
        main.rowconfigure(0, weight=1)
        main.rowconfigure(1, minsize=180)

    # ---------- Body ---------- #
        body = Frame(main, borderwidth=5, relief=SUNKEN)
        body.grid(row=0, column=0, sticky=NSEW)
        body.columnconfigure(0, weight=1)
        body.rowconfigure(0, weight=1)
        self.inv = ItemList2(body)
        self.inv.load_data()
        self.inv.tree.bind("<Double-1>", lambda event: self.open_opsi_product())
        
    # ---------- Footer ---------- #
        footer = Frame(main, bg="#1a3f3a", borderwidth=5, relief=RAISED)
        footer.grid(row=1, column=0, sticky=NSEW)

        Button(footer, text="TAMBAH PRODUK", command=self.open_select_category).grid()
        Button(footer, text="LOAD", command=self.inv.load_data).grid()
        Button(footer, text="CLEAR", command=self.inv.clear).grid()
        Button(footer, text="CLOSE", command=lambda:self.root.destroy()).grid()

    # ---------- Windows ---------- #
    def open_select_category(self):
        win = topWin(self.root)
        win.columnconfigure((0,2), minsize=10)
        win.columnconfigure(1, weight=1)
        win.rowconfigure(0, weight=1)
        win.rowconfigure(1, minsize=60)

        f1 = Frame(win, pady=20, borderwidth=5, relief=SUNKEN)
        f1.grid(row=0, column=1)
        f2 = Frame(win, bg="#1a3f3a", pady=20)
        f2.grid(row=1, column=1, sticky=NSEW)
        f2.columnconfigure((0,1), weight=1)
        f2.rowconfigure(0, weight=1)

        data = getColumn('KATEGORI')
        kategori = StringVar()

        Label(f1, text=f"KATEGORI  :", font='consolas', anchor=W, justify=LEFT).grid(row=0, column=0, sticky=EW)
        self.combobox1 = Combobox(f1, textvariable=kategori, values=data, font='consolas', width=10)
        self.combobox1.grid(row=0, column=1, sticky=NSEW)

        self.combobox1.bind("<<ComboboxSelected>>",lambda e: f2.focus())


        Button(f2, text="CANCEL", font='consolas', command=win.destroy).grid(column=0, row=0 ,sticky=NSEW)
        Button(f2, text="OK", font='consolas',
               command=lambda:[self.open_add_product(), win.destroy()]if self.combobox1.get() != ""
               else messagebox.showinfo(message="KATEGORI HARUS DI ISI!!!")).grid(column=1, row=0 ,sticky=NSEW)        

    def open_add_product(self):
        self.addProductWin = topWin(self.root, h=400)
        self.addProductWin.columnconfigure((0,2), minsize=10)
        self.addProductWin.columnconfigure(1, weight=1)
        self.addProductWin.rowconfigure(0, weight=1)
        self.addProductWin.rowconfigure(1, minsize=60)

        f1 = Frame(self.addProductWin, borderwidth=5, relief=SUNKEN)
        f1.grid(row=0, column=1)
        f2 = Frame(self.addProductWin, bg="#1a3f3a", pady=20)
        f2.grid(row=1, column=1, sticky=NSEW)
        f2.columnconfigure((0,1), weight=1, uniform='1')
        f2.rowconfigure(0, weight=1)

        labels = [f"KATEGORI PRODUK : ",
                  f"KODE PRODUK     : ",
                  f"NAMA PRODUK     : ",
                  f"SATUAN STOK     : "]
        
        var_: dict[str, StringVar] = {}
        
        for i, v in enumerate(labels):
            Label(f1, text=f"{v}", font='consolas', anchor=W, justify=LEFT).grid(row=i, column=0, sticky=EW)
            var_[v] = StringVar()
            Entry(f1, font='consolas', width=10, border=5, relief=GROOVE, textvariable=var_[v]).grid(row=i, column=1)

        var_["KATEGORI PRODUK : "].set(self.combobox1.get())
        var_["KODE PRODUK     : "].set(getCode(self.combobox1.get()))

        Button(f2, text="CANCEL", font='consolas', command=self.addProductWin.destroy).grid(column=0, row=0 ,sticky=NSEW)
        Button(f2, text="NEXT", font='consolas', command=lambda:self.open_add_unit(var_)).grid(column=1, row=0 ,sticky=NSEW)

    def open_add_unit(self, datas:dict[str, StringVar]):
        def onlyNumbers(p:str):
            if p.isdigit() or p == '':
                return True
            else:
                self.root.bell()
                return False
        
        validateNumbers = self.root.register(onlyNumbers)

        win = topWin(self.addProductWin, 600, 400)
        win.columnconfigure(1, weight=1)
        win.rowconfigure(0, weight=1)
        win.rowconfigure(1, minsize=60)

        f1 = Frame(win, borderwidth=5, relief=SUNKEN)
        f1.grid(row=0, column=1, sticky=NSEW)
        f1.rowconfigure(0, minsize=150)
        f1.rowconfigure(1, weight=1)
        f1.columnconfigure((0,1), weight=1, uniform='1')
        f2 = Frame(win, bg="#1a3f3a", pady=20)
        f2.grid(row=1, column=1, sticky=NSEW)
        f2.columnconfigure((0,1), weight=1, uniform='1')
        f2.rowconfigure(0, weight=1)

        treeFrame = Frame(f1, borderwidth=5, relief=SUNKEN)
        treeFrame.grid(column=0,row=0, columnspan=2, sticky=NSEW)
        treeFrame.columnconfigure(0, weight=1)
        treeFrame.rowconfigure(0, weight=1)
        treeFrame.grid_propagate(False)

        formFrame = Frame(f1, borderwidth=5, relief=GROOVE)
        formFrame.grid(column=0,row=1, columnspan=2, sticky=NSEW)
        formFrame.columnconfigure((0,1,2), weight=1, uniform='1')
        formFrame.rowconfigure((0,1,2), weight=1, uniform='1')
        formFrame.grid_propagate(False)

        self.tree = UnitList(treeFrame)

        labels = [f"SATUAN          : ",
                  f"KONVERSI        : ",
                  f"HARGA JUAL      : ",
                  f"HARGA GROSIR    : "]
        
        var_: dict[str, StringVar] = {}
        
        for i, v in enumerate(labels):
            Label(formFrame, text=f"{v}", font='consolas', anchor=W, justify=LEFT).grid(row=i, column=0, sticky=EW)
            var_[v] = StringVar()
            if i != 0:
                Entry(formFrame, font='consolas', width=10, border=5, relief=GROOVE, textvariable=var_[v],
                      validate="key", validatecommand=(validateNumbers, "%P")).grid(row=i, column=1)
                continue
            Entry(formFrame, font='consolas', width=10, border=5, relief=GROOVE, textvariable=var_[v]).grid(row=i, column=1)

        var_["SATUAN          : "].set(datas["SATUAN STOK     : "].get().title())

        Button(formFrame, text="ADD", font='consolas', command=lambda:self.tree.add(var_, datas["NAMA PRODUK     : "].get(), datas["KODE PRODUK     : "].get()), borderwidth=10, relief=RAISED).grid(column=2, row=0, rowspan=2, sticky=NSEW)
        Button(formFrame, text="DEL", font='consolas', command=lambda:self.tree.delete(), borderwidth=10, relief=RAISED).grid(column=2, row=2, rowspan=2, sticky=NSEW)
        Button(f2, text="BACK", font='consolas', command=lambda:[win.destroy(), self.addProductWin.grab_set()]).grid(column=0, row=0 ,sticky=NSEW)
        Button(f2, text="OK", font='consolas', command=lambda:self.addSubmit(datas)).grid(column=1, row=0 ,sticky=NSEW)

    def open_opsi_product(self):
        def hapus():
            if messagebox.askokcancel("KONFIRMASI", "Apakah anda yakin?"):
                self.opsiProductWin.destroy()
                delProduct(val[1])
                self.inv.refresh()
                return
            else: pass
        row = self.inv.tree.selection()
        if not row:
            return
        val = self.inv.tree.item(row[0], "values")
        self.opsiProductWin = topWin(self.root, 600, 400)
        self.opsiProductWin.columnconfigure((0,2), minsize=10)
        self.opsiProductWin.columnconfigure(1, weight=1)
        self.opsiProductWin.rowconfigure(0, weight=1)
        self.opsiProductWin.rowconfigure(1, minsize=60)

        f1 = Frame(self.opsiProductWin, bg="#1a3f3a")
        f1.grid(row=0, column=1, sticky=NSEW)
        f1.rowconfigure((0,1), weight=1, uniform='1')
        f1.columnconfigure((0,1,2,3), weight=1, uniform='1')
        f2 = Frame(self.opsiProductWin, bg="#1a3f3a", pady=20)
        f2.grid(row=1, column=1, sticky=NSEW)
        f2.columnconfigure((0,1), weight=1)
        f2.rowconfigure(0, weight=1)

        Button(f1, text="RESTOK", font='consolas', command=lambda: self.open_restock_product(val)).grid(column=0, row=0 ,sticky=NSEW, pady=(20, 10))
        Button(f1, text="HILANG/\nRUSAK", font='consolas', command=lambda: self.open_lost_product(val)).grid(column=1, row=0 ,sticky=NSEW, pady=(20, 10))
        Button(f1, text="TAMBAH\nSATUAN", font='consolas', command=lambda: self.open_edit_unit(val)).grid(column=2, row=0 ,sticky=NSEW, pady=(20, 10))
        Button(f1, text="EDIT", font='consolas', command=lambda: self.open_edit_product(val)).grid(column=3, row=0 ,sticky=NSEW, pady=(20, 10))
        Button(f1, text="HAPUS", font='consolas', command=lambda: hapus()).grid(column=0, row=1, columnspan=4, sticky=NSEW, pady=10)
        Button(f2, text="CANCEL", font='consolas', command=self.opsiProductWin.destroy).grid(column=0, row=0 ,sticky=NSEW, columnspan=2)

    def open_edit_product(self, data:list):
        self.editProductWin = topWin(self.root, 600, 400)
        self.editProductWin.columnconfigure((0,2), minsize=10)
        self.editProductWin.columnconfigure(1, weight=1)
        self.editProductWin.rowconfigure(0, weight=1)
        self.editProductWin.rowconfigure(1, minsize=60)

        f1 = Frame(self.editProductWin, pady=20, borderwidth=5, relief=SUNKEN)
        f1.grid(row=0, column=1)
        f2 = Frame(self.editProductWin, bg="#1a3f3a", pady=20)
        f2.grid(row=1, column=1, sticky=NSEW)
        f2.columnconfigure((0,1), weight=1)
        f2.rowconfigure(0, weight=1)

        labels = [f"KATEGORI PRODUK : ",
                  f"KODE PRODUK     : ",
                  f"NAMA PRODUK     : ",
                  f"SATUAN STOK     : ",
                  f"SATUAN UMUM     : ",]
        
        var_: dict[str, StringVar] = {}
        satuan = [key for key in getUnit(data[2])]
        
        for i, v in enumerate(labels):
            Label(f1, text=f"{v}", font='consolas', anchor=W, justify=LEFT).grid(row=i, column=0, sticky=EW)
            if i == 4:
                self.satuanUmum = Combobox(f1, values=satuan, state="readonly", font='consolas', width=10)
                self.satuanUmum.grid(row=i, column=1)
                continue
            var_[v] = StringVar()
            Entry(f1, font='consolas', width=10, border=5, relief=GROOVE, textvariable=var_[v], state="readonly").grid(row=i, column=1)

        var_["KATEGORI PRODUK : "].set(data[0])
        var_["KODE PRODUK     : "].set(data[1])
        var_["NAMA PRODUK     : "].set(data[2])
        var_["SATUAN STOK     : "].set(data[3])

        Button(f2, text="CANCEL", font='consolas', command=self.editProductWin.destroy).grid(column=0, row=0 ,sticky=NSEW)
        Button(f2, text="OK", font='consolas', command=lambda: self.editSubmit(var_)).grid(column=1, row=0 ,sticky=NSEW)

    def open_edit_unit(self, data:list):
        def onlyNumbers(p:str):
            if p.isdigit() or p == '':
                return True
            else:
                self.root.bell()
                return False
        
        validateNumbers = self.root.register(onlyNumbers)

        win = topWin(self.opsiProductWin, 600, 400)
        win.columnconfigure(1, weight=1)
        win.rowconfigure(0, weight=1)
        win.rowconfigure(1, minsize=60)

        f1 = Frame(win, borderwidth=5, relief=SUNKEN)
        f1.grid(row=0, column=1, sticky=NSEW)
        f1.rowconfigure(0, minsize=150)
        f1.rowconfigure(1, weight=1)
        f1.columnconfigure((0,1), weight=1, uniform='1')
        f2 = Frame(win, bg="#1a3f3a", pady=20)
        f2.grid(row=1, column=1, sticky=NSEW)
        f2.columnconfigure((0,1), weight=1, uniform='1')
        f2.rowconfigure(0, weight=1)

        treeFrame = Frame(f1, borderwidth=5, relief=SUNKEN)
        treeFrame.grid(column=0,row=0, columnspan=2, sticky=NSEW)
        treeFrame.columnconfigure(0, weight=1)
        treeFrame.rowconfigure(0, weight=1)
        treeFrame.grid_propagate(False)

        formFrame = Frame(f1, borderwidth=5, relief=GROOVE)
        formFrame.grid(column=0,row=1, columnspan=2, sticky=NSEW)
        formFrame.columnconfigure((0,1,2), weight=1, uniform='1')
        formFrame.rowconfigure((0,1,2), weight=1, uniform='1')
        formFrame.grid_propagate(False)

        self.tree = UnitList(treeFrame)
        self.tree.load_data(data[2])

        labels = [f"SATUAN          : ",
                  f"KONVERSI        : ",
                  f"HARGA JUAL      : ",
                  f"HARGA GROSIR    : "]
        
        var_: dict[str, StringVar] = {}
        
        for i, v in enumerate(labels):
            Label(formFrame, text=f"{v}", font='consolas', anchor=W, justify=LEFT).grid(row=i, column=0, sticky=EW)
            var_[v] = StringVar()
            if i != 0:
                Entry(formFrame, font='consolas', width=10, border=5, relief=GROOVE, textvariable=var_[v],
                      validate="key", validatecommand=(validateNumbers, "%P")).grid(row=i, column=1)
                continue
            Entry(formFrame, font='consolas', width=10, border=5, relief=GROOVE, textvariable=var_[v]).grid(row=i, column=1)

        Button(formFrame, text="ADD", font='consolas', command=lambda:self.submitAddUnit(var_, data), borderwidth=10, relief=RAISED).grid(column=2, row=0, rowspan=2, sticky=NSEW)
        Button(formFrame, text="DEL", font='consolas', command=lambda:self.submitDeleteUnit(), borderwidth=10, relief=RAISED).grid(column=2, row=2, rowspan=2, sticky=NSEW)
        Button(f2, text="DONE", font='consolas', command=lambda:win.destroy()).grid(column=0, row=0, columnspan=2 ,sticky=NSEW)

    def open_restock_product(self, data:list):
        def onlyNumbers(p:str):
            if p.isdigit() or p == '':
                return True
            else:
                self.root.bell()
                return False
        
        validateNumbers = self.root.register(onlyNumbers)

        win = topWin(self.opsiProductWin, 600, 400)
        win.columnconfigure((0,2), minsize=10)
        win.columnconfigure(1, weight=1)
        win.rowconfigure(0, weight=1)
        win.rowconfigure(1, minsize=60)

        f1 = Frame(win, pady=20, borderwidth=5, relief=SUNKEN)
        f1.grid(row=0, column=1)
        f2 = Frame(win, bg="#1a3f3a", pady=20)
        f2.grid(row=1, column=1, sticky=NSEW)
        f2.columnconfigure((0,1), weight=1)
        f2.rowconfigure(0, weight=1)

        labels = [f"KATEGORI PRODUK : ",
                  f"KODE PRODUK     : ",
                  f"NAMA PRODUK     : ",
                  f"SATUAN STOK     : ",
                  f"SATUAN RESTOCK  : ",
                  f"JUMLAH RESTOCK  : ",
                  f"HARGA BELI      : ",]
        
        var_: dict[str, StringVar] = {}
        satuan = [key for key in getUnit(data[2])]
        
        for i, v in enumerate(labels):
            Label(f1, text=f"{v}", font='consolas', anchor=W, justify=LEFT).grid(row=i, column=0, sticky=EW)
            if i == 4:
                self.satuanRestock = Combobox(f1, values=satuan, state="readonly", font='consolas', width=10)
                self.satuanRestock.grid(row=i, column=1)
                self.satuanRestock.set(satuan[0])
                continue
            var_[v] = StringVar()
            if i == 5 or i == 6:
                Entry(f1, font='consolas', width=10, border=5, relief=GROOVE, textvariable=var_[v],
                      validate="key", validatecommand=(validateNumbers, "%P")).grid(row=i, column=1)
                continue
            Entry(f1, font='consolas', width=10, border=5, relief=GROOVE, textvariable=var_[v], state="readonly").grid(row=i, column=1)

        var_["KATEGORI PRODUK : "].set(data[0])
        var_["KODE PRODUK     : "].set(data[1])
        var_["NAMA PRODUK     : "].set(data[2])
        var_["SATUAN STOK     : "].set(data[3])

        Button(f2, text="CANCEL", font='consolas', command=win.destroy).grid(column=0, row=0 ,sticky=NSEW)
        Button(f2, text="OK", font='consolas', command=lambda: self.restockSubmit(var_)).grid(column=1, row=0 ,sticky=NSEW)
    
    def open_lost_product(self, data:list):
        def onlyNumbers(p:str):
            if p.isdigit() or p == '':
                return True
            else:
                self.root.bell()
                return False
        
        validateNumbers = self.root.register(onlyNumbers)

        win = topWin(self.opsiProductWin, 600, 400)
        win.columnconfigure((0,2), minsize=10)
        win.columnconfigure(1, weight=1)
        win.rowconfigure(0, weight=1)
        win.rowconfigure(1, minsize=60)

        f1 = Frame(win, pady=20, borderwidth=5, relief=SUNKEN)
        f1.grid(row=0, column=1)
        f2 = Frame(win, bg="#1a3f3a", pady=20)
        f2.grid(row=1, column=1, sticky=NSEW)
        f2.columnconfigure((0,1), weight=1)
        f2.rowconfigure(0, weight=1)

        labels = [f"KATEGORI PRODUK : ",
                  f"KODE PRODUK     : ",
                  f"NAMA PRODUK     : ",
                  f"SATUAN STOK     : ",
                  f"SATUAN HILANG   : ",
                  f"JUMLAH HILANG   : ",]
        
        var_: dict[str, StringVar] = {}
        satuan = [key for key in getUnit(data[2])]
        
        for i, v in enumerate(labels):
            Label(f1, text=f"{v}", font='consolas', anchor=W, justify=LEFT).grid(row=i, column=0, sticky=EW)
            if i == 4:
                self.satuanHilang = Combobox(f1, values=satuan, state="readonly", font='consolas', width=10)
                self.satuanHilang.grid(row=i, column=1)
                self.satuanHilang.set(satuan[0])
                continue
            var_[v] = StringVar()
            if i == 5:
                Entry(f1, font='consolas', width=10, border=5, relief=GROOVE, textvariable=var_[v],
                      validate="key", validatecommand=(validateNumbers, "%P")).grid(row=i, column=1)
                continue
            Entry(f1, font='consolas', width=10, border=5, relief=GROOVE, textvariable=var_[v], state="readonly").grid(row=i, column=1)

        var_["KATEGORI PRODUK : "].set(data[0])
        var_["KODE PRODUK     : "].set(data[1])
        var_["NAMA PRODUK     : "].set(data[2])
        var_["SATUAN STOK     : "].set(data[3])

        Button(f2, text="CANCEL", font='consolas', command=win.destroy).grid(column=0, row=0 ,sticky=NSEW)
        Button(f2, text="OK", font='consolas', command=lambda: self.lostSubmit(var_)).grid(column=1, row=0 ,sticky=NSEW)

    # ---------- Action ---------- #
    def addSubmit(self, produk:dict[str, StringVar]):
        data = {k:v.get() for k,v in produk.items()}
        barang = []
        units = self.tree.list
        try:
            for i, v in enumerate(data.values()):
                if i == 0 or i == 1:
                    barang.append(v.upper())
                    continue
                barang.append(v.title())
        except Exception as e:
            print(e)
            messagebox.showerror(
                "VALUE ERROR",
                "INPUT TIDAK VALID\nSEMUA DATA HARUS TERISI\nDAN HARGA ATAU STOK HANYA BOLEH ANGKA!!!",
            )
            return
        
        addProduct(barang, units)
        self.addProductWin.destroy()
        self.inv.refresh()

    def editSubmit(self, produk:dict[str, StringVar]):
        data = {k:v.get() for k,v in produk.items()}

        editProduct(data["KODE PRODUK     : "], self.satuanUmum.get())
        self.editProductWin.destroy()
        self.opsiProductWin.destroy()
        self.inv.refresh()

    def submitAddUnit(self, datas:dict[str, StringVar], produk:list):
        data = {k:v.get() for k,v in datas.items()}
        barang = []

        for v in data.values():
            barang.append(v.title())
        barang.insert(0, produk[1])
        barang.insert(0, produk[2])

        satuan = [key for key in getUnit(produk[2])]
        if barang[2] in satuan:
            return

        addUnit(tuple(barang))
        self.tree.clear()
        self.tree.load_data(produk[2])

    def submitDeleteUnit(self):
        row = self.tree.tree.selection()
        if not row:
            return
        value = self.tree.tree.item(row[0], "values")
        for i in self.tree.list:
            if i[2] == value[0]:
                deleteUnit(i[0], i[2])
                self.tree.tree.delete(i[2])
                self.tree.list.remove(i)

    def restockSubmit(self, produk:dict[str, StringVar]):
        row = self.inv.tree.selection()
        if not row:
            return
        data = [v.get() for v in produk.values()]
        data.insert(4, self.satuanRestock.get())
        
        for d in data:
            if d == "":
                messagebox.showerror(
                "VALUE ERROR",
                "INPUT TIDAK VALID\nSEMUA DATA HARUS TERISI!!!",)
                return

        konversi = getKonversi(data[2], data[4], data[5] if data[5] != '' else 1)[0]
        if int(data[6]) <=0:
            messagebox.showerror(message="BILANGAN TIDAK BOLEH KURANG DARI 0 !!!")
            return
        if int(data[5]) <= 0:
            konversi = 0
        
        satuan = getUnit(data[2])
        stok = int(self.inv.tree.item(row[0], "values")[4])
        aset = int(((stok + konversi) / satuan[data[4]])) * int(data[6])
        restockProduct(data[1], data[4], data[6], konversi, aset)
        self.inv.refresh()
        self.opsiProductWin.destroy()

    def lostSubmit(self, produk:dict[str, StringVar]):
        row = self.inv.tree.selection()
        if not row:
            return
        data = [v.get() for v in produk.values()]
        data.insert(4, self.satuanHilang.get())
        
        for d in data:
            if d == "":
                messagebox.showerror(
                "VALUE ERROR",
                "INPUT TIDAK VALID\nSEMUA DATA HARUS TERISI!!!",)
                return
            
        if int(data[5]) <= 0:
            messagebox.showerror(message="BILANGAN TIDAK BOLEH KURANG DARI 0 !!!")
            return

        konversi = getKonversi(data[2], data[4], data[5] if data[5] != '' else 1)[0]
        stok = int(self.inv.tree.item(row[0], "values")[4])

        if stok < konversi:
            messagebox.showerror(message="STOK TIDAK CUKUP !!!")
            return

        satuan = getUnit(data[2])
        harga = str(self.inv.tree.item(row[0], "values")[6])
        harga = int("".join(v for v in harga if v.isdigit()))
        aset = int(((stok - konversi) / satuan[data[4]])) * int(harga)
        subtractProduct(data[1], konversi, aset)
        self.inv.refresh()
        self.opsiProductWin.destroy()

if __name__ == "__main__":
    app = Inventory()
    app.root.mainloop()