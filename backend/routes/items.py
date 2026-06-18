from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

import crud, schemas, models
from database import get_db

router = APIRouter(prefix="/items", tags=["items"])


# --- Categories ---
@router.get("/categories/all", response_model=List[schemas.Category])
def get_categories(db: Session = Depends(get_db)):
    categories = crud.get_categories(db)
    if not categories:
        # Auto-seed a default category
        default_cat = crud.create_category(db, "General Goods")
        return [default_cat]
    return categories


@router.post("/categories", response_model=schemas.Category)
def create_category(data: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, data.name)


# --- Units ---
@router.get("/units", response_model=List[schemas.Lookup])
def get_units(db: Session = Depends(get_db)):
    return crud.get_units(db)


@router.post("/units", response_model=schemas.Lookup)
def create_unit(data: schemas.LookupCreate, db: Session = Depends(get_db)):
    return crud.create_unit(db, data.name)


@router.delete("/units/{unit_id}")
def delete_unit(unit_id: int, db: Session = Depends(get_db)):
    if not crud.delete_unit(db, unit_id):
        raise HTTPException(status_code=404, detail="Unit not found")
    return {"ok": True}


# --- Designations ---
@router.get("/designations", response_model=List[schemas.Lookup])
def get_designations(db: Session = Depends(get_db)):
    return crud.get_designations(db)


@router.post("/designations", response_model=schemas.Lookup)
def create_designation(data: schemas.LookupCreate, db: Session = Depends(get_db)):
    return crud.create_designation(db, data.name)


@router.delete("/designations/{designation_id}")
def delete_designation(designation_id: int, db: Session = Depends(get_db)):
    if not crud.delete_designation(db, designation_id):
        raise HTTPException(status_code=404, detail="Designation not found")
    return {"ok": True}


# --- Items ---
@router.get("/", response_model=List[schemas.Item])
def list_items(
    skip: int = 0,
    limit: int = 100,
    search: str = "",
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    return crud.get_items(db, skip=skip, limit=limit, search=search, category_id=category_id)


@router.get("/{item_id}", response_model=schemas.Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)


@router.put("/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, data: schemas.ItemUpdate, db: Session = Depends(get_db)):
    item = crud.update_item(db, item_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    if not crud.delete_item(db, item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return {"ok": True}
