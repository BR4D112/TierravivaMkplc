from typing import List, Optional
from pydantic import BaseModel, EmailStr


# Modelos relacionados con productos
class Product(BaseModel):
    id_product: int
    id_categorie: int
    id_measure_prod: int
    product_name: str
    unit_value: float
    quantity: float
    description: str
    location: str
    image: str


class ProductCreate(BaseModel):
    id_categorie: int
    id_measure_prod: int
    product_name: str
    unit_value: float
    quantity: float
    description: str
    location: str
    image: str


class ProductUpdate(BaseModel):
    id_categorie: int
    id_measure_prod: int
    product_name: str
    unit_value: float
    quantity: float
    description: str
    location: str
    image: str


# Modelos relacionados con usuarios
class Person(BaseModel):
    first_name: str
    last_name: str
    doc_type: str
    doc_number: str
    phone_number: str
    location: str


class User(BaseModel):
    id_user: int
    id_person: int
    password: str
    email: str
    credit_number: str
    is_admin: int


class UserCreate(BaseModel):
    person: Person
    email: str
    credit_number: str
    password: str


# Modelos relacionados con contraseñas y autenticación
class UpdatePasswordRequest(BaseModel):
    email: str
    new_password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str]


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    code: str
    new_password: str


# Modelos relacionados con carritos de compras
class CartItem(BaseModel):
    id_publish_prod: int
    quantity: int


class CartItems(BaseModel):
    cart_items: List[CartItem]
