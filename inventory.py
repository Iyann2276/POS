from tkinter import *
from tkinter import messagebox

from models.db import addBarang, editBarang, hapusBarang,init_db
from style import setup_style
from models.baseModels import ItemList2

init_db()

class Inventory:
    def __init__(self):
        self.root = Tk()
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
        self.inv.tree.bind("<Double-1>", lambda event: self.open_opsi_product(self.inv.tree))
        
    # ---------- Footer ---------- #
        footer = Frame(main, bg="#1a3f3a", borderwidth=5, relief=RAISED)
        footer.grid(row=1, column=0, sticky=NSEW)

        Button(footer, text="TAMBAH PRODUK", command=self.open_add_product).grid()
        Button(footer, text="LOAD", command=self.inv.load_data).grid()
        Button(footer, text="CLEAR", command=self.inv.clear).grid()
        Button(footer, text="CLOSE", command=lambda:self.root.destroy()).grid()

    # ---------- Windows ---------- #
    def open_add_product(self):
        self.win = Toplevel(self.root, relief=RIDGE, borderwidth=10, bg='#1a3f3a')
        w = 600
        h = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width/2) - (w/2)
        y = (screen_height/2) - (h/2)
        self.win.geometry("%dx%d+%d+%d" % (600, 400, x, y))
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", False)
        self.win.grab_set()
        self.win.columnconfigure((0,2), minsize=10)
        self.win.columnconfigure(1, weight=1)
        self.win.rowconfigure(0, weight=1)
        self.win.rowconfigure(1, minsize=60)

        self.f1 = Frame(self.win, pady=20, borderwidth=5, relief=SUNKEN)
        self.f1.grid(row=0, column=1)
        self.f2 = Frame(self.win, bg="#1a3f3a", pady=20)
        self.f2.grid(row=1, column=1, sticky=NSEW)
        self.f2.columnconfigure((0,1), weight=1)
        self.f2.rowconfigure(0, weight=1)

        labels = [f"KODE PRODUK     : ",
                  f"KATEGORI PRODUK : ",
                  f"NAMA PRODUK     : ",
                  f"SATUAN PRODUK   : ",
                  f"HARGA PRODUK    : ",
                  f"STOK PRODUK     : ",
                  f"HARGA BELI      : ",]
        
        for i, v in enumerate(labels):
            Label(self.f1, text=f"{v}", font='consolas', anchor=W, justify=LEFT).grid(row=i, column=0, sticky=EW)

        self.kodeProduk = Entry(self.f1, font='consolas', width=10, border=5, relief=GROOVE)
        self.kodeProduk.grid(column=1, row=0)
        self.kategoriProduk = Entry(self.f1, font='consolas', width=10, border=5, relief=GROOVE)
        self.kategoriProduk.grid(column=1, row=1)
        self.namaProduk = Entry(self.f1, font='consolas', width=10, border=5, relief=GROOVE)
        self.namaProduk.grid(column=1, row=2)
        self.satuanProduk = Entry(self.f1, font='consolas', width=10, border=5, relief=GROOVE)
        self.satuanProduk.grid(column=1, row=3)
        self.hargaProduk = Entry(self.f1, font='consolas', width=10, border=5, relief=GROOVE)
        self.hargaProduk.grid(column=1, row=4)
        self.stokProduk = Entry(self.f1, font='consolas', width=10, border=5, relief=GROOVE)
        self.stokProduk.grid(column=1, row=5)
        self.hargaBeliProduk = Entry(self.f1, font='consolas', width=10, border=5, relief=GROOVE)
        self.hargaBeliProduk.grid(column=1, row=6)

        Button(self.f2, text="CANCEL", font='consolas', command=self.win.destroy).grid(column=0, row=0 ,sticky=NSEW)
        Button(self.f2, text="OK", font='consolas', command=self.addSubmit).grid(column=1, row=0 ,sticky=NSEW)

    def open_edit_product(self):
        self.win = Toplevel(self.root, relief=RIDGE, borderwidth=10, bg='#1a3f3a')
        w = 600
        h = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width/2) - (w/2)
        y = (screen_height/2) - (h/2)
        self.win.geometry("%dx%d+%d+%d" % (600, 400, x, y))
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", False)
        self.win.grab_set()
        self.win.columnconfigure((0,2), minsize=10)
        self.win.columnconfigure(1, weight=1)
        self.win.rowconfigure(0, weight=1)
        self.win.rowconfigure(1, minsize=60)

        self.f1 = Frame(self.win, pady=20, borderwidth=5, relief=SUNKEN)
        self.f1.grid(row=0, column=1)
        self.f2 = Frame(self.win, bg="#1a3f3a", pady=20)
        self.f2.grid(row=1, column=1, sticky=NSEW)
        self.f2.columnconfigure((0,1), weight=1)
        self.f2.rowconfigure(0, weight=1)

        labels = [f"KODE PRODUK     : ",
                  f"KATEGORI PRODUK : ",
                  f"NAMA PRODUK     : ",
                  f"SATUAN PRODUK   : ",
                  f"HARGA PRODUK    : ",
                  f"STOK PRODUK     : ",
                  f"HARGA BELI      : ",]
        
        for i, v in enumerate(labels):
            Label(self.f1, text=f"{v}", font='consolas', anchor=W, justify=LEFT).grid(row=i, column=0, sticky=EW)

        self.kodeProduk = Label(self.f1, font='consolas', width=10, border=5, relief=GROOVE, text=self.val[1], justify=LEFT, anchor=W)
        self.kodeProduk.grid(column=1, row=0)
        self.kategoriProduk = Label(self.f1, font='consolas', width=10, border=5, relief=GROOVE, text=self.val[0], justify=LEFT, anchor=W)
        self.kategoriProduk.grid(column=1, row=1)
        self.namaProduk = Label(self.f1, font='consolas', width=10, border=5, relief=GROOVE, text=self.val[2], justify=LEFT, anchor=W)
        self.namaProduk.grid(column=1, row=2)
        self.satuanProduk = Label(self.f1, font='consolas', width=10, border=5, relief=GROOVE, text=self.val[3], justify=LEFT, anchor=W)
        self.satuanProduk.grid(column=1, row=3)
        self.hargaProduk = Entry(self.f1, font='consolas', width=10, border=5, relief=GROOVE)
        self.hargaProduk.grid(column=1, row=4)
        self.hargaProduk.insert(0, self.val[5])
        self.stokProduk = Entry(self.f1, font='consolas', width=10, border=5, relief=GROOVE)
        self.stokProduk.grid(column=1, row=5)
        self.stokProduk.insert(0, self.val[4])
        self.hargaBeli = Entry(self.f1, font='consolas', width=10, border=5, relief=GROOVE)
        self.hargaBeli.grid(column=1, row=6)
        self.hargaBeli.insert(0, self.val[6])

        Button(self.f2, text="CANCEL", font='consolas', command=self.win.destroy).grid(column=0, row=0 ,sticky=NSEW)
        Button(self.f2, text="OK", font='consolas', command=self.editSubmit).grid(column=1, row=0 ,sticky=NSEW)

    def open_opsi_product(self, item_table):
        row = item_table.selection()
        if not row:
            return
        self.val = item_table.item(row[0], "values")
        # value tuple from treeview: (KATEGORI, ID, NAMA, SATUAN, STOK, HARGA)
        self.win = Toplevel(self.root, relief=RIDGE, borderwidth=10, bg='#1a3f3a')
        w = 600
        h = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width/2) - (w/2)
        y = (screen_height/2) - (h/2)
        self.win.geometry("%dx%d+%d+%d" % (600, 400, x, y))
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", False)
        self.win.grab_set()
        self.win.columnconfigure((0,2), minsize=10)
        self.win.columnconfigure(1, weight=1)
        self.win.rowconfigure(0, weight=1)
        self.win.rowconfigure(1, minsize=60)

        self.f1 = Frame(self.win, bg="#1a3f3a")
        self.f1.grid(row=0, column=1, sticky=NSEW)
        self.f1.rowconfigure((0,1), weight=1)
        self.f1.columnconfigure(0, weight=1)
        self.f2 = Frame(self.win, bg="#1a3f3a", pady=20)
        self.f2.grid(row=1, column=1, sticky=NSEW)
        self.f2.columnconfigure((0,1), weight=1)
        self.f2.rowconfigure(0, weight=1)

        Button(self.f1, text="EDIT", font='consolas', command=lambda: self.open_edit_product()).grid(column=0, row=0 ,sticky=NSEW, pady=(20, 10))
        Button(self.f1, text="HAPUS", font='consolas', command=lambda: [hapusBarang(self.val[1]), self.inv.refresh(), self.win.destroy()]).grid(column=0, row=1 ,sticky=NSEW, pady=10)
        Button(self.f2, text="CANCEL", font='consolas', command=self.win.destroy).grid(column=0, row=0 ,sticky=NSEW, columnspan=2)

    # ---------- Action ---------- #
    def addSubmit(self):
        try:
            values = [
                self.kodeProduk.get().upper(),
                self.kategoriProduk.get().upper(),
                self.namaProduk.get().title(),
                self.satuanProduk.get().capitalize(),
                int(self.hargaProduk.get()),
                int(self.stokProduk.get()),
                int(self.hargaBeliProduk.get())
            ]
        except ValueError:
            messagebox.showerror(
                "VALUE ERROR",
                "INPUT TIDAK VALID\nSEMUA DATA HARUS TERISI\nDAN HARGA ATAU STOK HANYA BOLEH ANGKA!!!",
            )
            return

        # Validate text fields are not empty
        if any(not str(v).strip() for v in values[:4]):
            messagebox.showerror(
                "VALUE ERROR",
                "INPUT TIDAK VALID\nHARGA ATAU STOK HANYA BOLEH ANGKA DAN TIDAK BOLEH KOSONG!!!",
            )
            return

        addBarang(values[0], values[1], values[2], values[3], values[4], values[5], values[6])
        self.win.destroy()
        self.inv.refresh()

    def editSubmit(self):
        try:
            values = [
                self.kodeProduk.cget("text").upper(),
                self.kategoriProduk.cget("text").upper(),
                self.namaProduk.cget("text").title(),
                self.satuanProduk.cget("text").capitalize(),
                int(self.hargaProduk.get()),
                int(self.stokProduk.get()),
            ]
        except ValueError:
            messagebox.showerror(
                "VALUE ERROR",
                "INPUT TIDAK VALID\nSEMUA DATA HARUS TERISI\nDAN HARGA ATAU STOK HANYA BOLEH ANGKA!!!",
            )
            return

        if any(not str(v).strip() for v in values[:4]):
            messagebox.showerror(
                "VALUE ERROR",
                "INPUT TIDAK VALID\nHARGA ATAU STOK HANYA BOLEH ANGKA DAN TIDAK BOLEH KOSONG!!!",
            )
            return

        editBarang(values[0], values[4], values[5])
        self.win.destroy()
        self.inv.refresh()

if __name__ == "__main__":
    app = Inventory()
    app.root.mainloop()