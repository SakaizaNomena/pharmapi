from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Adresse de la base SQLite.
# "sqlite:///./app.db" crée le fichier app.db à la racine du projet.
DATABASE_URL = "sqlite:///./app.db"

# L'engine est le point de connexion entre SQLAlchemy et la base de données.
# check_same_thread=False est nécessaire avec SQLite + FastAPI.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


# SQLite ne vérifie pas les clés étrangères par défaut.
# On active cette option pour que les suppressions en cascade fonctionnent.
@event.listens_for(engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# SessionLocal permet d'ouvrir une session (= une conversation) avec la base.
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Base est la classe parente de tous nos modèles (tables).
class Base(DeclarativeBase):
    pass


# Dépendance FastAPI : ouvre une session, la fournit à la route, puis la ferme.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
