

from fastapi import FastAPI, HTTPException, Query
from typing import List
from models import Note, NoteInput
from crud import create_note, get_notes, delete_note
from database import create_db

app = FastAPI()

SECRET_PASSWORD = "opensecret"
create_db()

@app.get("/")
def root():
    return {"message": "Structured Secret Notes API 🔐"}

@app.post("/notes")
def create(note: NoteInput, password: str = Query(...)):
    if password != SECRET_PASSWORD:
        raise HTTPException(status_code=403, detail="Incorrect password")
    note_db = create_note(note.content)
    return {"message": "Note added securely", "note_id": note_db.id}

@app.get("/notes", response_model=List[Note])
def read_notes(password: str = Query(...)):
    if password != SECRET_PASSWORD:
        raise HTTPException(status_code=403, detail="Access denied")
    return get_notes()

@app.delete("/notes/{note_id}")
def remove_note(note_id: int, password: str = Query(...)):
    if password != SECRET_PASSWORD:
        raise HTTPException(status_code=403, detail="Access denied")
    success = delete_note(note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted"}


