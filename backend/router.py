from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from schemas import ProductResponse, ProductUpdate, ProductCreate
from typing import List
from crud import (
    create_product,
    get_products,
    get_product,
    delete_product,
    update_product
)

router = APIRouter()

@router.get("/products/", response_model=List[ProductResponse])
def read_all_products(db: Session = Depends(get_db)):
    products = get_products(db)
    return products

@router.get("/products/{product_id}", response_model=ProductResponse)
def read_one_product(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Você está querendo buscar um produto que não existe!")
    return db_product

@router.post("/products/", response_model=ProductResponse)
def create_product_route(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(product=product, db=db)

@router.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product_route(product_id: int, db: Session = Depends(get_db)):
    product_db = delete_product(product_id=product_id, db=db)
    if product_db is None:
        raise HTTPException(status_code=404, detail="Você está querendo deletar um produto que não existe!")
    return product_db

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product_route(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    product_db = update_product(product_id=product_id, product=product, db=db)
    if product_db is None:
        raise HTTPException(status_code=404, detail="Você está querendo atualizar um produto que não existe!")
    return product_db