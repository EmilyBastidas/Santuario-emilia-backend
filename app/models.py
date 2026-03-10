from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class UrgentCaseBase(SQLModel):
    pet_name: str = Field(..., min_length=1, max_length=100, description="Nombre del peludo")
    status: str = Field(..., min_length=1, max_length=50, description="Estado actual del caso (Crítico, Estable, Mejorando, En tratamiento)")
    imagen: Optional[str] = Field(None, description="URL de la imagen del caso")
    description: Optional[str]=Field(None, min_length=1, max_length=1500, description="Descripción (ej: Fractura de fémur + trauma múltiple. Necesita cirugía urgente.)")
    goal: float = Field(..., gt=5000, le=5000000, description="Meta en pesos chilenos para el tratamiento/cuidado")

class UrgentCase(UrgentCaseBase, table=True):
    id: Optional[int]= Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Fecha y hora de creación del caso")


    