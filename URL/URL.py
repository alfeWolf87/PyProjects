import tkinter as tk
from tkinter import messagebox
import pyshorteners

def acortar_url():
    url_larga = entrada_url.get()
    
    # Validar que el usuario haya escrito algo
    if not url_larga:
        messagebox.showwarning("Error", "Por favor, introduce una URL válida.")
        return
    
    try:
        # Usamos la librería para conectar con el servicio de TinyURL
        s = pyshorteners.Shortener()
        url_corta = s.tinyurl.short(url_larga)
        
        # Mostrar el resultado en la interfaz
        resultado_url.delete(0, tk.END)
        resultado_url.insert(0, url_corta)
    except Exception as e:
        messagebox.onerror("Error", f"No se pudo acortar la URL. {e}")

# --- Configuración de la Ventana Visual (Tkinter) ---
ventana = tk.Tk()
ventana.title("Ventana URL")
ventana.geometry("450x250")
ventana.config(bg="#f0f2f5")

# Título
titulo = tk.Label(ventana, text="URL", font=("Arial", 16, "bold"), bg="#f0f2f5", fg="#333")
titulo.pack(pady=10)

# Entrada de la URL larga
lbl_entrada = tk.Label(ventana, text="Pega tu URL larga aquí:", bg="#f0f2f5", font=("Arial", 10))
lbl_entrada.pack()
entrada_url = tk.Entry(ventana, width=50, font=("Arial", 10))
entrada_url.pack(pady=5)

# Botón para accionar
btn_acortar = tk.Button(ventana, text="¡Acortar!", command=acortar_url, bg="#007bff", fg="white", font=("Arial", 10, "bold"), padx=10)
btn_acortar.pack(pady=10)

# Cuadro para mostrar el resultado
lbl_resultado = tk.Label(ventana, text="Tu URL corta:", bg="#f0f2f5", font=("Arial", 10))
lbl_resultado.pack()
resultado_url = tk.Entry(ventana, width=30, font=("Arial", 12, "bold"), justify="center", fg="green")
resultado_url.pack(pady=5)

# Arrancar la aplicación
ventana.mainloop()