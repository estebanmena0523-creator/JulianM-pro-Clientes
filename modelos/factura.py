from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="JULIANM-PRO-CLIENTES")


BD_CLIENTES = [
    {"id": 1, "nombre": "Julian", "email": "julian@mail.com", "descripcion": "joven estudiante del sena", },
    {"id": 2, "nombre": "karol", "email": "karol@mail.com",  "descripcion": "joven estudiante de la salle", },
]

class factura:
    id: int
    cliente:cliente
    Vr_total: float

#1 crea factura nueva
@app.post("/facturas", summary="Crear una nueva factura")
def crear_factura(nueva_factura: FacturaModelo):
    for factura in BD_FACTURAS:
        if factura["id"] == nueva_factura.id:
            raise HTTPException(status_code=400, detail="El ID de la factura ya existe")
        
    BD_FACTURAS.append(nueva_factura.model_dump())
    return {"mensaje": "Factura creada con éxito", "factura": nueva_factura}

#2 obtener factura
@app.get("/facturas", summary="Obtener todas las facturas")
def obtener_todas_las_facturas():
    return BD_FACTURAS

#3 especificacion
@app.get("/facturas/{factura_id}", summary="Obtener una factura por su ID")
def obtener_factura_por_id(factura_id: int):
    for factura in BD_FACTURAS:
        if factura["id"] == factura_id:
            return factura
    raise HTTPException(status_code=404, detail="Factura no encontrada")

#4 reclamar factura
@app.get("/facturas/cliente/{cliente_id}", summary="Obtener facturas de un cliente")
def obtener_facturas_por_cliente(cliente_id: int):
    # Filtramos las facturas donde el ID del cliente coincida
    facturas_cliente = [f for f in BD_FACTURAS if f["cliente"]["id"] == cliente_id]
    
    if not facturas_cliente:
        raise HTTPException(status_code=404, detail="No se encontraron facturas para este cliente")
        
    return facturas_cliente