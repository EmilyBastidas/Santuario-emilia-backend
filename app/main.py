from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from .database import create_db_and_tables, get_session
from app.models import UrgentCase, UrgentCaseBase

app = FastAPI(
    title="Santuario Emilia API 🐾",
    description="Backend para donaciones y más en el Santuario Emilia ❤️",
    version="0.1.0",
    swagger_ui_parameters={
        "syntaxHighlight.theme": "obsidian"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crea las tablas al iniciar el servidor
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    print("✅ Base de datos y tablas inicializadas correctamente")

@app.get("/ping")
def ping():
    return {"status": "ok", "message": "Santuario Emilia backend vivo 🐾🐶"}

# ==================== CRUD de Urgent Cases ====================

@app.post("/urgent-cases/")
def create_case(case: UrgentCaseBase, session: Session = Depends(get_session)):
    db_case = UrgentCase.from_orm(case)
    session.add(db_case)
    session.commit()
    session.refresh(db_case)
    return db_case


@app.get("/urgent-cases/")
def get_all_cases(session: Session = Depends(get_session)):
    cases = session.exec(select(UrgentCase)).all()
    
    result = []
    for case in cases:
        raised = 0   # Por ahora es 0 porque aún no tenemos donaciones
        percentage = round((raised / case.goal) * 100) if case.goal > 0 else 0
        
        result.append({
            "petName": case.pet_name,
            "status": case.status,
            "imageUrl": case.imagen,           # mapeamos "imagen" → "imageUrl"
            "description": case.description,
            "raised": raised,
            "goal": int(case.goal),
            "percentage": percentage
        })
    
    return result

@app.delete("/urgent-cases/{case_id}")
def delete_case(case_id: int, session: Session = Depends(get_session)):
    case = session.get(UrgentCase, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Caso no encontrado")
    session.delete(case)
    session.commit()
    return {"mensaje": "Caso eliminado correctamente"}


# Endpoint de estado (útil para debug)
@app.get("/status")
def status():
    return {
        "status": "running",
        "message": "Backend del Santuario Emilia funcionando correctamente 🐶❤️"
    }