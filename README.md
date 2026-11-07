# Servidor MCP — Inventario de Laboratorio

**Universidad de las Ciencias Informáticas**
**Asignatura:** Inteligencia Artificial Avanzada · **Equipo 6** · 2026

**Integrantes:**
- Addel Vidal García
- Alejandro Colón Álvarez
- Miguel Ángel Banteurt Blanco

Servidor **MCP (Model Context Protocol)** implementado en Python que
expone herramientas de consulta y modificación sobre un inventario de
laboratorio almacenado en `inventario.json` (20 artículos).
Permite a un cliente MCP buscar artículos, consultar existencias y
registrar solicitudes de material con validaciones estrictas y
confirmación previa del usuario.

> Ejercicio local simulado: no requiere acceso a sistemas oficiales
> de ninguna institución.

---

## 🛠️ Herramientas expuestas

| Herramienta | Tipo | Descripción |
|---|---|---|
| `buscar_articulo(nombre)` | Consulta (Read-Only) | Búsqueda parcial e insensible a mayúsculas por nombre |
| `consultar_existencias(articulo_id)` | Consulta (Read-Only) | Devuelve nombre, cantidad y unidad; valida que el ID exista |
| `registrar_solicitud(articulo_id, cantidad, confirmar)` | Modificación (State-Changing) | Descuenta stock tras validar rango, existencia y confirmación |

### Reglas de negocio de `registrar_solicitud`
1. Rechaza cantidades negativas o iguales a cero.
2. Rechaza cantidades superiores al stock disponible.
3. Rechaza identificadores inexistentes.
4. Exige confirmación explícita (`confirmar=true`) antes de persistir
   el cambio en `inventario.json` (patrón *human-in-the-loop*).

---

## 📁 Estructura del proyecto

```
mcp_inventario/
├── inventario.json        # Datos: 20 artículos (id, nombre, cantidad, unidad)
├── config.py              # Rutas centralizadas
├── gestor_inventario.py   # Lógica de negocio y validaciones
├── servidor_mcp.py        # Servidor MCP (FastMCP, transporte stdio)
├── requirements.txt       # Dependencias (mcp<2)
├── README.md
├── .gitignore
├── docs/                  # Informe técnico (Word)
└── evidencias/            # Capturas de las pruebas en MCP Inspector
~~~

---

## ⚙️ Requisitos

- Python 3.10 o superior
- SDK `mcp` de Python (versión 1.x)
- Node.js (solo para ejecutar el MCP Inspector durante las pruebas)

## 🚀 Instalación

```bash
python -m venv venv
.\venv\Scripts\activate        # Windows
# source venv/bin/activate     # Linux / macOS

pip install -r requirements.txt
```

## ▶️ Ejecución del servidor

```bash
python servidor_mcp.py
```

El servidor queda a la espera de conexiones JSON-RPC 2.0 sobre `stdio`
(la terminal permanece en silencio: es el comportamiento normal).

## 🧪 Pruebas con un cliente MCP (MCP Inspector)

```bash
npx @modelcontextprotocol/inspector python servidor_mcp.py
```

1. Abrir la URL mostrada (http://127.0.0.1:6274).
2. Pulsar **Connect** sobre el servidor `python`.
3. Ir a la pestaña **Tools** → **List Tools**.
4. Seleccionar cada herramienta, completar parámetros y pulsar **Run Tool**.

### Ejemplo de pregunta resuelta por el sistema

> *«¿Cuántos cables de red y multímetros hay disponibles?»*

- `buscar_articulo("cable")` → Cable de red UTP Cat6: **45 metros**
- `consultar_existencias(2)` → Multímetro digital: **8 unidades**

---

## 📚 Documentación y evidencias

- `docs/Informe_MCP_Inventario_Laboratorio.docx` → informe técnico
  completo (marco teórico, investigación consulta vs. modificación,
  arquitectura, metodología de pruebas y resultados).
- `evidencias/` → capturas de las 8 pruebas ejecutadas en MCP
  Inspector v2.13.0 (Anexo A del informe).