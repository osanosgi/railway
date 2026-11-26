
import os
from urllib.parse import quote_plus
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient
from django.utils import timezone

# Cargar variables del archivo .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Obtener credenciales
MONGO_USER = quote_plus(os.getenv("MONGO_USER", ""))
MONGO_PASSWORD = quote_plus(os.getenv("MONGO_PASSWORD", ""))
MONGO_HOST = os.getenv("MONGO_HOST", "")
MONGO_DB = os.getenv("MONGO_DB", "poliglota_mongo")


# Validar configuración
# if not all([MONGO_USER, MONGO_PASSWORD, MONGO_HOST]):
#     raise ValueError("Faltan variables de configuración MongoDB")

# Construir URI
MONGO_URI = (
    f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}"
    f"@{MONGO_HOST}/?retryWrites=true&w=majority"
)

# Conectar a Atlas
cliente = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=10000
)

db = cliente[MONGO_DB]
auditoria = db["auditoria"]


def registrar_auditoria(
    accion,
    registro_id,
    detalles=None,
    usuario=None
):
    evento = {
        "accion": accion,
        "entidad": "Producto",
        "registro_id": registro_id,
        "fecha": timezone.now(),
        "usuario": usuario,
        "detalles": detalles or {},
    }

    resultado = auditoria.insert_one(evento)
    return resultado.inserted_id


def probar_conexion():
    try:
        cliente.admin.command("ping")
        return "Conexión exitosa con MongoDB Atlas"
    except Exception as e:
        return f"Error de conexión: {e}"

