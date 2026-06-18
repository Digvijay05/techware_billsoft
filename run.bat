@echo off
echo Starting Techware BillSoft V2...
cd backend
start cmd /k ".\venv\Scripts\activate.bat && uvicorn main:app --host 127.0.0.1 --port 8000"
cd ..\frontend
start cmd /k "npm run dev"
cd ..
echo Application starting. The frontend should open automatically at localhost:5173.
