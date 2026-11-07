from mcp.server.fastmcp import FastMCP
from gestor_inventario import (
    buscar_articulo_logica, 
    consultar_existencias_logica, 
    registrar_solicitud_logica
)

# Inicializamos el servidor con un nombre descriptivo
mcp = FastMCP("InventarioLab")

# --- HERRAMIENTA 1: BÚSQUEDA ---
@mcp.tool()
def buscar_articulo(nombre: str) -> dict:
    """
    Busca artículos en el inventario por nombre (coincidencia parcial).
    Úsala cuando el usuario no sepa el ID exacto pero sepa qué busca.
    """
    return buscar_articulo_logica(nombre)

# --- HERRAMIENTA 2: CONSULTA ---
@mcp.tool()
def consultar_existencias(articulo_id: int) -> dict:
    """
    Obtiene la cantidad exacta y unidad de un artículo específico dado su ID.
    """
    return consultar_existencias_logica(articulo_id)

# --- HERRAMIENTA 3: MODIFICACIÓN (AMPLIACIÓN) ---
@mcp.tool()
def registrar_solicitud(articulo_id: int, cantidad: int, confirmar: bool = False) -> dict:
    """
    Registra una solicitud de salida de material.
    IMPORTANTE: Esta herramienta modifica el inventario. 
    1. Primero llama con confirmar=False para validar stock y pedir permiso.
    2. Si el usuario confirma explícitamente, llama de nuevo con confirmar=True.
    """
    return registrar_solicitud_logica(articulo_id, cantidad, confirmar)

if __name__ == "__main__":
    # Iniciamos el servidor usando stdio (estándar para clientes MCP locales)
    mcp.run(transport='stdio')