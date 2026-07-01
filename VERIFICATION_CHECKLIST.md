# LMS Project - Setup Verification Checklist

Use this checklist to verify your LMS installation is complete and working.

## Prerequisites ✓

- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] Git installed
- [ ] PostgreSQL 14+ installed (or using Docker)

## Backend Setup ✓

- [ ] Virtual environment created: `python -m venv .venv`
- [ ] Virtual environment activated
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] `.env` file created from `.env.example`
- [ ] Database URL configured in `.env`
- [ ] JWT secrets configured in `.env`
- [ ] Database created and migrations run: `alembic upgrade head`
- [ ] Superadmin created: `python -m app.scripts.create_superadmin`

## Backend Verification ✓

- [ ] Backend starts without errors: `uvicorn app.main:app --reload`
- [ ] Health endpoint responds: `curl http://localhost:8000/health`
- [ ] API docs available: http://localhost:8000/docs
- [ ] Can register new user via `/auth/register`
- [ ] Can login via `/auth/login`
- [ ] Can get courses via `/student/courses` (with auth header)

## Frontend Setup ✓

- [ ] Dependencies installed: `npm install`
- [ ] `.env.local` created with API base URL
- [ ] Development server starts: `npm run dev`
- [ ] Frontend loads: http://localhost:5173

## Frontend Verification ✓

- [ ] Can access login page
- [ ] Can access register page
- [ ] Can register new account
- [ ] Can login with created account
- [ ] Dashboard shows after login
- [ ] Can view courses page
- [ ] API calls work (check browser Network tab)

## Database Verification ✓

- [ ] Can connect to PostgreSQL
- [ ] `lms` database created
- [ ] All 15 tables created
- [ ] Sample data exists (if seeded)

Check with:
```bash
psql postgresql://user:password@localhost:5432/lms
\dt  # List tables
```

## Docker Setup (Optional) ✓

- [ ] Docker installed
- [ ] Docker Compose installed
- [ ] Services start: `docker-compose up --build`
- [ ] Can access frontend on http://localhost:5173
- [ ] Can access backend on http://localhost:8000
- [ ] Can access database on localhost:5432

## File Structure ✓

- [ ] `/backend` folder contains app structure
- [ ] `/frontend` folder contains React app
- [ ] `.env.example` files present
- [ ] `docker-compose.yml` present
- [ ] `README.md` documentation present
- [ ] `DEPLOYMENT.md` deployment guide present

## Environment Variables ✓

### Backend `.env`
```
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/lms
SECRET_KEY=<32+ character random string>
JWT_SECRET=<32+ character random string>
JWT_REFRESH_SECRET=<32+ character random string>
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
UPLOAD_DIR=uploads
FRONTEND_URL=http://localhost:5173
BACKEND_URL=http://localhost:8000
```

- [ ] All variables set
- [ ] Database URL is correct
- [ ] JWT secrets are unique and 32+ characters

### Frontend `.env.local`
```
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

- [ ] API base URL set correctly

## API Endpoints Test ✓

### Authentication
- [ ] `POST /auth/register` - Create account
- [ ] `POST /auth/login` - Get tokens
- [ ] `POST /auth/refresh` - Refresh token
- [ ] `POST /auth/logout` - Revoke token

### Admin
- [ ] `POST /admin/courses` - Create course
- [ ] `GET /admin/courses` - List courses
- [ ] `DELETE /admin/courses/{id}` - Delete course

### Student
- [ ] `GET /student/courses` - Browse courses
- [ ] `GET /student/courses/{id}/modules` - Get modules
- [ ] `GET /student/modules/{id}/lessons` - Get lessons

Test with:
```bash
curl -X GET http://localhost:8000/api/v1/student/courses \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

## Security Checklist ✓

- [ ] All SECRET_KEY values changed
- [ ] CORS configured for your domain
- [ ] HTTPS enabled in production
- [ ] Database password changed
- [ ] JWT secrets are unique
- [ ] No credentials in git (check .gitignore)
- [ ] Environment variables not committed

## Performance Checklist ✓

- [ ] Backend responds quickly (< 200ms)
- [ ] Frontend loads quickly (< 2s)
- [ ] No console errors
- [ ] No database connection pooling issues
- [ ] Async operations working (check logs)

## Documentation ✓

- [ ] Read `README.md`
- [ ] Read `PROJECT_SUMMARY.md`
- [ ] Reviewed `API_EXAMPLES.md`
- [ ] Reviewed `DEPLOYMENT.md`
- [ ] API docs accessible at `/docs`

## Ready to Deploy? ✓

- [ ] All above checks passed
- [ ] Production environment variables set
- [ ] Database backup plan in place
- [ ] Monitoring setup (optional)
- [ ] Domain configured
- [ ] SSL certificate ready
- [ ] Deployment platform chosen (Render, Vercel, Heroku)

## Common Issues & Solutions

### "ModuleNotFoundError: No module named 'sqlalchemy'"
**Solution**: Activate virtual environment and install requirements
```bash
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### "psycopg2: error: could not translate host name"
**Solution**: Check DATABASE_URL in .env
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/lms
```

### "CORS error in browser"
**Solution**: Check FRONTEND_URL in backend .env matches frontend URL
```
FRONTEND_URL=http://localhost:5173
```

### "Token expired immediately"
**Solution**: Verify JWT_SECRET is set and consistent
```
JWT_SECRET=your-32-character-minimum-secret
```

### "Cannot connect to database"
**Solution**: Ensure PostgreSQL is running
```bash
# Windows
pg_isready -h localhost

# macOS
brew services list

# Linux
sudo systemctl status postgresql
```

### Frontend shows blank page
**Solution**: Check browser console and API tab
- Verify VITE_API_BASE_URL in `.env.local`
- Check API is running on port 8000
- Look for 401/403 errors (auth issue)

## Getting Help

1. **Check logs**
   - Backend: stdout/terminal output
   - Frontend: Browser console (F12)
   - Database: PostgreSQL logs

2. **Review documentation**
   - API_EXAMPLES.md for endpoint usage
   - DEPLOYMENT.md for deployment issues
   - README.md for general info

3. **Check configuration**
   - Verify .env files
   - Check JWT secrets match
   - Confirm database connection

4. **Database debugging**
   ```bash
   # Connect to database
   psql postgresql://user:password@localhost:5432/lms
   
   # List tables
   \dt
   
   # Check users
   SELECT * FROM users;
   ```

## Success Indicators ✓

When everything is working:
- ✅ Backend API returns data
- ✅ Frontend communicates with API
- ✅ Authentication works (login/logout)
- ✅ Admin can create courses
- ✅ Students can view courses
- ✅ Tokens refresh automatically
- ✅ No errors in console
- ✅ Database persists data

## Next Steps

1. **Develop Features**
   - Add more pages/components
   - Implement new API endpoints
   - Add business logic in services

2. **Test Application**
   - Run unit tests: `pytest`
   - Test manually via UI
   - Check API responses

3. **Prepare Deployment**
   - Set up production database (Neon)
   - Configure deployment platform (Render, Vercel)
   - Set production environment variables

4. **Deploy**
   - Deploy backend to Render/Heroku
   - Deploy frontend to Vercel
   - Configure custom domain
   - Enable HTTPS

Congratulations! Your LMS is ready to use! 🎉
