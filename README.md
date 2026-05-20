# Assessment Test

A Django-based MCQ (Multiple Choice Question) assessment platform that uses Celery and Redis to handle background task processing — built to scale for real-world exam scenarios.

---

## Table of Contents

- [Tools & Technologies](#tools--technologies)
- [Architecture](#architecture)
- [How It Scales for Real-World Assessment Tests](#how-it-scales-for-real-world-assessment-tests)
- [Project Structure](#project-structure)
- [Setup & Run](#setup--run)
- [Environment Variables](#environment-variables)

---

## Tools & Technologies

| Tool | Purpose |
|---|---|
| **Python** | Core language |
| **Django** | Web framework — handles routing, views, templates, admin |
| **Celery** | Async task queue — offloads background jobs from the request cycle |
| **Redis** | Message broker for Celery + caching layer via django-redis |
| **django-redis** | Django cache backend powered by Redis |
| **HTML** | Django templates for the MCQ UI |
| **SQLite** | Default development database (`db.sqlite3` is gitignored) |

---

## Architecture

```
User Browser
     │
     │ HTTP Request
     ▼
Django (assessment_test_project)
  ├── mcq_app          ← MCQ exam logic, views, models, templates
  └── assessment_test_project  ← settings, urls, celery config
     │
     │ Dispatch async task
     ▼
Redis (Broker)  ←──────────────────────┐
     │                                  │
     │ Consume task                     │
     ▼                                  │
Celery Worker                           │
  └── Processes background jobs ────────┘
        (e.g. grading, result storage)
     │
     ▼
Database (SQLite / production DB)
```

**Flow:**
1. A user submits MCQ answers through the Django frontend (`mcq_app`)
2. Django immediately dispatches a Celery task to the Redis broker — no blocking wait
3. A Celery worker picks up the task, processes it (e.g. score calculation), and writes the result to the database
4. Redis also acts as a cache via django-redis to reduce repeated DB queries

---

## How It Scales for Real-World Assessment Tests

**Celery workers handle concurrency.** Exam submissions are pushed to a Redis queue and consumed by workers in parallel, meaning hundreds of simultaneous submissions don't slow down the web server.

**Redis decouples load.** Using Redis as both broker and cache backend means Django stays fast under traffic — session data, frequently accessed questions, and task queues all live in-memory.

**Horizontal scaling.** You can run additional Celery worker processes on the same or separate machines as user load grows — just point them at the same Redis instance.

**Celery Beat for scheduled tasks.** The project is configured to support periodic/scheduled tasks via Celery Beat (e.g. auto-closing an exam after a deadline, or sending result notifications).

---

## Project Structure

```
assessment_test_project/
├── assessment_test_project/   # Django project config
│   ├── settings.py            # Settings (Redis, Celery, installed apps)
│   ├── urls.py                # Root URL configuration
│   └── celery.py              # Celery application setup
├── mcq_app/                   # Core MCQ application
│   ├── models.py              # Data models (questions, answers, results)
│   ├── views.py               # Request handling and exam logic
│   ├── tasks.py               # Celery async tasks
│   ├── urls.py                # App-level URLs
│   └── templates/             # HTML templates for the exam UI
├── images/                    # Project images / assets
├── manage.py                  # Django management entrypoint
└── .gitignore                 # Python / Django / Celery standard ignores
```

---

## Setup & Run

### Prerequisites

- Python 3.9+
- Redis installed and running
- pip

---

### 1. Clone the Repository

```bash
git clone https://github.com/Shuvo018/assessment_test_project.git
cd assessment_test_project
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root (it is gitignored by default):

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
REDIS_URL=redis://localhost:6379/0
```

### 5. Start Redis

```bash
# Linux / macOS
redis-server

# Verify it is running
redis-cli ping
# Expected: PONG
```

### 6. Apply Migrations

```bash
python manage.py migrate
```

### 7. Create a Superuser

```bash
python manage.py createsuperuser
```

### 8. Start the Celery Worker

Open a **new terminal** with the virtualenv active:

```bash
celery -A assessment_test_project worker --loglevel=info
```

To also run scheduled/periodic tasks:

```bash
celery -A assessment_test_project beat --loglevel=info
```

### 9. Run the Development Server

```bash
python manage.py runserver
```

App: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
Admin: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Debug mode toggle (`True` / `False`) |
| `REDIS_URL` | Redis connection URL (e.g. `redis://localhost:6379/0`) |

> `.env` is gitignored. Never commit it to the repository.
