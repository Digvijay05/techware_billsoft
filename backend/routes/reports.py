from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List

import crud, schemas, models
from database import get_db

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/dashboard", response_model=schemas.DashboardStats)
def get_dashboard(db: Session = Depends(get_db)):
    return crud.get_dashboard_stats(db)


@router.get("/daily", response_model=schemas.ReportSummary)
def daily_report(date: Optional[str] = None, db: Session = Depends(get_db)):
    if date:
        day = datetime.strptime(date, "%Y-%m-%d")
    else:
        day = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    start = day.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return crud.get_report_summary(db, start, end)


@router.get("/monthly", response_model=schemas.ReportSummary)
def monthly_report(month: int = Query(None), year: int = Query(None), db: Session = Depends(get_db)):
    now = datetime.utcnow()
    m = month or now.month
    y = year or now.year
    start = datetime(y, m, 1)
    if m == 12:
        end = datetime(y + 1, 1, 1)
    else:
        end = datetime(y, m + 1, 1)
    return crud.get_report_summary(db, start, end)


@router.get("/yearly", response_model=schemas.ReportSummary)
def yearly_report(year: int = Query(None), db: Session = Depends(get_db)):
    y = year or datetime.utcnow().year
    start = datetime(y, 1, 1)
    end = datetime(y + 1, 1, 1)
    return crud.get_report_summary(db, start, end)


@router.get("/lifetime", response_model=schemas.ReportSummary)
def lifetime_report(db: Session = Depends(get_db)):
    start = datetime(2000, 1, 1)
    end = datetime(2100, 1, 1)
    return crud.get_report_summary(db, start, end)


@router.get("/invoices")
def report_invoices(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 500,
    db: Session = Depends(get_db),
):
    """Get invoices for a date range, suitable for report tables and export."""
    q = db.query(models.Invoice)
    if start_date:
        q = q.filter(models.Invoice.created_at >= datetime.strptime(start_date, "%Y-%m-%d"))
    if end_date:
        q = q.filter(models.Invoice.created_at <= datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1))
    if status:
        q = q.filter(models.Invoice.status == status)
    return q.order_by(models.Invoice.created_at.desc()).offset(skip).limit(limit).all()
