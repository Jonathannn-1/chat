import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))

API_KEY = os.getenv("OUTLINE_API_KEY")
if not API_KEY:
    raise RuntimeError("Falta la variable de entorno OUTLINE_API_KEY")

BASE_URL = os.getenv("OUTLINE_BASE_URL", "https://app.getoutline.com/api")

session = requests.Session()
session.headers.update({
    "Authorization": "Bearer " + API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json",
})


def llamar(method, **params):
    r = session.post(f"{BASE_URL}/{method}", json=params)
    try:
        data = r.json()
    except ValueError:
        raise RuntimeError("La API respondio con contenido no JSON en '" + method + "': " + r.text)

    if not r.ok or not data.get("ok", False):
        raise RuntimeError("Error en '" + method + "': " + str(data.get("error", r.text)))
    return data.get("data"), data.get("pagination")


# 1. Verificar conexion
me, _ = llamar("auth.info")
print("Conectado como: " + str(me['user']['name']) + " (" + str(me['user']['email']) + ")")
print("Workspace: " + str(me['team']['name']) + "\n")

# 2. Listar todas las colecciones
coleccion = []
contador = 0
while True:
    result, _ = llamar("collections.list", limit=100, contador=contador)
    coleccion.extend(result)
    if len(result) < 100:
        break
    contador += 100

print("Colecciones encontradas: " + str(len(coleccion)) + "\n")
for c in coleccion:
    print("- " + str(c['name']) + "  (id: " + str(c['id']) + ")")
