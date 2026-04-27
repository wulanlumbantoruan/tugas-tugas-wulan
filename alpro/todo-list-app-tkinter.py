# NOMOR 3
import tkinter as tk
from tkinter import messagebox

def add_task():
    """
    Menambahkan tugas baru ke daftar.
    """
    task = entry.get()
    if task.strip() == "":
        messagebox.showwarning("Peringatan", "Tugas tidak boleh kosong!")
    else:
        task_listbox.insert(tk.END, task)
        entry.delete(0, tk.END)

def remove_task():
    """
    Menghapus tugas yang dipilih dari daftar.
    """
    try:
        selected_task_index = task_listbox.curselection()[0]
        task_listbox.delete(selected_task_index)
    except IndexError:
        messagebox.showwarning("Peringatan", "Pilih tugas yang ingin dihapus!")

def clear_all_tasks():
    """
    Menghapus semua tugas dari daftar.
    """
    task_listbox.delete(0, tk.END)

# Membuat jendela utama
root = tk.Tk()
root.title("To-Do List")

# Entry untuk input tugas
entry = tk.Entry(root, width=40, font=("Arial", 14))
entry.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

# Tombol "Add Task"
add_button = tk.Button(root, text="Add Task", width=15, font=("Arial", 12), command=add_task)
add_button.grid(row=0, column=2, padx=10, pady=10)

# Listbox untuk menampilkan daftar tugas
task_listbox = tk.Listbox(root, width=60, height=15, font=("Arial", 12))
task_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Tombol "Remove Task"
remove_button = tk.Button(root, text="Remove Task", width=15, font=("Arial", 12), command=remove_task)
remove_button.grid(row=2, column=0, padx=10, pady=10)

# Tombol "Clear All"
clear_button = tk.Button(root, text="Clear All", width=15, font=("Arial", 12), command=clear_all_tasks)
clear_button.grid(row=2, column=2, padx=10, pady=10)

# Menjalankan aplikasi
root.mainloop()
