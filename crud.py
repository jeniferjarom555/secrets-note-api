from sqlmodel import Session, select
from database import engine
from models import Note
from encryption import fernet

def create_note(content: str) -> Note:
    encrypted_content = fernet.encrypt(content.encode()).decode()
    note = Note(content=encrypted_content)
    with Session(engine) as session:
        session.add(note)
        session.commit()
        session.refresh(note)
    return note

def get_notes() -> list[Note]:
    with Session(engine) as session:
        statement = select(Note)
        notes = session.exec(statement).all()
        for note in notes:
            note.content = fernet.decrypt(note.content.encode()).decode()
    return notes

def delete_note(note_id: int) -> bool:
    with Session(engine) as session:
        note = session.get(Note, note_id)
        if note:
            session.delete(note)
            session.commit()
            return True
    return False
