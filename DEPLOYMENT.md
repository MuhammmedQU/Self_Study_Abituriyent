# LMS - Deployment Guide

## Local Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Docker & Docker Compose (optional)

### Backend Setup

1. **Create Virtual Environment**
```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Environment**
Copy `.env.example` to `.env` and update values:
```bash
cp .env.example .env
```

Edit `.env`:
```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/lms
SECRET_KEY=your-secret-key-at-least-32-chars
JWT_SECRET=your-jwt-secret-at-least-32-chars
JWT_REFRESH_SECRET=your-refresh-secret-at-least-32-chars
FRONTEND_URL=http://localhost:5173
BACKEND_URL=http://localhost:8000
```

4. **Initialize Database**
```bash
# Using Alembic migrations
alembic upgrade head

# Or create tables directly
python -m app.scripts.create_superadmin
```

5. **Run Backend**
```bash
uvicorn app.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000/api/v1`
API docs: `http://localhost:8000/docs`

### Frontend Setup

1. **Install Dependencies**
```bash
cd frontend
npm install
```

2. **Configure Environment**
Create `.env.local`:
```bash
echo "VITE_API_BASE_URL=http://localhost:8000/api/v1" > .env.local
```

3. **Run Development Server**
```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

### Docker Deployment

```bash
# From project root
docker-compose up --build

# Services:
# - Backend: http://localhost:8000
# - Frontend: http://localhost:5173
# - Database: postgresql://postgres:postgres@db:5432/lms
```

## Production Deployment

### Option 1: Render + Vercel + Neon

#### Database (Neon)
1. Create account at https://neon.tech
2. Create new database
3. Copy connection string

#### Backend (Render)
1. Push code to GitHub
2. Create Web Service on Render
3. Connect to GitHub repository
4. Set environment variables:
   ```
   DATABASE_URL=<Neon connection string>
   SECRET_KEY=<generate 32+ char random string>
   JWT_SECRET=<generate 32+ char random string>
   JWT_REFRESH_SECRET=<generate 32+ char random string>
   FRONTEND_URL=https://your-frontend.vercel.app
   BACKEND_URL=https://your-backend.onrender.com
   ```
5. Set build command: `pip install -r requirements.txt && alembic upgrade head`
6. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

#### Frontend (Vercel)
1. Push code to GitHub
2. Create project on Vercel
3. Connect repository
4. Set environment variable:
   ```
   VITE_API_BASE_URL=https://your-backend.onrender.com/api/v1
   ```
5. Deploy

### Option 2: Heroku + Heroku Postgres

```bash
# Create app
heroku create your-lms-app

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your-secret
heroku config:set JWT_SECRET=your-jwt-secret
heroku config:set JWT_REFRESH_SECRET=your-refresh-secret

# Push code
git push heroku main

# Run migrations
heroku run "alembic upgrade head"

# View logs
heroku logs --tail
```

### Option 3: DigitalOcean App Platform

1. Push to GitHub
2. Create new App on DigitalOcean
3. Connect repository
4. Configure web service for backend
5. Configure static site for frontend
6. Set environment variables
7. Deploy

## Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Add new column"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Check current revision
alembic current
```

## Testing

### Backend Tests
```bash
pytest backend/tests/

# Run specific test
pytest backend/tests/test_auth.py::test_register

# With coverage
pytest --cov=app backend/tests/
```

### Frontend Tests
```bash
npm test
```

## Monitoring & Logging

### Backend
- API docs: `/docs` (Swagger UI)
- Logs: Check stdout/server logs
- Activity logs: `activity_log` table in database
- Health check: `GET /health`

### Frontend
- Browser console for client-side errors
- Network tab for API issues

## Troubleshooting

### Database Connection Error
```
Error: could not connect to server: Connection refused
```
Solution: Ensure PostgreSQL is running and DATABASE_URL is correct

### CORS Error
```
Access to XMLHttpRequest blocked by CORS policy
```
Solution: Check FRONTEND_URL in .env matches your frontend URL

### Token Expired
Tokens auto-refresh via interceptor. If issues persist:
1. Clear localStorage
2. Log out and log back in
3. Check JWT_SECRET matches on backend

### Module Not Found
```bash
pip install -r requirements.txt
npm install
```

## Performance Optimization

1. **Database**: Add indices on frequently queried columns (done)
2. **Caching**: Add Redis for session storage
3. **CDN**: Use Cloudflare for static assets
4. **Compression**: Gzip enabled via Vite/Uvicorn
5. **Async**: All backend operations are async/await

## Security Checklist

- [ ] Change all SECRET_KEY values
- [ ] Use HTTPS in production
- [ ] Set CORS to specific domain
- [ ] Enable password reset flow
- [ ] Set up rate limiting
- [ ] Regular database backups
- [ ] Keep dependencies updated

## Support & Documentation

- API Docs: `http://localhost:8000/docs`
- GitHub Issues: Report bugs
- Email: admin@lms.example.com
