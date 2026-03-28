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

#Modelo Gatito (Gestión Médica)

class GatitoBase(SQLModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    especie: str = Field(default="Felino")
    sexo: str = Field(...) # Macho / Hembra
    fecha_nacimiento: Optional[str] = Field(None) 
    edad_aprox: Optional[str] = Field(None)
    color: Optional[str] = Field(None)
    
    # Ficha Médica 
    esterilizado: str = Field(default="Desconocido") 
    vacunacion_anual: str = Field(default="No")
    desparasitacion_interna: Optional[str] = Field(None) 
    desparasitacion_externa: Optional[str] = Field(None)
    retrovirales: str = Field(default="Desconocido") # Negativo, Positivo, etc.
    portador_de: str = Field(default="Sano") # VIF, FeLV, Mycoplasma
    
    # Historias 
    historia_llegada: Optional[str] = Field(default="Sin información de rescate", max_length=2000)
    caracter: Optional[str] = Field(None, max_length=1000)
    ubicacion_actual: Optional[str] = Field(None)
    
    # Links y Multimedia
    foto_principal: Optional[str] = Field(None) # URL de Cloudinary
    link_nube: Optional[str] = Field(None) # URL del Drive
    
    # Control de vista
    estatus: str = Field(..., description="Adoptable, En tratamiento, Especial")

class Gatito(GatitoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)