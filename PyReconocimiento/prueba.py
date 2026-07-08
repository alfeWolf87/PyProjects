import face_recognition
import cv2
import numpy as np
import os
import pickle
import tkinter as tk
from tkinter import simpledialog, messagebox

# --- Configuración ---
DB_PATH = "faces_db.pkl"  # archivo donde se guardan nombres y codificaciones
MATCH_THRESHOLD = 0.5      # umbral de distancia para considerar "match"
BUTTON_RECT = (10, 420, 150, 470)  # x1, y1, x2, y2 del botón "Guardar"
USERS_BUTTON_RECT = (170, 420, 340, 470)  # botón "Usuarios" (abre gestor)

# Variables globales para el estado actual (actualizadas en el loop)
known_encodings = []
known_names = []
last_face_locations = []
last_face_encodings = []
last_message = ""

# --- Utilidades de DB ---

def load_database(path=DB_PATH):
    global known_encodings, known_names
    if os.path.exists(path):
        with open(path, 'rb') as f:
            data = pickle.load(f)
            known_encodings = data.get('encodings', [])
            known_names = data.get('names', [])
            print(f"Cargada DB con {len(known_names)} rostros")
    else:
        known_encodings = []
        known_names = []


def save_database(path=DB_PATH):
    data = {'encodings': known_encodings, 'names': known_names}
    with open(path, 'wb') as f:
        pickle.dump(data, f)
    print(f"Guardada DB con {len(known_names)} rostros")


# --- Matching ---

def find_match(face_encoding, threshold=MATCH_THRESHOLD):
    if not known_encodings:
        return None, None
    distances = face_recognition.face_distance(known_encodings, face_encoding)
    best_idx = np.argmin(distances)
    if distances[best_idx] <= threshold:
        return best_idx, distances[best_idx]
    return None, None


# --- Interacción ---

def ask_name():
    root = tk.Tk()
    root.withdraw()
    name = simpledialog.askstring("Nombre", "Ingrese nombre para este rostro:", parent=root)
    root.destroy()
    return name


def show_info(title, msg):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title, msg, parent=root)
    root.destroy()


def open_user_manager():
    """Ventana para listar y eliminar usuarios guardados."""
    root = tk.Tk()
    root.title("Gestor de Usuarios")
    root.geometry("320x300")

    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, selectmode=tk.SINGLE)
    listbox.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=listbox.yview)

    def refresh():
        listbox.delete(0, tk.END)
        for name in known_names:
            listbox.insert(tk.END, name)

    def show_selected():
        sel = listbox.curselection()
        if not sel:
            show_info("Info", "Seleccione un usuario")
            return
        idx = sel[0]
        name = known_names[idx]
        show_info("Usuario", f"Nombre: {name}\nÍndice: {idx}")

    def delete_selected():
        sel = listbox.curselection()
        if not sel:
            show_info("Error", "Seleccione un usuario a eliminar")
            return
        idx = sel[0]
        name = known_names[idx]
        if messagebox.askyesno("Confirmar", f"¿Eliminar usuario '{name}'?", parent=root):
            # eliminar encoding y nombre correspondientes
            try:
                del known_names[idx]
                del known_encodings[idx]
            except Exception as e:
                show_info("Error", f"No se pudo eliminar: {e}")
                return
            save_database()
            refresh()
            show_info("Eliminado", f"Usuario '{name}' eliminado")

    # Doble click para mostrar
    listbox.bind('<Double-Button-1>', lambda e: show_selected())

    btn_frame = tk.Frame(root)
    btn_frame.pack(fill=tk.X, padx=8, pady=(0,8))

    btn_show = tk.Button(btn_frame, text="Mostrar", command=show_selected)
    btn_show.pack(side=tk.LEFT, padx=(0,6))
    btn_delete = tk.Button(btn_frame, text="Eliminar", command=delete_selected)
    btn_delete.pack(side=tk.LEFT, padx=(0,6))
    btn_close = tk.Button(btn_frame, text="Cerrar", command=root.destroy)
    btn_close.pack(side=tk.RIGHT)

    refresh()
    root.mainloop()


# --- Dibujo del botón y mensajes ---

def draw_button(frame, rect=BUTTON_RECT, label="Guardar (G)"):
    x1, y1, x2, y2 = rect
    cv2.rectangle(frame, (x1, y1), (x2, y2), (50, 50, 200), -1)
    cv2.putText(frame, label, (x1 + 10, y1 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)


def draw_message(frame, msg):
    if msg:
        cv2.putText(frame, msg, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)


# Mouse callback para clicks en botón o en rostros

def mouse_callback(event, x, y, flags, param):
    global last_face_locations, last_face_encodings, last_message
    if event == cv2.EVENT_LBUTTONDOWN:
        # Botón Guardar
        x1, y1, x2, y2 = BUTTON_RECT
        if x1 <= x <= x2 and y1 <= y <= y2:
            if last_face_encodings:
                save_face(0)  # por simplicidad, guardar el primer rostro detectado
            else:
                last_message = "No hay rostros detectados"
            return
        # Botón Usuarios
        ux1, uy1, ux2, uy2 = USERS_BUTTON_RECT
        if ux1 <= x <= ux2 and uy1 <= y <= uy2:
            open_user_manager()
            return
        # Si clic dentro de algún rostro, guardarlo
        for i, (top, right, bottom, left) in enumerate(last_face_locations):
            if left <= x <= right and top <= y <= bottom:
                save_face(i)
                return


def save_face(index=0):
    global last_face_encodings, known_encodings, known_names, last_message
    if index >= len(last_face_encodings):
        last_message = "Índice de rostro inválido"
        return
    face_encoding = last_face_encodings[index]
    match_idx, dist = find_match(face_encoding)
    if match_idx is not None:
        last_message = f"Ya existe: {known_names[match_idx]} (dist={dist:.2f})"
        show_info("Duplicado", last_message)
        return
    # Pedir nombre
    nombre = ask_name()
    if not nombre:
        last_message = "Guardado cancelado"
        return
    known_encodings.append(face_encoding)
    known_names.append(nombre)
    save_database()
    last_message = f"Guardado: {nombre}"
    show_info("Guardado", last_message)


# --- Programa principal ---

def main():
    global last_face_locations, last_face_encodings, last_message

    load_database()

    video_capture = cv2.VideoCapture(0)
    cv2.namedWindow('Video Reconocimiento')
    cv2.setMouseCallback('Video Reconocimiento', mouse_callback)

    print("Iniciando cámara. Presione 'q' para salir, 'g' para guardar el primer rostro detectado, 'u' para gestionar usuarios.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Usar versión reducida para detección (más rápida)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        last_face_locations = []
        last_face_encodings = []

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # recalibrar a tamaño original
            top *= 4; right *= 4; bottom *= 4; left *= 4
            last_face_locations.append((top, right, bottom, left))
            last_face_encodings.append(face_encoding)

            # Intentar identificar
            match_idx, dist = find_match(face_encoding)
            name = "Desconocido"
            if match_idx is not None:
                name = f"{known_names[match_idx]}"

            # Dibujar caja y nombre
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 200, 0), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Dibujar UI
        draw_button(frame)
        draw_button(frame, USERS_BUTTON_RECT, "Usuarios (U)")
        draw_message(frame, last_message)

        cv2.imshow('Video Reconocimiento', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('g'):
            # Guardar primer rostro si hay
            if last_face_encodings:
                save_face(0)
            else:
                last_message = "No hay rostros detectados"
        if key == ord('u'):
            open_user_manager()

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()