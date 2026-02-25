# Santuario Emilia - Backend API

API gratuita para gestión de citas veterinarias y registro de intenciones de donación (vía WhatsApp)  
Desarrollada para donación a refugios/protectoras de animales sin fines de lucro.

## Tecnologías

- Python + FastAPI
- SQLModel + SQLite (fácil de migrar a PostgreSQL gratis)
- JWT para autenticación
- Todo gratuito y open source

## Instalación

1. `git clone https://github.com/tu-usuario/Santuario-emilia-backend.git`
2. `python3 -m venv venv && source venv/bin/activate`
3. `pip install -r requirements.txt`
4. Copia `.env.example` a `.env` y configura
5. `uvicorn app.main:app --reload`

Proyecto hecho con amor para ayudar a los animalitos
