from tkinter import ttk
def setup_style(root):
    style = ttk.Style(root)

    # Pilih theme dasar
    style.theme_use("default")

    # ---------- Warna Utama ----------
    bg = "#222831"
    surface = "#323841"
    highlight = "#00ADB5"
    text = "#EEEEEE"
    danger = "#ff4b4b"

    root.configure(bg=bg)

    # Treeview
    style.configure(
        "Treeview",
        background=surface,
        foreground=text,
        rowheight=28,
        fieldbackground=surface,
        bordercolor="white",
        borderwidth=0,
        font=("consolas", 13)
    )
    style.map("Treeview", background=[("selected", "#3d5c5e")])

    # Header (heading)
    style.configure(
        "Treeview.Heading",
        font=("consolas", 15, "bold"),
        background=highlight,
        foreground="#000000",
        relief="raised"
    )
    style.map("Treeview.Heading", background=[("active", "#05ced9")])

    # Buttons
    style.configure(
        "TButton",
        font=("consolas", 12),
        padding=10,
        background=highlight,
        foreground="#000000",
        relief="flat"
    )
    style.map(
        "TButton",
        background=[("active", "#05ced9")],
        foreground=[("disabled", "#777777")]
    )