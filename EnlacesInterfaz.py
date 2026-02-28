import customtkinter as ctk
import requests
from tkinter import messagebox

# --- Configuración General ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- Lógica de Comunicación con el Servidor (API) ---
def acortar_enlace():
    url_larga = entrada_url.get().strip()
    
    if not url_larga:
        label_mensaje.configure(text="Por favor, ingresa una URL válida.", text_color="#e74c3c")
        return

    # Validar que tenga http o https (buena práctica de UX)
    if not url_larga.startswith("http://") and not url_larga.startswith("https://"):
        url_larga = "https://" + url_larga

    label_mensaje.configure(text="Acortando...", text_color="gray")
    
    try:
        # 1. Preparamos los datos EXACTAMENTE como los espera nuestro modelo EnlaceRequest en FastAPI
        datos = {"url_larga": url_larga}
        
        # 2. Hacemos la petición POST a nuestro servidor local
        respuesta = requests.post("http://127.0.0.1:8000/acortar", json=datos)
        
        # 3. Verificamos si el servidor respondió con éxito (Código 200)
        if respuesta.status_code == 200:
            # Extraemos la información del JSON que nos devolvió FastAPI
            datos_respuesta = respuesta.json()
            url_corta = datos_respuesta.get("url_corta")
            
            # Mostramos el resultado en la interfaz
            entrada_resultado.configure(state="normal")
            entrada_resultado.delete(0, "end")
            entrada_resultado.insert(0, url_corta)
            entrada_resultado.configure(state="readonly")
            
            label_mensaje.configure(text="¡Enlace acortado con éxito!", text_color="#2ecc71")
            boton_copiar.configure(state="normal") 
        else:
            label_mensaje.configure(text="Error del servidor al acortar.", text_color="#e74c3c")
            
    except requests.exceptions.ConnectionError:
        # Si olvidaste prender Uvicorn, este error te avisará
        messagebox.showerror("Error de Conexión", "No se pudo conectar al servidor. ¿Te aseguraste de que Uvicorn esté corriendo en la otra terminal?")
        label_mensaje.configure(text="Servidor apagado.", text_color="#e74c3c")

def copiar_portapapeles():
    url_corta = entrada_resultado.get()
    if url_corta:
        root.clipboard_clear()
        root.clipboard_append(url_corta)
        label_mensaje.configure(text="¡Copiado al portapapeles!", text_color="#3498db")

# --- Interfaz de Usuario ---
root = ctk.CTk()
root.title("Acortador de Enlaces")
root.geometry("500x350")
root.resizable(False, False)

frame_principal = ctk.CTkFrame(root, corner_radius=15)
frame_principal.pack(pady=20, padx=20, fill="both", expand=True)

label_titulo = ctk.CTkLabel(frame_principal, text="Minimiza tus URLs", font=("Segoe UI", 22, "bold"))
label_titulo.pack(pady=(20, 10))

entrada_url = ctk.CTkEntry(frame_principal, placeholder_text="Pega tu enlace largo aquí (ej. https://...)", font=("Segoe UI", 14), width=350, height=40)
entrada_url.pack(pady=10)

# Botón para Acortar
boton_acortar = ctk.CTkButton(frame_principal, text="Acortar Enlace", font=("Segoe UI", 14, "bold"), command=acortar_enlace, height=40)
boton_acortar.pack(pady=10)

# Entrada para mostrar el Resultado
frame_resultado = ctk.CTkFrame(frame_principal, fg_color="transparent")
frame_resultado.pack(pady=10)

entrada_resultado = ctk.CTkEntry(frame_resultado, font=("Segoe UI", 14), width=250, height=40, state="readonly", justify="center")
entrada_resultado.pack(side="left", padx=(0, 10))

# Botón para Copiar 
boton_copiar = ctk.CTkButton(frame_resultado, text="Copiar", font=("Segoe UI", 14, "bold"), width=80, height=40, fg_color="#27ae60", hover_color="#2ecc71", command=copiar_portapapeles, state="disabled")
boton_copiar.pack(side="left")

# Mensaje de estado
label_mensaje = ctk.CTkLabel(frame_principal, text="", font=("Segoe UI", 12, "bold"))
label_mensaje.pack(pady=5)

root.mainloop()# EnlacesAcortados
