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

# Relación con las donaciones
    donations: List["Donation"] = Relationship(back_populates="urgent_case")

# ==================== Modelo Donation ====================

class DonationBase(SQLModel):
    amount: float = Field(..., gt=0, description="Monto de la donación en CLP (ej: 15000)")
    message: Optional[str] = Field(None, max_length=500, description="Mensaje opcional del donante (ej: Para la cirugía de Simba)")
    payment_method: str = Field(default="transferencia", description="Método de pago")
    urgent_case_id: Optional[int] = Field(None, description="ID del caso urgente al que va destinada esta donación (opcional)")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Donation(DonationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relación con el caso urgente al que pertenece la donación
    urgent_case_id: Optional[int] = Field(default=None, foreign_key="urgentcase.id")
    
    # Relación para poder acceder desde el caso
    urgent_case: Optional["UrgentCase"] = Relationship(back_populates="donations")
    