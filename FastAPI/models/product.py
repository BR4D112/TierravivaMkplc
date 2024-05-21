# models/product.py
from pydantic import BaseModel

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