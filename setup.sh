#!/bin/bash

# LMS Development Startup Script

echo "===== LMS Development Setup ====="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.12+"
    exit 1
fi

# Create virtual environment if not exists
if [ ! -d "backend/.venv" ]; then
    echo "📦 Creating virtual environment..."
    cd backend
    python3 -m venv .venv
    cd ..
fi

# Activate venv and install backend deps
echo "📦 Installing backend dependencies..."
if [ -f "backend/.venv/bin/activate" ]; then
    source backend/.venv/bin/activate
else
    source backend/.venv/Scripts/activate  # Windows Git Bash
fi

cd backend
pip install -r requirements.txt
cd ..

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Creating backend/.env from template..."
    cp backend/.env.example backend/.env
    echo "📝 Please edit backend/.env with your configuration"
fi

# Install frontend deps
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Check if frontend .env exists
if [ ! -f "frontend/.env.local" ]; then
    echo "⚠️  Creating frontend/.env.local..."
    echo "VITE_API_BASE_URL=http://localhost:8000/api/v1" > frontend/.env.local
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📖 Next steps:"
echo "1. Edit backend/.env if needed"
echo "2. Start backend: cd backend && uvicorn app.main:app --reload"
echo "3. Start frontend: cd frontend && npm run dev"
echo ""
echo "📚 Useful commands:"
echo "  Backend:  cd backend && .venv/bin/python -m app.scripts.create_superadmin"
echo "  DB:       cd backend && alembic upgrade head"
echo "  Tests:    cd backend && pytest"
echo ""
