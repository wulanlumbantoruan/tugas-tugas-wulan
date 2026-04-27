import tkinter as tk
from tkinter import ttk, messagebox


def submit_data():
    # Mengambil nilai dari input field
    name = entry_name.get().strip()
    age = entry_age.get().strip()
    
    # Validasi input
    if not name or not age:
        messagebox.showwarning("Validasi Gagal", "Harap isi semua data!")
    elif not age.isdigit():
        messagebox.showerror("Validasi Gagal", "Usia harus berupa angka!")
    else:
        messagebox.showinfo("Sukses", "Data berhasil disimpan!")
        # Reset input setelah validasi berhasil
        entry_name.delete(0, tk.END)
        entry_age.delete(0, tk.END)


# Membuat jendela utama
root = tk.Tk()
root.title("Aplikasi Input dan Validasi Data")
root.geometry("300x200")

# Membuat frame untuk tata letak
main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill="both", expand=True)

# Label dan Entry untuk Nama
label_name = ttk.Label(main_frame, text="Nama Lengkap:")
label_name.grid(row=0, column=0, sticky="w", pady=5)
entry_name = ttk.Entry(main_frame)
entry_name.grid(row=0, column=1, pady=5, sticky="ew")

# Label dan Entry untuk Usia
label_age = ttk.Label(main_frame, text="Usia:")
label_age.grid(row=1, column=0, sticky="w", pady=5)
entry_age = ttk.Entry(main_frame)
entry_age.grid(row=1, column=1, pady=5, sticky="ew")

# Tombol Submit
btn_submit = ttk.Button(main_frame, text="Submit", command=submit_data)
btn_submit.grid(row=2, column=0, columnspan=2, pady=10)

# Menyesuaikan lebar kolom agar responsif
main_frame.columnconfigure(1, weight=1)

# Menjalankan aplikasi
root.mainloop()