import tkinter as tk

def button_click(value):
    """
    Fungsi untuk menangani klik tombol angka atau operator.
    """
    current_text = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current_text + value)

def calculate():
    """
    Fungsi untuk menghitung ekspresi matematika.
    """
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

def clear():
    """
    Fungsi untuk mengosongkan input.
    """
    entry.delete(0, tk.END)

# Membuat jendela utama
root = tk.Tk()
root.title("Kalkulator Sederhana")

# Entry untuk menampilkan input dan hasil
entry = tk.Entry(root, width=20, font=("Arial", 18), borderwidth=5, justify="right")
entry.grid(row=0, column=0, columnspan=4, pady=10)

# Daftar tombol
buttons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
    ("C", 4, 0), ("0", 4, 1), ("=", 4, 2), ("+", 4, 3),
]

# Menambahkan tombol ke grid
for (text, row, col) in buttons:
    if text == "=":
        btn = tk.Button(root, text=text, width=5, height=2, font=("Arial", 14), bg="lightgreen", command=calculate)
    elif text == "C":
        btn = tk.Button(root, text=text, width=5, height=2, font=("Arial", 14), bg="lightcoral", command=clear)
    else:
        btn = tk.Button(root, text=text, width=5, height=2, font=("Arial", 14),
                        command=lambda t=text: button_click(t))
    btn.grid(row=row, column=col, padx=5, pady=5)

# Menjalankan aplikasi
root.mainloop()