from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import create_db_and_tables  # ← agrega esta importación
from fastapi import Depends
from .database import get_session
from sqlmodel import Session
from app.models import UrgentCase, UrgentCaseBase

app = FastAPI(
    title="Santuario Emilia API 🐾",
    description="Backend para donaciones y más en el Santuario Emilia ❤️",
    version="0.1.0",
    swagger_ui_parameters={
        "syntaxHighlight.theme": "obsidian"          # Tema oscuro muy lindo
        # Otras opciones bonitas: "monokai", "dracula", "arta", "nord", "tomorrow-night"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crea las tablas al iniciar el servidor (solo la primera vez o cuando cambies modelos)
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/ping")
def ping():
    return {"status": "ok", "message": "Santuario Emilia backend vivo 🐾🐶"}

@app.delete("/urgent-cases/{case_id}")
def delete_case(case_id: int, session: Session = Depends(get_session)):
    case = session.get(UrgentCase, case_id)
    if not case:
        raise HTTPException(404, "Caso no encontrado")
    session.delete(case)
    session.commit()
    return {"mensaje": "Caso eliminado"}

@app.post("/urgent-cases/")
def create_case(case: UrgentCaseBase, session: Session = Depends(get_session)):
    db_case = UrgentCase.from_orm(case)  # convierte el input a modelo de tabla
    session.add(db_case)
    session.commit()
    session.refresh(db_case)  # obtiene el ID generado
    return db_case