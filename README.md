# JulianM-pro-Clientes
from fastapi import FastAPI

app = FastAPI(title="nombre pro clientes")

@app.get("/")
def inicio():
    return {"mensaje": "Este es el proyecto de clientes a desarrollar"}

@app.get("/clientes")
def listar_clientes():
    clientes = [
        {"id": 1, "nombre": "Juan", "apellido": "Perez"},
        {"id": 2, "nombre": "Ana", "apellido": "Perez", "edad": 15}
    ]
    return clientes

@app.get("/saludar/{nombre}")
def saludar_nombre(nombre: str):
    return {"mensaje": f"Hola, {nombre}"}

@app.get("/saludar/{nombre}/{apellido}")
def saludar_completo(nombre: str, apellido: str, edad: int = None):
    if edad:
        return {"mensaje": f"Hola, {nombre} {apellido}. Tienes {edad} años"}
    return {"mensaje": f"Hola, {nombre} {apellido}"}
