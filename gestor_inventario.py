import json
from config import INVENTARIO_FILE

def cargar_datos():
    """Lee el JSON y devuelve el diccionario."""
    with open(INVENTARIO_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_datos(datos):
    """Sobrescribe el JSON con los nuevos datos."""
    with open(INVENTARIO_FILE, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def buscar_articulo_logica(nombre: str):
    """Búsqueda parcial e insensible a mayúsculas."""
    datos = cargar_datos()
    nombre_buscado = nombre.strip().lower()
    
    resultados = []
    for art in datos["articulos"]:
        if nombre_buscado in art["nombre"].lower():
            resultados.append(art)
            
    if not resultados:
        return {"status": "error", "mensaje": f"No se encontraron artículos con '{nombre}'."}
    
    return {"status": "ok", "resultados": resultados}

def consultar_existencias_logica(articulo_id: int):
    """Valida que el ID exista antes de responder."""
    datos = cargar_datos()
    
    # Validación de tipo (por si la IA manda un string)
    if not isinstance(articulo_id, int):
         return {"status": "error", "mensaje": "El ID debe ser un número entero."}

    for art in datos["articulos"]:
        if art["id"] == articulo_id:
            return {
                "status": "ok", 
                "articulo": art,
                "mensaje": f"Existencias de {art['nombre']}: {art['cantidad']} {art['unidad']}."
            }
            
    return {"status": "error", "mensaje": f"Error 404: El artículo con ID {articulo_id} no existe."}

def registrar_solicitud_logica(articulo_id: int, cantidad: int, confirmar: bool = False):
    """
    Lógica de la Ampliación Opcional.
    1. Valida entradas (negativos, ID).
    2. Valida stock.
    3. Si no hay confirmación, AVISA y espera.
    4. Si hay confirmación, modifica y guarda.
    """
    # 1. Validaciones básicas de entrada
    if not isinstance(cantidad, int) or cantidad <= 0:
        return {"status": "error", "mensaje": "Cantidad inválida. Debe ser un entero positivo."}

    datos = cargar_datos()
    articulo = None
    
    # Buscar artículo
    for art in datos["articulos"]:
        if art["id"] == articulo_id:
            articulo = art
            break
            
    if not articulo:
        return {"status": "error", "mensaje": f"ID {articulo_id} no encontrado."}

    # 2. Validación de Stock
    if cantidad > articulo["cantidad"]:
        return {
            "status": "error", 
            "mensaje": f"Stock insuficiente. Solicitaste {cantidad} pero solo hay {articulo['cantidad']} disponibles."
        }

    # 3. Flujo de Confirmación (Human-in-the-loop)
    if not confirmar:
        return {
            "status": "pendiente",
            "mensaje": f"⚠️ CONFIRMACIÓN REQUERIDA: Vas a retirar {cantidad} {articulo['unidad']} de '{articulo['nombre']}'. ¿Confirmas la operación?",
            "accion": "Por favor responde 'Sí' para proceder."
        }

    # 4. Ejecución (Modificación de datos)
    articulo["cantidad"] -= cantidad
    guardar_datos(datos)
    
    return {
        "status": "ok",
        "mensaje": f"✅ Solicitud aprobada. Nuevo stock de {articulo['nombre']}: {articulo['cantidad']} {articulo['unidad']}."
    }