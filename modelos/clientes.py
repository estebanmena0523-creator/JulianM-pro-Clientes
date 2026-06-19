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

#3 Obtener todos los clientes (GET)
@app.get("/clientes", summary="Obtener lista de clientes")
def obtener_clientes():
    return BD_CLIENTES

#4 Crear un nuevo cliente (POST)
@app.post("/clientes", summary="Crear un nuevo cliente")
def crear_cliente(nuevo_cliente: ClienteModelo):
    # Validamos que el ID no exista ya en nuestra "BD"
    for cliente in BD_CLIENTES:
        if cliente["id"] == nuevo_cliente.id:
            raise HTTPException(status_code=400, detail="El ID de cliente ya existe")
        
# Añadimos el cliente a la lista
    BD_CLIENTES.append(nuevo_cliente.model_dump())
    return {"mensaje": "Cliente creado con éxito", "cliente": nuevo_cliente}

# 5. Eliminar un cliente (DELETE)
@app.delete("/clientes/{cliente_id}", summary="Eliminar un cliente")
def eliminar_cliente(cliente_id: int):
    for indice, cliente in enumerate(BD_CLIENTES):
        if cliente["id"] == cliente_id:
            cliente_eliminado = BD_CLIENTES.pop(indice)
            return {"mensaje": f"Cliente con ID {cliente_id} eliminado", "cliente": cliente_eliminado}
    
    raise HTTPException(status_code=404, detail="Cliente no encontrado")