from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud, schemas
from database import get_db

router = APIRouter(prefix="/staff", tags=["staff"])


@router.get("/", response_model=List[schemas.Staff])
def list_staff(skip: int = 0, limit: int = 100, search: str = "", db: Session = Depends(get_db)):
    return crud.get_staff_list(db, skip=skip, limit=limit, search=search)


@router.get("/{staff_id}", response_model=schemas.Staff)
def get_staff(staff_id: int, db: Session = Depends(get_db)):
    s = crud.get_staff(db, staff_id)
    if not s:
        raise HTTPException(status_code=404, detail="Staff not found")
    return s


@router.post("/", response_model=schemas.Staff)
def create_staff(staff: schemas.StaffCreate, db: Session = Depends(get_db)):
    return crud.create_staff(db, staff)


@router.put("/{staff_id}", response_model=schemas.Staff)
def update_staff(staff_id: int, data: schemas.StaffUpdate, db: Session = Depends(get_db)):
    s = crud.update_staff(db, staff_id, data)
    if not s:
        raise HTTPException(status_code=404, detail="Staff not found")
    return s


@router.delete("/{staff_id}")
def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    if not crud.delete_staff(db, staff_id):
        raise HTTPException(status_code=404, detail="Staff not found")
    return {"ok": True}
