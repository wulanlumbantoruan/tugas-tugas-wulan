
# Nomor 1
target = 100000000
tabungan_per_orang = 2000000
total_tabungan = 0

def cek_tabungan(nama, tabungan):
    try:
        tabungan = int(tabungan)
        if tabungan > tabungan_per_orang:
            print(f"{nama}, uang tabungan mu melebihi nominal sebesar Rp{tabungan_per_orang}.")
            return 0
        elif tabungan < tabungan_per_orang:
            print(f"{nama}, uang tabungan mu kurang dari nominal sebesar Rp{tabungan_per_orang}.")
            return 0
        else:
            return tabungan

    except ValueError:
        print(f"Input tabungan untuk {nama} harus berupa angka.")
        return 0
    else:
        return tabungan

while total_tabungan < target:
    print(f"\nTotal tabungan saat ini: Rp{total_tabungan}")

    dina = input("Masukkan tabungan Dina: ")
    arif = input("Masukkan tabungan Arif: ")
    lila = input("Masukkan tabungan Lila: ")

    total_tabungan += cek_tabungan("Dina", dina)
    total_tabungan += cek_tabungan("Arif", arif)
    total_tabungan += cek_tabungan("Lila", lila)

    if total_tabungan >= target:
        print("\nHoree! Tabungan mu sudah mencapai target Rp100.000.000.")
        break


# Nomor 2
def cek_prima(n, i=2):
    if n < 2:
        return False
    if i * i > n:
        return True
    if n % i == 0:
        return False
    return cek_prima(n, i + 1)

angka = int(input("Masukkan bilangan yang ingin dicek: "))

if cek_prima(angka):
    print(f"{angka} adalah bilangan prima.")
else:
    print(f"{angka} bukan bilangan prima.")

