from sqlalchemy import Column, Integer, String, Date
from app.database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, nullable=True)
    birthday = Column(Date, nullable=True)
    additional_info = Column(String, nullable=True)
