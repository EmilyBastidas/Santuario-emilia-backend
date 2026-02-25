from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from .core.config import settings

# Motor síncrono para SQLite (más simple para empezar)
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # Cambia a True si quieres ver las consultas SQL en la consola (útil para debug)
)

# Opcional: motor asíncrono si más adelante quieres endpoints async (recomendado en FastAPI)
# async_engine = create_async_engine(settings.DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://"))

# Función para crear todas las tablas cuando el servidor arranque
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependencia para obtener una sesión de DB en cada request
def get_session() -> Session:
    with Session(engine) as session:
        yield session