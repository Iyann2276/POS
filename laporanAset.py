from tkinter import *

from Modules.Base_module import Laporan
from Modules.Database_module import getAset, getProfit
from style import setup_style

class LaporanAset():
    def __init__(self):
        if __name__ == "__main__": self.root = Tk()
        else: self.root = Toplevel()
        self.root.attributes('-fullscreen', True)
        setup_style(self.root)

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

        laporan = Laporan(body)
        laporan.load_data()

    # ---------- Footer ---------- #    
        footer = Frame(main, bg="#1a3f3a", borderwidth=5, relief=RAISED)
        footer.grid(row=1, column=0, sticky=NSEW)
        footer.columnconfigure((0,1,2,3,4,5), weight=1, uniform="1")
        footer.rowconfigure((0,1,2,3), weight=1, uniform="1")
        footer.grid_propagate(False)

        f1 = Frame(footer, borderwidth=5, relief=RIDGE)
        f1.grid(row = 0, column = 0, sticky = NSEW, rowspan=4)
        f2 = Frame(footer, borderwidth=5, relief=RIDGE)
        f2.grid(row = 0, column = 1, sticky = NSEW, rowspan=4)
        f3 = Frame(footer, borderwidth=5, relief=RIDGE)
        f3.grid(row = 0, column = 2, sticky = NSEW, rowspan=4, columnspan=2)
        f5 = Frame(footer, borderwidth=5, relief=RIDGE)
        f5.grid(row = 0, column = 4, sticky = NSEW, rowspan=4, columnspan=2)

        f1.grid_propagate(False)
        f2.grid_propagate(False)

        Button(f1, text="CLOSE", command=lambda:self.root.destroy()).grid(sticky=NSEW)
        
        total, aset, qris, barang = getAset()
        pendapatan, pengeluaran = getProfit()
        profit = pendapatan - pengeluaran

        f3.columnconfigure((0,1), weight=1)
        f3.rowconfigure((0,1,2,3), weight=1, uniform="2")
        f3.grid_propagate(False)
        Label(f3, text=" PENDAPATAN   :", font=("Consolas", 20), anchor=W).grid(row=0, column=0, sticky=NSEW)
        Label(f3, text=" PENGELUARAN  :", font=("Consolas", 20), anchor=W).grid(row=1, column=0, sticky=NSEW)
        Label(f3, text=" PROFIT       :", font=("Consolas", 20), anchor=W).grid(row=2, column=0, sticky=NSEW, rowspan=2)
        Label(f3, text=f"Rp {pendapatan:13,} ", font=("Consolas", 20), anchor=W).grid(row=0, column=1, sticky=NSEW)
        Label(f3, text=f"Rp {pengeluaran:13,} ", font=("Consolas", 20), anchor=W).grid(row=1, column=1, sticky=NSEW)
        Label(f3, text=f"Rp {profit:13,} ", font=("Consolas", 20), anchor=W).grid(row=2, column=1, sticky=NSEW, rowspan=2)


        f5.columnconfigure((0,1), weight=1)
        f5.rowconfigure((0,1,2,3), weight=1, uniform="2")
        f5.grid_propagate(False)
        Label(f5, text=" Cash         :", font=("Consolas", 20), anchor=W).grid(row=0, column=0, sticky=NSEW)
        Label(f5, text=" Qris         :", font=("Consolas", 20), anchor=W).grid(row=1, column=0, sticky=NSEW)
        Label(f5, text=" Barang       :", font=("Consolas", 20), anchor=W).grid(row=2, column=0, sticky=NSEW)
        Label(f5, text=" Total        :", font=("Consolas", 20), anchor=W).grid(row=3, column=0, sticky=NSEW)

        self.Aset = Label(f5, text=f"Rp {aset:13,} ", font=("Consolas", 20), anchor=E)
        self.Aset.grid(row=0, column=1, sticky=NSEW)
        self.Qris = Label(f5, text=f"Rp {qris:13,} ", font=("Consolas", 20), anchor=E)
        self.Qris.grid(row=1, column=1, sticky=NSEW)
        self.Barang = Label(f5, text=f"Rp {barang:13,} ", font=("Consolas", 20), anchor=E)
        self.Barang.grid(row=2, column=1, sticky=NSEW)
        self.totalAset = Label(f5, text=f"Rp {total:13,} ", font=("Consolas", 20), anchor=E)
        self.totalAset.grid(row=3, column=1, sticky=NSEW)

if __name__ == "__main__":
    app = LaporanAset()
    app.root.mainloop()