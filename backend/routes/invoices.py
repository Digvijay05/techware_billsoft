from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

import crud, models, schemas
from database import get_db

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.get("/", response_model=List[schemas.Invoice])
def list_invoices(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    search: str = "",
    db: Session = Depends(get_db),
):
    return crud.get_invoices(db, skip=skip, limit=limit, status=status, search=search)


@router.get("/{invoice_id}", response_model=schemas.Invoice)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    inv = crud.get_invoice(db, invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return inv


@router.post("/", response_model=schemas.Invoice)
def create_invoice(invoice: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_invoice(db=db, invoice=invoice)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{invoice_id}", response_model=schemas.Invoice)
def update_invoice(invoice_id: int, data: schemas.InvoiceUpdate, db: Session = Depends(get_db)):
    inv = crud.update_invoice(db, invoice_id, data)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return inv


@router.put("/{invoice_id}/status")
def update_invoice_status(invoice_id: int, status: str = Query(...), db: Session = Depends(get_db)):
    inv = crud.get_invoice(db, invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    inv.status = status
    db.commit()
    db.refresh(inv)
    return inv


@router.delete("/{invoice_id}")
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    if not crud.delete_invoice(db, invoice_id):
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {"ok": True}
