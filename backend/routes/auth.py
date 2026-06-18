from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, schemas
from database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_code(db, user.employee_code)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    return crud.create_user(db, user)


@router.post("/login", response_model=schemas.Token)
def login(creds: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, creds.employee_code, creds.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # Simple token: sha256 of employee_code + timestamp (for local desktop app)
    from hashlib import sha256
    from datetime import datetime
    token = sha256(f"{user.employee_code}{datetime.utcnow().isoformat()}".encode()).hexdigest()
    return schemas.Token(access_token=token, user=user)


@router.get("/me", response_model=schemas.User)
def get_current_user(employee_code: str, db: Session = Depends(get_db)):
    """Simplified auth check for local desktop app — pass employee_code as query param."""
    user = crud.get_user_by_code(db, employee_code)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
