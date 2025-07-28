# AI Chat Backend

## Overview
This backend is built with FastAPI and SQLAlchemy, using PostgreSQL as the database. It supports modules for Timesheets, Leaves, Emails, Tasks, and Jobs, each with their own API endpoints and database models.

## Features
- **Timesheets**: Submit, view, update, approve, remind, and send pending timesheets.
- **Leaves**: Submit and view leave requests.
- **Emails**: Draft, view, and manage emails related to timesheets and other modules.
- **Tasks**: Create and view tasks.
- **Jobs**: Create and view jobs.

## Project Structure
```
ai/
  backend/
    app/
      database.py         # DB connection and Base
      main.py             # FastAPI app and router registration
      models/             # SQLAlchemy models
      routes/             # FastAPI API routes
      schemas/            # Pydantic schemas
    requirements.txt      # Python dependencies
```

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repo-url>
cd ai/backend
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the database
- Update `DATABASE_URL` in `app/database.py` if needed.
- Ensure PostgreSQL is running and the database exists.

### 5. Run database migrations (if using Alembic)
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 6. Start the FastAPI server
```bash
uvicorn app.main:app --reload
```

- The API docs will be available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## API Endpoints

### Timesheets
- `GET /timesheets/` — View all timesheets
- `POST /timesheets/` — Submit a timesheet
- `PUT /timesheets/{id}` — Update a timesheet
- `POST /timesheets/{id}/approve?approver=NAME` — Approve a timesheet
- `GET /timesheets/pending` — List pending timesheets
- `POST /timesheets/send-pending?approver=NAME` — Batch approve all pending timesheets

### Leaves
- `GET /leaves/` — View leave requests
- `POST /leaves/` — Submit leave request

### Emails
- `GET /emails/` — View all emails
- `POST /emails/` — Create an email
- `GET /emails/remind-pending-timesheets` — List reminder emails for pending timesheets
- `GET /emails/submit-pending-timesheets` — List submission emails for pending timesheets
- `POST /emails/draft` — Create a draft email
- `GET /emails/drafts` — List all draft emails
- `GET /emails/{email_id}/context` — Provide email context

### Tasks
- `GET /tasks/` — View all tasks
- `POST /tasks/` — Create a task

### Jobs
- `GET /jobs/` — View all jobs
- `POST /jobs/` — Create a job

## Notes
- For schema changes, use Alembic migrations to keep your database in sync with your models.
- All endpoints are documented in the FastAPI Swagger UI.

---
For any questions or issues, please contact the project maintainer. 