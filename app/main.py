from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import create_db_and_tables  # ← agrega esta importación

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