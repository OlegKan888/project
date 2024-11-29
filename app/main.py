from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app import crud, models, schemas, auth
from app.auth import create_access_token, authenticate_user

app = FastAPI()

@app.post("/register", response_model=schemas.ContactOut)
def register_user(user: schemas.ContactCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user(db, user.email)
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists")
    return crud.create_user(db, user)

@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/contacts/", response_model=list[schemas.ContactOut])
def read_contacts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return crud.get_contacts(db=db, owner_id=current_user.id)
