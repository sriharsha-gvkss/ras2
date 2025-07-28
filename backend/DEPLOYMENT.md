# Deployment Guide for Render

## Prerequisites
- Render account
- PostgreSQL database (Render provides this)
- Your FastAPI application code

## Render Configuration

### 1. Create a New Web Service
- Go to your Render dashboard
- Click "New +" → "Web Service"
- Connect your GitHub repository

### 2. Configure the Service

**Basic Settings:**
- **Name:** `ai-assistant-backend` (or your preferred name)
- **Root Directory:** `backend` (since your FastAPI app is in the backend folder)
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Alternative Start Command (with Gunicorn):**
```
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

### 3. Environment Variables
Set these in your Render dashboard:

**Database:**
```
DATABASE_URL=postgresql://username:password@host:port/database_name
```

**Other Variables:**
```
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key
```

### 4. Database Setup
- Create a PostgreSQL database in Render
- Copy the database URL to your environment variables
- The tables will be created automatically when the app starts

## Local Testing

### Start the application locally:
```bash
cd backend
uvicorn app.main:app --reload
```

### Fix database issues (if needed):
```bash
cd backend
python fix_database.py
```

## API Endpoints

Your FastAPI application will be available at:
- **Local:** `http://localhost:8000`
- **Render:** `https://your-app-name.onrender.com`

### Available Endpoints:
- `GET /` - Health check
- `GET /health` - Health check
- `POST /auth/login` - User login
- `GET /leaves/` - List leaves
- `POST /leaves/` - Create leave
- `GET /timesheets/` - List timesheets
- `POST /timesheets/` - Create timesheet
- `GET /emails/` - List emails
- `GET /tasks/` - List tasks
- `GET /jobs/` - List jobs

## Troubleshooting

### Common Issues:

1. **Database Connection Errors:**
   - Check your `DATABASE_URL` environment variable
   - Ensure the database is accessible from Render

2. **Port Issues:**
   - Always use `$PORT` environment variable in start command
   - Use `0.0.0.0` as host for external connections

3. **Import Errors:**
   - Ensure all dependencies are in `requirements.txt`
   - Check that the root directory is set correctly

4. **Schema Errors:**
   - Run `python fix_database.py` to recreate tables
   - Check that models match your database schema

### Logs:
- Check Render logs in the dashboard
- Use `print()` statements for debugging (they appear in logs)

## Performance Tips

1. **Use Gunicorn for Production:**
   ```
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
   ```

2. **Database Connection Pooling:**
   - Consider using connection pooling for better performance

3. **Caching:**
   - Implement Redis caching for frequently accessed data

## Security

1. **Environment Variables:**
   - Never commit secrets to your repository
   - Use Render's environment variable feature

2. **CORS:**
   - Update CORS origins in `main.py` for production
   - Remove `"*"` from allow_origins in production

3. **HTTPS:**
   - Render automatically provides HTTPS
   - Ensure your frontend uses HTTPS URLs 