@echo off
REM LMS Development Startup Script for Windows

echo.
echo ===== LMS Development Setup =====
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

REM Create virtual environment if not exists
if not exist "backend\.venv" (
    echo - Creating virtual environment...
    cd backend
    python -m venv .venv
    cd ..
)

REM Activate venv and install backend deps
echo - Installing backend dependencies...
call backend\.venv\Scripts\activate.bat
cd backend
pip install -r requirements.txt
cd ..

REM Check if .env exists
if not exist "backend\.env" (
    echo - Creating backend\.env from template...
    copy backend\.env.example backend\.env
    echo ! Please edit backend\.env with your configuration
)

REM Install frontend deps
if not exist "frontend\node_modules" (
    echo - Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
)

REM Check if frontend .env exists
if not exist "frontend\.env.local" (
    echo - Creating frontend\.env.local...
    (
        echo VITE_API_BASE_URL=http://localhost:8000/api/v1
    ) > frontend\.env.local
)

echo.
echo * Setup complete!
echo.
echo Next steps:
echo 1. Edit backend\.env if needed
echo 2. Start backend: cd backend ^&^& .venv\Scripts\activate ^&^& uvicorn app.main:app --reload
echo 3. Start frontend: cd frontend ^&^& npm run dev
echo.
echo Useful commands:
echo   Backend:  cd backend ^&^& .venv\Scripts\python -m app.scripts.create_superadmin
echo   DB:       cd backend ^&^& alembic upgrade head
echo   Tests:    cd backend ^&^& pytest
echo.
pause
