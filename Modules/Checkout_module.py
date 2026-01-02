from Modules.Database_module import sellProduct, dataForCheckout, getKonversi, addPenjualan, addLaporanAset
from datetime import *

def penjualan(method:str, subtotal, payment, hargaBeli,  discount = 0.0):
    date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    total = round(subtotal - discount, 2)
    change = round(payment - total, 0)

    data = (date,subtotal,discount,total,payment,change,method.upper())
    addPenjualan(data)

    data1 = (datetime.now().strftime("%m"), datetime.now().strftime("%d"),
            datetime.now().strftime("%H:%M:%S"), method, total, "MASUK", "PEMBELIAN")
    data2 = (datetime.now().strftime("%m"), datetime.now().strftime("%d"),
            datetime.now().strftime("%H:%M:%S"), "BARANG", hargaBeli, "KELUAR", "PEMBELIAN")
    
    forAset = [data1, data2]

    addLaporanAset(forAset)

    return total, change

def checkout(cart:list):
    items =[]
    hargaBeli = []

    for item in cart:
        totalHargaBeli= dataForCheckout(item[3], item[4], item[1])
        konversi = getKonversi(item[3], item[4], item[1])[0]

        hargaBeli.append(totalHargaBeli)
        items.append((
            konversi, totalHargaBeli, item[3]
        ))
    
    print(items)
    sellProduct(items)
    return sum(hargaBeli)