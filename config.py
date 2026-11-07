import os

# Definimos la ruta al archivo JSON de forma dinámica
# Esto asegura que funcione sin importar desde qué carpeta ejecutes el script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTARIO_FILE = os.path.join(BASE_DIR, "inventario.json")