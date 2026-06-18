from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

import crud, schemas, models
from database import get_db

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/", response_model=List[schemas.Customer])
def list_customers(skip: int = 0, limit: int = 100, search: str = "", db: Session = Depends(get_db)):
    return crud.get_customers(db, skip=skip, limit=limit, search=search)


@router.get("/{customer_id}", response_model=schemas.Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    c = crud.get_customer(db, customer_id)
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")
    return c


@router.post("/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    existing = crud.get_customer_by_phone(db, customer.phone)
    if existing:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    return crud.create_customer(db=db, customer=customer)


@router.put("/{customer_id}", response_model=schemas.Customer)
def update_customer(customer_id: int, data: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    c = crud.update_customer(db, customer_id, data)
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")
    return c


@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    if not crud.delete_customer(db, customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"ok": True}
