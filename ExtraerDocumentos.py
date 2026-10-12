import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))

API_KEY = os.getenv("OUTLINE_API_KEY")
if not API_KEY:
    raise RuntimeError("Falta la variable de entorno OUTLINE_API_KEY")

BASE_URL = os.getenv("OUTLINE_BASE_URL", "https://app.getoutline.com/api")
COLECCION_ID = os.getenv("OUTLINE_COLLECTION_ID")
if not COLECCION_ID:
    raise RuntimeError("Falta la variable de entorno OUTLINE_COLLECTION_ID")

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


# 1. Listar todos los documentos de la coleccion
documents = []
contador = 0
while True:
    result, _ = llamar(
        "documents.list",
        collectionId=COLECCION_ID,
        limit=100,
        contador=contador,
    )
    documents.extend(result)
    if len(result) < 100:
        break
    contador += 100

print("Documentos encontrados en la coleccion: " + str(len(documents)) + "\n")

for i, doc_meta in enumerate(documents, start=1):
    doc, _ = llamar("documents.info", id=doc_meta["id"])
    title = doc.get("title", "Sin titulo")
    text = doc.get("text", "")

    print('=' * 60)
    print(f"[{i}] {title}")
    print('=' * 60)
    print(text)
    print("\n")
