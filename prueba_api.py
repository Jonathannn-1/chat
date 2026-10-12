import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))

API_KEY = os.getenv("OUTLINE_API_KEY")
if not API_KEY:
    raise RuntimeError("Falta la variable de entorno OUTLINE_API_KEY")

BASE_URL = os.getenv("OUTLINE_BASE_URL", "https://app.getoutline.com/api")

response = requests.post(
    f"{BASE_URL}/auth.info",
    headers={
        "Authorization": "Bearer " + API_KEY,
        "Content-Type": "application/json",
    }
)

print(response.status_code)
print(response.json())
