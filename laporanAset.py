from tkinter import *

from models.db import init_db
from models.baseModels import Laporan
from style import setup_style

init_db()

class LaporanAset():
    def __init__(self):
        self.root = Tk()
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

if __name__ == "__main__":
    app = LaporanAset()
    app.root.mainloop()