from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import ContactCreate, ContactResponse
from models import Contact, User
from auth import get_current_user

contacts_router = APIRouter(prefix="/contacts", tags=["Contacts"])

@contacts_router.post("/", response_model=ContactResponse, status_code=201)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_contact = Contact(**contact.dict(), owner_id=current_user.id)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

@contacts_router.get("/", response_model=list[ContactResponse])
def get_contacts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Contact).filter(Contact.owner_id == current_user.id).all()
