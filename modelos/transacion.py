from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="JULIANM-PRO-CLIENTES")


# 1. Definimos el modelo de Pydantic para Transacciones
class TransaccionModelo(BaseModel):
    id: int
    Vr_unitario: float
    cantidad: int 
    factura_id: int

# Simulación de la base de datos de transacciones
BD_TRANSACCIONES = [
    {"id": 1, "Vr_unitario": 1500.0, "cantidad": 2, "factura_id": 101},
    {"id": 2, "Vr_unitario": 5000.0, "cantidad": 1, "factura_id": 102}
]

# --- 5 ENDPOINTS PARA TRANSACCIONES ---

# Endpoint 1: Obtener todas las transacciones (GET)
@app.get("/transacciones", summary="Obtener todas las transacciones")
def obtener_transacciones():
    return BD_TRANSACCIONES


# Endpoint 2: Obtener una transacción específica por su ID (GET)
@app.get("/transacciones/{transaccion_id}", summary="Obtener una transacción por ID")
def obtener_transaccion_por_id(transaccion_id: int):
    for transaccion in BD_TRANSACCIONES:
        if transaccion["id"] == transaccion_id:
            return transaccion
    raise HTTPException(status_code=404, detail="Transación no encontrada")


# Endpoint 3: Crear una nueva transacción (POST)
@app.post("/transacciones", summary="Crear una nueva transacción")
def crear_transaccion(nueva_transaccion: TransaccionModelo):
    # Validar que el ID no esté repetido
    for t in BD_TRANSACCIONES:
        if t["id"] == nueva_transaccion.id:
            raise HTTPException(status_code=400, detail="El ID de la transacción ya existe")
    
    BD_TRANSACCIONES.append(nueva_transaccion.model_dump())
    return {"mensaje": "Transación registrada con éxito", "transaccion": nueva_transaccion}


# Endpoint 4: Obtener todas las transacciones de una Factura específica (GET)
# Muy útil para listar los "detalles" o artículos de una sola factura
@app.get("/transacciones/factura/{factura_id}", summary="Obtener transacciones de una factura")
def obtener_transacciones_por_factura(factura_id: int):
    transacciones_factura = [t for t in BD_TRANSACCIONES if t["factura_id"] == factura_id]
    if not transacciones_factura:
        raise HTTPException(status_code=404, detail="No se encontraron transacciones para esta factura")
    return transacciones_factura


# Endpoint 5: Eliminar una transacción (DELETE)
@app.delete("/transacciones/{transaccion_id}", summary="Eliminar una transacción")
def eliminar_transaccion(transaccion_id: int):
    for indice, transaccion in enumerate(BD_TRANSACCIONES):
        if transaccion["id"] == transaccion_id:
            transaccion_eliminada = BD_TRANSACCIONES.pop(indice)
            return {"mensaje": f"Transacción con ID {transaccion_id} eliminada", "transaccion": transaccion_eliminada}
    raise HTTPException(status_code=404, detail="Transación no encontrada")