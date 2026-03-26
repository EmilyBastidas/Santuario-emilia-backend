from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, func

from .database import create_db_and_tables, get_session
from .models import UrgentCase, UrgentCaseBase, Donation, DonationBase


app = FastAPI(
    title="Santuario Emilia API 🐾",
    description="Backend para donaciones y más en el Santuario Emilia ",
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

# Creo las tablas al iniciar el servidor
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    print("✅ Base de datos y tablas inicializadas correctamente")

@app.get("/ping")
def ping():
    return {"status": "ok", "message": "Santuario Emilia backend vivo 🐾🐶"}

#CRUD de Urgent Cases

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
        # Calcular el total recaudado para este caso
        raised_query = select(func.sum(Donation.amount)).where(Donation.urgent_case_id == case.id)
        raised = session.exec(raised_query).one() or 0.0
        
        percentage = round((raised / case.goal) * 100) if case.goal and case.goal > 0 else 0
        
        result.append({
            "petName": case.pet_name,
            "status": case.status,
            "imageUrl": case.imagen,
            "description": case.description,
            "raised": int(raised),
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

#CRUD de donations

@app.post("/donations/")
def create_donation(donation: DonationBase, session: Session = Depends(get_session)):
    db_donation = Donation.from_orm(donation)
    session.add(db_donation)
    session.commit()
    session.refresh(db_donation)
    return db_donation


@app.get("/donations/")
def get_all_donations(session: Session = Depends(get_session)):
    donations = session.exec(select(Donation)).all()
    return donations

@app.put("/donations/{donation_id}/assign/{case_id}")
def assign_donation_to_case(donation_id: int, case_id: int, session: Session = Depends(get_session)):
    donation = session.get(Donation, donation_id)
    if not donation:
        raise HTTPException(404, "Donación no encontrada")
    
    donation.urgent_case_id = case_id
    session.add(donation)
    session.commit()
    session.refresh(donation)
    
    return {"mensaje": f"Donación {donation_id} asignada al caso {case_id}"}

@app.delete("/donations/{donation_id}")
def delete_donation(donation_id: int, session: Session = Depends(get_session)):
    donation = session.get(Donation, donation_id)
    if not donation:
        raise HTTPException(status_code=404, detail="Donación no encontrada")
    
    session.delete(donation)
    session.commit()
    return {"mensaje": f"Donación {donation_id} eliminada correctamente"}