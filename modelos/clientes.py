from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="JULIANM-PRO-CLIENTES")


BD_CLIENTES = [
    {"id": 1, "nombre": "Julian", "email": "julian@mail.com", "descripcion": "joven estudiante del sena", },
    {"id": 2, "nombre": "karol", "email": "karol@mail.com",  "descripcion": "joven estudiante de la salle", },
]


class ClienteModelo(BaseModel):
    id: int
    nombre: str
    email: str
    descripcion: str 
#1 saludo
@app.get("/saludar/{nombre}") 
def saludar_nombre(nombre: str): 
    return {"mensaje": f"Hola, {nombre}"}

#2 actualizar el cliente
@app.put("/clientes/{cliente_id}", summary="Actualizar todo el cliente")
def actualizar_cliente_completo(cliente_id: int, datos_actualizados: ClienteModelo):
    for cliente in BD_CLIENTES:
        if cliente["id"] == cliente_id:
            cliente.update(datos_actualizados.dict())
            return {"mensaje": f"Cliente con ID {cliente_id} actualizado con éxito", "cliente": cliente}

# 3. Obtener todos los clientes (GET)
@app.get("/clientes", summary="Obtener lista de clientes")
def obtener_clientes():
    return BD_CLIENTES