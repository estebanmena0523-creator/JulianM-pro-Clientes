from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="nombre pro clientes")


BD_CLIENTES = [
    {"id": 1, "nombre": "Julian", "apellido": "murillo", "edad": 30, "email": "julian@mail.com","descripcion": "joven estudiante del sena", "activo": True},
    {"id": 2, "nombre": "karol", "apellido": "fontecha", "edad": 15, "email": "karol@mail.com", "descripcion": "joven estudiante de la salle", "activo": True},
]


class ClienteModelo(BaseModel):
    id: int
    nombre: str
    apellido: str
    edad: int = Field(..., gt=0, lt=120) 
    email: str
    descripcion: str 
    activo: bool = True

class Transacciones:
    id: int
    Vr_unitario: float
    cantidad: int 
    factura_id: int

class factura:
    id: int
    cliente: cliente
    Vr_total: float

@app.get("/") 
def inicio(): 
    return {"mensaje": "Este es el proyecto de clientes a desarrollar"}

@app.get("/clientes") 
def listar_clientes(): 
    return BD_CLIENTES


@app.get("/saludar/{nombre}") 
def saludar_nombre(nombre: str): 
    return {"mensaje": f"Hola, {nombre}"}

@app.get("/saludar/{nombre}/{apellido}") 
def saludar_completo(nombre: str, apellido: str, edad: int = None): 
    if edad: 
        return {"mensaje": f"Hola, {nombre} {apellido}. Tienes {edad} años"} 
    return {"mensaje": f"Hola, {nombre} {apellido}"}

@app.put("/clientes/{cliente_id}", summary="Actualizar todo el cliente")
def actualizar_cliente_completo(cliente_id: int, datos_actualizados: ClienteModelo):
    for cliente in BD_CLIENTES:
        if cliente["id"] == cliente_id:
            cliente.update(datos_actualizados.dict())
            return {"mensaje": f"Cliente con ID {cliente_id} actualizado con éxito", "cliente": cliente}
    
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@app.put("/clientes/{cliente_id}/estado", summary="Actualizar estado activo/inactivo")
def actualizar_estado_cliente(cliente_id: int, activo: bool):
    for cliente in BD_CLIENTES:
        if cliente["id"] == cliente_id:
            cliente["activo"] = activo
            estado_str = "activado" if activo else "desactivado"
            return {"mensaje": f"El cliente {cliente['nombre']} ha sido {estado_str}"}
            
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@app.put("/clientes/configuracion/cumpleanos-masivo", summary="Sumar un año a todos los clientes")
def incrementar_edad_masiva(incremento: int = 1):
    for cliente in BD_CLIENTES:
        cliente["edad"] += incremento
    return {"mensaje": f"Se ha incrementado la edad de todos los clientes en {incremento} años", "clientes": BD_CLIENTES}

@app.put("/clientes/{cliente_id}/contacto", summary="Actualizar email de un cliente")
def actualizar_email(cliente_id: int, nuevo_email: str):
    for cliente in BD_CLIENTES:
        if cliente["id"] == cliente_id:
            cliente["email"] = nuevo_email
            return {"mensaje": "Email actualizado", "cliente_id": cliente_id, "nuevo_email": nuevo_email}
    raise HTTPException(status_code=404, detail="Cliente no encontrado")


@app.put("/clientes/{cliente_id}/categoria", summary="Cambiar el nivel de membresía del cliente")
def cambiar_categoria_cliente(cliente_id: int, nivel: str):
    niveles_validos = ["Silver", "Gold", "Platinum"]
    if nivel not in niveles_validos:
        raise HTTPException(status_code=400, detail=f"Nivel inválido. Use uno de estos: {niveles_validos}")
        
    for cliente in BD_CLIENTES:
        if cliente["id"] == cliente_id:
            cliente["categoria"] = nivel
            return {"mensaje": f"Cliente promovido a rango {nivel}", "cliente": cliente}
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@app.put("/clientes/marketing/descuento-por-edad", summary="Aplicar descuento masivo por rango de edad")
def aplicar_descuento_por_edad(edad_minima: int, porcentaje_descuento: int):
    clientes_afectados = 0
    for cliente in BD_CLIENTES:
        if cliente["edad"] >= edad_minima:
            cliente["descuento_asignado"] = f"{porcentaje_descuento}%"
            clientes_afectados += 1
            
    return {
        "mensaje": f"Se aplicó un {porcentaje_descuento}% de descuento exitosamente",
        "clientes_beneficiados": clientes_afectados,
        "base_datos_actualizada": BD_CLIENTES
    }

@app.put("/clientes/{cliente_id}/roles", summary="Modificar rol de acceso del cliente")
def actualizar_rol_cliente(cliente_id: int, rol: str = "usuario_estandar"):
    roles_permitidos = ["admin", "usuario_estandar", "soporte"]
    if rol not in roles_permitidos:
        raise HTTPException(status_code=400, detail="Rol no reconocido por el sistema")
        
    for cliente in BD_CLIENTES:
        if cliente["id"] == cliente_id:
            cliente["rol"] = rol
            return {"mensaje": f"Rol del cliente {cliente_id} cambiado a {rol}"}
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@app.put("/clientes/{cliente_id}/restablecer", summary="Restablecer configuraciones del cliente")
def restablecer_cliente(cliente_id: int):
    for cliente in BD_CLIENTES:
        if cliente["id"] == cliente_id:
            cliente["activo"] = True
            cliente["rol"] = "usuario_estandar"
            cliente.pop("descuento_asignado", None) 
            cliente.pop("categoria", None)
            return {"mensaje": "Configuraciones del cliente reestablecidas", "cliente": cliente}
    raise HTTPException(status_code=404, detail="Cliente no encontrado")
