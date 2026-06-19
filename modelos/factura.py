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

