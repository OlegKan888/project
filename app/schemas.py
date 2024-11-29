from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class UserBase(BaseModel):
    email: str

class ContactCreate(UserBase):
    password: str

class ContactOut(UserBase):
    id: int

    class Config:
        orm_mode = True

