from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI(title="JULIANM-PRO-CLIENTES")

# Base de datos simulada de clientes
BD_CLIENTES = [
    {"id": 1, "nombre": "Julian", "email": "julian@mail.com", "descripcion": "joven estudiante del sena"},
    {"id": 2, "nombre": "karol", "email": "karol@mail.com", "descripcion": "joven estudiante de la salle"},
]

# Base de datos simulada de facturas (Faltaba definirla)
BD_FACTURAS = []

# Modelo para validar la estructura de un cliente
class ClienteModelo(BaseModel):
    id: int
    nombre: str
    email: str
    descripcion: Optional[str] = None

# Modelo para validar la estructura de una factura
class FacturaModelo(BaseModel):
    id: int
    cliente: ClienteModelo  # Corregido: usa el modelo de Pydantic
    Vr_total: float

# 1. Crear factura nueva
@app.post("/facturas", summary="Crear una nueva factura")
def crear_factura(nueva_factura: FacturaModelo):
    for factura in BD_FACTURAS:
        if factura["id"] == nueva_factura.id:
            raise HTTPException(status_code=400, detail="El ID de la factura ya existe")
        
    BD_FACTURAS.append(nueva_factura.model_dump())
    return {"mensaje": "Factura creada con éxito", "factura": nueva_factura}

# 2. Obtener todas las facturas
@app.get("/facturas", summary="Obtener todas las facturas")
def obtener_todas_las_facturas():
    return BD_FACTURAS

# 3. Obtener factura por ID
@app.get("/facturas/{factura_id}", summary="Obtener una factura por su ID")
def obtener_factura_por_id(factura_id: int):
    for factura in BD_FACTURAS:
        if factura["id"] == factura_id:
            return factura
    raise HTTPException(status_code=404, detail="Factura no encontrada")

# 4. Obtener facturas de un cliente específico
@app.get("/facturas/cliente/{cliente_id}", summary="Obtener facturas de un cliente")
def obtener_facturas_por_cliente(cliente_id: int):
    # Filtramos las facturas donde el ID del cliente coincida
    facturas_cliente = [f for f in BD_FACTURAS if f["cliente"]["id"] == cliente_id]
    
    if not facturas_cliente:
        raise HTTPException(status_code=404, detail="No se encontraron facturas para este cliente")
        
    return facturas_cliente

# 5. Eliminar factura
@app.delete("/facturas/{factura_id}", summary="Eliminar una factura")
def eliminar_factura(factura_id: int):
    for indice, factura in enumerate(BD_FACTURAS):
        if factura["id"] == factura_id:
            factura_eliminada = BD_FACTURAS.pop(indice)
            return {"mensaje": f"Factura con ID {factura_id} eliminada", "factura": factura_eliminada}
    raise HTTPException(status_code=404, detail="Factura no encontrada")