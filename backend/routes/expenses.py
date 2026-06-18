from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud, schemas
from database import get_db

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("/", response_model=List[schemas.Expense])
def list_expenses(skip: int = 0, limit: int = 100, category: str = None, db: Session = Depends(get_db)):
    return crud.get_expenses(db, skip=skip, limit=limit, category=category)


@router.post("/", response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_expense(db, expense)


@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    if not crud.delete_expense(db, expense_id):
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"ok": True}


@router.get("/categories", response_model=List[schemas.Lookup])
def list_expense_categories(db: Session = Depends(get_db)):
    return crud.get_expense_categories(db)


@router.post("/categories", response_model=schemas.Lookup)
def create_expense_category(data: schemas.LookupCreate, db: Session = Depends(get_db)):
    return crud.create_expense_category(db, data.name)
