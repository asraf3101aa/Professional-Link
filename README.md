# Smart Notification
A Django web application with PostgreSQL database and Celery for background task processing.

## Requirements

- Python 3.12
- PostgreSQL 12+
- Redis (for Celery broker)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/asraf3101aa/Professional-Link
cd Professional-Link
```

### 2. Create virtual environment

```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Environment variables configuration

Create a `.env` file in the project root and set environment variables:
| Variable | Description | Required |
|----------|-------------|---------|
| `APP_ENVIRONMENT` | Enable debug mode | False |
| `SECRET_KEY` | Django secret key | True |
| `DATABASE_URL` | PostgreSQL connection string | True |
| `CELERY_BROKER_URL` | Redis connection string | True |


### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Create superuser (optional)

```bash
python manage.py createsuperuser
```

## Running the Application

### Development Server

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

### Celery Worker

In a separate terminal, start the Celery worker:

```bash
celery -A core worker --loglevel=info
```
---
