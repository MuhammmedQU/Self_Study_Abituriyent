# LMS - Learning Management System

A complete, production-ready Learning Management System built with FastAPI, SQLAlchemy, PostgreSQL, React, and Vite.

## Features

- **User Authentication**: JWT access tokens + refresh token rotation with revocation
- **Admin Dashboard**: Course, module, lesson, and resource management with activity logging
- **Student Dashboard**: Browse courses, track progress, take quizzes, earn certificates
- **Quiz System**: Random question selection, scoring, unlock logic (70% to unlock next lesson)
- **Certificate Generation**: PDF certificates with QR codes for verification
- **Progress Tracking**: Module-level completion tracking with time spent metrics
- **Soft Deletes**: Admin delete operations with audit trail tracking
- **Activity Logging**: All admin actions logged for compliance

## Quick Start

### Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Database Setup
```bash
# Option 1: Docker (recommended)
docker-compose up -d db

# Option 2: Local PostgreSQL
createdb lms
```

### Initialize Backend
```bash
# Run migrations
cd backend
alembic upgrade head

# Create admin account
python -m app.scripts.create_superadmin
```

### Run Backend
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
# Create .env.local
echo "VITE_API_BASE_URL=http://localhost:8000/api/v1" > .env.local
npm run dev
```

## Architecture

### Backend
- **FastAPI**: Modern Python web framework with async support
- **SQLAlchemy 2.0**: ORM with async database operations
- **PostgreSQL**: Reliable relational database with asyncpg driver
- **Repository Pattern**: Clean separation of data access (repositories) and business logic (services)
- **Service Layer**: All business logic centralized (auth, quiz scoring, progress calculation)
- **Async/Await**: Non-blocking operations throughout

### Frontend
- **React 18**: UI library with hooks
- **Vite 6**: Lightning-fast build tool
- **React Router**: Client-side routing
- **Axios**: HTTP client with token refresh interceptor
- **Context API**: Global auth state management

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user (status=pending)
- `POST /auth/login` - Login (returns tokens)
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - Logout (revokes token)

### Admin
- `POST /admin/courses` - Create course
- `GET /admin/courses` - List courses
- `DELETE /admin/courses/{id}` - Soft delete course
- `POST /admin/modules` - Create module
- `GET /admin/modules/{course_id}` - List modules
- `DELETE /admin/modules/{id}` - Soft delete module
- `POST /admin/lessons` - Create lesson
- `DELETE /admin/lessons/{id}` - Soft delete lesson

### Student
- `GET /student/courses` - Browse courses
- `GET /student/courses/{id}/modules` - Course modules
- `GET /student/modules/{id}/lessons` - Module lessons
- `GET /student/lessons/{id}/resources` - Lesson resources
- `GET /student/quiz/{id}/questions` - Random quiz questions
- `POST /student/quiz/submit` - Submit quiz attempt
- `GET /student/progress/{module_id}` - Get progress

## Authentication Flow

1. **Register**: Email + password (min 8 chars, must contain letter+digit) → pending
2. **Admin Approval**: Admin updates status → active
3. **Login**: Email + password → {access_token, refresh_token, user_id}
4. **Token Refresh**: Access token valid 15 min, refresh token valid 7 days
5. **Token Rotation**: New refresh_token issued on refresh, old one revoked
6. **Logout**: Refresh token revoked

## Database Schema (15 tables)

- `users` - Student/admin accounts with soft delete
- `refresh_tokens` - Hashed tokens for revocation support
- `courses` - Course definitions
- `modules` - Course subdivisions  
- `lessons` - Learning units
- `resources` - Media (videos, PDFs, attachments)
- `quizzes` - Assessment containers (1 per lesson)
- `questions` - Quiz questions (supports 10+ per quiz with random selection)
- `options` - Multiple choice answers
- `quiz_attempts` - Student submissions with scores
- `progress` - Module-level completion tracking
- `certificates` - Module/course achievements with PDF + QR code
- `notifications` - User alerts (triggered on events)
- `announcements` - Admin messages
- `activity_logs` - Admin audit trail

## Docker Deployment

```bash
docker-compose up --build
```

Services:
- **db**: PostgreSQL 16 on port 5432
- **backend**: FastAPI on port 8000
- **frontend**: React Vite on port 5173

## Production Deployment

### Backend (Render)
1. Push code to GitHub
2. Create Web Service on Render from repository
3. Set environment variables:
   - `DATABASE_URL`: Neon PostgreSQL connection
   - `JWT_SECRET`, `JWT_REFRESH_SECRET`: 32+ character secrets
   - `FRONTEND_URL`: Production frontend URL
4. Deploy

### Frontend (Vercel)
1. Connect repository to Vercel
2. Set environment variable: `VITE_API_BASE_URL`
3. Deploy

### Database (Neon)
1. Create PostgreSQL database
2. Copy connection string to backend `DATABASE_URL`
3. Run migrations: `alembic upgrade head`

## Environment Variables

```
# Backend .env
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/lms
SECRET_KEY=your-secret-key-min-32-chars
JWT_SECRET=your-jwt-secret-min-32-chars
JWT_REFRESH_SECRET=your-refresh-secret-min-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
UPLOAD_DIR=uploads
FRONTEND_URL=http://localhost:5173
BACKEND_URL=http://localhost:8000

# Frontend .env.local
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## Development

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## Project Status

✅ Backend complete: Auth, admin CRUD, student endpoints, quiz logic
✅ Frontend started: Login, register, dashboard, courses pages
⏳ Next: Quiz UI, certificate generation, advanced search, notifications
⏳ Testing: Unit tests, integration tests, E2E tests

## License

MIT
- UPLOAD_DIR
- FRONTEND_URL
- BACKEND_URL
- RATE_LIMIT_LOGIN
- RATE_LIMIT_DEFAULT

## Folder Structure

- backend/
- frontend/
- docker-compose.yml
- README.md
