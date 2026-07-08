import tkinter as tk



ventana = tk.Tk()
ventana.title("Hola Mundo")
ventana.geometry("450x250")
ventana.config(bg="#2154a0")

titulo = tk.Label(ventana, text="Ventana de pruebas", font=("Arial", 16, "bold"), bg="#2154a0", fg="#333")
titulo.pack(pady=5)



ventana.mainloop()