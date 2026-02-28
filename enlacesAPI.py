from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import random
import string

# 1. Inicializamos la aplicación 
app = FastAPI(title="Motor Acortador de Enlaces")

# 2. Base de datos simulada 
base_de_datos = {}

# 3. Modelo de datos 
class EnlaceRequest(BaseModel):
    url_larga: str

# 4. Función para generar el código corto aleatorio
def generar_codigo_corto(longitud=5):
    caracteres = string.ascii_letters + string.digits
    return "".join(random.choice(caracteres) for _ in range(longitud))

# --- ENDPOINTS ---

@app.post("/acortar")
def acortar_url(peticion: EnlaceRequest):
    codigo = generar_codigo_corto()
    while codigo in base_de_datos:
        codigo = generar_codigo_corto()
    base_de_datos[codigo] = peticion.url_larga
    url_corta = f"http://127.0.0.1:8000/{codigo}"
    return {"url_corta": url_corta, "url_original": peticion.url_larga}

@app.get("/{codigo_corto}")
def redirigir(codigo_corto: str):
    url_real = base_de_datos.get(codigo_corto)
    if url_real:
        return RedirectResponse(url=url_real)
    else:
        raise HTTPException(status_code=404, detail="Enlace no encontrado")
