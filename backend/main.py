from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine

# Import routers
from routes import customers, items, invoices, reports, staff, expenses, auth

# Create all database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Techware BillSoft API", version="2.0")

# Configure CORS for React frontend (Vite dev + Electron production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all route modules
app.include_router(auth.router)
app.include_router(customers.router)
app.include_router(items.router)
app.include_router(invoices.router)
app.include_router(reports.router)
app.include_router(staff.router)
app.include_router(expenses.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Techware BillSoft API V2 (Local Service)"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
