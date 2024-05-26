# models/user.py
from pydantic import BaseModel

class Person(BaseModel):
    first_name: str
    last_name: str
    doc_type: str
    doc_number: str
    phone_number: str
    location: str

class UserCreate(BaseModel):
    person: Person
    email: str
    credit_number: str
    password: str

class User(BaseModel):
    id_user: int
    id_person: int
    password: str
    email: str
    credit_number: str
    is_admin: int


class LoginRequest(BaseModel):
    email: str
    password: str

class UserInfo(BaseModel):
        email: str
        first_name: str
        last_name: str
        doc_type: str
        doc_number: str
        phone_number: str
        location: str

class LoginRequest(BaseModel):
        email: str
        password: str