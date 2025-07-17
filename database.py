from sqlmodel import create_engine, SQLModel

DATABASE_URL = "sqlite:///notes.db"
engine = create_engine(DATABASE_URL)

def create_db():
    SQLModel.metadata.create_all(engine)
